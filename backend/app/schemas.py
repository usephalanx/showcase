"""Pydantic models for request/response validation.

Each pair of Create/Update/Response schemas corresponds to an ORM model
defined in ``models.py``.
"""

from __future__ import annotations

import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


# ---------------------------------------------------------------------------
# Enumerations
# ---------------------------------------------------------------------------


class ProjectStatus(str, Enum):
    """Allowed status values for a project."""

    active = "active"
    completed = "completed"
    archived = "archived"


class TaskStatus(str, Enum):
    """Allowed status values for a task."""

    todo = "todo"
    in_progress = "in_progress"
    done = "done"


class TaskPriority(str, Enum):
    """Allowed priority levels for a task."""

    low = "low"
    medium = "medium"
    high = "high"


# ---------------------------------------------------------------------------
# Project schemas
# ---------------------------------------------------------------------------


class ProjectCreate(BaseModel):
    """Schema for creating a new project."""

    name: str = Field(
        ..., min_length=1, max_length=100, description="Project name"
    )
    description: Optional[str] = Field(
        None, max_length=500, description="Optional project description"
    )
    status: ProjectStatus = Field(
        ProjectStatus.active, description="Initial project status"
    )


class ProjectUpdate(BaseModel):
    """Schema for updating an existing project (partial update)."""

    name: Optional[str] = Field(
        None, min_length=1, max_length=100, description="Project name"
    )
    description: Optional[str] = Field(
        None, max_length=500, description="Project description"
    )
    status: Optional[ProjectStatus] = Field(
        None, description="Project status"
    )


class ProjectResponse(BaseModel):
    """Schema returned when reading a project."""

    id: int
    name: str
    description: Optional[str] = None
    status: ProjectStatus
    created_at: datetime.datetime

    model_config = {"from_attributes": True}


# ---------------------------------------------------------------------------
# Task schemas
# ---------------------------------------------------------------------------


class TaskCreate(BaseModel):
    """Schema for creating a new task."""

    project_id: int = Field(
        ..., description="ID of the parent project"
    )
    title: str = Field(
        ..., min_length=1, max_length=200, description="Task title"
    )
    status: TaskStatus = Field(
        TaskStatus.todo, description="Initial task status"
    )
    priority: TaskPriority = Field(
        TaskPriority.medium, description="Task priority level"
    )
    due_date: Optional[datetime.date] = Field(
        None, description="Optional due date (YYYY-MM-DD)"
    )


class TaskUpdate(BaseModel):
    """Schema for updating an existing task (partial update)."""

    title: Optional[str] = Field(
        None, min_length=1, max_length=200, description="Task title"
    )
    status: Optional[TaskStatus] = Field(
        None, description="Task status"
    )
    priority: Optional[TaskPriority] = Field(
        None, description="Task priority level"
    )
    due_date: Optional[datetime.date] = Field(
        None, description="Due date (YYYY-MM-DD)"
    )


class TaskStatusUpdate(BaseModel):
    """Schema for updating only the status of a task."""

    status: TaskStatus = Field(
        ..., description="New task status"
    )


class TaskResponse(BaseModel):
    """Schema returned when reading a task."""

    id: int
    project_id: int
    title: str
    status: TaskStatus
    priority: TaskPriority
    due_date: Optional[datetime.date] = None

    model_config = {"from_attributes": True}
