"""Tests for Pydantic schemas in app.schemas.

Covers validation, defaults, serialisation, enum constraints, and
edge cases for TaskCreate, TaskUpdate, TaskPatch, and TaskResponse.
"""

from __future__ import annotations

from datetime import date, datetime
from typing import Any, Dict

import pytest
from pydantic import ValidationError

from app.schemas import (
    TaskCreate,
    TaskPatch,
    TaskResponse,
    TaskStatusEnum,
    TaskUpdate,
)


# ---------------------------------------------------------------------------
# TaskStatusEnum
# ---------------------------------------------------------------------------


class TestTaskStatusEnum:
    """Tests for the TaskStatusEnum enumeration."""

    def test_enum_values(self) -> None:
        """Enum must expose exactly three valid values."""
        assert TaskStatusEnum.TODO.value == "todo"
        assert TaskStatusEnum.IN_PROGRESS.value == "in-progress"
        assert TaskStatusEnum.DONE.value == "done"

    def test_enum_member_count(self) -> None:
        """Ensure no unexpected members are present."""
        assert len(TaskStatusEnum) == 3

    def test_enum_is_str_subclass(self) -> None:
        """Enum members should be usable as plain strings."""
        assert isinstance(TaskStatusEnum.TODO, str)
        assert TaskStatusEnum.TODO == "todo"


# ---------------------------------------------------------------------------
# TaskCreate
# ---------------------------------------------------------------------------


class TestTaskCreate:
    """Tests for the TaskCreate schema."""

    def test_minimal_creation(self) -> None:
        """Only title is required; status defaults to 'todo', due_date to None."""
        task = TaskCreate(title="Write tests")
        assert task.title == "Write tests"
        assert task.status == TaskStatusEnum.TODO
        assert task.due_date is None

    def test_all_fields_provided(self) -> None:
        """All fields can be explicitly set."""
        task = TaskCreate(
            title="Deploy app",
            status="in-progress",
            due_date="2025-12-31",
        )
        assert task.title == "Deploy app"
        assert task.status == TaskStatusEnum.IN_PROGRESS
        assert task.due_date == date(2025, 12, 31)

    def test_status_default_is_todo(self) -> None:
        """Default status must be 'todo'."""
        task = TaskCreate(title="a")
        assert task.status == TaskStatusEnum.TODO

    def test_title_required(self) -> None:
        """Omitting title must raise a validation error."""
        with pytest.raises(ValidationError) as exc_info:
            TaskCreate()  # type: ignore[call-arg]
        errors = exc_info.value.errors()
        assert any(e["loc"] == ("title",) for e in errors)

    def test_title_empty_string_rejected(self) -> None:
        """An empty title must be rejected (min_length=1)."""
        with pytest.raises(ValidationError) as exc_info:
            TaskCreate(title="")
        errors = exc_info.value.errors()
        assert any(e["loc"] == ("title",) for e in errors)

    def test_title_max_length_exceeded(self) -> None:
        """Titles exceeding 255 characters must be rejected."""
        with pytest.raises(ValidationError) as exc_info:
            TaskCreate(title="x" * 256)
        errors = exc_info.value.errors()
        assert any(e["loc"] == ("title",) for e in errors)

    def test_title_max_length_boundary(self) -> None:
        """Titles of exactly 255 characters must be accepted."""
        task = TaskCreate(title="x" * 255)
        assert len(task.title) == 255

    def test_invalid_status_rejected(self) -> None:
        """An invalid status string must raise a validation error."""
        with pytest.raises(ValidationError) as exc_info:
            TaskCreate(title="test", status="invalid")
        errors = exc_info.value.errors()
        assert any(e["loc"] == ("status",) for e in errors)

    def test_status_accepts_all_valid_values(self) -> None:
        """All three enum values must be accepted."""
        for status_val in ("todo", "in-progress", "done"):
            task = TaskCreate(title="t", status=status_val)
            assert task.status.value == status_val

    def test_due_date_with_date_object(self) -> None:
        """due_date accepts native date objects."""
        d = date(2025, 6, 15)
        task = TaskCreate(title="t", due_date=d)
        assert task.due_date == d

    def test_due_date_with_iso_string(self) -> None:
        """due_date accepts ISO 8601 date strings."""
        task = TaskCreate(title="t", due_date="2025-01-01")
        assert task.due_date == date(2025, 1, 1)

    def test_due_date_invalid_string_rejected(self) -> None:
        """Non-date strings must be rejected."""
        with pytest.raises(ValidationError):
            TaskCreate(title="t", due_date="not-a-date")

    def test_serialisation_round_trip(self) -> None:
        """model_dump should produce a JSON-compatible dict."""
        task = TaskCreate(
            title="Round trip",
            status="done",
            due_date="2025-03-15",
        )
        data = task.model_dump(mode="json")
        assert data["title"] == "Round trip"
        assert data["status"] == "done"
        assert data["due_date"] == "2025-03-15"


