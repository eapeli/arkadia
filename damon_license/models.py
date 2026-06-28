"""
Damon License System - Core Models
"""
from __future__ import annotations

import enum
import uuid
from datetime import datetime, timezone
from typing import Optional, List, Dict, Any

from pydantic import BaseModel, Field, field_validator
from sqlalchemy import (
    String, DateTime, Enum, ForeignKey, Index, Text, Boolean, Integer, JSON
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.sql import func


class Base(DeclarativeBase):
    pass


class LicenseStatus(str, enum.Enum):
    ACTIVE = "active"
    EXPIRED = "expired"
    REVOKED = "revoked"
    SUSPENDED = "suspended"
    PENDING = "pending"
    TRIAL = "trial"


class LicenseTier(str, enum.Enum):
    FREE = "free"
    STARTER = "starter"
    PROFESSIONAL = "professional"
    TEAM = "team"
    ENTERPRISE = "enterprise"


class SubscriptionStatus(str, enum.Enum):
    ACTIVE = "active"
    PAST_DUE = "past_due"
    CANCELED = "canceled"
    INCOMPLETE = "incomplete"
    TRIALING = "trialing"
    PAUSED = "paused"


class BillingInterval(str, enum.Enum):
    MONTHLY = "monthly"
    YEARLY = "yearly"


# =============================================================================
# Pydantic Schemas (API)
# =============================================================================

class LicenseFeatures(BaseModel):
    """Feature flags per tier"""
    max_agents: int = 1
    max_concurrent_sessions: int = 1
    max_skills: int = 10
    max_memory_mb: int = 100
    max_tool_calls_per_minute: int = 60
    gateway_platforms: List[str] = Field(default_factory=lambda: ["cli"])
    custom_skills: bool = False
    priority_support: bool = False
    sso_saml: bool = False
    audit_logs: bool = False
    white_label: bool = False
    on_premise: bool = False
    dedicated_support: bool = False
    custom_integrations: bool = False
    sla_uptime: float = 0.0  # 99.9 = 99.9%

    @classmethod
    def for_tier(cls, tier: LicenseTier) -> "LicenseFeatures":
        features = {
            LicenseTier.FREE: cls(
                max_agents=1,
                max_concurrent_sessions=1,
                max_skills=5,
                max_memory_mb=50,
                max_tool_calls_per_minute=30,
                gateway_platforms=["cli"],
            ),
            LicenseTier.STARTER: cls(
                max_agents=3,
                max_concurrent_sessions=2,
                max_skills=20,
                max_memory_mb=500,
                max_tool_calls_per_minute=120,
                gateway_platforms=["cli", "telegram", "discord"],
                custom_skills=True,
            ),
            LicenseTier.PROFESSIONAL: cls(
                max_agents=10,
                max_concurrent_sessions=5,
                max_skills=100,
                max_memory_mb=2048,
                max_tool_calls_per_minute=600,
                gateway_platforms=["cli", "telegram", "discord", "slack", "whatsapp", "webhook"],
                custom_skills=True,
                priority_support=True,
                audit_logs=True,
            ),
            LicenseTier.TEAM: cls(
                max_agents=50,
                max_concurrent_sessions=20,
                max_skills=500,
                max_memory_mb=10240,
                max_tool_calls_per_minute=3000,
                gateway_platforms=["cli", "telegram", "discord", "slack", "whatsapp", "webhook", "teams", "matrix", "signal"],
                custom_skills=True,
                priority_support=True,
                audit_logs=True,
                sso_saml=True,
                custom_integrations=True,
                sla_uptime=99.5,
            ),
            LicenseTier.ENTERPRISE: cls(
                max_agents=9999,
                max_concurrent_sessions=9999,
                max_skills=9999,
                max_memory_mb=999999,
                max_tool_calls_per_minute=999999,
                gateway_platforms=["cli", "telegram", "discord", "slack", "whatsapp", "webhook", "teams", "matrix", "signal", "email", "sms", "custom"],
                custom_skills=True,
                priority_support=True,
                audit_logs=True,
                sso_saml=True,
                white_label=True,
                on_premise=True,
                dedicated_support=True,
                custom_integrations=True,
                sla_uptime=99.9,
            ),
        }
        return features.get(tier, features[LicenseTier.FREE])


class LicenseBase(BaseModel):
    tier: LicenseTier = LicenseTier.FREE
    status: LicenseStatus = LicenseStatus.PENDING
    features: Optional[LicenseFeatures] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)

    @field_validator("features", mode="before")
    @classmethod
    def set_features_from_tier(cls, v, info):
        if v is None and "tier" in info.data:
            return LicenseFeatures.for_tier(info.data["tier"])
        return v


class LicenseCreate(LicenseBase):
    user_email: str
    user_name: Optional[str] = None
    organization: Optional[str] = None
    stripe_customer_id: Optional[str] = None
    trial_days: int = 14


class LicenseUpdate(BaseModel):
    tier: Optional[LicenseTier] = None
    status: Optional[LicenseStatus] = None
    features: Optional[LicenseFeatures] = None
    metadata: Optional[Dict[str, Any]] = None


class LicenseResponse(LicenseBase):
    id: uuid.UUID
    key: str  # Public license key (prefix + hash)
    user_email: str
    user_name: Optional[str]
    organization: Optional[str]
    stripe_customer_id: Optional[str]
    stripe_subscription_id: Optional[str]
    issued_at: datetime
    expires_at: Optional[datetime]
    last_validated_at: Optional[datetime]
    validation_count: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class LicenseValidateRequest(BaseModel):
    key: str
    machine_id: Optional[str] = None
    version: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)


class LicenseValidateResponse(BaseModel):
    valid: bool
    license: Optional[LicenseResponse] = None
    error: Optional[str] = None
    features: Optional[LicenseFeatures] = None
    expires_in_days: Optional[int] = None


