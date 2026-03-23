"""Pydantic schemas for the User resource.

Defines request (register/login) and response models used by the
authentication routers for data validation and serialisation.
"""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field


class UserCreate(BaseModel):
    """Schema for registering a new user."""

    username: str = Field(
        ..., min_length=3, max_length=150, description="Unique username"
    )
    password: str = Field(
        ..., min_length=6, max_length=128, description="Plain-text password"
    )


class UserLogin(BaseModel):
    """Schema for logging in an existing user."""

    username: str = Field(..., min_length=1, description="Username")
    password: str = Field(..., min_length=1, description="Plain-text password")


class UserResponse(BaseModel):
    """Schema for returning a user in API responses (no password)."""

    id: int
    username: str
    created_at: datetime

    model_config = {"from_attributes": True}


class Token(BaseModel):
    """Schema for JWT token response."""

    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """Schema for decoded token payload data."""

    username: str | None = None
