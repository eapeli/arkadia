"""
Damon License System - Client SDK
"""
from damon_license.client import (
    DamonLicenseClient,
    MachineInfo,
    LicenseCache,
    get_license_client,
    validate_license,
    check_feature,
    get_limit,
    LicenseCLI,
)
from damon_license.models import (
    LicenseTier,
    LicenseStatus,
    LicenseFeatures,
    LicenseValidateRequest,
    LicenseValidateResponse,
    LicenseResponse,
    LicenseCreate,
    LicenseUpdate,
    SubscriptionStatus,
    BillingInterval,
    CheckoutSessionRequest,
    CheckoutSessionResponse,
    PortalSessionRequest,
    PortalSessionResponse,
)

__version__ = "0.1.0"

__all__ = [
    # Client
    "DamonLicenseClient",
    "MachineInfo",
    "LicenseCache",
    "get_license_client",
    "validate_license",
    "check_feature",
    "get_limit",
    "LicenseCLI",
    # Models
    "LicenseTier",
    "LicenseStatus",
    "LicenseFeatures",
    "LicenseValidateRequest",
    "LicenseValidateResponse",
    "LicenseResponse",
    "LicenseCreate",
    "LicenseUpdate",
    "SubscriptionStatus",
    "BillingInterval",
    "CheckoutSessionRequest",
    "CheckoutSessionResponse",
    "PortalSessionRequest",
    "PortalSessionResponse",
]