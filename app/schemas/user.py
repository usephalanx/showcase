"""Pydantic schemas for user / auth operations."""

from pydantic import BaseModel
from typing import Optional


class TokenData(BaseModel):
    """Data embedded inside a JWT token."""

    username: Optional[str] = None
    role: Optional[str] = None
    user_id: Optional[int] = None
