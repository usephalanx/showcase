"""Pydantic schemas for the Task resource.

Defines request (create/update) and response models used by the API
routers for data validation and serialisation.
"""

from __future__ import annotations

from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, Field

from app.models.task import TaskPriority, TaskStatus


class TaskCreate(BaseModel):
    """Schema for creating a new task."""

    project_id: int = Field(..., description="ID of the parent project")
    title: str = Field(..., min_length=1, max_length=512, description="Task title")
    status: TaskStatus = Field(
        default=TaskStatus.todo, description="Initial task status"
    )
    priority: TaskPriority = Field(
        default=TaskPriority.medium, description="Task priority level"
    )
    due_date: Optional[date] = Field(default=None, description="Optional due date")


class TaskUpdate(BaseModel):
    """Schema for partially updating an existing task.

    All fields are optional; only supplied fields will be updated.
    """

    title: Optional[str] = Field(
        default=None, min_length=1, max_length=512, description="Task title"
    )
    status: Optional[TaskStatus] = Field(default=None, description="Task status")
    priority: Optional[TaskPriority] = Field(
        default=None, description="Task priority level"
    )
    due_date: Optional[date] = Field(default=None, description="Optional due date")


class TaskResponse(BaseModel):
    """Schema for returning a task in API responses."""

    id: int
    project_id: int
    title: str
    status: TaskStatus
    priority: TaskPriority
    due_date: Optional[date]
    created_at: datetime

    model_config = {"from_attributes": True}