# ---------------------------------------------------------------------------
# TaskUpdate
# ---------------------------------------------------------------------------


class TestTaskUpdate:
    """Tests for the TaskUpdate (PUT) schema."""

    def test_all_fields_required(self) -> None:
        """title and status are required; due_date defaults to None."""
        task = TaskUpdate(title="Updated", status="done")
        assert task.title == "Updated"
        assert task.status == TaskStatusEnum.DONE
        assert task.due_date is None

    def test_missing_title_rejected(self) -> None:
        """Omitting title raises a validation error."""
        with pytest.raises(ValidationError):
            TaskUpdate(status="todo")  # type: ignore[call-arg]

    def test_missing_status_rejected(self) -> None:
        """Omitting status raises a validation error."""
        with pytest.raises(ValidationError):
            TaskUpdate(title="test")  # type: ignore[call-arg]

    def test_invalid_status_rejected(self) -> None:
        """Invalid status value must raise a validation error."""
        with pytest.raises(ValidationError):
            TaskUpdate(title="t", status="pending")

    def test_due_date_nullable(self) -> None:
        """Explicitly passing None for due_date must be accepted."""
        task = TaskUpdate(title="t", status="todo", due_date=None)
        assert task.due_date is None

    def test_due_date_provided(self) -> None:
        """Providing a valid date must be accepted."""
        task = TaskUpdate(
            title="t",
            status="in-progress",
            due_date="2025-06-01",
        )
        assert task.due_date == date(2025, 6, 1)

    def test_title_empty_string_rejected(self) -> None:
        """An empty title must be rejected."""
        with pytest.raises(ValidationError):
            TaskUpdate(title="", status="todo")

    def test_title_max_length_exceeded(self) -> None:
        """Title over 255 chars must be rejected."""
        with pytest.raises(ValidationError):
            TaskUpdate(title="x" * 256, status="todo")


# ---------------------------------------------------------------------------
# TaskPatch
# ---------------------------------------------------------------------------


class TestTaskPatch:
    """Tests for the TaskPatch (PATCH) schema."""

    def test_all_fields_optional(self) -> None:
        """An empty body should produce a valid instance with all None."""
        patch = TaskPatch()
        assert patch.title is None
        assert patch.status is None
        assert patch.due_date is None

    def test_single_field_update(self) -> None:
        """Only supplying title must leave other fields as None."""
        patch = TaskPatch(title="New title")
        assert patch.title == "New title"
        assert patch.status is None
        assert patch.due_date is None

    def test_status_only(self) -> None:
        """Only supplying status must work."""
        patch = TaskPatch(status="done")
        assert patch.status == TaskStatusEnum.DONE
        assert patch.title is None

    def test_due_date_only(self) -> None:
        """Only supplying due_date must work."""
        patch = TaskPatch(due_date="2025-12-25")
        assert patch.due_date == date(2025, 12, 25)

    def test_all_fields_supplied(self) -> None:
        """All fields can be supplied at once."""
        patch = TaskPatch(
            title="All fields",
            status="in-progress",
            due_date="2025-07-04",
        )
        assert patch.title == "All fields"
        assert patch.status == TaskStatusEnum.IN_PROGRESS
        assert patch.due_date == date(2025, 7, 4)

    def test_invalid_status_rejected(self) -> None:
        """Invalid status must be rejected even in a patch."""
        with pytest.raises(ValidationError):
            TaskPatch(status="cancelled")

    def test_title_empty_string_rejected(self) -> None:
        """Empty title must be rejected when provided."""
        with pytest.raises(ValidationError):
            TaskPatch(title="")

    def test_title_max_length_exceeded(self) -> None:
        """Over-length title must be rejected."""
        with pytest.raises(ValidationError):
            TaskPatch(title="x" * 256)

    def test_model_dump_excludes_unset(self) -> None:
        """model_dump(exclude_unset=True) should only contain provided fields."""
        patch = TaskPatch(status="done")
        data = patch.model_dump(exclude_unset=True)
        assert "status" in data
        assert "title" not in data
        assert "due_date" not in data


# ---------------------------------------------------------------------------
# TaskResponse
# ---------------------------------------------------------------------------


