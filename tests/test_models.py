"""Tests for Pydantic schemas defined in app.models."""

from __future__ import annotations

import pytest
from pydantic import ValidationError

from app.models import TodoCreate, TodoResponse, TodoUpdate


class TestTodoCreate:
    """Tests for the TodoCreate schema."""

    def test_valid_title_only(self) -> None:
        """TodoCreate with just a title should default description to empty string."""
        todo = TodoCreate(title="Buy milk")
        assert todo.title == "Buy milk"
        assert todo.description == ""

    def test_valid_title_and_description(self) -> None:
        """TodoCreate with title and description should preserve both."""
        todo = TodoCreate(title="Buy milk", description="From the store")
        assert todo.title == "Buy milk"
        assert todo.description == "From the store"

    def test_missing_title_raises(self) -> None:
        """TodoCreate without a title should raise a ValidationError."""
        with pytest.raises(ValidationError):
            TodoCreate()  # type: ignore[call-arg]

    def test_empty_title_raises(self) -> None:
        """TodoCreate with an empty title should raise a ValidationError."""
        with pytest.raises(ValidationError):
            TodoCreate(title="")


class TestTodoUpdate:
    """Tests for the TodoUpdate schema."""

    def test_all_none_by_default(self) -> None:
        """TodoUpdate with no arguments should have all fields as None."""
        update = TodoUpdate()
        assert update.title is None
        assert update.description is None
        assert update.completed is None

    def test_partial_update_title(self) -> None:
        """TodoUpdate with only title set should leave others None."""
        update = TodoUpdate(title="New title")
        assert update.title == "New title"
        assert update.description is None
        assert update.completed is None

    def test_partial_update_completed(self) -> None:
        """TodoUpdate with only completed set should leave others None."""
        update = TodoUpdate(completed=True)
        assert update.completed is True
        assert update.title is None

    def test_empty_title_raises(self) -> None:
        """TodoUpdate with an empty title string should raise ValidationError."""
        with pytest.raises(ValidationError):
            TodoUpdate(title="")


class TestTodoResponse:
    """Tests for the TodoResponse schema."""

    def test_valid_response(self) -> None:
        """TodoResponse should accept all required fields."""
        resp = TodoResponse(id=1, title="Test", description="Desc", completed=False)
        assert resp.id == 1
        assert resp.title == "Test"
        assert resp.description == "Desc"
        assert resp.completed is False

    def test_missing_id_raises(self) -> None:
        """TodoResponse without an id should raise ValidationError."""
        with pytest.raises(ValidationError):
            TodoResponse(title="Test", description="Desc", completed=False)  # type: ignore[call-arg]
