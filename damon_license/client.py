"""
Damon License Client SDK
"""
from __future__ import annotations

import hashlib
import hmac
import json
import os
import platform
import subprocess
import uuid
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Optional, Dict, Any, List

import httpx
from pydantic import BaseModel, Field

from damon_license.models import (
    LicenseTier,
    LicenseStatus,
    LicenseFeatures,
    LicenseValidateRequest,
    LicenseValidateResponse,
    LicenseResponse,
)


class MachineInfo(BaseModel):
    """Machine identification information"""
    machine_id: str
    machine_name: str
    platform: str
    platform_version: str
    architecture: str
    cpu_count: int
    memory_gb: float
    disk_gb: float


class LicenseCache(BaseModel):
    """Cached license data for offline validation"""
    license: LicenseResponse
    features: LicenseFeatures
    validated_at: datetime
    expires_at: Optional[datetime]
    signature: str  # JWT signature


class DamonLicenseClient:
    """
    Client SDK for Damon License System.
    Handles license validation, caching, and feature gating.
    """

    def __init__(
        self,
        server_url: str = "https://license.damon-agent.dev",
        cache_dir: Optional[Path] = None,
        timeout: float = 10.0,
        offline_grace_days: int = 7,
    ):
        self.server_url = server_url.rstrip("/")
        self.timeout = timeout
        self.offline_grace_days = offline_grace_days

        # Cache directory
        if cache_dir is None:
            cache_dir = self._get_default_cache_dir()
        self.cache_dir = cache_dir
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.cache_file = self.cache_dir / "license_cache.json"
        self.key_file = self.cache_dir / "license_key"

        # Public key for offline validation (embedded at build time)
        self._public_key_pem = self._get_embedded_public_key()

        # HTTP client
        self._client: Optional[httpx.AsyncClient] = None

    def _get_default_cache_dir(self) -> Path:
        """Get platform-appropriate cache directory"""
        if platform.system() == "Windows":
            base = Path(os.environ.get("LOCALAPPDATA", Path.home() / "AppData" / "Local"))
        elif platform.system() == "Darwin":
            base = Path.home() / "Library" / "Application Support"
        else:
            base = Path(os.environ.get("XDG_CACHE_HOME", Path.home() / ".cache"))
        return base / "damon-agent" / "license"

    def _get_embedded_public_key(self) -> str:
        """Get embedded RSA public key for offline validation"""
        # In production, this would be embedded at build time
        # For now, return a placeholder
        return """-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA...
-----END PUBLIC KEY-----"""

    def _get_machine_id(self) -> str:
        """Get stable machine ID"""
        # Try to get from cache first
        machine_id_file = self.cache_dir / "machine_id"
        if machine_id_file.exists():
            return machine_id_file.read_text().strip()

        # Generate from hardware info
        parts = []

        # Platform-specific machine ID
        if platform.system() == "Linux":
            try:
                with open("/etc/machine-id") as f:
                    parts.append(f.read().strip())
            except:
                pass
            try:
                with open("/var/lib/dbus/machine-id") as f:
                    parts.append(f.read().strip())
            except:
                pass
        elif platform.system() == "Darwin":
            try:
                result = subprocess.run(
                    ["ioreg", "-rd1", "-c", "IOPlatformExpertDevice"],
                    capture_output=True, text=True, timeout=5
                )
                for line in result.stdout.split("\n"):
                    if "IOPlatformUUID" in line:
                        parts.append(line.split("=")[-1].strip().strip('"'))
                        break
            except:
                pass
        elif platform.system() == "Windows":
            try:
                import winreg
                with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Cryptography") as key:
                    parts.append(winreg.QueryValueEx(key, "MachineGuid")[0])
            except:
                pass

        # Fallback: hash of platform info
        if not parts:
            fallback = f"{platform.node()}-{platform.processor()}-{platform.machine()}"
            machine_id = hashlib.sha256(fallback.encode()).hexdigest()[:32]
        else:
            machine_id = hashlib.sha256("|".join(parts).encode()).hexdigest()[:32]

        # Cache it
        machine_id_file.write_text(machine_id)
        return machine_id

    def _get_machine_info(self) -> MachineInfo:
        """Get detailed machine information"""
        import psutil

        return MachineInfo(
            machine_id=self._get_machine_id(),
            machine_name=platform.node(),
            platform=platform.system(),
            platform_version=platform.version(),
            architecture=platform.machine(),
            cpu_count=psutil.cpu_count(logical=True) or 1,
            memory_gb=round(psutil.virtual_memory().total / (1024**3), 1),
            disk_gb=round(psutil.disk_usage("/").total / (1024**3), 1),
        )

    async def _get_client(self) -> httpx.AsyncClient:
        """Get or create HTTP client"""
        if self._client is None or self._client.is_closed:
            self._client = httpx.AsyncClient(
                base_url=self.server_url,
                timeout=self.timeout,
                headers={"User-Agent": f"damon-license/{self._get_version()}"},
            )
        return self._client

    def _get_version(self) -> str:
        """Get package version"""
        try:
            from importlib.metadata import version
            return version("damon-license")
        except:
            return "0.1.0"

    # -------------------------------------------------------------------------
    # License Key Management
    # -------------------------------------------------------------------------

    def save_license_key(self, key: str) -> None:
        """Save license key to file"""
        self.key_file.write_text(key.strip())
        self.key_file.chmod(0o600)

    def load_license_key(self) -> Optional[str]:
        """Load license key from file"""
        if self.key_file.exists():
            return self.key_file.read_text().strip()
        return None

    def clear_license_key(self) -> None:
        """Clear saved license key"""
        if self.key_file.exists():
            self.key_file.unlink()
        if self.cache_file.exists():
            self.cache_file.unlink()

    # -------------------------------------------------------------------------
    # Online Validation
    # -------------------------------------------------------------------------

    async def validate_online(self, key: Optional[str] = None) -> LicenseValidateResponse:
        """Validate license with server"""
        if key is None:
            key = self.load_license_key()

        if not key:
            return LicenseValidateResponse(
                valid=False,
                error="No license key found",
            )

        machine_info = self._get_machine_info()

        request = LicenseValidateRequest(
            key=key,
            machine_id=machine_info.machine_id,
            version=self._get_version(),
            metadata={
                "machine_name": machine_info.machine_name,
                "platform": machine_info.platform,
                "architecture": machine_info.architecture,
            },
        )

        try:
            client = await self._get_client()
            response = await client.post(
                "/api/v1/license/validate",
                json=request.model_dump(mode="json"),
            )
            response.raise_for_status()
            data = response.json()

            result = LicenseValidateResponse(**data)

            # Cache successful validation
            if result.valid and result.license:
                await self._cache_license(result.license, result.features, key)

            return result

        except httpx.TimeoutException:
            return LicenseValidateResponse(
                valid=False,
                error="Validation timeout",
            )
        except httpx.HTTPStatusError as e:
            return LicenseValidateResponse(
                valid=False,
                error=f"Server error: {e.response.status_code}",
            )
        except Exception as e:
            return LicenseValidateResponse(
                valid=False,
                error=f"Validation failed: {str(e)}",
            )

    # -------------------------------------------------------------------------
    # Offline Validation
    # -------------------------------------------------------------------------

    async def _cache_license(
        self,
        license: LicenseResponse,
        features: Optional[LicenseFeatures],
        key: str,
    ) -> None:
        """Cache license for offline use"""
        if features is None:
            features = LicenseFeatures.for_tier(license.tier)

        # Create cache entry
        cache = LicenseCache(
            license=license,
            features=features,
            validated_at=datetime.now(timezone.utc),
            expires_at=license.expires_at,
            signature=self._sign_cache(license, features),
        )

        # Save to file
        cache_data = cache.model_dump(mode="json")
        self.cache_file.write_text(json.dumps(cache_data, indent=2))
        self.cache_file.chmod(0o600)

    def _sign_cache(self, license: LicenseResponse, features: LicenseFeatures) -> str:
        """Sign cache with HMAC for tamper detection"""
        # In production, use RSA signature with embedded private key
        # For now, use HMAC with a derived key
        data = f"{license.id}{license.key}{license.tier.value}{license.status.value}".encode()
        key = hashlib.sha256(b"damon-license-cache").digestdigestdigest()
        return hmac.new(key, data, hashlib.sha256).hexdigest()

    def _verify_cache_signature(self, cache: LicenseCache) -> bool:
        """Verify cache signature"""
        expected = self._sign_cache(cache.license, cache.features)
        return hmac.compare_digest(cache.signature, expected)

    def load_cached_license(self) -> Optional[LicenseCache]:
        """Load cached license for offline validation"""
        if not self.cache_file.exists():
            return None

        try:
            data = json.loads(self.cache_file.read_text())
            cache = LicenseCache(**data)

            # Verify signature
            if not self._verify_cache_signature(cache):
                return None

            # Check if cache is within grace period
            if cache.validated_at:
                age = datetime.now(timezone.utc) - cache.validated_at
                if age > timedelta(days=self.offline_grace_days):
                    return None

            return cache
        except Exception:
            return None

    def validate_offline(self) -> LicenseValidateResponse:
        """Validate license using cached data (offline)"""
        cache = self.load_cached_license()

        if not cache:
            return LicenseValidateResponse(
                valid=False,
                error="No valid cached license found",
            )

        # Check expiration
        if cache.expires_at and cache.expires_at < datetime.now(timezone.utc):
            return LicenseValidateResponse(
                valid=False,
                error="License expired",
                license=cache.license,
                features=cache.features,
                expires_in_days=0,
            )

        return LicenseValidateResponse(
            valid=True,
            license=cache.license,
            features=cache.features,
            expires_in_days=(
                (cache.expires_at - datetime.now(timezone.utc)).days
                if cache.expires_at else None
            ),
        )

    # -------------------------------------------------------------------------
    # Unified Validation (Online with Offline Fallback)
    # -------------------------------------------------------------------------

    async def validate(self, key: Optional[str] = None) -> LicenseValidateResponse:
        """
        Validate license - tries online first, falls back to offline cache.
        """
        # Try online validation
        result = await self.validate_online(key)

        if result.valid:
            return result

        # If online fails, try offline cache
        if "timeout" in (result.error or "").lower() or "connection" in (result.error or "").lower():
            offline_result = self.validate_offline()
            if offline_result.valid:
                offline_result.error = "Using offline cache (server unreachable)"
                return offline_result

        return result

    # -------------------------------------------------------------------------
    # Feature Gating
    # -------------------------------------------------------------------------

    def check_feature(self, feature: str, features: Optional[LicenseFeatures] = None) -> bool:
        """Check if a feature is enabled"""
        if features is None:
            cache = self.load_cached_license()
            if cache:
                features = cache.features
            else:
                features = LicenseFeatures.for_tier(LicenseTier.FREE)

        return getattr(features, feature, False)

    def get_limit(self, limit: str, features: Optional[LicenseFeatures] = None) -> int:
        """Get a numeric limit"""
        if features is None:
            cache = self.load_cached_license()
            if cache:
                features = cache.features
            else:
                features = LicenseFeatures.for_tier(LicenseTier.FREE)

        return getattr(features, limit, 0)

    def get_tier(self) -> LicenseTier:
        """Get current license tier"""
        cache = self.load_cached_license()
        if cache:
            return cache.license.tier
        return LicenseTier.FREE

    def is_pro_or_above(self) -> bool:
        """Check if license is Pro tier or higher"""
        tier = self.get_tier()
        return tier in [LicenseTier.PROFESSIONAL, LicenseTier.TEAM, LicenseTier.ENTERPRISE]

    def is_enterprise(self) -> bool:
        """Check if license is Enterprise tier"""
        return self.get_tier() == LicenseTier.ENTERPRISE

    # -------------------------------------------------------------------------
    # Lifecycle
    # -------------------------------------------------------------------------

    async def close(self):
        """Close HTTP client"""
        if self._client and not self._client.is_closed:
            await self._client.aclose()


