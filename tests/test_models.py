"""Unit tests for Pydantic models in models.py."""

from __future__ import annotations

import pytest
from pydantic import ValidationError

from models import TodoCreate, TodoResponse, TodoUpdate


# ---------------------------------------------------------------------------
# TodoCreate
# ---------------------------------------------------------------------------


class TestTodoCreate:
    """Tests for the TodoCreate schema."""

    def test_minimal_creation(self) -> None:
        """Only title is required; defaults should be applied."""
        todo = TodoCreate(title="Buy milk")
        assert todo.title == "Buy milk"
        assert todo.description is None
        assert todo.completed is False

    def test_full_creation(self) -> None:
        """All fields can be supplied explicitly."""
        todo = TodoCreate(
            title="Deploy app",
            description="Push to production",
            completed=True,
        )
        assert todo.title == "Deploy app"
        assert todo.description == "Push to production"
        assert todo.completed is True

    def test_empty_title_rejected(self) -> None:
        """An empty title string must be rejected by the min_length constraint."""
        with pytest.raises(ValidationError):
            TodoCreate(title="")

    def test_missing_title_rejected(self) -> None:
        """Title is required — omitting it must raise a validation error."""
        with pytest.raises(ValidationError):
            TodoCreate()  # type: ignore[call-arg]


# ---------------------------------------------------------------------------
# TodoUpdate
# ---------------------------------------------------------------------------


class TestTodoUpdate:
    """Tests for the TodoUpdate schema."""

    def test_all_fields_optional(self) -> None:
        """Creating an update with no fields should succeed."""
        update = TodoUpdate()
        assert update.title is None
        assert update.description is None
        assert update.completed is None

    def test_partial_update(self) -> None:
        """Only some fields can be set."""
        update = TodoUpdate(completed=True)
        assert update.completed is True
        assert update.title is None

    def test_empty_title_rejected(self) -> None:
        """An empty title string must be rejected."""
        with pytest.raises(ValidationError):
            TodoUpdate(title="")


# ---------------------------------------------------------------------------
# TodoResponse
# ---------------------------------------------------------------------------


class TestTodoResponse:
    """Tests for the TodoResponse schema."""

    def test_full_response(self) -> None:
        """All fields present should produce a valid response model."""
        resp = TodoResponse(
            id=1,
            title="Test",
            description="A description",
            completed=False,
            created_at="2024-01-01T00:00:00+00:00",
        )
        assert resp.id == 1
        assert resp.title == "Test"
        assert resp.description == "A description"
        assert resp.completed is False

    def test_description_defaults_to_none(self) -> None:
        """Description should default to None if omitted."""
        resp = TodoResponse(
            id=2,
            title="No desc",
            completed=True,
            created_at="2024-01-01T00:00:00+00:00",
        )
        assert resp.description is None

    def test_missing_required_field(self) -> None:
        """Omitting a required field must raise a validation error."""
        with pytest.raises(ValidationError):
            TodoResponse(title="Missing id", completed=False, created_at="now")  # type: ignore[call-arg]
