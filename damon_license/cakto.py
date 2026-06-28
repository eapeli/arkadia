"""Cakto Payment Gateway Integration for Damon Licensing System."""
from __future__ import annotations

import os
import uuid
import json
import time
import logging
from typing import Optional, Dict, Any, List
from dataclasses import dataclass
from enum import Enum

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

logger = logging.getLogger(__name__)


class CaktoEnvironment(Enum):
    PRODUCTION = "production"
    SANDBOX = "sandbox"


@dataclass
class CaktoConfig:
    client_id: str
    client_secret: str
    environment: CaktoEnvironment = CaktoEnvironment.PRODUCTION
    base_url: Optional[str] = None

    def __post_init__(self):
        if self.base_url is None:
            if self.environment == CaktoEnvironment.PRODUCTION:
                self.base_url = "https://api.cakto.com.br"
            else:
                self.base_url = "https://api-sandbox.cakto.com.br"


@dataclass
class AccessToken:
    access_token: str
    expires_in: int
    token_type: str
    scope: str
    obtained_at: float = 0.0

    @property
    def is_expired(self) -> bool:
        if self.obtained_at == 0:
            return True
        return time.time() >= (self.obtained_at + self.expires_in - 60)  # 60s buffer


class CaktoAPIError(Exception):
    def __init__(self, message: str, status_code: int = 0, response_data: Optional[Dict] = None):
        super().__init__(message)
        self.status_code = status_code
        self.response_data = response_data or {}


