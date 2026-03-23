"""Tests for Pydantic schemas."""

from __future__ import annotations

from datetime import date, datetime

import pytest
from pydantic import ValidationError

from app.models import TaskPriority, TaskStatus
from app.schemas import (
    ProjectCreate,
    ProjectDetailResponse,
    ProjectResponse,
    TaskCreate,
    TaskResponse,
    TaskUpdate,
)


class TestProjectCreate:
    """Tests for the ProjectCreate schema."""

    def test_valid(self) -> None:
        """Valid data is accepted."""
        schema = ProjectCreate(name="My Project", description="desc")
        assert schema.name == "My Project"
        assert schema.description == "desc"

    def test_default_description(self) -> None:
        """Description defaults to empty string."""
        schema = ProjectCreate(name="P")
        assert schema.description == ""

    def test_empty_name_rejected(self) -> None:
        """An empty name raises a validation error."""
        with pytest.raises(ValidationError):
            ProjectCreate(name="")

    def test_name_too_long(self) -> None:
        """A name exceeding 100 characters is rejected."""
        with pytest.raises(ValidationError):
            ProjectCreate(name="x" * 101)


class TestProjectResponse:
    """Tests for the ProjectResponse schema."""

    def test_from_dict(self) -> None:
        """Can be constructed from a plain dictionary."""
        data = {
            "id": 1,
            "name": "P",
            "description": "d",
            "created_at": datetime(2025, 1, 1, 12, 0, 0),
        }
        schema = ProjectResponse(**data)
        assert schema.id == 1
        assert schema.name == "P"


class TestProjectDetailResponse:
    """Tests for the ProjectDetailResponse schema."""

    def test_with_tasks(self) -> None:
        """Can include a list of tasks."""
        now = datetime(2025, 1, 1, 12, 0, 0)
        task_data = {
            "id": 1,
            "project_id": 1,
            "title": "T",
            "description": "",
            "status": TaskStatus.todo,
            "priority": TaskPriority.low,
            "due_date": None,
            "created_at": now,
        }
        schema = ProjectDetailResponse(
            id=1,
            name="P",
            description="",
            created_at=now,
            tasks=[task_data],
        )
        assert len(schema.tasks) == 1
        assert schema.tasks[0].title == "T"


class TestTaskCreate:
    """Tests for the TaskCreate schema."""

    def test_defaults(self) -> None:
        """Default status is todo and priority is medium."""
        schema = TaskCreate(title="Do thing")
        assert schema.status == TaskStatus.todo
        assert schema.priority == TaskPriority.medium
        assert schema.due_date is None

    def test_all_fields(self) -> None:
        """All fields can be supplied."""
        schema = TaskCreate(
            title="Do thing",
            description="details",
            status=TaskStatus.in_progress,
            priority=TaskPriority.high,
            due_date=date(2025, 6, 15),
        )
        assert schema.status == TaskStatus.in_progress
        assert schema.priority == TaskPriority.high
        assert schema.due_date == date(2025, 6, 15)

    def test_empty_title_rejected(self) -> None:
        """An empty title is rejected."""
        with pytest.raises(ValidationError):
            TaskCreate(title="")


class TestTaskUpdate:
    """Tests for the TaskUpdate schema."""

    def test_partial_update(self) -> None:
        """Only supplied fields are set; others remain None."""
        schema = TaskUpdate(status=TaskStatus.done)
        assert schema.status == TaskStatus.done
        assert schema.title is None
        assert schema.priority is None

    def test_empty_is_valid(self) -> None:
        """An empty body is valid (no fields to update)."""
        schema = TaskUpdate()
        assert schema.title is None


class TestTaskResponse:
    """Tests for the TaskResponse schema."""

    def test_from_dict(self) -> None:
        """Can be constructed from a dictionary."""
        now = datetime(2025, 1, 1, 12, 0, 0)
        data = {
            "id": 1,
            "project_id": 1,
            "title": "T",
            "description": "d",
            "status": TaskStatus.todo,
            "priority": TaskPriority.medium,
            "due_date": date(2025, 3, 1),
            "created_at": now,
        }
        schema = TaskResponse(**data)
        assert schema.id == 1
        assert schema.due_date == date(2025, 3, 1)
