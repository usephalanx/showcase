"""Tests for backend.schemas module.

Verifies Pydantic schemas: TaskCreate, TaskUpdate, TaskResponse.
Covers validation rules, defaults, enum constraints, and
serialization from ORM-like objects.
"""

from __future__ import annotations

from datetime import date, datetime
from typing import Optional

import pytest
from pydantic import ValidationError

from backend.schemas import TaskCreate, TaskResponse, TaskStatus, TaskUpdate


class TestTaskStatus:
    """Verify the TaskStatus enum."""

    def test_values(self) -> None:
        """TaskStatus should contain exactly three values."""
        assert set(TaskStatus) == {
            TaskStatus.TODO,
            TaskStatus.IN_PROGRESS,
            TaskStatus.DONE,
        }

    def test_string_values(self) -> None:
        """Enum members should have the expected string representations."""
        assert TaskStatus.TODO.value == "todo"
        assert TaskStatus.IN_PROGRESS.value == "in-progress"
        assert TaskStatus.DONE.value == "done"

    def test_is_str_subclass(self) -> None:
        """TaskStatus members should be usable as plain strings."""
        assert isinstance(TaskStatus.TODO, str)


class TestTaskCreate:
    """Verify TaskCreate schema validation."""

    def test_minimal_valid(self) -> None:
        """Only title is required; status defaults to 'todo'."""
        schema = TaskCreate(title="Buy groceries")
        assert schema.title == "Buy groceries"
        assert schema.status == TaskStatus.TODO
        assert schema.due_date is None

    def test_all_fields(self) -> None:
        """All fields can be explicitly set."""
        schema = TaskCreate(
            title="Deploy",
            status="in-progress",
            due_date=date(2025, 6, 15),
        )
        assert schema.status == TaskStatus.IN_PROGRESS
        assert schema.due_date == date(2025, 6, 15)

    def test_title_required(self) -> None:
        """Omitting title should raise a validation error."""
        with pytest.raises(ValidationError) as exc_info:
            TaskCreate()  # type: ignore[call-arg]
        errors = exc_info.value.errors()
        assert any(e["loc"] == ("title",) for e in errors)

    def test_title_empty_string(self) -> None:
        """An empty title string should fail min_length validation."""
        with pytest.raises(ValidationError):
            TaskCreate(title="")

    def test_title_max_length(self) -> None:
        """A title exceeding 255 characters should fail validation."""
        with pytest.raises(ValidationError):
            TaskCreate(title="x" * 256)

    def test_title_exactly_max_length(self) -> None:
        """A 255-character title should be accepted."""
        schema = TaskCreate(title="x" * 255)
        assert len(schema.title) == 255

    def test_invalid_status(self) -> None:
        """An invalid status string should raise a validation error."""
        with pytest.raises(ValidationError):
            TaskCreate(title="Test", status="invalid")

    def test_status_done(self) -> None:
        """Status 'done' should be accepted."""
        schema = TaskCreate(title="Test", status="done")
        assert schema.status == TaskStatus.DONE


class TestTaskUpdate:
    """Verify TaskUpdate schema validation."""

    def test_empty_update(self) -> None:
        """All fields are optional — an empty body is valid."""
        schema = TaskUpdate()
        assert schema.title is None
        assert schema.status is None
        assert schema.due_date is None

    def test_partial_update_title(self) -> None:
        """Only title can be updated."""
        schema = TaskUpdate(title="New title")
        assert schema.title == "New title"
        assert schema.status is None

    def test_partial_update_status(self) -> None:
        """Only status can be updated."""
        schema = TaskUpdate(status="done")
        assert schema.status == TaskStatus.DONE
        assert schema.title is None

    def test_partial_update_due_date(self) -> None:
        """Only due_date can be updated."""
        schema = TaskUpdate(due_date=date(2025, 1, 1))
        assert schema.due_date == date(2025, 1, 1)

    def test_all_fields(self) -> None:
        """All fields can be set simultaneously."""
        schema = TaskUpdate(
            title="Updated",
            status="in-progress",
            due_date=date(2025, 3, 1),
        )
        assert schema.title == "Updated"
        assert schema.status == TaskStatus.IN_PROGRESS
        assert schema.due_date == date(2025, 3, 1)

    def test_invalid_status(self) -> None:
        """An invalid status should raise a validation error."""
        with pytest.raises(ValidationError):
            TaskUpdate(status="cancelled")

    def test_title_empty_string(self) -> None:
        """An empty title string should fail min_length validation."""
        with pytest.raises(ValidationError):
            TaskUpdate(title="")

    def test_title_max_length(self) -> None:
        """A title exceeding 255 characters should fail validation."""
        with pytest.raises(ValidationError):
            TaskUpdate(title="y" * 256)


