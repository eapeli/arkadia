"""
Damon License Server - FastAPI Application
"""
from __future__ import annotations

import os
import uuid
from contextlib import asynccontextmanager
from datetime import datetime, timezone
from typing import Optional, List

import stripe
from fastapi import FastAPI, Depends, HTTPException, Request, Header, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession, AsyncEngine, async_sessionmaker
from sqlalchemy.orm import selectinload
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from damon_license.models import (
    Base,
    License,
    LicenseTier,
    LicenseStatus,
    LicenseFeatures,
    Subscription,
    LicenseValidation,
    AuditLog,
    LicenseCreate,
    LicenseUpdate,
    LicenseResponse,
    LicenseValidateRequest,
    LicenseValidateResponse,
    SubscriptionResponse,
    CheckoutSessionRequest,
    CheckoutSessionResponse,
    PortalSessionRequest,
    PortalSessionResponse,
    WebhookEvent,
)
from damon_license.service import LicenseService, create_engine_and_session, get_session


# -------------------------------------------------------------------------
# Configuration
# -------------------------------------------------------------------------

class Settings(BaseModel):
    # Database
    database_url: str = os.getenv("DATABASE_URL", "postgresql+asyncpg://postgres:postgres@localhost:5432/damon_license")

    # Stripe
    stripe_secret_key: str = os.getenv("STRIPE_SECRET_KEY", "")
    stripe_publishable_key: str = os.getenv("STRIPE_PUBLISHABLE_KEY", "")
    stripe_webhook_secret: str = os.getenv("STRIPE_WEBHOOK_SECRET", "")

    # Server
    license_server_url: str = os.getenv("LICENSE_SERVER_URL", "https://license.damon-agent.dev")
    api_host: str = os.getenv("API_HOST", "0.0.0.0")
    api_port: int = int(os.getenv("API_PORT", "8000"))

    # Security
    secret_key: str = os.getenv("SECRET_KEY", secrets.token_urlsafe(32))
    encryption_key: str = os.getenv("ENCRYPTION_KEY", secrets.token_urlsafe(32))
    jwt_algorithm: str = "RS256"
    jwt_expiry_hours: int = 24

    # CORS
    cors_origins: List[str] = ["*"]

    # Rate limiting
    rate_limit: str = "100/minute"

    # Admin
    admin_api_key: str = os.getenv("ADMIN_API_KEY", "")


settings = Settings()

# -------------------------------------------------------------------------
# Rate Limiter
# -------------------------------------------------------------------------

limiter = Limiter(key_func=get_remote_address)

# -------------------------------------------------------------------------
# Database
# -------------------------------------------------------------------------

engine: Optional[AsyncEngine] = None
session_factory: Optional[async_sessionmaker] = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global engine, session_factory
    engine, session_factory = await create_engine_and_session(settings.database_url)
    yield
    await engine.dispose()


# -------------------------------------------------------------------------
# FastAPI App
# -------------------------------------------------------------------------

app = FastAPI(
    title="Damon License Server",
    description="License & Subscription Management for Damon Agent",
    version="0.1.0",
    lifespan=lifespan,
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------------------------------------------------------
# Dependencies
# -------------------------------------------------------------------------

security = HTTPBearer(auto_error=False)


async def get_db() -> AsyncSession:
    async with get_session(session_factory) as session:
        yield session


async def get_license_service(db: AsyncSession = Depends(get_db)) -> LicenseService:
    return LicenseService(
        session=db,
        stripe_secret_key=settings.stripe_secret_key,
        license_server_url=settings.license_server_url,
        encryption_key=settings.encryption_key.encode(),
    )


async def verify_admin_key(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
    x_admin_key: Optional[str] = Header(None),
) -> bool:
    """Verify admin API key"""
    key = credentials.credentials if credentials else x_admin_key
    if not key or key != settings.admin_api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid admin API key",
        )
    return True


# -------------------------------------------------------------------------
# Health Check
# -------------------------------------------------------------------------

@app.get("/health", tags=["Health"])
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now(timezone.utc).isoformat()}


