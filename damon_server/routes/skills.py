"""
Damon Server - Skills Routes
"""
from __future__ import annotations

from typing import List, Optional
from uuid import UUID
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, Query, status, UploadFile, File
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

from damon_server.auth import require_auth, require_permission, TokenData
from damon_server.database import get_db

router = APIRouter(prefix="/skills", tags=["Skills"])


# Schemas
class SkillBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    display_name: str = Field(..., min_length=1, max_length=200)
    description: str
    category: str
    version: str = "1.0.0"
    author: Optional[str] = None
    license: str = "MIT"
    repository: Optional[str] = None
    homepage: Optional[str] = None
    tags: List[str] = []
    requires_license_tier: str = "free"
    config_schema: dict = {}
    default_config: dict = {}


class SkillCreate(SkillBase):
    pass


class SkillUpdate(BaseModel):
    display_name: Optional[str] = None
    description: Optional[str] = None
    version: Optional[str] = None
    tags: Optional[List[str]] = None
    requires_license_tier: Optional[str] = None
    config_schema: Optional[dict] = None
    default_config: Optional[dict] = None
    is_active: Optional[bool] = None


class SkillResponse(SkillBase):
    id: UUID
    is_active: bool = True
    is_official: bool = False
    download_count: int = 0
    rating: float = 0.0
    created_at: str
    updated_at: str

    class Config:
        from_attributes = True


class SkillListResponse(BaseModel):
    skills: List[SkillResponse]
    total: int
    page: int
    page_size: int


class SkillInstallRequest(BaseModel):
    skill_id: UUID
    config: dict = {}


class SkillInstallResponse(BaseModel):
    success: bool
    skill_id: UUID
    message: str


# In-memory storage
_skills_db: dict = {}


# Initialize with some default skills
def _init_default_skills():
    default_skills = [
        {
            "id": "00000000-0000-0000-0000-000000000001",
            "name": "web-search",
            "display_name": "Web Search",
            "description": "Search the web for information",
            "category": "research",
            "version": "1.0.0",
            "author": "Damon Team",
            "license": "MIT",
            "tags": ["search", "web", "research"],
            "requires_license_tier": "free",
            "is_official": True,
            "is_active": True,
            "download_count": 10000,
            "rating": 4.8,
        },
        {
            "id": "00000000-0000-0000-0000-000000000002",
            "name": "code-execution",
            "display_name": "Code Execution",
            "description": "Execute code in sandboxed environment",
            "category": "development",
            "version": "1.0.0",
            "author": "Damon Team",
            "license": "MIT",
            "tags": ["code", "python", "execution"],
            "requires_license_tier": "starter",
            "is_official": True,
            "is_active": True,
            "download_count": 8000,
            "rating": 4.9,
        },
        {
            "id": "00000000-0000-0000-0000-000000000003",
            "name": "file-operations",
            "display_name": "File Operations",
            "description": "Read, write, and manage files",
            "category": "utility",
            "version": "1.0.0",
            "author": "Damon Team",
            "license": "MIT",
            "tags": ["files", "read", "write"],
            "requires_license_tier": "free",
            "is_official": True,
            "is_active": True,
            "download_count": 12000,
            "rating": 4.7,
        },
    ]

    for skill in default_skills:
        skill["created_at"] = datetime.now(timezone.utc).isoformat()
        skill["updated_at"] = datetime.now(timezone.utc).isoformat()
        _skills_db[skill["id"]] = SkillResponse(**skill)


_init_default_skills()


@router.get(
    "",
    response_model=SkillListResponse,
    summary="List skills",
)
async def list_skills(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    category: Optional[str] = None,
    tier: Optional[str] = None,
    search: Optional[str] = None,
    official_only: bool = Query(False),
    current_user: TokenData = Depends(require_auth),
    db: AsyncSession = Depends(get_db),
):
    """List available skills"""
    skills = list(_skills_db.values())

    # Filter by tier access
    tier_hierarchy = {"free": 0, "starter": 1, "professional": 2, "team": 3, "enterprise": 4}
    user_tier_level = tier_hierarchy.get(current_user.tier, 0)
    skills = [s for s in skills if tier_hierarchy.get(s.requires_license_tier, 0) <= user_tier_level]

    # Filter by category
    if category:
        skills = [s for s in skills if s.category == category]

    # Filter by tier
    if tier:
        skills = [s for s in skills if s.requires_license_tier == tier]

    # Filter official
    if official_only:
        skills = [s for s in skills if s.is_official]

    # Search
    if search:
        search_lower = search.lower()
        skills = [
            s for s in skills
            if search_lower in s.name.lower()
            or search_lower in s.display_name.lower()
            or search_lower in s.description.lower()
            or any(search_lower in tag.lower() for tag in s.tags)
        ]

    # Sort by popularity
    skills.sort(key=lambda s: s.download_count, reverse=True)

    total = len(skills)
    start = (page - 1) * page_size
    end = start + page_size

    return SkillListResponse(
        skills=skills[start:end],
        total=total,
        page=page,
        page_size=page_size,
    )


@router.get(
    "/categories",
    summary="Get skill categories",
)
async def get_categories(
    current_user: TokenData = Depends(require_auth),
):
    """Get all skill categories"""
    categories = set()
    for skill in _skills_db.values():
        categories.add(skill.category)
    return {"categories": sorted(categories)}


