"""Tests for the in-memory TodoStore in storage.py."""

from __future__ import annotations

import pytest

from storage import TodoStore


@pytest.fixture()
def store() -> TodoStore:
    """Provide a fresh TodoStore for each test."""
    return TodoStore()


class TestAdd:
    """Tests for TodoStore.add."""

    def test_add_returns_todo_with_id(self, store: TodoStore) -> None:
        """Adding a todo returns a dict with an auto-incremented ID."""
        todo = store.add(title="First")
        assert todo["id"] == 1
        assert todo["title"] == "First"
        assert todo["description"] is None
        assert todo["completed"] is False
        assert "created_at" in todo

    def test_add_increments_id(self, store: TodoStore) -> None:
        """Each new todo gets a unique, incrementing ID."""
        t1 = store.add(title="A")
        t2 = store.add(title="B")
        assert t2["id"] == t1["id"] + 1

    def test_add_with_description_and_completed(self, store: TodoStore) -> None:
        """Optional fields are stored when provided."""
        todo = store.add(title="X", description="detail", completed=True)
        assert todo["description"] == "detail"
        assert todo["completed"] is True


class TestGet:
    """Tests for TodoStore.get."""

    def test_get_existing(self, store: TodoStore) -> None:
        """Retrieving an existing todo returns its data."""
        created = store.add(title="Find me")
        found = store.get(created["id"])
        assert found is not None
        assert found["title"] == "Find me"

    def test_get_nonexistent_returns_none(self, store: TodoStore) -> None:
        """Retrieving a missing ID returns None."""
        assert store.get(999) is None

    def test_get_returns_copy(self, store: TodoStore) -> None:
        """Returned dict is a copy — mutating it doesn't affect the store."""
        created = store.add(title="Original")
        fetched = store.get(created["id"])
        assert fetched is not None
        fetched["title"] = "Mutated"
        assert store.get(created["id"])["title"] == "Original"  # type: ignore[index]


class TestGetAll:
    """Tests for TodoStore.get_all."""

    def test_get_all_empty(self, store: TodoStore) -> None:
        """An empty store returns an empty list."""
        assert store.get_all() == []

    def test_get_all_returns_all(self, store: TodoStore) -> None:
        """All added items appear in get_all results."""
        store.add(title="A")
        store.add(title="B")
        all_todos = store.get_all()
        assert len(all_todos) == 2


class TestUpdate:
    """Tests for TodoStore.update."""

    def test_update_title(self, store: TodoStore) -> None:
        """Updating only the title leaves other fields unchanged."""
        created = store.add(title="Old")
        updated = store.update(created["id"], title="New")
        assert updated is not None
        assert updated["title"] == "New"
        assert updated["completed"] is False

    def test_update_completed(self, store: TodoStore) -> None:
        """Updating the completed flag works."""
        created = store.add(title="Task")
        updated = store.update(created["id"], completed=True)
        assert updated is not None
        assert updated["completed"] is True

    def test_update_nonexistent_returns_none(self, store: TodoStore) -> None:
        """Updating a missing ID returns None."""
        assert store.update(999, title="Nope") is None

    def test_update_no_fields_is_noop(self, store: TodoStore) -> None:
        """Calling update with no optional fields returns the item unchanged."""
        created = store.add(title="Same")
        updated = store.update(created["id"])
        assert updated is not None
        assert updated["title"] == "Same"


class TestDelete:
    """Tests for TodoStore.delete."""

    def test_delete_existing(self, store: TodoStore) -> None:
        """Deleting an existing todo returns True and removes it."""
        created = store.add(title="Bye")
        assert store.delete(created["id"]) is True
        assert store.get(created["id"]) is None

    def test_delete_nonexistent_returns_false(self, store: TodoStore) -> None:
        """Deleting a missing ID returns False."""
        assert store.delete(999) is False


class TestReset:
    """Tests for TodoStore.reset."""

    def test_reset_clears_all(self, store: TodoStore) -> None:
        """Reset empties the store and resets the ID counter."""
        store.add(title="A")
        store.add(title="B")
        store.reset()
        assert store.get_all() == []
        new = store.add(title="C")
        assert new["id"] == 1
