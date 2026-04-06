"""Pydantic schemas for request / response validation."""

from __future__ import annotations

from datetime import date, datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class TaskStatusEnum(str, Enum):
    """Valid status values accepted in API requests."""

    TODO = "todo"
    IN_PROGRESS = "in-progress"
    DONE = "done"


class TaskCreate(BaseModel):
    """Request body for creating a new task."""

    title: str = Field(..., min_length=1, max_length=255, description="Task title")
    status: TaskStatusEnum = Field(
        default=TaskStatusEnum.TODO, description="Initial task status"
    )
    due_date: Optional[date] = Field(default=None, description="Optional due date")


class TaskUpdate(BaseModel):
    """Request body for fully updating a task (PUT)."""

    title: str = Field(..., min_length=1, max_length=255)
    status: TaskStatusEnum
    due_date: Optional[date] = None


class TaskPatch(BaseModel):
    """Request body for partially updating a task (PATCH).

    All fields are optional — only supplied fields are updated.
    """

    title: Optional[str] = Field(default=None, min_length=1, max_length=255)
    status: Optional[TaskStatusEnum] = None
    due_date: Optional[date] = None


class TaskResponse(BaseModel):
    """Response body representing a persisted task."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    status: str
    due_date: Optional[date] = None
    created_at: datetime
    updated_at: datetime
