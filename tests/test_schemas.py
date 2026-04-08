"""Tests for app.schemas Pydantic models.

Covers validation rules, default values, orm_mode compatibility,
and edge cases for TodoBase, TodoCreate, TodoUpdate, and TodoResponse.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict

import pytest
from pydantic import ValidationError

from app.schemas import TodoBase, TodoCreate, TodoResponse, TodoUpdate


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


class _FakeTodoORM:
    """Mimics a SQLAlchemy model instance for orm_mode testing."""

    def __init__(self, **kwargs: Any) -> None:
        """Initialise with arbitrary attributes."""
        for key, value in kwargs.items():
            setattr(self, key, value)


def _valid_response_data() -> Dict[str, Any]:
    """Return a minimal valid dict for TodoResponse."""
    return {
        "id": 1,
        "title": "Buy milk",
        "description": None,
        "completed": False,
        "created_at": datetime(2024, 1, 1, 12, 0, 0),
    }


# ---------------------------------------------------------------------------
# TodoBase
# ---------------------------------------------------------------------------


class TestTodoBase:
    """Tests for the TodoBase schema."""

    def test_valid_with_title_only(self) -> None:
        """TodoBase accepts just a title; description defaults to None."""
        schema = TodoBase(title="Do laundry")
        assert schema.title == "Do laundry"
        assert schema.description is None

    def test_valid_with_title_and_description(self) -> None:
        """TodoBase accepts both title and description."""
        schema = TodoBase(title="Clean house", description="Kitchen and bathroom")
        assert schema.title == "Clean house"
        assert schema.description == "Kitchen and bathroom"

    def test_title_required(self) -> None:
        """Omitting title raises a ValidationError."""
        with pytest.raises(ValidationError) as exc_info:
            TodoBase()  # type: ignore[call-arg]
        assert "title" in str(exc_info.value)

    def test_empty_title_rejected(self) -> None:
        """An empty string title violates the min_length constraint."""
        with pytest.raises(ValidationError) as exc_info:
            TodoBase(title="")
        assert "title" in str(exc_info.value)

    def test_title_max_length(self) -> None:
        """A title exceeding 255 characters is rejected."""
        with pytest.raises(ValidationError):
            TodoBase(title="x" * 256)

    def test_description_max_length(self) -> None:
        """A description exceeding 1024 characters is rejected."""
        with pytest.raises(ValidationError):
            TodoBase(title="Valid", description="y" * 1025)


# ---------------------------------------------------------------------------
# TodoCreate
# ---------------------------------------------------------------------------


class TestTodoCreate:
    """Tests for the TodoCreate schema."""

    def test_inherits_todo_base(self) -> None:
        """TodoCreate is a subclass of TodoBase."""
        assert issubclass(TodoCreate, TodoBase)

    def test_valid_creation(self) -> None:
        """TodoCreate works with title only."""
        schema = TodoCreate(title="Write tests")
        assert schema.title == "Write tests"
        assert schema.description is None

    def test_valid_creation_with_description(self) -> None:
        """TodoCreate works with title and description."""
        schema = TodoCreate(title="Write tests", description="Unit and integration")
        assert schema.description == "Unit and integration"

    def test_title_required(self) -> None:
        """Omitting title in TodoCreate raises ValidationError."""
        with pytest.raises(ValidationError):
            TodoCreate()  # type: ignore[call-arg]


# ---------------------------------------------------------------------------
# TodoUpdate
# ---------------------------------------------------------------------------


class TestTodoUpdate:
    """Tests for the TodoUpdate schema."""

    def test_all_fields_optional(self) -> None:
        """TodoUpdate can be created with no arguments."""
        schema = TodoUpdate()
        assert schema.title is None
        assert schema.description is None
        assert schema.completed is None

    def test_partial_update_title(self) -> None:
        """Only title can be supplied."""
        schema = TodoUpdate(title="New title")
        assert schema.title == "New title"
        assert schema.description is None
        assert schema.completed is None

    def test_partial_update_completed(self) -> None:
        """Only completed can be supplied."""
        schema = TodoUpdate(completed=True)
        assert schema.completed is True
        assert schema.title is None

    def test_partial_update_description(self) -> None:
        """Only description can be supplied."""
        schema = TodoUpdate(description="Updated desc")
        assert schema.description == "Updated desc"

    def test_all_fields_supplied(self) -> None:
        """All three fields can be supplied together."""
        schema = TodoUpdate(
            title="Revised", description="Revised desc", completed=True
        )
        assert schema.title == "Revised"
        assert schema.description == "Revised desc"
        assert schema.completed is True

    def test_empty_title_rejected(self) -> None:
        """An empty string title is rejected even in updates."""
        with pytest.raises(ValidationError):
            TodoUpdate(title="")

    def test_title_max_length(self) -> None:
        """Title exceeding 255 chars is rejected in updates."""
        with pytest.raises(ValidationError):
            TodoUpdate(title="x" * 256)

    def test_description_max_length(self) -> None:
        """Description exceeding 1024 chars is rejected in updates."""
        with pytest.raises(ValidationError):
            TodoUpdate(description="y" * 1025)


# ---------------------------------------------------------------------------
# TodoResponse
# ---------------------------------------------------------------------------


class TestTodoResponse:
    """Tests for the TodoResponse schema."""

    def test_valid_response(self) -> None:
        """TodoResponse accepts all required fields."""
        data = _valid_response_data()
        schema = TodoResponse(**data)
        assert schema.id == 1
        assert schema.title == "Buy milk"
        assert schema.description is None
        assert schema.completed is False
        assert isinstance(schema.created_at, datetime)

    def test_inherits_todo_base(self) -> None:
        """TodoResponse is a subclass of TodoBase."""
        assert issubclass(TodoResponse, TodoBase)

    def test_orm_mode_enabled(self) -> None:
        """TodoResponse Config has orm_mode set to True."""
        assert TodoResponse.Config.orm_mode is True

    def test_from_orm_object(self) -> None:
        """TodoResponse can be constructed from an ORM-like object."""
        now = datetime.now(tz=timezone.utc)
        orm_obj = _FakeTodoORM(
            id=42,
            title="ORM test",
            description="From ORM",
            completed=True,
            created_at=now,
        )
        schema = TodoResponse.from_orm(orm_obj)
        assert schema.id == 42
        assert schema.title == "ORM test"
        assert schema.description == "From ORM"
        assert schema.completed is True
        assert schema.created_at == now

    def test_missing_id_rejected(self) -> None:
        """Omitting id raises ValidationError."""
        data = _valid_response_data()
        del data["id"]
        with pytest.raises(ValidationError):
            TodoResponse(**data)

    def test_missing_completed_rejected(self) -> None:
        """Omitting completed raises ValidationError."""
        data = _valid_response_data()
        del data["completed"]
        with pytest.raises(ValidationError):
            TodoResponse(**data)

    def test_missing_created_at_rejected(self) -> None:
        """Omitting created_at raises ValidationError."""
        data = _valid_response_data()
        del data["created_at"]
        with pytest.raises(ValidationError):
            TodoResponse(**data)

    def test_response_with_description(self) -> None:
        """TodoResponse correctly stores a non-None description."""
        data = _valid_response_data()
        data["description"] = "Some details"
        schema = TodoResponse(**data)
        assert schema.description == "Some details"

    def test_created_at_accepts_string(self) -> None:
        """TodoResponse coerces an ISO datetime string to a datetime object."""
        data = _valid_response_data()
        data["created_at"] = "2024-06-15T10:30:00"
        schema = TodoResponse(**data)
        assert isinstance(schema.created_at, datetime)
        assert schema.created_at.year == 2024
        assert schema.created_at.month == 6
