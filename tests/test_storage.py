"""Unit tests for the in-memory TodoStore."""

from __future__ import annotations

import pytest

from storage import TodoStore


@pytest.fixture()
def store() -> TodoStore:
    """Return a fresh TodoStore instance."""
    return TodoStore()


class TestAdd:
    """Tests for TodoStore.add."""

    def test_add_returns_dict(self, store: TodoStore) -> None:
        """add() should return a dictionary."""
        result = store.add(title="Test")
        assert isinstance(result, dict)

    def test_add_assigns_id(self, store: TodoStore) -> None:
        """add() should assign an auto-incrementing id."""
        first = store.add(title="First")
        second = store.add(title="Second")
        assert first["id"] == 1
        assert second["id"] == 2

    def test_add_stores_fields(self, store: TodoStore) -> None:
        """add() should store title, description, completed, and created_at."""
        result = store.add(title="T", description="D", completed=True)
        assert result["title"] == "T"
        assert result["description"] == "D"
        assert result["completed"] is True
        assert "created_at" in result

    def test_add_defaults(self, store: TodoStore) -> None:
        """add() should default description to None and completed to False."""
        result = store.add(title="X")
        assert result["description"] is None
        assert result["completed"] is False


class TestGetAll:
    """Tests for TodoStore.get_all."""

    def test_empty_store(self, store: TodoStore) -> None:
        """get_all() should return an empty list on a fresh store."""
        assert store.get_all() == []

    def test_returns_all(self, store: TodoStore) -> None:
        """get_all() should return every added todo."""
        store.add(title="A")
        store.add(title="B")
        assert len(store.get_all()) == 2


class TestGet:
    """Tests for TodoStore.get."""

    def test_get_existing(self, store: TodoStore) -> None:
        """get() should return the todo when it exists."""
        added = store.add(title="Find me")
        found = store.get(added["id"])
        assert found is not None
        assert found["title"] == "Find me"

    def test_get_missing(self, store: TodoStore) -> None:
        """get() should return None for a non-existent id."""
        assert store.get(42) is None


class TestUpdate:
    """Tests for TodoStore.update."""

    def test_update_title(self, store: TodoStore) -> None:
        """update() should change the title."""
        added = store.add(title="Old")
        updated = store.update(added["id"], title="New")
        assert updated is not None
        assert updated["title"] == "New"

    def test_update_completed(self, store: TodoStore) -> None:
        """update() should change the completed flag."""
        added = store.add(title="Task")
        updated = store.update(added["id"], completed=True)
        assert updated is not None
        assert updated["completed"] is True

    def test_update_missing(self, store: TodoStore) -> None:
        """update() should return None for a non-existent id."""
        assert store.update(99, title="X") is None

    def test_partial_update_leaves_other_fields(self, store: TodoStore) -> None:
        """update() should only change fields that are provided."""
        added = store.add(title="Keep", description="Me")
        updated = store.update(added["id"], completed=True)
        assert updated is not None
        assert updated["title"] == "Keep"
        assert updated["description"] == "Me"


class TestDelete:
    """Tests for TodoStore.delete."""

    def test_delete_existing(self, store: TodoStore) -> None:
        """delete() should return True and remove the todo."""
        added = store.add(title="Bye")
        assert store.delete(added["id"]) is True
        assert store.get(added["id"]) is None

    def test_delete_missing(self, store: TodoStore) -> None:
        """delete() should return False for a non-existent id."""
        assert store.delete(99) is False


class TestReset:
    """Tests for TodoStore.reset."""

    def test_reset_clears_store(self, store: TodoStore) -> None:
        """reset() should remove all todos."""
        store.add(title="A")
        store.add(title="B")
        store.reset()
        assert store.get_all() == []

    def test_reset_resets_counter(self, store: TodoStore) -> None:
        """reset() should reset the ID counter so next add starts at 1."""
        store.add(title="A")
        store.reset()
        new = store.add(title="B")
        assert new["id"] == 1
