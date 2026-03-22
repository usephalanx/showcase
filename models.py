"""Pydantic models for the Todo application.

Defines request and response schemas used by the FastAPI endpoints
for creating, updating, and returning todo items.
"""

from __future__ import annotations

from pydantic import BaseModel, Field


class TodoCreate(BaseModel):
    """Request body for creating a new todo item."""

    title: str = Field(
        ...,
        min_length=1,
        max_length=500,
        description="Title of the todo item",
    )


class TodoUpdate(BaseModel):
    """Request body for updating the completion status of a todo item."""

    completed: bool = Field(
        ...,
        description="New completion status for the todo item",
    )


class TodoResponse(BaseModel):
    """Response body representing a single todo item."""

    id: int
    title: str
    completed: bool
    created_at: str