# -------------------------------------------------------------------------
# Convenience Functions
# -------------------------------------------------------------------------

_default_client: Optional[DamonLicenseClient] = None


def get_license_client() -> DamonLicenseClient:
    """Get or create default license client"""
    global _default_client
    if _default_client is None:
        _default_client = DamonLicenseClient()
    return _default_client


async def validate_license(key: Optional[str] = None) -> LicenseValidateResponse:
    """Quick license validation"""
    client = get_license_client()
    return await client.validate(key)


def check_feature(feature: str) -> bool:
    """Quick feature check (uses cache)"""
    client = get_license_client()
    return client.check_feature(feature)


def get_limit(limit: str) -> int:
    """Quick limit check (uses cache)"""
    client = get_license_client()
    return client.get_limit(limit)


# -------------------------------------------------------------------------
# CLI Integration
# -------------------------------------------------------------------------

class LicenseCLI:
    """CLI integration for license commands"""

    def __init__(self, client: DamonLicenseClient):
        self.client = client

    async def activate(self, key: str) -> LicenseValidateResponse:
        """Activate a license key"""
        self.client.save_license_key(key)
        return await self.client.validate_online(key)

    async def status(self) -> LicenseValidateResponse:
        """Check license status"""
        return await self.client.validate()

    def deactivate(self) -> None:
        """Deactivate license (clear local)"""
        self.client.clear_license_key()

    def get_info(self) -> Dict[str, Any]:
        """Get license info for display"""
        cache = self.client.load_cached_license()
        if not cache:
            return {"status": "no_license", "tier": "free"}

        return {
            "status": cache.license.status.value,
            "tier": cache.license.tier.value,
            "key": cache.license.key[:20] + "...",
            "email": cache.license.user_email,
            "expires": cache.license.expires_at.isoformat() if cache.license.expires_at else "never",
            "features": cache.features.model_dump(),
        }

    async def open_portal(self) -> str:
        """Open Stripe billing portal"""
        key = self.client.load_license_key()
        if not key:
            raise ValueError("No license key found")

        import httpx
        async with httpx.AsyncClient() as http:
            resp = await http.post(
                f"{self.client.server_url}/api/v1/license/portal",
                json={"license_key": key},
                timeout=30,
            )
            resp.raise_for_status()
            return resp.json()["url"]