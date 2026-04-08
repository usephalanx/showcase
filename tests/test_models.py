"""Tests for Pydantic models defined in models.py."""

from __future__ import annotations

from datetime import datetime, timezone

import pytest
from pydantic import ValidationError

from models import TodoCreate, TodoResponse, TodoUpdate


class TestTodoCreate:
    """Tests for the TodoCreate schema."""

    def test_create_with_title_only(self) -> None:
        """TodoCreate should accept just a title, defaulting description to None."""
        todo = TodoCreate(title="Buy milk")
        assert todo.title == "Buy milk"
        assert todo.description is None

    def test_create_with_title_and_description(self) -> None:
        """TodoCreate should accept both title and description."""
        todo = TodoCreate(title="Buy milk", description="2% milk from store")
        assert todo.title == "Buy milk"
        assert todo.description == "2% milk from store"

    def test_create_missing_title_raises(self) -> None:
        """TodoCreate should reject a missing title."""
        with pytest.raises(ValidationError):
            TodoCreate()  # type: ignore[call-arg]

    def test_create_empty_title_raises(self) -> None:
        """TodoCreate should reject an empty string title."""
        with pytest.raises(ValidationError):
            TodoCreate(title="")


class TestTodoUpdate:
    """Tests for the TodoUpdate schema."""

    def test_update_all_none_by_default(self) -> None:
        """TodoUpdate with no args should have all fields as None."""
        update = TodoUpdate()
        assert update.title is None
        assert update.description is None
        assert update.completed is None

    def test_update_partial_fields(self) -> None:
        """TodoUpdate should accept any subset of fields."""
        update = TodoUpdate(completed=True)
        assert update.completed is True
        assert update.title is None
        assert update.description is None

    def test_update_all_fields(self) -> None:
        """TodoUpdate should accept all fields."""
        update = TodoUpdate(
            title="Updated", description="New desc", completed=False
        )
        assert update.title == "Updated"
        assert update.description == "New desc"
        assert update.completed is False

    def test_update_empty_title_raises(self) -> None:
        """TodoUpdate should reject an empty string title."""
        with pytest.raises(ValidationError):
            TodoUpdate(title="")


class TestTodoResponse:
    """Tests for the TodoResponse schema."""

    def test_response_with_all_fields(self) -> None:
        """TodoResponse should correctly store all provided fields."""
        now = datetime.now(timezone.utc)
        resp = TodoResponse(
            id=1,
            title="Test",
            description="A test todo",
            completed=False,
            created_at=now,
        )
        assert resp.id == 1
        assert resp.title == "Test"
        assert resp.description == "A test todo"
        assert resp.completed is False
        assert resp.created_at == now

    def test_response_description_defaults_to_none(self) -> None:
        """TodoResponse should default description to None."""
        now = datetime.now(timezone.utc)
        resp = TodoResponse(
            id=1, title="Test", completed=False, created_at=now
        )
        assert resp.description is None

    def test_response_missing_required_field_raises(self) -> None:
        """TodoResponse should reject missing required fields."""
        with pytest.raises(ValidationError):
            TodoResponse(id=1, title="Test")  # type: ignore[call-arg]
