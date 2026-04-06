"""Pydantic schemas for the Todo application.

Defines request/response models used by the FastAPI endpoints for
validating and serializing Task data.
"""

from __future__ import annotations

from datetime import date
from typing import Optional

from pydantic import BaseModel, Field


class TaskBase(BaseModel):
    """Base schema containing the common Task fields.

    Attributes:
        title: The title text of the task.
        status: Current status of the task (default ``'todo'``).
        due_date: Optional date by which the task should be completed.
    """

    title: str = Field(..., min_length=1, description="Title of the task")
    status: str = Field(
        default="todo",
        description="Current status of the task (todo, in-progress, done)",
    )
    due_date: Optional[date] = Field(
        default=None,
        description="Optional due date for the task",
    )


class TaskCreate(TaskBase):
    """Schema for creating a new task.

    Inherits all fields and validation rules from :class:`TaskBase`.
    """

    pass


class TaskUpdate(BaseModel):
    """Schema for updating an existing task.

    All fields are optional to support partial updates.

    Attributes:
        title: Updated title text.
        status: Updated status value.
        due_date: Updated due date (or ``None`` to clear it).
    """

    title: Optional[str] = Field(
        default=None,
        min_length=1,
        description="Updated title of the task",
    )
    status: Optional[str] = Field(
        default=None,
        description="Updated status of the task (todo, in-progress, done)",
    )
    due_date: Optional[date] = Field(
        default=None,
        description="Updated due date for the task",
    )


class TaskResponse(TaskBase):
    """Schema for returning a task in API responses.

    Includes the database-generated ``id`` field and is configured for
    ORM mode so SQLAlchemy model instances can be serialized directly.

    Attributes:
        id: Primary-key identifier of the task.
    """

    id: int

    class Config:
        """Pydantic configuration for ORM compatibility."""

        orm_mode = True
