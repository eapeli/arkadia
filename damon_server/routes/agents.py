"""
Damon Server - Agents Routes
"""
from __future__ import annotations

from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel, Field
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from damon_server.auth import require_auth, require_permission, TokenData
from damon_server.database import get_db

router = APIRouter(prefix="/agents", tags=["Agents"])


# Schemas
class AgentBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    model: str = "gpt-4"
    provider: str = "openai"
    temperature: float = Field(default=0.7, ge=0, le=2)
    max_tokens: int = Field(default=4096, ge=1, le=128000)
    system_prompt: Optional[str] = None
    enabled_tools: List[str] = []
    disabled_tools: List[str] = []
    config: dict = {}


class AgentCreate(AgentBase):
    pass


class AgentUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = None
    model: Optional[str] = None
    provider: Optional[str] = None
    temperature: Optional[float] = Field(None, ge=0, le=2)
    max_tokens: Optional[int] = Field(None, ge=1, le=128000)
    system_prompt: Optional[str] = None
    enabled_tools: Optional[List[str]] = None
    disabled_tools: Optional[List[str]] = None
    config: Optional[dict] = None


class AgentResponse(AgentBase):
    id: UUID
    owner_id: UUID
    status: str
    created_at: str
    updated_at: str

    class Config:
        from_attributes = True


class AgentListResponse(BaseModel):
    agents: List[AgentResponse]
    total: int
    page: int
    page_size: int


# In-memory storage (replace with database model)
_agents_db: dict = {}


@router.post(
    "",
    response_model=AgentResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new agent",
)
async def create_agent(
    agent: AgentCreate,
    current_user: TokenData = Depends(require_permission("agents:create")),
    db: AsyncSession = Depends(get_db),
):
    """Create a new agent"""
    import uuid
    from datetime import datetime, timezone

    agent_id = uuid.uuid4()
    now = datetime.now(timezone.utc).isoformat()

    agent_data = AgentResponse(
        id=agent_id,
        owner_id=current_user.user_id or uuid.uuid4(),
        status="created",
        created_at=now,
        updated_at=now,
        **agent.model_dump(),
    )

    _agents_db[str(agent_id)] = agent_data
    return agent_data


@router.get(
    "",
    response_model=AgentListResponse,
    summary="List agents",
)
async def list_agents(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    status: Optional[str] = None,
    current_user: TokenData = Depends(require_auth),
    db: AsyncSession = Depends(get_db),
):
    """List agents with pagination"""
    agents = list(_agents_db.values())

    # Filter by owner (unless admin)
    if "admin" not in current_user.scopes:
        agents = [a for a in agents if a.owner_id == current_user.user_id]

    # Filter by status
    if status:
        agents = [a for a in agents if a.status == status]

    total = len(agents)
    start = (page - 1) * page_size
    end = start + page_size

    return AgentListResponse(
        agents=agents[start:end],
        total=total,
        page=page,
        page_size=page_size,
    )


@router.get(
    "/{agent_id}",
    response_model=AgentResponse,
    summary="Get agent by ID",
)
async def get_agent(
    agent_id: UUID,
    current_user: TokenData = Depends(require_auth),
    db: AsyncSession = Depends(get_db),
):
    """Get agent by ID"""
    agent = _agents_db.get(str(agent_id))
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")

    # Check ownership
    if "admin" not in current_user.scopes and agent.owner_id != current_user.user_id:
        raise HTTPException(status_code=403, detail="Not authorized")

    return agent


@router.patch(
    "/{agent_id}",
    response_model=AgentResponse,
    summary="Update agent",
)
async def update_agent(
    agent_id: UUID,
    agent_update: AgentUpdate,
    current_user: TokenData = Depends(require_permission("agents:update")),
    db: AsyncSession = Depends(get_db),
):
    """Update an agent"""
    agent = _agents_db.get(str(agent_id))
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")

    # Check ownership
    if "admin" not in current_user.scopes and agent.owner_id != current_user.user_id:
        raise HTTPException(status_code=403, detail="Not authorized")

    # Update fields
    update_data = agent_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(agent, field, value)

    from datetime import datetime, timezone
    agent.updated_at = datetime.now(timezone.utc).isoformat()

    _agents_db[str(agent_id)] = agent
    return agent


@router.delete(
    "/{agent_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete agent",
)
async def delete_agent(
    agent_id: UUID,
    current_user: TokenData = Depends(require_permission("agents:delete")),
    db: AsyncSession = Depends(get_db),
):
    """Delete an agent"""
    agent = _agents_db.get(str(agent_id))
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")

    # Check ownership
    if "admin" not in current_user.scopes and agent.owner_id != current_user.user_id:
        raise HTTPException(status_code=403, detail="Not authorized")

    del _agents_db[str(agent_id)]


@router.post(
    "/{agent_id}/start",
    response_model=AgentResponse,
    summary="Start agent",
)
async def start_agent(
    agent_id: UUID,
    current_user: TokenData = Depends(require_permission("agents:control")),
    db: AsyncSession = Depends(get_db),
):
    """Start an agent"""
    agent = _agents_db.get(str(agent_id))
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")

    if "admin" not in current_user.scopes and agent.owner_id != current_user.user_id:
        raise HTTPException(status_code=403, detail="Not authorized")

    agent.status = "running"
    from datetime import datetime, timezone
    agent.updated_at = datetime.now(timezone.utc).isoformat()
    _agents_db[str(agent_id)] = agent

    return agent


@router.post(
    "/{agent_id}/stop",
    response_model=AgentResponse,
    summary="Stop agent",
)
async def stop_agent(
    agent_id: UUID,
    current_user: TokenData = Depends(require_permission("agents:control")),
    db: AsyncSession = Depends(get_db),
):
    """Stop an agent"""
    agent = _agents_db.get(str(agent_id))
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")

    if "admin" not in current_user.scopes and agent.owner_id != current_user.user_id:
        raise HTTPException(status_code=403, detail="Not authorized")

    agent.status = "stopped"
    from datetime import datetime, timezone
    agent.updated_at = datetime.now(timezone.utc).isoformat()
    _agents_db[str(agent_id)] = agent

    return agent


@router.get(
    "/{agent_id}/logs",
    summary="Get agent logs",
)
async def get_agent_logs(
    agent_id: UUID,
    lines: int = Query(100, ge=1, le=10000),
    current_user: TokenData = Depends(require_auth),
    db: AsyncSession = Depends(get_db),
):
    """Get agent logs"""
    agent = _agents_db.get(str(agent_id))
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")

    if "admin" not in current_user.scopes and agent.owner_id != current_user.user_id:
        raise HTTPException(status_code=403, detail="Not authorized")

    # In production, read from log files
    return {
        "agent_id": str(agent_id),
        "logs": [
            {
                "timestamp": "2026-01-01T00:00:00Z",
                "level": "INFO",
                "message": "Agent started",
            }
        ],
    }