"""Tests for app.schemas Pydantic models."""

from __future__ import annotations

from datetime import date
from types import SimpleNamespace

import pytest

from app.schemas import TaskBase, TaskCreate, TaskResponse, TaskUpdate


# ---------------------------------------------------------------------------
# TaskBase
# ---------------------------------------------------------------------------


class TestTaskBase:
    """Tests for the TaskBase schema."""

    def test_minimal_valid(self) -> None:
        """Only title is required; status and due_date have defaults."""
        task = TaskBase(title="Buy groceries")
        assert task.title == "Buy groceries"
        assert task.status == "todo"
        assert task.due_date is None

    def test_all_fields(self) -> None:
        """All fields can be explicitly set."""
        task = TaskBase(
            title="Write report",
            status="in-progress",
            due_date=date(2025, 12, 31),
        )
        assert task.title == "Write report"
        assert task.status == "in-progress"
        assert task.due_date == date(2025, 12, 31)

    def test_title_required(self) -> None:
        """Omitting title must raise a validation error."""
        with pytest.raises(Exception):  # ValidationError
            TaskBase()  # type: ignore[call-arg]

    def test_title_min_length(self) -> None:
        """An empty string title must be rejected."""
        with pytest.raises(Exception):
            TaskBase(title="")

    def test_due_date_none_explicit(self) -> None:
        """Explicitly passing None for due_date is valid."""
        task = TaskBase(title="Task", due_date=None)
        assert task.due_date is None

    def test_due_date_string_coercion(self) -> None:
        """Pydantic should coerce an ISO-format string to a date."""
        task = TaskBase(title="Task", due_date="2025-06-15")  # type: ignore[arg-type]
        assert task.due_date == date(2025, 6, 15)

    def test_status_default_value(self) -> None:
        """Default status must be 'todo'."""
        task = TaskBase(title="Task")
        assert task.status == "todo"

    def test_status_custom_value(self) -> None:
        """Custom status values are accepted."""
        task = TaskBase(title="Task", status="done")
        assert task.status == "done"


# ---------------------------------------------------------------------------
# TaskCreate
# ---------------------------------------------------------------------------


class TestTaskCreate:
    """Tests for the TaskCreate schema."""

    def test_inherits_task_base(self) -> None:
        """TaskCreate must be a subclass of TaskBase."""
        assert issubclass(TaskCreate, TaskBase)

    def test_valid_creation(self) -> None:
        """Standard creation with defaults works."""
        task = TaskCreate(title="Deploy app")
        assert task.title == "Deploy app"
        assert task.status == "todo"
        assert task.due_date is None

    def test_all_fields(self) -> None:
        """All inherited fields can be supplied."""
        task = TaskCreate(
            title="Release",
            status="in-progress",
            due_date=date(2025, 1, 1),
        )
        assert task.title == "Release"
        assert task.status == "in-progress"
        assert task.due_date == date(2025, 1, 1)


# ---------------------------------------------------------------------------
# TaskUpdate
# ---------------------------------------------------------------------------


class TestTaskUpdate:
    """Tests for the TaskUpdate schema."""

    def test_all_fields_optional(self) -> None:
        """Constructing with no arguments must succeed (partial update)."""
        task = TaskUpdate()
        assert task.title is None
        assert task.status is None
        assert task.due_date is None

    def test_partial_update_title_only(self) -> None:
        """Updating only the title is valid."""
        task = TaskUpdate(title="New title")
        assert task.title == "New title"
        assert task.status is None
        assert task.due_date is None

    def test_partial_update_status_only(self) -> None:
        """Updating only the status is valid."""
        task = TaskUpdate(status="done")
        assert task.title is None
        assert task.status == "done"

    def test_partial_update_due_date_only(self) -> None:
        """Updating only the due_date is valid."""
        task = TaskUpdate(due_date=date(2025, 3, 15))
        assert task.due_date == date(2025, 3, 15)

    def test_full_update(self) -> None:
        """Supplying all fields is valid."""
        task = TaskUpdate(
            title="Updated",
            status="in-progress",
            due_date=date(2025, 7, 4),
        )
        assert task.title == "Updated"
        assert task.status == "in-progress"
        assert task.due_date == date(2025, 7, 4)

    def test_title_empty_string_rejected(self) -> None:
        """An empty string title must be rejected even for updates."""
        with pytest.raises(Exception):
            TaskUpdate(title="")

    def test_is_not_subclass_of_task_base(self) -> None:
        """TaskUpdate inherits from BaseModel directly, not TaskBase."""
        assert not issubclass(TaskUpdate, TaskBase)


# ---------------------------------------------------------------------------
# TaskResponse
# ---------------------------------------------------------------------------


class TestTaskResponse:
    """Tests for the TaskResponse schema."""

    def test_inherits_task_base(self) -> None:
        """TaskResponse must be a subclass of TaskBase."""
        assert issubclass(TaskResponse, TaskBase)

    def test_requires_id(self) -> None:
        """Omitting `id` must raise a validation error."""
        with pytest.raises(Exception):
            TaskResponse(title="Task")  # type: ignore[call-arg]

    def test_valid_response(self) -> None:
        """Construct a valid response with all fields."""
        task = TaskResponse(
            id=1,
            title="Read book",
            status="todo",
            due_date=date(2025, 8, 1),
        )
        assert task.id == 1
        assert task.title == "Read book"
        assert task.status == "todo"
        assert task.due_date == date(2025, 8, 1)

    def test_orm_mode_enabled(self) -> None:
        """The Config class must have orm_mode set to True."""
        assert TaskResponse.Config.orm_mode is True

    def test_from_orm_object(self) -> None:
        """TaskResponse should be constructable from an ORM-like object."""
        orm_obj = SimpleNamespace(
            id=42,
            title="ORM task",
            status="done",
            due_date=date(2025, 11, 11),
        )
        task = TaskResponse.from_orm(orm_obj)
        assert task.id == 42
        assert task.title == "ORM task"
        assert task.status == "done"
        assert task.due_date == date(2025, 11, 11)

    def test_from_orm_object_without_due_date(self) -> None:
        """ORM objects with None due_date should serialize correctly."""
        orm_obj = SimpleNamespace(
            id=7,
            title="No deadline",
            status="todo",
            due_date=None,
        )
        task = TaskResponse.from_orm(orm_obj)
        assert task.id == 7
        assert task.due_date is None

    def test_dict_output(self) -> None:
        """The .dict() output must contain all expected keys."""
        task = TaskResponse(
            id=1,
            title="Serialize me",
            status="todo",
            due_date=None,
        )
        d = task.dict()
        assert set(d.keys()) == {"id", "title", "status", "due_date"}

    def test_json_output(self) -> None:
        """The .json() output must be a valid JSON string."""
        import json

        task = TaskResponse(
            id=1,
            title="JSON test",
            status="todo",
            due_date=date(2025, 1, 1),
        )
        parsed = json.loads(task.json())
        assert parsed["id"] == 1
        assert parsed["title"] == "JSON test"
        assert parsed["due_date"] == "2025-01-01"

    def test_response_defaults_from_base(self) -> None:
        """Status defaults should still apply from TaskBase."""
        task = TaskResponse(id=99, title="Defaults")
        assert task.status == "todo"
        assert task.due_date is None
