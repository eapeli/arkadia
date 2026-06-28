"""
Damon Server - Sessions Routes
"""
from __future__ import annotations

from typing import List, Optional
from uuid import UUID
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel, Field
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from damon_server.auth import require_auth, require_permission, TokenData
from damon_server.database import get_db

router = APIRouter(prefix="/sessions", tags=["Sessions"])


# Schemas
class SessionBase(BaseModel):
    agent_id: UUID
    title: Optional[str] = None
    metadata: dict = {}


class SessionCreate(SessionBase):
    pass


class SessionUpdate(BaseModel):
    title: Optional[str] = None
    metadata: Optional[dict] = None


class MessageBase(BaseModel):
    role: str  # user, assistant, tool, system
    content: str
    metadata: dict = {}


class MessageCreate(MessageBase):
    pass


class MessageResponse(MessageBase):
    id: UUID
    session_id: UUID
    created_at: str

    class Config:
        from_attributes = True


class SessionResponse(SessionBase):
    id: UUID
    owner_id: UUID
    status: str  # active, archived, completed
    message_count: int = 0
    created_at: str
    updated_at: str
    last_message_at: Optional[str] = None

    class Config:
        from_attributes = True


class SessionListResponse(BaseModel):
    sessions: List[SessionResponse]
    total: int
    page: int
    page_size: int


class SessionWithMessages(SessionResponse):
    messages: List[MessageResponse] = []


# In-memory storage (replace with database model)
_sessions_db: dict = {}
_messages_db: dict = {}


@router.post(
    "",
    response_model=SessionResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new session",
)
async def create_session(
    session: SessionCreate,
    current_user: TokenData = Depends(require_permission("sessions:create")),
    db: AsyncSession = Depends(get_db),
):
    """Create a new session"""
    import uuid

    session_id = uuid.uuid4()
    now = datetime.now(timezone.utc).isoformat()

    session_data = SessionResponse(
        id=session_id,
        owner_id=current_user.user_id or uuid.uuid4(),
        status="active",
        message_count=0,
        created_at=now,
        updated_at=now,
        last_message_at=None,
        **session.model_dump(),
    )

    _sessions_db[str(session_id)] = session_data
    _messages_db[str(session_id)] = []

    return session_data


@router.get(
    "",
    response_model=SessionListResponse,
    summary="List sessions",
)
async def list_sessions(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    status: Optional[str] = None,
    agent_id: Optional[UUID] = None,
    current_user: TokenData = Depends(require_auth),
    db: AsyncSession = Depends(get_db),
):
    """List sessions with pagination"""
    sessions = list(_sessions_db.values())

    # Filter by owner (unless admin)
    if "admin" not in current_user.scopes:
        sessions = [s for s in sessions if s.owner_id == current_user.user_id]

    # Filter by status
    if status:
        sessions = [s for s in sessions if s.status == status]

    # Filter by agent
    if agent_id:
        sessions = [s for s in sessions if s.agent_id == agent_id]

    # Sort by last activity
    sessions.sort(key=lambda s: s.last_message_at or s.created_at, reverse=True)

    total = len(sessions)
    start = (page - 1) * page_size
    end = start + page_size

    return SessionListResponse(
        sessions=sessions[start:end],
        total=total,
        page=page,
        page_size=page_size,
    )


@router.get(
    "/{session_id}",
    response_model=SessionWithMessages,
    summary="Get session with messages",
)
async def get_session(
    session_id: UUID,
    include_messages: bool = Query(True),
    message_limit: int = Query(100, ge=1, le=1000),
    current_user: TokenData = Depends(require_auth),
    db: AsyncSession = Depends(get_db),
):
    """Get session by ID with optional messages"""
    session = _sessions_db.get(str(session_id))
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    # Check ownership
    if "admin" not in current_user.scopes and session.owner_id != current_user.user_id:
        raise HTTPException(status_code=403, detail="Not authorized")

    if include_messages:
        messages = _messages_db.get(str(session_id), [])
        return SessionWithMessages(
            **session.model_dump(),
            messages=messages[-message_limit:],
        )

    return SessionWithMessages(**session.model_dump(), messages=[])


@router.patch(
    "/{session_id}",
    response_model=SessionResponse,
    summary="Update session",
)
async def update_session(
    session_id: UUID,
    session_update: SessionUpdate,
    current_user: TokenData = Depends(require_permission("sessions:update")),
    db: AsyncSession = Depends(get_db),
):
    """Update a session"""
    session = _sessions_db.get(str(session_id))
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    if "admin" not in current_user.scopes and session.owner_id != current_user.user_id:
        raise HTTPException(status_code=403, detail="Not authorized")

    update_data = session_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(session, field, value)

    session.updated_at = datetime.now(timezone.utc).isoformat()
    _sessions_db[str(session_id)] = session

    return session


@router.delete(
    "/{session_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete session",
)
async def delete_session(
    session_id: UUID,
    current_user: TokenData = Depends(require_permission("sessions:delete")),
    db: AsyncSession = Depends(get_db),
):
    """Delete a session"""
    session = _sessions_db.get(str(session_id))
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    if "admin" not in current_user.scopes and session.owner_id != current_user.user_id:
        raise HTTPException(status_code=403, detail="Not authorized")

    del _sessions_db[str(session_id)]
    if str(session_id) in _messages_db:
        del _messages_db[str(session_id)]


@router.post(
    "/{session_id}/messages",
    response_model=MessageResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Add message to session",
)
async def add_message(
    session_id: UUID,
    message: MessageCreate,
    current_user: TokenData = Depends(require_permission("sessions:write")),
    db: AsyncSession = Depends(get_db),
):
    """Add a message to a session"""
    session = _sessions_db.get(str(session_id))
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    if "admin" not in current_user.scopes and session.owner_id != current_user.user_id:
        raise HTTPException(status_code=403, detail="Not authorized")

    import uuid
    message_id = uuid.uuid4()
    now = datetime.now(timezone.utc).isoformat()

    message_data = MessageResponse(
        id=message_id,
        session_id=session_id,
        created_at=now,
        **message.model_dump(),
    )

    if str(session_id) not in _messages_db:
        _messages_db[str(session_id)] = []

    _messages_db[str(session_id)].append(message_data)

    # Update session
    session.message_count += 1
    session.last_message_at = now
    session.updated_at = now
    _sessions_db[str(session_id)] = session

    return message_data


@router.get(
    "/{session_id}/messages",
    response_model=List[MessageResponse],
    summary="Get session messages",
)
async def get_messages(
    session_id: UUID,
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
    current_user: TokenData = Depends(require_auth),
    db: AsyncSession = Depends(get_db),
):
    """Get messages for a session"""
    session = _sessions_db.get(str(session_id))
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    if "admin" not in current_user.scopes and session.owner_id != current_user.user_id:
        raise HTTPException(status_code=403, detail="Not authorized")

    messages = _messages_db.get(str(session_id), [])
    return messages[offset:offset + limit]


@router.post(
    "/{session_id}/archive",
    response_model=SessionResponse,
    summary="Archive session",
)
async def archive_session(
    session_id: UUID,
    current_user: TokenData = Depends(require_permission("sessions:update")),
    db: AsyncSession = Depends(get_db),
):
    """Archive a session"""
    session = _sessions_db.get(str(session_id))
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    if "admin" not in current_user.scopes and session.owner_id != current_user.user_id:
        raise HTTPException(status_code=403, detail="Not authorized")

    session.status = "archived"
    session.updated_at = datetime.now(timezone.utc).isoformat()
    _sessions_db[str(session_id)] = session

    return session