"""Pydantic schemas for the Todo API.

Defines request/response models used by the route handlers.
"""

from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Field


class TodoCreate(BaseModel):
    """Request body for creating a new todo item.

    Attributes:
        title: Title of the todo item.  Must be at least 1 character.
        description: Optional longer description.  Defaults to empty string.
    """

    title: str = Field(..., min_length=1, description="Title of the todo item")
    description: str = Field(
        default="",
        description="Optional longer description of the todo item",
    )


class TodoUpdate(BaseModel):
    """Request body for updating an existing todo item.

    All fields are optional to support partial updates.  Only fields
    explicitly provided in the request body will be applied.

    Attributes:
        title: New title (optional).
        description: New description (optional).
        completed: New completion status (optional).
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
    """Response body representing a single todo item.

    Attributes:
        id: Unique auto-generated identifier.
        title: Title of the todo item.
        description: Longer description (may be empty string).
        completed: Whether the todo has been completed.
    """

    id: int
    title: str
    description: str
    completed: bool
