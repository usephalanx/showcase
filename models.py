"""Pydantic models for the Todo API.

Defines request/response schemas used across the application:
- TodoCreate: fields required when creating a new todo
- TodoUpdate: fields that may be updated (all optional)
- TodoResponse: full representation returned to clients
"""

from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class TodoCreate(BaseModel):
    """Request body for creating a new todo item."""

    title: str = Field(..., min_length=1, description="Title of the todo item")
    description: Optional[str] = Field(
        None, description="Optional longer description of the todo"
    )
    completed: Optional[bool] = Field(
        False, description="Whether the todo is completed (defaults to False)"
    )


class TodoUpdate(BaseModel):
    """Request body for updating an existing todo item.

    All fields are optional — only supplied fields are changed.
    """

    title: Optional[str] = Field(None, min_length=1, description="New title")
    description: Optional[str] = Field(None, description="New description")
    completed: Optional[bool] = Field(None, description="New completion status")


class TodoResponse(BaseModel):
    """Response body representing a single todo item."""

    id: int
    title: str
    description: Optional[str] = None
    completed: bool
    created_at: str