class TestTaskResponse:
    """Verify TaskResponse schema serialization."""

    def test_from_dict(self) -> None:
        """TaskResponse should be constructable from a plain dict."""
        now = datetime(2025, 1, 15, 10, 30, 0)
        data = {
            "id": 1,
            "title": "Test task",
            "status": "todo",
            "due_date": None,
            "created_at": now,
            "updated_at": now,
        }
        schema = TaskResponse(**data)
        assert schema.id == 1
        assert schema.title == "Test task"
        assert schema.status == TaskStatus.TODO
        assert schema.due_date is None
        assert schema.created_at == now
        assert schema.updated_at == now

    def test_from_orm_like_object(self) -> None:
        """TaskResponse should work with from_attributes=True (ORM mode)."""

        class FakeORM:
            """Simulates an ORM model instance."""

            id = 42
            title = "ORM task"
            status = "in-progress"
            due_date = date(2025, 6, 1)
            created_at = datetime(2025, 1, 1, 0, 0, 0)
            updated_at = datetime(2025, 1, 2, 12, 0, 0)

        schema = TaskResponse.model_validate(FakeORM())
        assert schema.id == 42
        assert schema.status == TaskStatus.IN_PROGRESS
        assert schema.due_date == date(2025, 6, 1)

    def test_with_due_date(self) -> None:
        """TaskResponse should correctly serialize a non-null due_date."""
        now = datetime(2025, 1, 15, 10, 30, 0)
        data = {
            "id": 2,
            "title": "Due task",
            "status": "done",
            "due_date": date(2025, 12, 25),
            "created_at": now,
            "updated_at": now,
        }
        schema = TaskResponse(**data)
        assert schema.due_date == date(2025, 12, 25)
        assert schema.status == TaskStatus.DONE

    def test_serialization_to_dict(self) -> None:
        """model_dump() should produce a JSON-serializable dictionary."""
        now = datetime(2025, 1, 15, 10, 30, 0)
        schema = TaskResponse(
            id=1,
            title="Serialize me",
            status="todo",
            due_date=None,
            created_at=now,
            updated_at=now,
        )
        d = schema.model_dump()
        assert isinstance(d, dict)
        assert d["id"] == 1
        assert d["title"] == "Serialize me"
        assert d["status"] == TaskStatus.TODO

    def test_invalid_status_rejected(self) -> None:
        """TaskResponse should reject an invalid status value."""
        now = datetime(2025, 1, 15, 10, 30, 0)
        with pytest.raises(ValidationError):
            TaskResponse(
                id=1,
                title="Bad status",
                status="invalid",
                created_at=now,
                updated_at=now,
            )

    def test_missing_required_fields(self) -> None:
        """TaskResponse should require id, title, status, created_at, updated_at."""
        with pytest.raises(ValidationError) as exc_info:
            TaskResponse()  # type: ignore[call-arg]
        error_locs = {e["loc"][0] for e in exc_info.value.errors()}
        assert "id" in error_locs
        assert "title" in error_locs
        assert "status" in error_locs
        assert "created_at" in error_locs
        assert "updated_at" in error_locs
