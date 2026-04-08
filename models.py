"""Pydantic schemas for the Todo API.

Defines request and response models used by the API endpoints for
creating, updating, and returning todo items.
"""

from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class TodoCreate(BaseModel):
    """Request body for creating a new todo item.

    Attributes:
        title: The title of the todo item. Required.
        description: An optional longer description of the todo item.
    """

    title: str = Field(..., min_length=1, description="Title of the todo item")
    description: Optional[str] = Field(
        None, description="Optional description of the todo item"
    )


class TodoUpdate(BaseModel):
    """Request body for updating an existing todo item.

    All fields are optional so that partial updates are supported.

    Attributes:
        title: New title for the todo item.
        description: New description for the todo item.
        completed: New completion status for the todo item.
    """

    title: Optional[str] = Field(
        None, min_length=1, description="New title of the todo item"
    )
    description: Optional[str] = Field(
        None, description="New description of the todo item"
    )
    completed: Optional[bool] = Field(
        None, description="New completion status of the todo item"
    )


class TodoResponse(BaseModel):
    """Response body representing a single todo item.

    Attributes:
        id: The unique identifier of the todo item.
        title: The title of the todo item.
        description: The description of the todo item, or None.
        completed: Whether the todo item is completed.
        created_at: The UTC timestamp when the todo item was created.
    """

    id: int
    title: str
    description: Optional[str] = None
    completed: bool
    created_at: datetime