class TestTaskResponse:
    """Tests for the TaskResponse schema."""

    @pytest.fixture()
    def sample_response_data(self) -> Dict[str, Any]:
        """Return a valid response payload dict."""
        return {
            "id": 1,
            "title": "Sample task",
            "status": "todo",
            "due_date": None,
            "created_at": datetime(2025, 1, 1, 12, 0, 0),
            "updated_at": datetime(2025, 1, 2, 8, 30, 0),
        }

    def test_valid_response(self, sample_response_data: Dict[str, Any]) -> None:
        """A full valid payload should be accepted."""
        resp = TaskResponse(**sample_response_data)
        assert resp.id == 1
        assert resp.title == "Sample task"
        assert resp.status == TaskStatusEnum.TODO
        assert resp.due_date is None
        assert resp.created_at == datetime(2025, 1, 1, 12, 0, 0)
        assert resp.updated_at == datetime(2025, 1, 2, 8, 30, 0)

    def test_with_due_date(self, sample_response_data: Dict[str, Any]) -> None:
        """due_date should be accepted when present."""
        sample_response_data["due_date"] = date(2025, 6, 30)
        resp = TaskResponse(**sample_response_data)
        assert resp.due_date == date(2025, 6, 30)

    def test_status_is_enum(self, sample_response_data: Dict[str, Any]) -> None:
        """The status field should be deserialized to the enum."""
        sample_response_data["status"] = "in-progress"
        resp = TaskResponse(**sample_response_data)
        assert resp.status == TaskStatusEnum.IN_PROGRESS
        assert isinstance(resp.status, TaskStatusEnum)

    def test_from_attributes(self) -> None:
        """TaskResponse should accept ORM model instances via from_attributes."""

        class FakeORM:
            """Minimal ORM-like object for testing from_attributes."""

            id = 42
            title = "ORM task"
            status = "done"
            due_date = date(2025, 3, 1)
            created_at = datetime(2025, 1, 1, 0, 0, 0)
            updated_at = datetime(2025, 1, 2, 0, 0, 0)

        resp = TaskResponse.model_validate(FakeORM())
        assert resp.id == 42
        assert resp.title == "ORM task"
        assert resp.status == TaskStatusEnum.DONE
        assert resp.due_date == date(2025, 3, 1)

    def test_missing_id_rejected(self, sample_response_data: Dict[str, Any]) -> None:
        """id is required in the response."""
        del sample_response_data["id"]
        with pytest.raises(ValidationError):
            TaskResponse(**sample_response_data)

    def test_missing_title_rejected(self, sample_response_data: Dict[str, Any]) -> None:
        """title is required in the response."""
        del sample_response_data["title"]
        with pytest.raises(ValidationError):
            TaskResponse(**sample_response_data)

    def test_missing_created_at_rejected(
        self, sample_response_data: Dict[str, Any]
    ) -> None:
        """created_at is required in the response."""
        del sample_response_data["created_at"]
        with pytest.raises(ValidationError):
            TaskResponse(**sample_response_data)

    def test_missing_updated_at_rejected(
        self, sample_response_data: Dict[str, Any]
    ) -> None:
        """updated_at is required in the response."""
        del sample_response_data["updated_at"]
        with pytest.raises(ValidationError):
            TaskResponse(**sample_response_data)

    def test_invalid_status_in_response_rejected(
        self, sample_response_data: Dict[str, Any]
    ) -> None:
        """Invalid status must be rejected even on the response side."""
        sample_response_data["status"] = "unknown"
        with pytest.raises(ValidationError):
            TaskResponse(**sample_response_data)

    def test_serialisation_json_mode(
        self, sample_response_data: Dict[str, Any]
    ) -> None:
        """JSON serialisation should produce string representations."""
        sample_response_data["due_date"] = date(2025, 6, 15)
        resp = TaskResponse(**sample_response_data)
        data = resp.model_dump(mode="json")
        assert isinstance(data["id"], int)
        assert isinstance(data["title"], str)
        assert isinstance(data["status"], str)
        assert data["status"] == "todo"
        assert data["due_date"] == "2025-06-15"
        assert isinstance(data["created_at"], str)
        assert isinstance(data["updated_at"], str)

    def test_all_statuses_in_response(self) -> None:
        """All three status enum values should be representable in a response."""
        now = datetime.now()
        for status_val in TaskStatusEnum:
            resp = TaskResponse(
                id=1,
                title="t",
                status=status_val,
                created_at=now,
                updated_at=now,
            )
            assert resp.status == status_val
