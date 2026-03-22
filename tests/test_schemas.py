"""Tests for Pydantic request/response schemas."""

from __future__ import annotations

import datetime

import pytest
from pydantic import ValidationError

from backend.app.schemas import (
    ProjectCreate,
    ProjectResponse,
    ProjectStatus,
    ProjectUpdate,
    TaskCreate,
    TaskPriority,
    TaskResponse,
    TaskStatus,
    TaskStatusUpdate,
    TaskUpdate,
)


# ---------------------------------------------------------------------------
# ProjectCreate
# ---------------------------------------------------------------------------


class TestProjectCreate:
    """Validation tests for ProjectCreate."""

    def test_minimal(self) -> None:
        """Only name is required; defaults should be applied."""
        schema = ProjectCreate(name="My Project")
        assert schema.name == "My Project"
        assert schema.description is None
        assert schema.status == ProjectStatus.active

    def test_all_fields(self) -> None:
        """All fields can be provided."""
        schema = ProjectCreate(
            name="Full", description="desc", status="completed"
        )
        assert schema.status == ProjectStatus.completed

    def test_name_required(self) -> None:
        """Omitting name raises a validation error."""
        with pytest.raises(ValidationError):
            ProjectCreate()  # type: ignore[call-arg]

    def test_name_min_length(self) -> None:
        """Empty name should fail validation."""
        with pytest.raises(ValidationError):
            ProjectCreate(name="")

    def test_name_max_length(self) -> None:
        """Name exceeding 100 chars should fail."""
        with pytest.raises(ValidationError):
            ProjectCreate(name="x" * 101)

    def test_description_max_length(self) -> None:
        """Description exceeding 500 chars should fail."""
        with pytest.raises(ValidationError):
            ProjectCreate(name="ok", description="x" * 501)

    def test_invalid_status(self) -> None:
        """An invalid status value should fail."""
        with pytest.raises(ValidationError):
            ProjectCreate(name="ok", status="deleted")  # type: ignore[arg-type]


# ---------------------------------------------------------------------------
# ProjectUpdate
# ---------------------------------------------------------------------------


class TestProjectUpdate:
    """Validation tests for ProjectUpdate."""

    def test_all_optional(self) -> None:
        """All fields are optional."""
        schema = ProjectUpdate()
        assert schema.name is None
        assert schema.description is None
        assert schema.status is None

    def test_partial_update(self) -> None:
        """Only provided fields should be set."""
        schema = ProjectUpdate(name="Updated")
        assert schema.name == "Updated"
        assert schema.status is None

    def test_invalid_status(self) -> None:
        """Invalid status in update should fail."""
        with pytest.raises(ValidationError):
            ProjectUpdate(status="nope")  # type: ignore[arg-type]


# ---------------------------------------------------------------------------
# ProjectResponse
# ---------------------------------------------------------------------------


class TestProjectResponse:
    """Validation tests for ProjectResponse."""

    def test_from_dict(self) -> None:
        """Should parse a valid dictionary."""
        data = {
            "id": 1,
            "name": "Test",
            "description": None,
            "status": "active",
            "created_at": datetime.datetime(2025, 1, 1, 12, 0, 0),
        }
        schema = ProjectResponse(**data)
        assert schema.id == 1
        assert schema.status == ProjectStatus.active

    def test_from_attributes_config(self) -> None:
        """model_config should enable from_attributes."""
        assert ProjectResponse.model_config.get("from_attributes") is True


# ---------------------------------------------------------------------------
# TaskCreate
# ---------------------------------------------------------------------------


class TestTaskCreate:
    """Validation tests for TaskCreate."""

    def test_minimal(self) -> None:
        """Only project_id and title required; defaults applied."""
        schema = TaskCreate(project_id=1, title="Do stuff")
        assert schema.status == TaskStatus.todo
        assert schema.priority == TaskPriority.medium
        assert schema.due_date is None

    def test_all_fields(self) -> None:
        """All fields can be provided."""
        schema = TaskCreate(
            project_id=1,
            title="Full",
            status="done",
            priority="high",
            due_date=datetime.date(2025, 6, 1),
        )
        assert schema.status == TaskStatus.done
        assert schema.priority == TaskPriority.high
        assert schema.due_date == datetime.date(2025, 6, 1)

    def test_title_required(self) -> None:
        """Missing title should fail."""
        with pytest.raises(ValidationError):
            TaskCreate(project_id=1)  # type: ignore[call-arg]

    def test_project_id_required(self) -> None:
        """Missing project_id should fail."""
        with pytest.raises(ValidationError):
            TaskCreate(title="test")  # type: ignore[call-arg]

    def test_title_min_length(self) -> None:
        """Empty title should fail."""
        with pytest.raises(ValidationError):
            TaskCreate(project_id=1, title="")

    def test_title_max_length(self) -> None:
        """Title exceeding 200 chars should fail."""
        with pytest.raises(ValidationError):
            TaskCreate(project_id=1, title="x" * 201)

    def test_invalid_status(self) -> None:
        """Invalid status should fail."""
        with pytest.raises(ValidationError):
            TaskCreate(project_id=1, title="t", status="unknown")  # type: ignore[arg-type]

    def test_invalid_priority(self) -> None:
        """Invalid priority should fail."""
        with pytest.raises(ValidationError):
            TaskCreate(project_id=1, title="t", priority="urgent")  # type: ignore[arg-type]


# ---------------------------------------------------------------------------
# TaskUpdate
# ---------------------------------------------------------------------------


class TestTaskUpdate:
    """Validation tests for TaskUpdate."""

    def test_all_optional(self) -> None:
        """All fields are optional."""
        schema = TaskUpdate()
        assert schema.title is None
        assert schema.status is None
        assert schema.priority is None
        assert schema.due_date is None

    def test_partial(self) -> None:
        """Only supplied fields should be set."""
        schema = TaskUpdate(priority="low")
        assert schema.priority == TaskPriority.low


# ---------------------------------------------------------------------------
# TaskStatusUpdate
# ---------------------------------------------------------------------------


class TestTaskStatusUpdate:
    """Validation tests for TaskStatusUpdate."""

    def test_valid(self) -> None:
        """Should accept a valid status."""
        schema = TaskStatusUpdate(status="done")
        assert schema.status == TaskStatus.done

    def test_status_required(self) -> None:
        """Status is required."""
        with pytest.raises(ValidationError):
            TaskStatusUpdate()  # type: ignore[call-arg]

    def test_invalid_status(self) -> None:
        """Invalid status should fail."""
        with pytest.raises(ValidationError):
            TaskStatusUpdate(status="invalid")  # type: ignore[arg-type]


# ---------------------------------------------------------------------------
# TaskResponse
# ---------------------------------------------------------------------------


class TestTaskResponse:
    """Validation tests for TaskResponse."""

    def test_from_dict(self) -> None:
        """Should parse a valid dictionary."""
        data = {
            "id": 5,
            "project_id": 1,
            "title": "Task",
            "status": "in_progress",
            "priority": "high",
            "due_date": datetime.date(2025, 3, 1),
        }
        schema = TaskResponse(**data)
        assert schema.id == 5
        assert schema.status == TaskStatus.in_progress

    def test_due_date_optional(self) -> None:
        """due_date can be None."""
        data = {
            "id": 5,
            "project_id": 1,
            "title": "Task",
            "status": "todo",
            "priority": "low",
            "due_date": None,
        }
        schema = TaskResponse(**data)
        assert schema.due_date is None

    def test_from_attributes_config(self) -> None:
        """model_config should enable from_attributes."""
        assert TaskResponse.model_config.get("from_attributes") is True
