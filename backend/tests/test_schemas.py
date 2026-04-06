"""Tests for Pydantic schemas."""

from __future__ import annotations

from datetime import date, datetime

import pytest
from pydantic import ValidationError

from app.schemas import (
    TaskCreate,
    TaskPatch,
    TaskResponse,
    TaskStatusEnum,
    TaskUpdate,
)


class TestTaskCreate:
    """Validation tests for the TaskCreate schema."""

    def test_minimal(self) -> None:
        """Only title is required."""
        tc = TaskCreate(title="Hello")
        assert tc.title == "Hello"
        assert tc.status == TaskStatusEnum.TODO
        assert tc.due_date is None

    def test_all_fields(self) -> None:
        """All fields can be provided."""
        tc = TaskCreate(
            title="Full",
            status=TaskStatusEnum.IN_PROGRESS,
            due_date=date(2025, 6, 15),
        )
        assert tc.status == TaskStatusEnum.IN_PROGRESS
        assert tc.due_date == date(2025, 6, 15)

    def test_empty_title_rejected(self) -> None:
        """An empty title must be rejected."""
        with pytest.raises(ValidationError):
            TaskCreate(title="")

    def test_invalid_status_rejected(self) -> None:
        """An invalid status value must be rejected with 422."""
        with pytest.raises(ValidationError):
            TaskCreate(title="X", status="invalid")


class TestTaskUpdate:
    """Validation tests for the TaskUpdate schema (PUT)."""

    def test_valid(self) -> None:
        """All required fields must be supplied."""
        tu = TaskUpdate(title="Updated", status=TaskStatusEnum.DONE, due_date=None)
        assert tu.title == "Updated"
        assert tu.status == TaskStatusEnum.DONE

    def test_missing_title_rejected(self) -> None:
        """Missing title should fail."""
        with pytest.raises(ValidationError):
            TaskUpdate(status=TaskStatusEnum.TODO)

    def test_missing_status_rejected(self) -> None:
        """Missing status should fail."""
        with pytest.raises(ValidationError):
            TaskUpdate(title="No status")


class TestTaskPatch:
    """Validation tests for the TaskPatch schema (PATCH)."""

    def test_empty_patch(self) -> None:
        """All fields are optional — an empty body is valid."""
        tp = TaskPatch()
        assert tp.title is None
        assert tp.status is None
        assert tp.due_date is None

    def test_partial_patch(self) -> None:
        """Only the supplied fields should be set."""
        tp = TaskPatch(status=TaskStatusEnum.IN_PROGRESS)
        assert tp.status == TaskStatusEnum.IN_PROGRESS
        assert tp.title is None

    def test_invalid_status_rejected(self) -> None:
        """Invalid status in a patch must be rejected."""
        with pytest.raises(ValidationError):
            TaskPatch(status="nope")


class TestTaskResponse:
    """Validation tests for the TaskResponse schema."""

    def test_from_dict(self) -> None:
        """TaskResponse should accept a plain dictionary."""
        now = datetime.utcnow()
        tr = TaskResponse(
            id=1,
            title="Test",
            status="todo",
            due_date=None,
            created_at=now,
            updated_at=now,
        )
        assert tr.id == 1
        assert tr.status == "todo"

    def test_from_attributes(self) -> None:
        """TaskResponse should work with from_attributes (ORM mode)."""

        class FakeORM:
            """Mimics an ORM model instance."""

            id = 42
            title = "ORM task"
            status = "done"
            due_date = date(2025, 3, 1)
            created_at = datetime(2025, 1, 1, 0, 0, 0)
            updated_at = datetime(2025, 1, 2, 0, 0, 0)

        tr = TaskResponse.model_validate(FakeORM())
        assert tr.id == 42
        assert tr.due_date == date(2025, 3, 1)


class TestTaskStatusEnum:
    """Ensure the status enum has the expected values."""

    def test_values(self) -> None:
        """Enum must contain exactly todo, in-progress, done."""
        values = {s.value for s in TaskStatusEnum}
        assert values == {"todo", "in-progress", "done"}
