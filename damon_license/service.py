"""
Damon License System - Core Services
"""
from __future__ import annotations

import hashlib
import hmac
import secrets
import uuid
from datetime import datetime, timedelta, timezone
from typing import Optional, List, Dict, Any, Tuple
from contextlib import asynccontextmanager

import stripe
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from sqlalchemy import select, func, and_, or_
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import selectinload

from damon_license.models import (
    Base,
    License,
    LicenseStatus,
    LicenseTier,
    LicenseFeatures,
    Subscription,
    SubscriptionStatus,
    BillingInterval,
    LicenseValidation,
    LicenseMachine,
    AuditLog,
    LicenseCreate,
    LicenseUpdate,
    LicenseResponse,
    LicenseValidateRequest,
    LicenseValidateResponse,
    SubscriptionCreate,
    SubscriptionResponse,
    CheckoutSessionRequest,
    CheckoutSessionResponse,
    PortalSessionRequest,
    PortalSessionResponse,
    LicensePaymentRequest,
    LicensePaymentResult,
)
from damon_license.cakto import CaktoClient, CaktoLicensingService, CaktoConfig, CaktoEnvironment


class LicenseService:
    """Core license management service"""

    # Key format: DAMON-{TIER}-{RANDOM}
    KEY_PREFIXES = {
        LicenseTier.FREE: "DAMON-FREE",
        LicenseTier.STARTER: "DAMON-STRT",
        LicenseTier.PROFESSIONAL: "DAMON-PRO",
        LicenseTier.TEAM: "DAMON-TEAM",
        LicenseTier.ENTERPRISE: "DAMON-ENT",
    }

    # Ed25519 key pair for offline license signing
    # In production: generate once, store private key securely (HSM/KMS)
    # Public key embedded in client SDK
    _private_key: Optional[rsa.RSAPrivateKey] = None
    _public_key: Optional[rsa.RSAPublicKey] = None

    def __init__(
        self,
        session: AsyncSession,
        stripe_secret_key: str,
        license_server_url: str,
        encryption_key: bytes,
        cakto_client_id: Optional[str] = None,
        cakto_client_secret: Optional[str] = None,
        cakto_environment: str = "production",
    ):
        self.session = session
        self.stripe_secret_key = stripe_secret_key
        self.license_server_url = license_server_url
        self.encryption_key = encryption_key
        stripe.api_key = stripe_secret_key
        self._init_crypto()

        # Initialize Cakto service if credentials provided
        self._cakto_service: Optional[CaktoLicensingService] = None
        if cakto_client_id and cakto_client_secret:
            cakto_config = CaktoConfig(
                client_id=cakto_client_id,
                client_secret=cakto_client_secret,
                environment=CaktoEnvironment.SANDBOX if cakto_environment == "sandbox" else CaktoEnvironment.PRODUCTION,
            )
            self._cakto_service = CaktoLicensingService(CaktoClient(cakto_config))

    @property
    def cakto_service(self) -> Optional[CaktoLicensingService]:
        return self._cakto_service

    def _init_crypto(self):
        """Initialize RSA key pair for license signing"""
        # In production: load from secure storage
        # For now, generate deterministic key from encryption_key
        private_numbers = rsa.RSAPrivateNumbers(
            p=0xE7D1F1F7E5E5E5E5E5E5E5E5E5E5E5E5E5E5E5E5E5E5E5E5E5E5E5E5E5E5E5E5,
            q=0xD1E7F1F7E5E5E5E5E5E5E5E5E5E5E5E5E5E5E5E5E5E5E5E5E5E5E5E5E5E5E5E5,
            d=0x1,
            dmp1=0x1,
            dmq1=0x1,
            iqmp=0x1,
            public_numbers=rsa.RSAPublicNumbers(
                e=65537,
                n=0xC1E7F1F7E5E5E5E5E5E5E5E5E5E5E5E5E5E5E5E5E5E5E5E5E5E5E5E5E5E5E5E5,
            ),
        )
        # NOTE: This is a placeholder. In production, use proper key generation.
        pass

    @classmethod
    def generate_key_pair(cls) -> Tuple[bytes, bytes]:
        """Generate RSA key pair for license signing"""
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
        )
        private_pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption(),
        )
        public_key = private_key.public_key()
        public_pem = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        )
        return private_pem, public_pem

    # -------------------------------------------------------------------------
    # License Key Generation & Hashing
    # -------------------------------------------------------------------------

    @classmethod
    def generate_license_key(cls, tier: LicenseTier) -> Tuple[str, str, str]:
        """
        Generate a new license key.
        Returns: (full_key, key_prefix, key_hash)
        """
        prefix = cls.KEY_PREFIXES.get(tier, "DAMON-FREE")
        random_part = secrets.token_urlsafe(24)  # 32 chars
        full_key = f"{prefix}-{random_part}"

        # Hash for storage (SHA-256)
        key_hash = hashlib.sha256(full_key.encode()).hexdigest()

        return full_key, prefix, key_hash

    @classmethod
    def hash_license_key(cls, key: str) -> str:
        """Hash a license key for storage/lookup"""
        return hashlib.sha256(key.encode()).hexdigest()

    @classmethod
    def extract_tier_from_key(cls, key: str) -> Optional[LicenseTier]:
        """Extract tier from license key prefix"""
        for tier, prefix in cls.KEY_PREFIXES.items():
            if key.startswith(prefix):
                return tier
        return None

    @classmethod
    def validate_key_format(cls, key: str) -> bool:
        """Validate license key format"""
        if not key or not isinstance(key, str):
            return False
        parts = key.split("-")
        if len(parts) != 3:
            return False
        prefix = f"{parts[0]}-{parts[1]}"
        return prefix in cls.KEY_PREFIXES.values()

    # -------------------------------------------------------------------------
    # License CRUD
    # -------------------------------------------------------------------------

    async def create_license(self, data: LicenseCreate) -> LicenseResponse:
        """Create a new license"""
        full_key, prefix, key_hash = self.generate_license_key(data.tier)
        expires_at = None
        if data.trial_days > 0:
            expires_at = datetime.now(timezone.utc) + timedelta(days=data.trial_days)

        features = LicenseFeatures.for_tier(data.tier)

        license = License(
            key_hash=key_hash,
            key_prefix=prefix,
            tier=data.tier,
            status=LicenseStatus.TRIAL if data.trial_days > 0 else LicenseStatus.ACTIVE,
            user_email=data.user_email.lower(),
            user_name=data.user_name,
            organization=data.organization,
            stripe_customer_id=data.stripe_customer_id,
            features=features.model_dump(),
            expires_at=expires_at,
        )

        self.session.add(license)
        await self.session.flush()

        # Create Stripe checkout session if needed
        if data.tier != LicenseTier.FREE and not data.stripe_customer_id:
            checkout = await self.create_checkout_session(
                CheckoutSessionRequest(
                    tier=data.tier,
                    email=data.user_email,
                    name=data.user_name,
                    organization=data.organization,
                    trial_days=data.trial_days,
                )
            )
            # Store session ID for later retrieval
            license.license_metadata["checkout_session_id"] = checkout.session_id

        await self.session.commit()
        await self.session.refresh(license)

        # Audit log
        await self._audit_log(
            license_id=license.id,
            action="create",
            resource_type="license",
            resource_id=str(license.id),
            new_values={"tier": data.tier.value, "email": data.user_email},
        )

        return self._to_response(license, full_key)

    async def get_license(self, license_id: uuid.UUID) -> Optional[License]:
        """Get license by ID"""
        result = await self.session.execute(
            select(License)
            .options(selectinload(License.subscriptions), selectinload(License.machines))
            .where(License.id == license_id)
        )
        return result.scalar_one_or_none()

    async def get_license_by_key(self, key: str) -> Optional[License]:
        """Get license by key (hash lookup)"""
        key_hash = self.hash_license_key(key)
        result = await self.session.execute(
            select(License)
            .options(selectinload(License.subscriptions), selectinload(License.machines))
            .where(License.key_hash == key_hash)
        )
        return result.scalar_one_or_none()

    async def get_license_by_email(self, email: str) -> List[License]:
        """Get all licenses for an email"""
        result = await self.session.execute(
            select(License)
            .where(License.user_email == email.lower())
            .order_by(License.created_at.desc())
        )
        return list(result.scalars().all())

    async def update_license(self, license_id: uuid.UUID, data: LicenseUpdate) -> Optional[LicenseResponse]:
        """Update license"""
        license = await self.get_license(license_id)
        if not license:
            return None

        old_values = {
            "tier": license.tier.value,
            "status": license.status.value,
        }

        if data.tier is not None:
            license.tier = data.tier
            license.features = LicenseFeatures.for_tier(data.tier).model_dump()
        if data.status is not None:
            license.status = data.status
        if data.features is not None:
            license.features = data.features.model_dump()
        if data.metadata is not None:
            license.license_metadata = data.metadata

        license.updated_at = datetime.now(timezone.utc)
        await self.session.commit()
        await self.session.refresh(license)

        await self._audit_log(
            license_id=license.id,
            action="update",
            resource_type="license",
            resource_id=str(license.id),
            old_values=old_values,
            new_values={"tier": license.tier.value, "status": license.status.value},
        )

        return self._to_response(license)

    async def revoke_license(self, license_id: uuid.UUID, reason: str) -> bool:
        """Revoke a license"""
        license = await self.get_license(license_id)
        if not license:
            return False

        license.status = LicenseStatus.REVOKED
        license.revoked_at = datetime.now(timezone.utc)
        license.revoked_reason = reason
        await self.session.commit()

        await self._audit_log(
            license_id=license.id,
            action="revoke",
            resource_type="license",
            resource_id=str(license.id),
            new_values={"reason": reason},
        )
        return True

    async def list_licenses(
        self,
        tier: Optional[LicenseTier] = None,
        status: Optional[LicenseStatus] = None,
        email: Optional[str] = None,
        limit: int = 50,
        offset: int = 0,
    ) -> List[LicenseResponse]:
        """List licenses with filters"""
        query = select(License).order_by(License.created_at.desc())

        if tier:
            query = query.where(License.tier == tier)
        if status:
            query = query.where(License.status == status)
        if email:
            query = query.where(License.user_email.ilike(f"%{email}%"))

        query = query.limit(limit).offset(offset)
        result = await self.session.execute(query)
        licenses = result.scalars().all()

        return [self._to_response(l) for l in licenses]

    # -------------------------------------------------------------------------
    # License Validation
    # -------------------------------------------------------------------------

    async def validate_license(self, request: LicenseValidateRequest) -> LicenseValidateResponse:
        """Validate a license key"""
        license = await self.get_license_by_key(request.key)

        if not license:
            await self._log_validation(None, request, False, "Invalid license key")
            return LicenseValidateResponse(
                valid=False,
                error="Invalid license key",
            )

        # Check status
        if license.status == LicenseStatus.REVOKED:
            await self._log_validation(license, request, False, "License revoked")
            return LicenseValidateResponse(
                valid=False,
                error="License has been revoked",
                license=self._to_response(license),
            )

        if license.status == LicenseStatus.EXPIRED:
            await self._log_validation(license, request, False, "License expired")
            return LicenseValidateResponse(
                valid=False,
                error="License has expired",
                license=self._to_response(license),
            )

        if license.status == LicenseStatus.SUSPENDED:
            await self._log_validation(license, request, False, "License suspended")
            return LicenseValidateResponse(
                valid=False,
                error="License is suspended",
                license=self._to_response(license),
            )

        # Check expiration
        expires_in_days = None
        if license.expires_at:
            delta = license.expires_at - datetime.now(timezone.utc)
            expires_in_days = max(0, delta.days)
            if delta.total_seconds() <= 0:
                license.status = LicenseStatus.EXPIRED
                await self.session.commit()
                await self._log_validation(license, request, False, "License expired")
                return LicenseValidateResponse(
                    valid=False,
                    error="License has expired",
                    license=self._to_response(license),
                    expires_in_days=0,
                )

        # Machine binding check (optional)
        if request.machine_id:
            machine_result = await self.session.execute(
                select(LicenseMachine).where(
                    and_(
                        LicenseMachine.license_id == license.id,
                        LicenseMachine.machine_id == request.machine_id,
                        LicenseMachine.is_active == True,
                    )
                )
            )
            machine = machine_result.scalar_one_or_none()
            if not machine:
                # First time on this machine - register it
                machine = LicenseMachine(
                    license_id=license.id,
                    machine_id=request.machine_id,
                    platform=request.metadata.get("platform"),
                    machine_metadata=request.metadata,
                )
                self.session.add(machine)
            else:
                machine.last_seen = datetime.now(timezone.utc)
                machine.machine_metadata = request.metadata

        # Update validation tracking
        license.last_validated_at = datetime.now(timezone.utc)
        license.validation_count += 1
        await self.session.commit()

        await self._log_validation(license, request, True, None)

        features = LicenseFeatures(**license.features) if license.features else LicenseFeatures.for_tier(license.tier)

        return LicenseValidateResponse(
            valid=True,
            license=self._to_response(license),
            features=features,
            expires_in_days=expires_in_days,
        )

    async def _log_validation(
        self,
        license: Optional[License],
        request: LicenseValidateRequest,
        success: bool,
        error: Optional[str],
    ):
        """Log validation attempt"""
        validation = LicenseValidation(
            license_id=license.id if license else None,
            machine_id=request.machine_id,
            version=request.version,
            ip_address=request.metadata.get("ip"),
            user_agent=request.metadata.get("user_agent"),
            validation_metadata=request.metadata,
            success=success,
            error=error,
        )
        self.session.add(validation)
        await self.session.commit()

    # -------------------------------------------------------------------------
    # Cakto Integration (Brazil Payments)
    # -------------------------------------------------------------------------

    async def create_cakto_payment(self, request: LicensePaymentRequest) -> LicensePaymentResult:
        """Create a payment via Cakto (PIX, Boleto, Credit Card)"""
        if not self._cakto_service:
            raise RuntimeError("Cakto service not configured. Provide cakto_client_id and cakto_client_secret.")

        return self._cakto_service.create_license_payment(request)

    async def check_cakto_payment_status(self, payment_id: str) -> Dict[str, Any]:
        """Check Cakto payment status"""
        if not self._cakto_service:
            raise RuntimeError("Cakto service not configured.")
        return self._cakto_service.check_payment_status(payment_id)

    async def get_cakto_subscriptions(self, customer_email: str) -> List[Dict[str, Any]]:
        """Get Cakto subscriptions for a customer"""
        if not self._cakto_service:
            raise RuntimeError("Cakto service not configured.")
        return self._cakto_service.get_subscription_by_customer(customer_email)

    async def cancel_cakto_subscription(self, subscription_id: str) -> Dict[str, Any]:
        """Cancel Cakto subscription"""
        if not self._cakto_service:
            raise RuntimeError("Cakto service not configured.")
        return self._cakto_service.cancel_subscription(subscription_id)

    async def handle_cakto_webhook(self, payload: Dict[str, Any], signature: str) -> bool:
        """Handle Cakto webhook events"""
        # Cakto webhook verification would go here
        # For now, we trust the payload
        event_type = payload.get("event")
        data = payload.get("data", {})

        if event_type == "purchase_approved":
            await self._handle_cakto_purchase_approved(data)
        elif event_type == "subscription_cancelled":
            await self._handle_cakto_subscription_cancelled(data)
        elif event_type == "payment_failed":
            await self._handle_cakto_payment_failed(data)

        return True

    async def _handle_cakto_purchase_approved(self, data: Dict):
        """Handle approved purchase from Cakto"""
        # Extract license info from metadata
        metadata = data.get("metadata", {})
        license_tier = metadata.get("license_tier")
        billing_cycle = metadata.get("billing_cycle")
        customer_email = data.get("customer", {}).get("email")

        if not license_tier or not customer_email:
            return

        # Find or create license
        licenses = await self.get_license_by_email(customer_email)
        license = None
        tier = LicenseTier(license_tier)
        for l in licenses:
            if l.tier == tier and l.status in [LicenseStatus.PENDING, LicenseStatus.TRIAL]:
                license = l
                break

        if license:
            license.status = LicenseStatus.ACTIVE
            license.tier = tier
            license.features = LicenseFeatures.for_tier(tier).model_dump()
            # Store Cakto payment ID
            license.license_metadata["cakto_payment_id"] = data.get("id")
            license.license_metadata["cakto_ref_id"] = data.get("refId")
            await self.session.commit()

            # Create subscription record
            interval = BillingInterval.YEARLY if billing_cycle == "yearly" else BillingInterval.MONTHLY
            sub = Subscription(
                license_id=license.id,
                stripe_subscription_id=f"cakto_{data.get('id')}",  # Use Cakto ID as subscription ID
                stripe_price_id=f"cakto_{license_tier}_{billing_cycle}",
                tier=tier,
                status=SubscriptionStatus.ACTIVE,
                interval=interval,
                current_period_start=datetime.now(timezone.utc),
                current_period_end=datetime.now(timezone.utc) + timedelta(days=365 if interval == BillingInterval.YEARLY else 30),
                subscription_metadata=metadata,
            )
            self.session.add(sub)
            await self.session.commit()

    async def _handle_cakto_subscription_cancelled(self, data: Dict):
        """Handle cancelled subscription from Cakto"""
        cakto_payment_id = data.get("id")
        if not cakto_payment_id:
            return

        # Find subscription by Cakto ID
        result = await self.session.execute(
            select(Subscription).where(Subscription.stripe_subscription_id == f"cakto_{cakto_payment_id}")
        )
        sub = result.scalar_one_or_none()
        if sub:
            sub.status = SubscriptionStatus.CANCELED
            sub.canceled_at = datetime.now(timezone.utc)
            if sub.license:
                sub.license.status = LicenseStatus.EXPIRED
                sub.license.tier = LicenseTier.FREE
                sub.license.features = LicenseFeatures.for_tier(LicenseTier.FREE).model_dump()
            await self.session.commit()

    async def _handle_cakto_payment_failed(self, data: Dict):
        """Handle failed payment from Cakto"""
        cakto_payment_id = data.get("id")
        if not cakto_payment_id:
            return

        result = await self.session.execute(
            select(Subscription).where(Subscription.stripe_subscription_id == f"cakto_{cakto_payment_id}")
        )
        sub = result.scalar_one_or_none()
        if sub and sub.license:
            sub.license.status = LicenseStatus.SUSPENDED
            await self.session.commit()

    # -------------------------------------------------------------------------
    # Unified Payment Creation
    # -------------------------------------------------------------------------

    async def create_payment(
        self,
        tier: LicenseTier,
        interval: BillingInterval,
        email: str,
        name: str,
        payment_method: str = "stripe",  # "stripe" | "cakto"
        phone: Optional[str] = None,
        document: Optional[str] = None,
        fingerprint: Optional[str] = None,
        metadata: Optional[Dict[str, str]] = None,
    ) -> Dict[str, Any]:
        """
        Create a payment for license purchase.
        
        Args:
            tier: License tier
            interval: Billing interval
            email: Customer email
            name: Customer name
            payment_method: "stripe" (international) or "cakto" (Brazil)
            phone: Customer phone (required for Cakto)
            document: CPF/CNPJ (required for Cakto)
            fingerprint: Device fingerprint (required for Cakto)
            metadata: Additional metadata
            
        Returns:
            Dict with payment details (checkout_url for Stripe, qr_code/boleto for Cakto)
        """
        if payment_method == "cakto":
            if not self._cakto_service:
                raise RuntimeError("Cakto service not configured. Provide cakto_client_id and cakto_client_secret.")
            
            # Map LicenseTier to Cakto tier string
            tier_map = {
                LicenseTier.STARTER: "starter",
                LicenseTier.PROFESSIONAL: "professional",
                LicenseTier.TEAM: "team",
                LicenseTier.ENTERPRISE: "enterprise",
            }
            cakto_tier = tier_map.get(tier, "professional")
            cakto_cycle = "yearly" if interval == BillingInterval.YEARLY else "monthly"
            
            request = LicensePaymentRequest(
                license_tier=cakto_tier,
                billing_cycle=cakto_cycle,
                customer_email=email,
                customer_name=name,
                customer_phone=phone or "",
                customer_document=document or "",
                customer_fingerprint=fingerprint or str(uuid.uuid4()),
                payment_method="pix",  # Default to PIX for Brazil
                metadata=metadata,
            )
            
            result = await self.create_cakto_payment(request)
            return {
                "payment_method": "cakto",
                "payment_id": result.payment_id,
                "ref_id": result.ref_id,
                "status": result.status,
                "amount": result.amount,
                "payment_method_type": result.payment_method,
                "pix_qr_code": result.pix_qr_code,
                "pix_qr_code_base64": result.pix_qr_code_base64,
                "pix_expires_at": result.pix_expires_at,
                "boleto_barcode": result.boleto_barcode,
                "boleto_pdf_url": result.boleto_pdf_url,
                "boleto_due_date": result.boleto_due_date,
                "checkout_url": result.checkout_url,
            }
        else:
            # Use Stripe
            request = CheckoutSessionRequest(
                tier=tier,
                interval=interval,
                email=email,
                name=name,
                metadata=metadata or {},
            )
            result = await self.create_checkout_session(request)
            return {
                "payment_method": "stripe",
                "session_id": result.session_id,
                "checkout_url": result.url,
            }

    # -------------------------------------------------------------------------
    # Stripe Integration
    # -------------------------------------------------------------------------

    async def create_checkout_session(self, request: CheckoutSessionRequest) -> CheckoutSessionResponse:
        """Create Stripe Checkout session"""
        # Map tier to price IDs (configured in Stripe dashboard)
        price_map = {
            (LicenseTier.STARTER, BillingInterval.MONTHLY): "price_starter_monthly",
            (LicenseTier.STARTER, BillingInterval.YEARLY): "price_starter_yearly",
            (LicenseTier.PROFESSIONAL, BillingInterval.MONTHLY): "price_pro_monthly",
            (LicenseTier.PROFESSIONAL, BillingInterval.YEARLY): "price_pro_yearly",
            (LicenseTier.TEAM, BillingInterval.MONTHLY): "price_team_monthly",
            (LicenseTier.TEAM, BillingInterval.YEARLY): "price_team_yearly",
            (LicenseTier.ENTERPRISE, BillingInterval.MONTHLY): "price_ent_monthly",
            (LicenseTier.ENTERPRISE, BillingInterval.YEARLY): "price_ent_yearly",
        }

        price_id = price_map.get((request.tier, request.interval))
        if not price_id:
            raise ValueError(f"No price configured for {request.tier.value} {request.interval.value}")

        # Create or get customer
        customer = None
        if request.email:
            customers = stripe.Customer.list(email=request.email, limit=1)
            if customers.data:
                customer = customers.data[0]
            else:
                customer = stripe.Customer.create(
                    email=request.email,
                    name=request.name,
                    metadata={
                        "organization": request.organization or "",
                        "tier": request.tier.value,
                    },
                )

        trial_days = request.trial_days if request.tier != LicenseTier.FREE else 0

        session = stripe.checkout.Session.create(
            mode="subscription",
            payment_method_types=["card"],
            line_items=[{"price": price_id, "quantity": 1}],
            customer=customer.id if customer else None,
            customer_email=request.email if not customer else None,
            trial_period_days=trial_days if trial_days > 0 else None,
            success_url=request.success_url or f"{self.license_server_url}/checkout/success?session_id={{CHECKOUT_SESSION_ID}}",
            cancel_url=request.cancel_url or f"{self.license_server_url}/checkout/cancel",
            metadata={
                "tier": request.tier.value,
                "interval": request.interval.value,
                "email": request.email,
                "organization": request.organization or "",
            } | request.metadata,
            subscription_data={
                "trial_period_days": trial_days if trial_days > 0 else None,
                "metadata": {
                    "tier": request.tier.value,
                    "interval": request.interval.value,
                } | request.metadata,
            } if trial_days > 0 else None,
        )

        return CheckoutSessionResponse(session_id=session.id, url=session.url)

    async def create_portal_session(self, request: PortalSessionRequest) -> PortalSessionResponse:
        """Create Stripe Billing Portal session"""
        license = await self.get_license_by_key(request.license_key)
        if not license or not license.stripe_customer_id:
            raise ValueError("License not found or no billing account")

        session = stripe.billing_portal.Session.create(
            customer=license.stripe_customer_id,
            return_url=request.return_url or f"{self.license_server_url}/billing",
        )
        return PortalSessionResponse(url=session.url)

    async def handle_webhook(self, event: stripe.Event) -> bool:
        """Handle Stripe webhook events"""
        event_type = event.type
        data = event.data.object

        if event_type == "checkout.session.completed":
            await self._handle_checkout_completed(data)
        elif event_type == "customer.subscription.created":
            await self._handle_subscription_created(data)
        elif event_type == "customer.subscription.updated":
            await self._handle_subscription_updated(data)
        elif event_type == "customer.subscription.deleted":
            await self._handle_subscription_deleted(data)
        elif event_type == "invoice.payment_failed":
            await self._handle_payment_failed(data)
        elif event_type == "invoice.paid":
            await self._handle_invoice_paid(data)

        return True

    async def _handle_checkout_completed(self, session: Dict):
        """Handle successful checkout"""
        metadata = session.get("metadata", {})
        tier = LicenseTier(metadata.get("tier", "free"))
        email = metadata.get("email")
        customer_id = session.get("customer")
        subscription_id = session.get("subscription")

        if not email:
            return

        # Find or create license
        licenses = await self.get_license_by_email(email)
        license = None
        for l in licenses:
            if l.tier == tier and l.status in [LicenseStatus.PENDING, LicenseStatus.TRIAL]:
                license = l
                break

        if license:
            license.stripe_customer_id = customer_id
            license.stripe_subscription_id = subscription_id
            license.status = LicenseStatus.TRIAL if session.get("trial_end") else LicenseStatus.ACTIVE
            await self.session.commit()

    async def _handle_subscription_created(self, subscription: Dict):
        """Handle subscription creation"""
        customer_id = subscription.get("customer")
        tier = LicenseTier(subscription.get("metadata", {}).get("tier", "free"))
        interval = BillingInterval(subscription.get("metadata", {}).get("interval", "monthly"))

        # Find license by customer
        result = await self.session.execute(
            select(License).where(License.stripe_customer_id == customer_id)
        )
        license = result.scalar_one_or_none()
        if not license:
            return

        sub = Subscription(
            license_id=license.id,
            stripe_subscription_id=subscription["id"],
            stripe_price_id=subscription["items"]["data"][0]["price"]["id"],
            tier=tier,
            status=SubscriptionStatus(subscription["status"]),
            interval=interval,
            current_period_start=datetime.fromtimestamp(subscription["current_period_start"], tz=timezone.utc),
            current_period_end=datetime.fromtimestamp(subscription["current_period_end"], tz=timezone.utc),
            trial_end=datetime.fromtimestamp(subscription["trial_end"], tz=timezone.utc) if subscription.get("trial_end") else None,
        )
        self.session.add(sub)

        license.tier = tier
        license.stripe_subscription_id = subscription["id"]
        license.status = LicenseStatus.ACTIVE
        await self.session.commit()

    async def _handle_subscription_updated(self, subscription: Dict):
        """Handle subscription update"""
        sub_id = subscription["id"]
        result = await self.session.execute(
            select(Subscription).where(Subscription.stripe_subscription_id == sub_id)
        )
        sub = result.scalar_one_or_none()
        if not sub:
            return

        sub.status = SubscriptionStatus(subscription["status"])
        sub.current_period_start = datetime.fromtimestamp(subscription["current_period_start"], tz=timezone.utc)
        sub.current_period_end = datetime.fromtimestamp(subscription["current_period_end"], tz=timezone.utc)
        sub.cancel_at_period_end = subscription.get("cancel_at_period_end", False)
        sub.canceled_at = datetime.fromtimestamp(subscription["canceled_at"], tz=timezone.utc) if subscription.get("canceled_at") else None

        # Update license status
        if sub.license:
            if sub.status == SubscriptionStatus.ACTIVE or sub.status == SubscriptionStatus.TRIALING:
                sub.license.status = LicenseStatus.ACTIVE
                sub.license.tier = sub.tier
            elif sub.status == SubscriptionStatus.PAST_DUE:
                sub.license.status = LicenseStatus.SUSPENDED
            elif sub.status in [SubscriptionStatus.CANCELED, SubscriptionStatus.INCOMPLETE]:
                sub.license.status = LicenseStatus.EXPIRED

        await self.session.commit()

    async def _handle_subscription_deleted(self, subscription: Dict):
        """Handle subscription cancellation"""
        sub_id = subscription["id"]
        result = await self.session.execute(
            select(Subscription).where(Subscription.stripe_subscription_id == sub_id)
        )
        sub = result.scalar_one_or_none()
        if not sub:
            return

        sub.status = SubscriptionStatus.CANCELED
        sub.canceled_at = datetime.now(timezone.utc)

        if sub.license:
            sub.license.status = LicenseStatus.EXPIRED
            sub.license.tier = LicenseTier.FREE
            sub.license.features = LicenseFeatures.for_tier(LicenseTier.FREE).model_dump()

        await self.session.commit()

    async def _handle_payment_failed(self, invoice: Dict):
        """Handle failed payment"""
        customer_id = invoice.get("customer")
        result = await self.session.execute(
            select(License).where(License.stripe_customer_id == customer_id)
        )
        license = result.scalar_one_or_none()
        if license:
            license.status = LicenseStatus.SUSPENDED
            await self.session.commit()

    async def _handle_invoice_paid(self, invoice: Dict):
        """Handle successful invoice payment"""
        customer_id = invoice.get("customer")
        result = await self.session.execute(
            select(License).where(License.stripe_customer_id == customer_id)
        )
        license = result.scalar_one_or_none()
        if license and license.status == LicenseStatus.SUSPENDED:
            license.status = LicenseStatus.ACTIVE
            await self.session.commit()

    # -------------------------------------------------------------------------
    # Utility
    # -------------------------------------------------------------------------

    def _to_response(self, license: License, full_key: Optional[str] = None) -> LicenseResponse:
        """Convert License model to response schema"""
        return LicenseResponse(
            id=license.id,
            key=full_key or f"{license.key_prefix}-{'*' * 24}",
            tier=license.tier,
            status=license.status,
            features=LicenseFeatures(**license.features) if license.features else None,
            user_email=license.user_email,
            user_name=license.user_name,
            organization=license.organization,
            stripe_customer_id=license.stripe_customer_id,
            stripe_subscription_id=license.stripe_subscription_id,
            issued_at=license.issued_at,
            expires_at=license.expires_at,
            last_validated_at=license.last_validated_at,
            validation_count=license.validation_count,
            metadata=license.license_metadata,
            created_at=license.created_at,
            updated_at=license.updated_at,
        )

    async def _audit_log(
        self,
        license_id: Optional[uuid.UUID],
        action: str,
        resource_type: str,
        resource_id: Optional[str],
        old_values: Optional[Dict] = None,
        new_values: Optional[Dict] = None,
        ip: Optional[str] = None,
        user_agent: Optional[str] = None,
    ):
        """Create audit log entry"""
        log = AuditLog(
            license_id=license_id,
            action=action,
            resource_type=resource_type,
            resource_id=resource_id,
            old_values=old_values,
            new_values=new_values,
            ip_address=ip,
            user_agent=user_agent,
        )
        self.session.add(log)
        await self.session.commit()


# -------------------------------------------------------------------------
# Database Setup
# -------------------------------------------------------------------------

async def create_engine_and_session(database_url: str):
    """Create async engine and session factory"""
    engine = create_async_engine(
        database_url,
        echo=False,
        pool_pre_ping=True,
        pool_size=10,
        max_overflow=20,
    )

    async_session = async_sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )

    # Create tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    return engine, async_session


@asynccontextmanager
async def get_session(session_factory):
    """Context manager for database sessions"""
    async with session_factory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()