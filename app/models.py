"""Pydantic schemas for the Todo API.

Defines request/response models used by the route handlers.
"""

from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Field


class TodoCreate(BaseModel):
    """Request body for creating a new todo item."""

    title: str = Field(..., min_length=1, description="Title of the todo item")
    description: str = Field(
        default="",
        description="Optional longer description of the todo item",
    )


class TodoUpdate(BaseModel):
    """Request body for updating an existing todo item.

    All fields are optional to support partial updates.
    """

    title: Optional[str] = Field(
        default=None, min_length=1, description="New title"
    )
    description: Optional[str] = Field(
        default=None, description="New description"
    )
    completed: Optional[bool] = Field(
        default=None, description="New completion status"
    )


class TodoResponse(BaseModel):
    """Response body representing a single todo item."""

    id: int
    title: str
    description: str
    completed: bool