class SubscriptionBase(BaseModel):
    stripe_subscription_id: str
    stripe_price_id: str
    tier: LicenseTier
    status: SubscriptionStatus
    interval: BillingInterval
    current_period_start: datetime
    current_period_end: datetime
    trial_end: Optional[datetime] = None
    cancel_at_period_end: bool = False
    metadata: Dict[str, Any] = Field(default_factory=dict)


class SubscriptionCreate(SubscriptionBase):
    license_id: uuid.UUID


class SubscriptionResponse(SubscriptionBase):
    id: uuid.UUID
    license_id: uuid.UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class CheckoutSessionRequest(BaseModel):
    tier: LicenseTier
    interval: BillingInterval = BillingInterval.MONTHLY
    email: str
    name: Optional[str] = None
    organization: Optional[str] = None
    trial_days: int = 14
    success_url: Optional[str] = None
    cancel_url: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)


class CheckoutSessionResponse(BaseModel):
    session_id: str
    url: str


class PortalSessionRequest(BaseModel):
    license_key: str
    return_url: Optional[str] = None


class PortalSessionResponse(BaseModel):
    url: str


class WebhookEvent(BaseModel):
    id: str
    type: str
    data: Dict[str, Any]
    created: int


# =============================================================================
# SQLAlchemy Models (Database)
# =============================================================================

class License(Base):
    __tablename__ = "licenses"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    key_hash: Mapped[str] = mapped_column(String(64), unique=True, index=True, nullable=False)
    key_prefix: Mapped[str] = mapped_column(String(16), index=True, nullable=False)
    tier: Mapped[LicenseTier] = mapped_column(Enum(LicenseTier), default=LicenseTier.FREE, nullable=False)
    status: Mapped[LicenseStatus] = mapped_column(Enum(LicenseStatus), default=LicenseStatus.PENDING, nullable=False)
    user_email: Mapped[str] = mapped_column(String(255), index=True, nullable=False)
    user_name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    organization: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    stripe_customer_id: Mapped[Optional[str]] = mapped_column(String(255), index=True, nullable=True)
    stripe_subscription_id: Mapped[Optional[str]] = mapped_column(String(255), index=True, nullable=True)
    features: Mapped[Dict[str, Any]] = mapped_column(JSON, default=dict, nullable=False)
    license_metadata: Mapped[Dict[str, Any]] = mapped_column(JSON, default=dict, nullable=False)
    issued_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    expires_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    last_validated_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    validation_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    revoked_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    revoked_reason: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    subscriptions: Mapped[List["Subscription"]] = relationship(back_populates="license", cascade="all, delete-orphan")
    validations: Mapped[List["LicenseValidation"]] = relationship(back_populates="license", cascade="all, delete-orphan")
    machines: Mapped[List["LicenseMachine"]] = relationship(back_populates="license", cascade="all, delete-orphan")

    __table_args__ = (
        Index("ix_licenses_email_status", "user_email", "status"),
        Index("ix_licenses_stripe_sub", "stripe_subscription_id"),
    )


class Subscription(Base):
    __tablename__ = "subscriptions"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    license_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("licenses.id", ondelete="CASCADE"), nullable=False)
    stripe_subscription_id: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    stripe_price_id: Mapped[str] = mapped_column(String(255), nullable=False)
    tier: Mapped[LicenseTier] = mapped_column(Enum(LicenseTier), nullable=False)
    status: Mapped[SubscriptionStatus] = mapped_column(Enum(SubscriptionStatus), nullable=False)
    interval: Mapped[BillingInterval] = mapped_column(Enum(BillingInterval), nullable=False)
    current_period_start: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    current_period_end: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    trial_end: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    cancel_at_period_end: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    canceled_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    subscription_metadata: Mapped[Dict[str, Any]] = mapped_column(JSON, default=dict, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    license: Mapped["License"] = relationship(back_populates="subscriptions")


class LicenseValidation(Base):
    __tablename__ = "license_validations"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    license_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("licenses.id", ondelete="CASCADE"), nullable=False)
    machine_id: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    version: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    ip_address: Mapped[Optional[str]] = mapped_column(String(45), nullable=True)
    user_agent: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    validation_metadata: Mapped[Dict[str, Any]] = mapped_column(JSON, default=dict, nullable=False)
    success: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    error: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    license: Mapped["License"] = relationship(back_populates="validations")

    __table_args__ = (
        Index("ix_validations_license_created", "license_id", "created_at"),
        Index("ix_validations_machine", "machine_id"),
    )


class LicenseMachine(Base):
    __tablename__ = "license_machines"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    license_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("licenses.id", ondelete="CASCADE"), nullable=False)
    machine_id: Mapped[str] = mapped_column(String(255), index=True, nullable=False)
    machine_name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    platform: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    first_seen: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    last_seen: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    machine_metadata: Mapped[Dict[str, Any]] = mapped_column(JSON, default=dict, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    license: Mapped["License"] = relationship(back_populates="machines")

    __table_args__ = (
        Index("ix_machines_license_machine", "license_id", "machine_id", unique=True),
    )


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    license_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("licenses.id", ondelete="SET NULL"), nullable=True)
    user_id: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    action: Mapped[str] = mapped_column(String(100), nullable=False)
    resource_type: Mapped[str] = mapped_column(String(100), nullable=False)
    resource_id: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    old_values: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True)
    new_values: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True)
    ip_address: Mapped[Optional[str]] = mapped_column(String(45), nullable=True)
    user_agent: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    __table_args__ = (
        Index("ix_audit_license_created", "license_id", "created_at"),
        Index("ix_audit_action_created", "action", "created_at"),
    )