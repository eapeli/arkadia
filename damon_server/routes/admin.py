"""Admin routes."""
from fastapi import APIRouter, Depends
from pydantic import BaseModel

router = APIRouter()


class AdminStats(BaseModel):
    users: int
    active_licenses: int
    revenue: float


@router.get("/stats", response_model=AdminStats)
async def admin_stats():
    return AdminStats(users=0, active_licenses=0, revenue=0.0)
