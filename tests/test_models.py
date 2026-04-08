"""Tests for Pydantic models defined in models.py."""

from __future__ import annotations

import pytest
from pydantic import ValidationError

from models import TodoCreate, TodoResponse, TodoUpdate


class TestTodoCreate:
    """Tests for the TodoCreate model."""

    def test_create_with_title_only(self) -> None:
        """Title is the only required field."""
        todo = TodoCreate(title="Buy milk")
        assert todo.title == "Buy milk"
        assert todo.description is None
        assert todo.completed is False

    def test_create_with_all_fields(self) -> None:
        """All fields can be provided explicitly."""
        todo = TodoCreate(title="Buy milk", description="2% milk", completed=True)
        assert todo.title == "Buy milk"
        assert todo.description == "2% milk"
        assert todo.completed is True

    def test_create_missing_title_raises(self) -> None:
        """Omitting title must raise a validation error."""
        with pytest.raises(ValidationError):
            TodoCreate()  # type: ignore[call-arg]

    def test_create_empty_title_raises(self) -> None:
        """An empty string title must raise a validation error."""
        with pytest.raises(ValidationError):
            TodoCreate(title="")


class TestTodoUpdate:
    """Tests for the TodoUpdate model."""

    def test_update_all_none_by_default(self) -> None:
        """All fields default to None."""
        update = TodoUpdate()
        assert update.title is None
        assert update.description is None
        assert update.completed is None

    def test_update_partial(self) -> None:
        """Only supplied fields are set."""
        update = TodoUpdate(completed=True)
        assert update.completed is True
        assert update.title is None


class TestTodoResponse:
    """Tests for the TodoResponse model."""

    def test_response_roundtrip(self) -> None:
        """All fields are populated correctly."""
        data = {
            "id": 1,
            "title": "Test",
            "description": "A test todo",
            "completed": False,
            "created_at": "2024-01-01T00:00:00+00:00",
        }
        resp = TodoResponse(**data)
        assert resp.id == 1
        assert resp.title == "Test"
        assert resp.description == "A test todo"
        assert resp.completed is False
        assert resp.created_at == "2024-01-01T00:00:00+00:00"

    def test_response_description_defaults_to_none(self) -> None:
        """Description is optional and defaults to None."""
        resp = TodoResponse(
            id=2, title="No desc", completed=False, created_at="2024-01-01T00:00:00"
        )
        assert resp.description is None
