"""Tests for Pydantic models (models.py).

Covers: TodoCreate, TodoUpdate, TodoResponse validation and defaults.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest
from pydantic import ValidationError

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from models import TodoCreate, TodoResponse, TodoUpdate


class TestTodoCreate:
    """Tests for the TodoCreate model."""

    def test_valid_creation(self) -> None:
        """A TodoCreate with just a title is valid."""
        tc = TodoCreate(title="Test")
        assert tc.title == "Test"
        assert tc.description is None
        assert tc.completed is False

    def test_with_all_fields(self) -> None:
        """All fields can be provided."""
        tc = TodoCreate(title="T", description="D", completed=True)
        assert tc.title == "T"
        assert tc.description == "D"
        assert tc.completed is True

    def test_empty_title_rejected(self) -> None:
        """An empty-string title is rejected."""
        with pytest.raises(ValidationError):
            TodoCreate(title="")

    def test_missing_title_rejected(self) -> None:
        """Omitting title raises a validation error."""
        with pytest.raises(ValidationError):
            TodoCreate()  # type: ignore[call-arg]


class TestTodoUpdate:
    """Tests for the TodoUpdate model."""

    def test_all_fields_optional(self) -> None:
        """An empty TodoUpdate is valid."""
        tu = TodoUpdate()
        assert tu.title is None
        assert tu.description is None
        assert tu.completed is None

    def test_partial_update(self) -> None:
        """Only some fields can be provided."""
        tu = TodoUpdate(completed=True)
        assert tu.completed is True
        assert tu.title is None

    def test_empty_title_rejected(self) -> None:
        """An empty-string title is rejected even in update."""
        with pytest.raises(ValidationError):
            TodoUpdate(title="")


class TestTodoResponse:
    """Tests for the TodoResponse model."""

    def test_valid_response(self) -> None:
        """A fully populated TodoResponse is valid."""
        tr = TodoResponse(
            id=1,
            title="Task",
            completed=False,
            created_at="2024-01-01T00:00:00+00:00",
        )
        assert tr.id == 1
        assert tr.title == "Task"
        assert tr.completed is False

    def test_description_optional(self) -> None:
        """Description defaults to None."""
        tr = TodoResponse(
            id=1,
            title="Task",
            completed=False,
            created_at="2024-01-01T00:00:00",
        )
        assert tr.description is None

    def test_with_description(self) -> None:
        """Description can be provided."""
        tr = TodoResponse(
            id=1,
            title="Task",
            description="Details",
            completed=False,
            created_at="2024-01-01T00:00:00",
        )
        assert tr.description == "Details"
