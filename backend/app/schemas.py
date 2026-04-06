"""Pydantic schemas for request / response validation."""

from __future__ import annotations

from datetime import date, datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class TaskStatusEnum(str, Enum):
    """Valid status values accepted in API requests.

    Members:
        TODO: Task has not been started.
        IN_PROGRESS: Task is currently being worked on.
        DONE: Task has been completed.
    """

    TODO = "todo"
    IN_PROGRESS = "in-progress"
    DONE = "done"


class TaskCreate(BaseModel):
    """Request body for creating a new task.

    Attributes:
        title: Short description of the task (required, 1-255 chars).
        status: Initial workflow status; defaults to 'todo'.
        due_date: Optional target completion date.
    """

    title: str = Field(
        ...,
        min_length=1,
        max_length=255,
        description="Task title",
        examples=["Buy groceries"],
    )
    status: TaskStatusEnum = Field(
        default=TaskStatusEnum.TODO,
        description="Initial task status",
    )
    due_date: Optional[date] = Field(
        default=None,
        description="Optional due date",
    )


class TaskUpdate(BaseModel):
    """Request body for fully updating a task (PUT).

    All fields are required.  Use :class:`TaskPatch` when only a subset
    of fields should be modified.

    Attributes:
        title: Updated task title (required, 1-255 chars).
        status: Updated workflow status (required).
        due_date: Updated target completion date (nullable).
    """

    title: str = Field(
        ...,
        min_length=1,
        max_length=255,
        description="Task title",
    )
    status: TaskStatusEnum = Field(
        ...,
        description="Task status",
    )
    due_date: Optional[date] = Field(
        default=None,
        description="Optional due date",
    )


class TaskPatch(BaseModel):
    """Request body for partially updating a task (PATCH).

    All fields are optional — only supplied fields are updated.

    Attributes:
        title: Updated task title (optional, 1-255 chars if provided).
        status: Updated workflow status (optional).
        due_date: Updated target completion date (optional).
    """

    title: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=255,
        description="Task title",
    )
    status: Optional[TaskStatusEnum] = Field(
        default=None,
        description="Task status",
    )
    due_date: Optional[date] = Field(
        default=None,
        description="Optional due date",
    )


class TaskResponse(BaseModel):
    """Response body representing a persisted task.

    Attributes:
        id: Auto-incrementing primary key.
        title: Short description of the task.
        status: Current workflow status.
        due_date: Target completion date or ``None``.
        created_at: Timestamp of row creation.
        updated_at: Timestamp of last modification.
    """

    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    status: TaskStatusEnum
    due_date: Optional[date] = None
    created_at: datetime
    updated_at: datetime