@router.get(
    "/{skill_id}",
    response_model=SkillResponse,
    summary="Get skill by ID",
)
async def get_skill(
    skill_id: UUID,
    current_user: TokenData = Depends(require_auth),
    db: AsyncSession = Depends(get_db),
):
    """Get skill by ID"""
    skill = _skills_db.get(str(skill_id))
    if not skill:
        raise HTTPException(status_code=404, detail="Skill not found")

    # Check tier access
    tier_hierarchy = {"free": 0, "starter": 1, "professional": 2, "team": 3, "enterprise": 4}
    user_tier_level = tier_hierarchy.get(current_user.tier, 0)
    if tier_hierarchy.get(skill.requires_license_tier, 0) > user_tier_level:
        raise HTTPException(status_code=403, detail="Skill requires higher license tier")

    return skill


@router.post(
    "",
    response_model=SkillResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create skill (admin only)",
)
async def create_skill(
    skill: SkillCreate,
    current_user: TokenData = Depends(require_permission("skills:create")),
    db: AsyncSession = Depends(get_db),
):
    """Create a new skill (admin only)"""
    import uuid

    skill_id = uuid.uuid4()
    now = datetime.now(timezone.utc).isoformat()

    skill_data = SkillResponse(
        id=skill_id,
        is_active=True,
        is_official=False,
        download_count=0,
        rating=0.0,
        created_at=now,
        updated_at=now,
        **skill.model_dump(),
    )

    _skills_db[str(skill_id)] = skill_data
    return skill_data


@router.patch(
    "/{skill_id}",
    response_model=SkillResponse,
    summary="Update skill (admin only)",
)
async def update_skill(
    skill_id: UUID,
    skill_update: SkillUpdate,
    current_user: TokenData = Depends(require_permission("skills:update")),
    db: AsyncSession = Depends(get_db),
):
    """Update a skill (admin only)"""
    skill = _skills_db.get(str(skill_id))
    if not skill:
        raise HTTPException(status_code=404, detail="Skill not found")

    update_data = skill_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(skill, field, value)

    skill.updated_at = datetime.now(timezone.utc).isoformat()
    _skills_db[str(skill_id)] = skill

    return skill


@router.delete(
    "/{skill_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete skill (admin only)",
)
async def delete_skill(
    skill_id: UUID,
    current_user: TokenData = Depends(require_permission("skills:delete")),
    db: AsyncSession = Depends(get_db),
):
    """Delete a skill (admin only)"""
    skill = _skills_db.get(str(skill_id))
    if not skill:
        raise HTTPException(status_code=404, detail="Skill not found")

    if skill.is_official:
        raise HTTPException(status_code=400, detail="Cannot delete official skills")

    del _skills_db[str(skill_id)]


@router.post(
    "/{skill_id}/install",
    response_model=SkillInstallResponse,
    summary="Install skill for current user",
)
async def install_skill(
    skill_id: UUID,
    request: SkillInstallRequest,
    current_user: TokenData = Depends(require_permission("skills:install")),
    db: AsyncSession = Depends(get_db),
):
    """Install a skill for the current user"""
    skill = _skills_db.get(str(skill_id))
    if not skill:
        raise HTTPException(status_code=404, detail="Skill not found")

    # Check tier access
    tier_hierarchy = {"free": 0, "starter": 1, "professional": 2, "team": 3, "enterprise": 4}
    user_tier_level = tier_hierarchy.get(current_user.tier, 0)
    if tier_hierarchy.get(skill.requires_license_tier, 0) > user_tier_level:
        raise HTTPException(
            status_code=403,
            detail=f"Skill requires {skill.requires_license_tier} tier or higher",
        )

    # In production, save to user's installed skills
    skill.download_count += 1
    _skills_db[str(skill_id)] = skill

    return SkillInstallResponse(
        success=True,
        skill_id=skill_id,
        message=f"Skill '{skill.display_name}' installed successfully",
    )


@router.post(
    "/{skill_id}/uninstall",
    response_model=SkillInstallResponse,
    summary="Uninstall skill for current user",
)
async def uninstall_skill(
    skill_id: UUID,
    current_user: TokenData = Depends(require_permission("skills:install")),
    db: AsyncSession = Depends(get_db),
):
    """Uninstall a skill for the current user"""
    skill = _skills_db.get(str(skill_id))
    if not skill:
        raise HTTPException(status_code=404, detail="Skill not found")

    # In production, remove from user's installed skills
    return SkillInstallResponse(
        success=True,
        skill_id=skill_id,
        message=f"Skill '{skill.display_name}' uninstalled successfully",
    )


@router.get(
    "/installed/list",
    response_model=List[SkillResponse],
    summary="List installed skills for current user",
)
async def list_installed_skills(
    current_user: TokenData = Depends(require_auth),
    db: AsyncSession = Depends(get_db),
):
    """List skills installed by current user"""
    # In production, query user's installed skills
    # For now, return all active skills they have access to
    tier_hierarchy = {"free": 0, "starter": 1, "professional": 2, "team": 3, "enterprise": 4}
    user_tier_level = tier_hierarchy.get(current_user.tier, 0)

    skills = [
        s for s in _skills_db.values()
        if s.is_active and tier_hierarchy.get(s.requires_license_tier, 0) <= user_tier_level
    ]
    return skills