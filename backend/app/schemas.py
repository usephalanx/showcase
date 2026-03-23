"""Pydantic schemas for request validation and response serialisation.

All schemas use Pydantic v2 ``model_config`` with ``from_attributes = True``
so they can be constructed directly from SQLAlchemy model instances.
"""

from __future__ import annotations

from datetime import date, datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field

from app.models import TaskPriority, TaskStatus


# ---------------------------------------------------------------------------
# Project schemas
# ---------------------------------------------------------------------------


class ProjectCreate(BaseModel):
    """Request body for creating a new project."""

    name: str = Field(..., min_length=1, max_length=100, description="Project name")
    description: Optional[str] = Field(
        default="", max_length=2000, description="Project description"
    )


class ProjectResponse(BaseModel):
    """Response body representing a single project (without tasks)."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: Optional[str]
    created_at: datetime


class ProjectDetailResponse(BaseModel):
    """Response body representing a project including its tasks."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: Optional[str]
    created_at: datetime
    tasks: List["TaskResponse"] = []


# ---------------------------------------------------------------------------
# Task schemas
# ---------------------------------------------------------------------------


class TaskCreate(BaseModel):
    """Request body for creating a new task."""

    title: str = Field(..., min_length=1, max_length=200, description="Task title")
    description: Optional[str] = Field(
        default="", max_length=2000, description="Task description"
    )
    status: TaskStatus = Field(default=TaskStatus.todo, description="Task status")
    priority: TaskPriority = Field(
        default=TaskPriority.medium, description="Task priority"
    )
    due_date: Optional[date] = Field(default=None, description="Task due date")


class TaskUpdate(BaseModel):
    """Request body for partially updating an existing task."""

    title: Optional[str] = Field(
        default=None, min_length=1, max_length=200, description="Task title"
    )
    description: Optional[str] = Field(
        default=None, max_length=2000, description="Task description"
    )
    status: Optional[TaskStatus] = Field(default=None, description="Task status")
    priority: Optional[TaskPriority] = Field(default=None, description="Task priority")
    due_date: Optional[date] = Field(default=None, description="Task due date")


class TaskResponse(BaseModel):
    """Response body representing a single task."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    project_id: int
    title: str
    description: Optional[str]
    status: TaskStatus
    priority: TaskPriority
    due_date: Optional[date]
    created_at: datetime


# Rebuild forward-referenced models so TaskResponse is available
# inside ProjectDetailResponse.
ProjectDetailResponse.model_rebuild()
