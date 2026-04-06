"""Pydantic schemas for request/response validation.

Three schemas are provided:

* :class:`TaskCreate` — used when creating a new task.
* :class:`TaskUpdate` — used for partial updates to an existing task.
* :class:`TaskResponse` — serialised representation returned to clients.
"""

from __future__ import annotations

from datetime import date, datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class TaskStatus(str, Enum):
    """Allowed status values for a task."""

    TODO = "todo"
    IN_PROGRESS = "in-progress"
    DONE = "done"


class TaskCreate(BaseModel):
    """Schema for creating a new task.

    Attributes:
        title: Short description of the task.  Must be between 1 and
            255 characters.
        status: Initial workflow state.  Defaults to ``'todo'``.
        due_date: Optional target completion date.
    """

    title: str = Field(
        ...,
        min_length=1,
        max_length=255,
        description="Short description of the task",
    )
    status: TaskStatus = Field(
        default=TaskStatus.TODO,
        description="Workflow state of the task",
    )
    due_date: Optional[date] = Field(
        default=None,
        description="Optional target completion date",
    )


class TaskUpdate(BaseModel):
    """Schema for partially updating an existing task.

    All fields are optional — only the supplied fields will be updated.

    Attributes:
        title: New task description.
        status: New workflow state.
        due_date: New target completion date (set to ``None`` to clear).
    """

    title: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=255,
        description="Short description of the task",
    )
    status: Optional[TaskStatus] = Field(
        default=None,
        description="Workflow state of the task",
    )
    due_date: Optional[date] = Field(
        default=None,
        description="Optional target completion date",
    )


class TaskResponse(BaseModel):
    """Schema for the task representation returned to API clients.

    Attributes:
        id: Primary key.
        title: Short description of the task.
        status: Current workflow state.
        due_date: Target completion date, or ``None``.
        created_at: Timestamp of creation.
        updated_at: Timestamp of last modification.
    """

    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    status: TaskStatus
    due_date: Optional[date] = None
    created_at: datetime
    updated_at: datetime
