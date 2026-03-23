"""Pydantic schemas for request / response validation."""

from __future__ import annotations

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, EmailStr, Field


# ---------------------------------------------------------------------------
# Auth
# ---------------------------------------------------------------------------


class AuthRegisterRequest(BaseModel):
    """Request body for user registration."""

    email: str = Field(..., min_length=1, description="User email address")
    password: str = Field(..., min_length=6, description="User password (min 6 chars)")


class AuthLoginRequest(BaseModel):
    """Request body for user login."""

    email: str = Field(..., min_length=1)
    password: str = Field(..., min_length=1)


class AuthResponse(BaseModel):
    """Response containing a JWT access token."""

    access_token: str
    token_type: str = "bearer"


class UserResponse(BaseModel):
    """Public user information."""

    id: int
    email: str
    created_at: datetime

    model_config = {"from_attributes": True}


# ---------------------------------------------------------------------------
# Board
# ---------------------------------------------------------------------------


class BoardCreate(BaseModel):
    """Request body for creating a board."""

    title: str = Field(..., min_length=1, max_length=255)


class BoardResponse(BaseModel):
    """Board summary (without nested columns)."""

    id: int
    title: str
    user_id: int
    created_at: datetime

    model_config = {"from_attributes": True}


# ---------------------------------------------------------------------------
# Column
# ---------------------------------------------------------------------------


class ColumnCreate(BaseModel):
    """Request body for creating a column."""

    title: str = Field(..., min_length=1, max_length=255)
    position: int = Field(default=0, ge=0)


class CardResponse(BaseModel):
    """Card detail."""

    id: int
    title: str
    description: str
    column_id: int
    position: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class ColumnResponse(BaseModel):
    """Column with nested cards."""

    id: int
    title: str
    board_id: int
    position: int
    cards: List[CardResponse] = []

    model_config = {"from_attributes": True}


class BoardDetailResponse(BaseModel):
    """Board with nested columns and cards."""

    id: int
    title: str
    user_id: int
    created_at: datetime
    columns: List[ColumnResponse] = []

    model_config = {"from_attributes": True}


# ---------------------------------------------------------------------------
# Card
# ---------------------------------------------------------------------------


class CardCreate(BaseModel):
    """Request body for creating a card."""

    title: str = Field(..., min_length=1, max_length=255)
    description: str = Field(default="", max_length=5000)
    position: int = Field(default=0, ge=0)


class CardUpdate(BaseModel):
    """Request body for updating a card."""

    title: Optional[str] = Field(default=None, min_length=1, max_length=255)
    description: Optional[str] = Field(default=None, max_length=5000)


class CardMoveRequest(BaseModel):
    """Request body for moving a card to a new column / position."""

    column_id: int
    position: int = Field(..., ge=0)