# -------------------------------------------------------------------------
# Public License Validation (Client SDK calls this)
# -------------------------------------------------------------------------

@app.post(
    "/api/v1/license/validate",
    response_model=LicenseValidateResponse,
    tags=["License"],
    summary="Validate a license key",
)
@limiter.limit("60/minute")
async def validate_license(
    request: Request,
    payload: LicenseValidateRequest,
    service: LicenseService = Depends(get_license_service),
):
    """Validate a license key - called by client applications"""
    return await service.validate_license(payload)


@app.post(
    "/api/v1/license/activate",
    response_model=LicenseResponse,
    tags=["License"],
    summary="Activate a license (first time setup)",
)
@limiter.limit("10/minute")
async def activate_license(
    request: Request,
    payload: LicenseCreate,
    service: LicenseService = Depends(get_license_service),
):
    """Activate a new license - creates trial or paid license"""
    return await service.create_license(payload)


# -------------------------------------------------------------------------
# Billing & Subscriptions (Stripe Integration)
# -------------------------------------------------------------------------

@app.post(
    "/api/v1/billing/checkout",
    response_model=CheckoutSessionResponse,
    tags=["Billing"],
    summary="Create Stripe Checkout session",
)
@limiter.limit("20/minute")
async def create_checkout(
    request: Request,
    payload: CheckoutSessionRequest,
    service: LicenseService = Depends(get_license_service),
):
    """Create a Stripe Checkout session for subscription purchase"""
    return await service.create_checkout_session(payload)


@app.post(
    "/api/v1/billing/portal",
    response_model=PortalSessionResponse,
    tags=["Billing"],
    summary="Create Stripe Billing Portal session",
)
@limiter.limit("20/minute")
async def create_portal(
    request: Request,
    payload: PortalSessionRequest,
    service: LicenseService = Depends(get_license_service),
):
    """Create a Stripe Billing Portal session for subscription management"""
    return await service.create_portal_session(payload)


@app.post(
    "/api/v1/webhooks/stripe",
    tags=["Webhooks"],
    summary="Handle Stripe webhooks",
)
async def stripe_webhook(
    request: Request,
    service: LicenseService = Depends(get_license_service),
):
    """Handle Stripe webhook events"""
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.stripe_webhook_secret
        )
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid payload")
    except stripe.error.SignatureVerificationError:
        raise HTTPException(status_code=400, detail="Invalid signature")

    await service.handle_webhook(event)
    return {"status": "ok"}


# -------------------------------------------------------------------------
# Admin API (Protected)
# -------------------------------------------------------------------------

@app.get(
    "/api/v1/admin/licenses",
    response_model=List[LicenseResponse],
    tags=["Admin"],
    summary="List all licenses",
)
@limiter.limit("100/minute")
async def list_licenses(
    request: Request,
    tier: Optional[LicenseTier] = None,
    status: Optional[LicenseStatus] = None,
    email: Optional[str] = None,
    limit: int = 50,
    offset: int = 0,
    _: bool = Depends(verify_admin_key),
    service: LicenseService = Depends(get_license_service),
):
    """List all licenses with filters (admin only)"""
    return await service.list_licenses(tier, status, email, limit, offset)


@app.get(
    "/api/v1/admin/licenses/{license_id}",
    response_model=LicenseResponse,
    tags=["Admin"],
    summary="Get license by ID",
)
@limiter.limit("100/minute")
async def get_license(
    request: Request,
    license_id: uuid.UUID,
    _: bool = Depends(verify_admin_key),
    service: LicenseService = Depends(get_license_service),
):
    """Get license details (admin only)"""
    license = await service.get_license(license_id)
    if not license:
        raise HTTPException(status_code=404, detail="License not found")
    return service._to_response(license)


@app.patch(
    "/api/v1/admin/licenses/{license_id}",
    response_model=LicenseResponse,
    tags=["Admin"],
    summary="Update license",
)
@limiter.limit("50/minute")
async def update_license(
    request: Request,
    license_id: uuid.UUID,
    payload: LicenseUpdate,
    _: bool = Depends(verify_admin_key),
    service: LicenseService = Depends(get_license_service),
):
    """Update license (admin only)"""
    license = await service.update_license(license_id, payload)
    if not license:
        raise HTTPException(status_code=404, detail="License not found")
    return license


