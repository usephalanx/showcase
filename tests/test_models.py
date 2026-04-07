"""Tests for app.models Pydantic schemas."""

from __future__ import annotations

import pytest
from pydantic import ValidationError

from app.models import TodoCreate, TodoResponse, TodoUpdate


# ---------------------------------------------------------------------------
# TodoCreate
# ---------------------------------------------------------------------------


class TestTodoCreate:
    """Tests for the TodoCreate schema."""

    def test_create_with_title_only(self) -> None:
        """TodoCreate can be instantiated with just a title."""
        todo = TodoCreate(title="Buy milk")
        assert todo.title == "Buy milk"
        assert todo.description is None

    def test_create_with_title_and_description(self) -> None:
        """TodoCreate accepts an optional description."""
        todo = TodoCreate(title="Buy milk", description="From the store")
        assert todo.title == "Buy milk"
        assert todo.description == "From the store"

    def test_create_requires_title(self) -> None:
        """TodoCreate raises ValidationError when title is missing."""
        with pytest.raises(ValidationError):
            TodoCreate()  # type: ignore[call-arg]

    def test_create_rejects_empty_title(self) -> None:
        """TodoCreate rejects an empty string title."""
        with pytest.raises(ValidationError):
            TodoCreate(title="")


# ---------------------------------------------------------------------------
# TodoUpdate
# ---------------------------------------------------------------------------


class TestTodoUpdate:
    """Tests for the TodoUpdate schema."""

    def test_update_all_none_by_default(self) -> None:
        """TodoUpdate fields default to None when not provided."""
        update = TodoUpdate()
        assert update.title is None
        assert update.description is None
        assert update.completed is None

    def test_update_partial_fields(self) -> None:
        """TodoUpdate allows setting a subset of fields."""
        update = TodoUpdate(completed=True)
        assert update.title is None
        assert update.description is None
        assert update.completed is True

    def test_update_all_fields(self) -> None:
        """TodoUpdate accepts all fields simultaneously."""
        update = TodoUpdate(
            title="New title", description="New desc", completed=False
        )
        assert update.title == "New title"
        assert update.description == "New desc"
        assert update.completed is False

    def test_update_rejects_empty_title(self) -> None:
        """TodoUpdate rejects an empty string title when provided."""
        with pytest.raises(ValidationError):
            TodoUpdate(title="")

    def test_update_model_dump_exclude_unset(self) -> None:
        """model_dump(exclude_unset=True) only includes explicitly set fields."""
        update = TodoUpdate(completed=True)
        dumped = update.model_dump(exclude_unset=True)
        assert dumped == {"completed": True}


# ---------------------------------------------------------------------------
# TodoResponse
# ---------------------------------------------------------------------------


class TestTodoResponse:
    """Tests for the TodoResponse schema."""

    def test_response_all_fields(self) -> None:
        """TodoResponse can be created with all fields."""
        resp = TodoResponse(
            id=1, title="Test", description="Desc", completed=False
        )
        assert resp.id == 1
        assert resp.title == "Test"
        assert resp.description == "Desc"
        assert resp.completed is False

    def test_response_description_defaults_to_none(self) -> None:
        """TodoResponse defaults description to None when omitted."""
        resp = TodoResponse(id=1, title="Test", completed=True)
        assert resp.description is None

    def test_response_requires_id(self) -> None:
        """TodoResponse raises ValidationError when id is missing."""
        with pytest.raises(ValidationError):
            TodoResponse(title="Test", completed=False)  # type: ignore[call-arg]

    def test_response_requires_title(self) -> None:
        """TodoResponse raises ValidationError when title is missing."""
        with pytest.raises(ValidationError):
            TodoResponse(id=1, completed=False)  # type: ignore[call-arg]

    def test_response_requires_completed(self) -> None:
        """TodoResponse raises ValidationError when completed is missing."""
        with pytest.raises(ValidationError):
            TodoResponse(id=1, title="Test")  # type: ignore[call-arg]
