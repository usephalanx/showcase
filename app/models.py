"""Pydantic models for the Todo API.

Defines request/response schemas used across the application:
- TodoCreate: fields required when creating a new todo
- TodoUpdate: optional fields for partial updates
- TodoResponse: full todo representation returned to clients
"""

from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Field


class TodoCreate(BaseModel):
    """Schema for creating a new todo item.

    Attributes:
        title: The title of the todo item. Required.
        description: An optional longer description of the todo item.
    """

    title: str = Field(..., min_length=1, description="Title of the todo item")
    description: Optional[str] = Field(
        default=None, description="Optional description of the todo item"
    )


class TodoUpdate(BaseModel):
    """Schema for updating an existing todo item.

    All fields are optional; only provided fields will be updated.

    Attributes:
        title: New title for the todo item.
        description: New description for the todo item.
        completed: New completion status for the todo item.
    """

    title: Optional[str] = Field(
        default=None, min_length=1, description="New title of the todo item"
    )
    description: Optional[str] = Field(
        default=None, description="New description of the todo item"
    )
    completed: Optional[bool] = Field(
        default=None, description="New completion status"
    )


class TodoResponse(BaseModel):
    """Schema for a todo item returned in API responses.

    Attributes:
        id: The unique identifier of the todo item.
        title: The title of the todo item.
        description: The optional description of the todo item.
        completed: Whether the todo item has been completed.
    """

    id: int
    title: str
    description: Optional[str] = None
    completed: bool
