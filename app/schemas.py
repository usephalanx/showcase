"""Pydantic schemas for the Todo API.

Defines request and response validation models:

- **TodoBase** – Shared fields for creation (title, optional description).
- **TodoCreate** – Inherits TodoBase; used for ``POST /todos`` requests.
- **TodoUpdate** – All-optional fields for partial updates via ``PUT``.
- **TodoResponse** – Full representation returned to clients, including
  server-set fields (``id``, ``completed``, ``created_at``).  Configured
  with ``orm_mode = True`` so it can be constructed directly from
  SQLAlchemy model instances.
"""

from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class TodoBase(BaseModel):
    """Base schema containing the common writable Todo fields.

    Attributes:
        title: Short title of the todo item (min 1 character).
        description: Optional longer description of the todo.
    """

    title: str = Field(
        ...,
        min_length=1,
        max_length=255,
        description="Title of the todo item",
    )
    description: Optional[str] = Field(
        None,
        max_length=1024,
        description="Optional longer description of the todo",
    )


class TodoCreate(TodoBase):
    """Schema for creating a new Todo item.

    Inherits ``title`` and ``description`` from :class:`TodoBase`.
    No additional fields are required — ``completed`` and ``created_at``
    are set by the server.
    """


class TodoUpdate(BaseModel):
    """Schema for partially updating an existing Todo item.

    Every field is optional so that clients may send only the fields
    they wish to change.  Fields set to ``None`` (or omitted) are
    left unchanged on the server side.

    Attributes:
        title: New title (min 1 character if provided).
        description: New description, or ``None`` to leave unchanged.
        completed: New completion status, or ``None`` to leave unchanged.
    """

    title: Optional[str] = Field(
        None,
        min_length=1,
        max_length=255,
        description="Updated title of the todo item",
    )
    description: Optional[str] = Field(
        None,
        max_length=1024,
        description="Updated description of the todo item",
    )
    completed: Optional[bool] = Field(
        None,
        description="Updated completion status",
    )


class TodoResponse(TodoBase):
    """Schema returned to clients representing a persisted Todo item.

    Includes all base fields plus the server-managed attributes.

    Attributes:
        id: Unique auto-incrementing identifier.
        completed: Whether the todo has been completed.
        created_at: Timestamp of when the todo was created (UTC).
    """

    id: int
    completed: bool
    created_at: datetime

    class Config:
        """Pydantic model configuration."""

        orm_mode = True
