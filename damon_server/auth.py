"""
Damon Server - Security & Authentication
"""
from __future__ import annotations

import time
from datetime import datetime, timedelta, timezone
from typing import Optional, Dict, Any
from uuid import UUID

from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from damon_server.config import settings
from damon_server.database import get_db

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT
security = HTTPBearer(auto_error=False)


class TokenData(BaseModel):
    user_id: Optional[UUID] = None
    license_id: Optional[UUID] = None
    email: Optional[str] = None
    tier: str = "free"
    scopes: list[str] = []
    exp:exp: int = 0


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int
    refresh_token: Optional[str] = None


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def create_access_token(
    data: dict,
    expires_delta: Optional[timedelta] = None,
) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.jwt_access_token_expire_minutes
        )
    to_encode.update({"exp": expire, "iat": datetime.now(timezone.utc)})
    encoded_jwt = jwt.encode(
        to_encode,
        settings.secret_key,
        algorithm=settings.jwt_algorithm,
    )
    return encoded_jwt


def create_refresh_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(days=settings.jwt_refresh_token_expire_days)
    to_encode.update({"exp": expire, "iat": datetime.now(timezone.utc), "type": "refresh"})
    encoded_jwt = jwt.encode(
        to_encode,
        settings.secret_key,
        algorithm=settings.jwt_algorithm,
    )
    return encoded_jwt


def decode_token(token: str) -> Optional[TokenData]:
    try:
        payload = jwt.decode(
            token,
            settings.secret_key,
            algorithms=[settings.jwt_algorithm],
            issuer=settings.jwt_issuer,
            audience=settings.jwt_audience,
        )
        return TokenData(**payload)
    except JWTError:
        return None


async def get_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
    db: AsyncSession = Depends(get_db),
) -> Optional[TokenData]:
    """Get current authenticated user from JWT token"""
    if not credentials:
        return None

    token_data = decode_token(credentials.credentials)
    if not token_data:
        return None

    # Check if token is expired
    if token_data.exp < int(time.time()):
        return None

    return token_data


async def require_auth(
    current_user: Optional[TokenData] = Depends(get_current_user),
) -> TokenData:
    """Require authentication"""
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return current_user


async def require_admin(
    current_user: TokenData = Depends(require_auth),
    request: Request = None,
) -> TokenData:
    """Require admin access"""
    # Check admin API key header
    admin_key = request.headers.get("X-Admin-Key") if request else None
    if admin_key == settings.admin_api_key:
        return current_user

    # Check if user has admin scope
    if "admin" not in current_user.scopes:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required",
        )
    return current_user


def check_permission(user: TokenData, permission: str) -> bool:
    """Check if user has a specific permission"""
    if "admin" in user.scopes:
        return True
    return permission in user.scopes


def require_permission(permission: str):
    """Dependency to require a specific permission"""
    async def _check_permission(current_user: TokenData = Depends(require_auth)):
        if not check_permission(current_user, permission):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Permission required: {permission}",
            )
        return current_user
    return _check_permission


# License validation
async def validate_license(
    license_key: str,
    machine_id: Optional[str] = None,
) -> Dict[str, Any]:
    """Validate license with license server"""
    if not settings.license_server_enabled:
        return {"valid": True, "tier": "enterprise", "features": {}}

    import httpx

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.post(
                f"{settings.license_server_url}/api/v1/license/validate",
                json={
                    "key": license_key,
                    "machine_id": machine_id,
                    "version": settings.app_version,
                },
            )
            response.raise_for_status()
            return response.json()
    except httpx.TimeoutException:
        return {"valid": False, "error": "License server timeout"}
    except httpx.HTTPStatusError as e:
        return {"valid": False, "error": f"License server error: {e.response.status_code}"}
    except Exception as e:
        return {"valid": False, "error": str(e)}


def generate_api_key(prefix: str = "damon") -> str:
    """Generate a new API key"""
    return f"{prefix}_{secrets.token_urlsafe(32)}"