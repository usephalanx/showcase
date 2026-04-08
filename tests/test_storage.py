"""Tests for the in-memory TodoStore defined in storage.py."""

from __future__ import annotations

from datetime import datetime, timezone

import pytest

from storage import TodoStore


@pytest.fixture()
def store() -> TodoStore:
    """Return a fresh TodoStore instance for each test."""
    return TodoStore()


class TestCreate:
    """Tests for TodoStore.create()."""

    def test_create_returns_todo_with_id(self, store: TodoStore) -> None:
        """create() should return a dict with an auto-incremented id."""
        todo = store.create(title="First")
        assert todo["id"] == 1
        assert todo["title"] == "First"
        assert todo["description"] is None
        assert todo["completed"] is False
        assert isinstance(todo["created_at"], datetime)

    def test_create_increments_id(self, store: TodoStore) -> None:
        """Successive creates should produce increasing IDs."""
        t1 = store.create(title="First")
        t2 = store.create(title="Second")
        assert t2["id"] == t1["id"] + 1

    def test_create_with_description(self, store: TodoStore) -> None:
        """create() should accept an optional description."""
        todo = store.create(title="Task", description="Details here")
        assert todo["description"] == "Details here"


class TestGetAll:
    """Tests for TodoStore.get_all()."""

    def test_get_all_empty(self, store: TodoStore) -> None:
        """get_all() on an empty store should return an empty list."""
        assert store.get_all() == []

    def test_get_all_returns_all_todos(self, store: TodoStore) -> None:
        """get_all() should return every created todo."""
        store.create(title="A")
        store.create(title="B")
        todos = store.get_all()
        assert len(todos) == 2


class TestGetById:
    """Tests for TodoStore.get_by_id()."""

    def test_get_existing_todo(self, store: TodoStore) -> None:
        """get_by_id() should return the correct todo."""
        created = store.create(title="Find me")
        found = store.get_by_id(created["id"])
        assert found is not None
        assert found["title"] == "Find me"

    def test_get_nonexistent_todo_returns_none(self, store: TodoStore) -> None:
        """get_by_id() should return None for missing IDs."""
        assert store.get_by_id(999) is None


class TestUpdate:
    """Tests for TodoStore.update()."""

    def test_update_title(self, store: TodoStore) -> None:
        """update() should change the title when provided."""
        created = store.create(title="Old")
        updated = store.update(created["id"], title="New")
        assert updated is not None
        assert updated["title"] == "New"

    def test_update_completed(self, store: TodoStore) -> None:
        """update() should change the completed flag."""
        created = store.create(title="Task")
        updated = store.update(created["id"], completed=True)
        assert updated is not None
        assert updated["completed"] is True

    def test_update_description_to_none(self, store: TodoStore) -> None:
        """update() should allow setting description to None explicitly."""
        created = store.create(title="Task", description="Has desc")
        updated = store.update(created["id"], description=None)
        assert updated is not None
        assert updated["description"] is None

    def test_update_nonexistent_returns_none(self, store: TodoStore) -> None:
        """update() should return None for a missing ID."""
        assert store.update(999, title="Nope") is None


class TestDelete:
    """Tests for TodoStore.delete()."""

    def test_delete_existing_todo(self, store: TodoStore) -> None:
        """delete() should return True and remove the todo."""
        created = store.create(title="Remove me")
        assert store.delete(created["id"]) is True
        assert store.get_by_id(created["id"]) is None

    def test_delete_nonexistent_returns_false(self, store: TodoStore) -> None:
        """delete() should return False for a missing ID."""
        assert store.delete(999) is False


class TestClear:
    """Tests for TodoStore.clear()."""

    def test_clear_removes_all_and_resets_counter(self, store: TodoStore) -> None:
        """clear() should empty the store and reset the ID counter."""
        store.create(title="A")
        store.create(title="B")
        store.clear()
        assert store.get_all() == []
        # Next ID should be 1 again
        todo = store.create(title="C")
        assert todo["id"] == 1
