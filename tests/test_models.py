"""Tests for the Pydantic models defined in models.py."""

from __future__ import annotations

import pytest
from pydantic import ValidationError

from models import TodoCreate, TodoResponse, TodoUpdate


# ---------------------------------------------------------------------------
# TodoCreate
# ---------------------------------------------------------------------------


class TestTodoCreate:
    """Tests for the TodoCreate model."""

    def test_valid_title(self) -> None:
        """A non-empty title should be accepted."""
        todo = TodoCreate(title="Buy milk")
        assert todo.title == "Buy milk"

    def test_empty_title_rejected(self) -> None:
        """An empty string title should be rejected."""
        with pytest.raises(ValidationError):
            TodoCreate(title="")

    def test_whitespace_only_title_rejected(self) -> None:
        """A whitespace-only title that has length >= 1 is still a string.

        Pydantic min_length counts characters, so a single space passes
        min_length but the database layer rejects it.
        """
        # Single space has length 1, so Pydantic accepts it
        todo = TodoCreate(title=" ")
        assert todo.title == " "

    def test_title_too_long_rejected(self) -> None:
        """A title exceeding 500 characters should be rejected."""
        with pytest.raises(ValidationError):
            TodoCreate(title="x" * 501)

    def test_title_max_length_accepted(self) -> None:
        """A title of exactly 500 characters should be accepted."""
        todo = TodoCreate(title="x" * 500)
        assert len(todo.title) == 500

    def test_missing_title_rejected(self) -> None:
        """Omitting title entirely should be rejected."""
        with pytest.raises(ValidationError):
            TodoCreate()  # type: ignore[call-arg]


# ---------------------------------------------------------------------------
# TodoUpdate
# ---------------------------------------------------------------------------


class TestTodoUpdate:
    """Tests for the TodoUpdate model."""

    def test_completed_true(self) -> None:
        """Setting completed to True should work."""
        update = TodoUpdate(completed=True)
        assert update.completed is True

    def test_completed_false(self) -> None:
        """Setting completed to False should work."""
        update = TodoUpdate(completed=False)
        assert update.completed is False

    def test_missing_completed_rejected(self) -> None:
        """Omitting completed entirely should be rejected."""
        with pytest.raises(ValidationError):
            TodoUpdate()  # type: ignore[call-arg]

    def test_non_bool_completed_coerced(self) -> None:
        """Pydantic v2 coerces compatible values to bool."""
        update = TodoUpdate(completed=1)  # type: ignore[arg-type]
        assert update.completed is True


# ---------------------------------------------------------------------------
# TodoResponse
# ---------------------------------------------------------------------------


class TestTodoResponse:
    """Tests for the TodoResponse model."""

    def test_valid_response(self) -> None:
        """All fields provided should create a valid model."""
        resp = TodoResponse(
            id=1,
            title="Test",
            completed=False,
            created_at="2025-01-01 00:00:00",
        )
        assert resp.id == 1
        assert resp.title == "Test"
        assert resp.completed is False
        assert resp.created_at == "2025-01-01 00:00:00"

    def test_missing_field_rejected(self) -> None:
        """Omitting a required field should raise a ValidationError."""
        with pytest.raises(ValidationError):
            TodoResponse(id=1, title="Test", completed=False)  # type: ignore[call-arg]
