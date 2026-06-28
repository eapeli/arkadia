"""Billing routes."""
from fastapi import APIRouter, Depends
from pydantic import BaseModel

router = APIRouter()


class CheckoutRequest(BaseModel):
    plan: str
    interval: str = "monthly"


class CheckoutResponse(BaseModel):
    checkout_url: str


@router.post("/checkout", response_model=CheckoutResponse)
async def create_checkout(req: CheckoutRequest):
    return CheckoutResponse(checkout_url=f"https://billing.example.com/checkout?plan={req.plan}&interval={req.interval}")