class CaktoClient:
    """Cakto API Client with automatic token management."""

    def __init__(self, config: CaktoConfig):
        self.config = config
        self.token: Optional[AccessToken] = None
        self.session = self._create_session()

    def _create_session(self) -> requests.Session:
        session = requests.Session()
        retry_strategy = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["HEAD", "GET", "OPTIONS", "POST"]
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        return session

    def _get_token(self) -> str:
        if self.token is None or self.token.is_expired:
            self._refresh_token()
        return self.token.access_token

    def _refresh_token(self) -> None:
        url = f"{self.config.base_url}/public_api/token/"
        data = {
            "client_id": self.config.client_id,
            "client_secret": self.config.client_secret,
        }
        headers = {"Content-Type": "application/x-www-form-urlencoded"}

        try:
            response = self.session.post(url, data=data, headers=headers, timeout=30)
            response.raise_for_status()
            token_data = response.json()

            self.token = AccessToken(
                access_token=token_data["access_token"],
                expires_in=token_data["expires_in"],
                token_type=token_data["token_type"],
                scope=token_data.get("scope", ""),
                obtained_at=time.time()
            )
            logger.info("Cakto token refreshed successfully")
        except requests.RequestException as e:
            logger.error(f"Failed to refresh Cakto token: {e}")
            raise CaktoAPIError(f"Authentication failed: {e}", status_code=getattr(e.response, 'status_code', 0))

    def _request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        url = f"{self.config.base_url}{endpoint}"
        headers = kwargs.pop("headers", {})
        headers.update({
            "Authorization": f"Bearer {self._get_token()}",
            "Content-Type": "application/json",
        })

        # Add idempotency key for mutating requests
        if method.upper() in ("POST", "PUT", "PATCH", "DELETE"):
            headers.setdefault("X-Idempotency-Key", str(uuid.uuid4()))

        try:
            response = self.session.request(method, url, headers=headers, timeout=30, **kwargs)
            
            if response.status_code == 401:
                # Token might be expired, force refresh and retry once
                self.token = None
                headers["Authorization"] = f"Bearer {self._get_token()}"
                response = self.session.request(method, url, headers=headers, timeout=30, **kwargs)

            response.raise_for_status()
            
            if response.content:
                return response.json()
            return {}
        except requests.RequestException as e:
            status_code = getattr(e.response, 'status_code', 0)
            response_data = {}
            if e.response is not None:
                try:
                    response_data = e.response.json()
                except Exception:
                    pass
            logger.error(f"Cakto API error: {method} {endpoint} - {e}")
            raise CaktoAPIError(f"API request failed: {e}", status_code=status_code, response_data=response_data)

    # Payment Methods
    def create_pix_charge(
        self,
        product_id: str,
        offer_id: str,
        customer: Dict[str, Any],
        amount: float,
        pix_expires_in: int = 3600,
        metadata: Optional[Dict[str, str]] = None,
        affiliate_short_id: Optional[str] = None,
        coupon: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Create a PIX charge for license purchase."""
        payload = {
            "productId": product_id,
            "paymentMethod": "pix",
            "customer": customer,
            "items": [{"offerId": offer_id, "quantity": 1, "offerType": "main"}],
            "pixExpiresIn": pix_expires_in,
        }
        
        if metadata:
            payload["metadata"] = metadata
        if affiliate_short_id:
            payload["affiliateShortId"] = affiliate_short_id
        if coupon:
            payload["coupon"] = coupon

        return self._request("POST", "/public_api/payments/", json=payload)

    def create_boleto_charge(
        self,
        product_id: str,
        offer_id: str,
        customer: Dict[str, Any],
        due_date: str,
        metadata: Optional[Dict[str, str]] = None,
        affiliate_short_id: Optional[str] = None,
        coupon: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Create a Boleto charge for license purchase."""
        payload = {
            "productId": product_id,
            "paymentMethod": "boleto",
            "customer": customer,
            "items": [{"offerId": offer_id, "quantity": 1, "offerType": "main"}],
            "dueDate": due_date,
        }
        
        if metadata:
            payload["metadata"] = metadata
        if affiliate_short_id:
            payload["affiliateShortId"] = affiliate_short_id
        if coupon:
            payload["coupon"] = coupon

        return self._request("POST", "/public_api/payments/", json=payload)

    def create_credit_card_charge(
        self,
        product_id: str,
        offer_id: str,
        customer: Dict[str, Any],
        card_token: str,
        metadata: Optional[Dict[str, str]] = None,
        affiliate_short_id: Optional[str] = None,
        coupon: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Create a credit card charge (3DS) for license purchase."""
        payload = {
            "productId": product_id,
            "paymentMethod": "threeDs",
            "customer": customer,
            "items": [{"offerId": offer_id, "quantity": 1, "offerType": "main"}],
            "cardToken": card_token,
        }
        
        if metadata:
            payload["metadata"] = metadata
        if affiliate_short_id:
            payload["affiliateShortId"] = affiliate_short_id
        if coupon:
            payload["coupon"] = coupon

        return self._request("POST", "/public_api/payments/", json=payload)

    def get_payment(self, payment_id: str) -> Dict[str, Any]:
        """Get payment details by ID."""
        return self._request("GET", f"/public_api/payments/{payment_id}/")

    def list_subscriptions(
        self,
        status: Optional[str] = None,
        payment_method: Optional[str] = None,
        current_situation: Optional[str] = None,
        search: Optional[str] = None,
        page: int = 1,
        limit: int = 50,
    ) -> Dict[str, Any]:
        """List subscriptions with filters."""
        params = {"page": page, "limit": limit}
        if status:
            params["status"] = status
        if payment_method:
            params["paymentMethod"] = payment_method
        if current_situation:
            params["current_situation"] = current_situation
        if search:
            params["search"] = search
        
        return self._request("GET", "/public_api/subscriptions/", params=params)

    def get_subscription(self, subscription_id: str) -> Dict[str, Any]:
        """Get subscription details by ID."""
        return self._request("GET", f"/public_api/subscriptions/{subscription_id}/")

    def cancel_subscription(self, subscription_id: str) -> Dict[str, Any]:
        """Cancel a subscription."""
        return self._request("POST", f"/public_api/subscriptions/{subscription_id}/cancel/")

    def get_products(self) -> Dict[str, Any]:
        """List all products."""
        return self._request("GET", "/public_api/products/")

    def get_product(self, product_id: str) -> Dict[str, Any]:
        """Get product details."""
        return self._request("GET", f"/public_api/products/{product_id}/")

    def get_offers(self, product_id: str) -> Dict[str, Any]:
        """Get offers for a product."""
        return self._request("GET", f"/public_api/products/{product_id}/offers/")


def create_cakto_client_from_env() -> CaktoClient:
    """Create CaktoClient from environment variables."""
    client_id = os.getenv("CAKTO_CLIENT_ID")
    client_secret = os.getenv("CAKTO_CLIENT_SECRET")
    environment = os.getenv("CAKTO_ENVIRONMENT", "production").lower()

    if not client_id or not client_secret:
        raise ValueError("CAKTO_CLIENT_ID and CAKTO_CLIENT_SECRET must be set in environment")

    env = CaktoEnvironment.SANDBOX if environment == "sandbox" else CaktoEnvironment.PRODUCTION
    config = CaktoConfig(client_id=client_id, client_secret=client_secret, environment=env)
    return CaktoClient(config)


# Convenience functions for licensing integration
@dataclass
class LicensePaymentRequest:
    license_tier: str  # "pro", "enterprise", "team"
    billing_cycle: str  # "monthly", "yearly"
    customer_email: str
    customer_name: str
    customer_phone: str
    customer_document: str  # CPF/CNPJ
    customer_fingerprint: str
    payment_method: str  # "pix", "boleto", "credit_card"
    metadata: Optional[Dict[str, str]] = None


@dataclass
class LicensePaymentResult:
    payment_id: str
    ref_id: str
    status: str
    amount: str
    payment_method: str
    pix_qr_code: Optional[str] = None
    pix_qr_code_base64: Optional[str] = None
    pix_expires_at: Optional[str] = None
    boleto_barcode: Optional[str] = None
    boleto_pdf_url: Optional[str] = None
    boleto_due_date: Optional[str] = None
    checkout_url: Optional[str] = None


class CaktoLicensingService:
    """High-level service for handling Damon license payments via Cakto."""

    # Product/Offer mapping for Damon tiers
    TIER_MAPPING = {
        "pro": {
            "monthly": {"product_id": "damon-pro", "offer_id": "damon-pro-monthly"},
            "yearly": {"product_id": "damon-pro", "offer_id": "damon-pro-yearly"},
        },
        "enterprise": {
            "monthly": {"product_id": "damon-enterprise", "offer_id": "damon-enterprise-monthly"},
            "yearly": {"product_id": "damon-enterprise", "offer_id": "damon-enterprise-yearly"},
        },
        "team": {
            "monthly": {"product_id": "damon-team", "offer_id": "damon-team-monthly"},
            "yearly": {"product_id": "damon-team", "offer_id": "damon-team-yearly"},
        },
    }

    def __init__(self, client: CaktoClient):
        self.client = client

    def _get_product_offer(self, tier: str, cycle: str) -> tuple[str, str]:
        try:
            mapping = self.TIER_MAPPING[tier][cycle]
            return mapping["product_id"], mapping["offer_id"]
        except KeyError:
            raise ValueError(f"Invalid tier/cycle combination: {tier}/{cycle}")

    def create_license_payment(self, request: LicensePaymentRequest) -> LicensePaymentResult:
        """Create a payment for a new license purchase."""
        product_id, offer_id = self._get_product_offer(request.license_tier, request.billing_cycle)

        customer = {
            "name": request.customer_name,
            "email": request.customer_email,
            "phone": request.customer_phone,
            "fingerprint": request.customer_fingerprint,
            "docType": "cpf" if len(request.customer_document) == 11 else "cnpj",
            "docNumber": request.customer_document,
        }

        metadata = {
            "license_tier": request.license_tier,
            "billing_cycle": request.billing_cycle,
            "damon_version": "1.0.0",
        }
        if request.metadata:
            metadata.update(request.metadata)

        if request.payment_method == "pix":
            response = self.client.create_pix_charge(
                product_id=product_id,
                offer_id=offer_id,
                customer=customer,
                amount=0,  # Amount is determined by offer
                pix_expires_in=3600,
                metadata=metadata,
            )
            return LicensePaymentResult(
                payment_id=response["id"],
                ref_id=response["refId"],
                status=response["status"],
                amount=response["amount"],
                payment_method=response["paymentMethod"],
                pix_qr_code=response.get("pix", {}).get("qrCode"),
                pix_qr_code_base64=response.get("pix", {}).get("qrCodeBase64"),
                pix_expires_at=response.get("pix", {}).get("expirationDate"),
                checkout_url=response.get("checkoutUrl"),
            )

        elif request.payment_method == "boleto":
            # Due date: 3 days from now
            from datetime import datetime, timedelta
            due_date = (datetime.now() + timedelta(days=3)).strftime("%Y-%m-%d")
            
            response = self.client.create_boleto_charge(
                product_id=product_id,
                offer_id=offer_id,
                customer=customer,
                due_date=due_date,
                metadata=metadata,
            )
            return LicensePaymentResult(
                payment_id=response["id"],
                ref_id=response["refId"],
                status=response["status"],
                amount=response["amount"],
                payment_method=response["paymentMethod"],
                boleto_barcode=response.get("boleto", {}).get("barcode"),
                boleto_pdf_url=response.get("boleto", {}).get("pdfUrl"),
                boleto_due_date=response.get("boleto", {}).get("dueDate"),
                checkout_url=response.get("checkoutUrl"),
            )

        elif request.payment_method == "credit_card":
            # Requires card_token from Cakto SDK frontend
            raise NotImplementedError("Credit card payments require frontend SDK integration. Use create_credit_card_charge directly.")

        else:
            raise ValueError(f"Unsupported payment method: {request.payment_method}")

    def check_payment_status(self, payment_id: str) -> Dict[str, Any]:
        """Check the status of a payment."""
        return self.client.get_payment(payment_id)

    def get_subscription_by_customer(self, customer_email: str) -> List[Dict[str, Any]]:
        """Get all subscriptions for a customer email."""
        response = self.client.list_subscriptions(search=customer_email)
        return response.get("results", [])

    def cancel_subscription(self, subscription_id: str) -> Dict[str, Any]:
        """Cancel a customer's subscription."""
        return self.client.cancel_subscription(subscription_id)