@app.post(
    "/api/v1/admin/licenses/{license_id}/revoke",
    tags=["Admin"],
    summary="Revoke license",
)
@limiter.limit("20/minute")
async def revoke_license(
    request: Request,
    license_id: uuid.UUID,
    reason: str,
    _: bool = Depends(verify_admin_key),
    service: LicenseService = Depends(get_license_service),
):
    """Revoke a license (admin only)"""
    success = await service.revoke_license(license_id, reason)
    if not success:
        raise HTTPException(status_code=404, detail="License not found")
    return {"success": True, "message": "License revoked"}


@app.get(
    "/api/v1/admin/stats",
    tags=["Admin"],
    summary="Get license statistics",
)
@limiter.limit("30/minute")
async def get_stats(
    request: Request,
    _: bool = Depends(verify_admin_key),
    db: AsyncSession = Depends(get_db),
):
    """Get license statistics (admin only)"""
    # Total licenses
    total = await db.scalar(select(func.count(License.id)))

    # By tier
    tier_stats = await db.execute(
        select(License.tier, func.count(License.id)).group_by(License.tier)
    )
    by_tier = {tier.value: count for tier, count in tier_stats.all()}

    # By status
    status_stats = await db.execute(
        select(License.status, func.count(License.id)).group_by(License.status)
    )
    by_status = {status.value: count for status, count in status_stats.all()}

    # Active subscriptions
    active_subs = await db.scalar(
        select(func.count(Subscription.id)).where(Subscription.status == "active")
    )

    # Revenue (MRR approximation)
    mrr_result = await db.execute(
        select(
            func.sum(
                func.case(
                    (Subscription.interval == "monthly", 1),
                    (Subscription.interval == "yearly", 1/12),
                    else_=0,
                )
            )
        ).where(Subscription.status == "active")
    )
    mrr = mrr_result.scalar() or 0

    return {
        "total_licenses": total,
        "by_tier": by_tier,
        "by_status": by_status,
        "active_subscriptions": active_subs,
        "estimated_mrr": round(mrr, 2),
    }


@app.get(
    "/api/v1/admin/audit-logs",
    tags=["Admin"],
    summary="Get audit logs",
)
@limiter.limit("50/minute")
async def get_audit_logs(
    request: Request,
    license_id: Optional[uuid.UUID] = None,
    action: Optional[str] = None,
    limit: int = 100,
    offset: int = 0,
    _: bool = Depends(verify_admin_key),
    db: AsyncSession = Depends(get_db),
):
    """Get audit logs (admin only)"""
    query = select(AuditLog).order_by(AuditLog.created_at.desc())

    if license_id:
        query = query.where(AuditLog.license_id == license_id)
    if action:
        query = query.where(AuditLog.action == action)

    query = query.limit(limit).offset(offset)
    result = await db.execute(query)
    logs = result.scalars().all()

    return [
        {
            "id": log.id,
            "license_id": log.license_id,
            "action": log.action,
            "resource_type": log.resource_type,
            "resource_id": log.resource_id,
            "old_values": log.old_values,
            "new_values": log.new_values,
            "ip_address": log.ip_address,
            "created_at": log.created_at.isoformat(),
        }
        for log in logs
    ]


# -------------------------------------------------------------------------
# Client SDK Info
# -------------------------------------------------------------------------

@app.get(
    "/api/v1/client/info",
    tags=["Client"],
    summary="Get client SDK information",
)
async def client_info():
    """Get information for client SDK"""
    return {
        "server_url": settings.license_server_url,
        "api_version": "v1",
        "public_key": "",  # Embedded in client SDK
        "supported_tiers": [t.value for t in LicenseTier],
    }


# -------------------------------------------------------------------------
# Error Handlers
# -------------------------------------------------------------------------

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail, "status_code": exc.status_code},
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error", "detail": str(exc)},
    )


# -------------------------------------------------------------------------
# Main
# -------------------------------------------------------------------------

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "damon_license.server:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=True,
    )