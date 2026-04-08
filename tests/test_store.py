"""Unit tests for the in-memory store modules (storage.py and store.py)."""

from __future__ import annotations

import store as functional_store
from storage import TodoStore


# ---------------------------------------------------------------------------
# TodoStore (class-based, storage.py)
# ---------------------------------------------------------------------------


class TestTodoStore:
    """Tests for the class-based TodoStore."""

    def setup_method(self) -> None:
        """Create a fresh store before every test."""
        self.store = TodoStore()

    def test_add_returns_complete_todo(self) -> None:
        """add() should return a dict with all expected keys."""
        todo = self.store.add(title="First")
        assert todo["id"] == 1
        assert todo["title"] == "First"
        assert todo["description"] is None
        assert todo["completed"] is False
        assert "created_at" in todo

    def test_auto_increment_ids(self) -> None:
        """Each call to add() should produce a monotonically increasing id."""
        t1 = self.store.add(title="A")
        t2 = self.store.add(title="B")
        assert t2["id"] == t1["id"] + 1

    def test_get_existing(self) -> None:
        """get() should return the correct todo for a valid id."""
        created = self.store.add(title="Find me")
        fetched = self.store.get(created["id"])
        assert fetched is not None
        assert fetched["title"] == "Find me"

    def test_get_nonexistent(self) -> None:
        """get() should return None for an unknown id."""
        assert self.store.get(999) is None

    def test_get_all_empty(self) -> None:
        """get_all() on an empty store should return an empty list."""
        assert self.store.get_all() == []

    def test_get_all_multiple(self) -> None:
        """get_all() should return all added todos."""
        self.store.add(title="A")
        self.store.add(title="B")
        assert len(self.store.get_all()) == 2

    def test_update_partial(self) -> None:
        """update() should only change supplied fields."""
        created = self.store.add(title="Original", description="desc")
        updated = self.store.update(created["id"], completed=True)
        assert updated is not None
        assert updated["title"] == "Original"
        assert updated["description"] == "desc"
        assert updated["completed"] is True

    def test_update_nonexistent(self) -> None:
        """update() on a missing id should return None."""
        assert self.store.update(999, title="Nope") is None

    def test_delete_existing(self) -> None:
        """delete() should return True and remove the todo."""
        created = self.store.add(title="Delete me")
        assert self.store.delete(created["id"]) is True
        assert self.store.get(created["id"]) is None

    def test_delete_nonexistent(self) -> None:
        """delete() on a missing id should return False."""
        assert self.store.delete(999) is False

    def test_reset(self) -> None:
        """reset() should clear all todos and reset the counter."""
        self.store.add(title="A")
        self.store.add(title="B")
        self.store.reset()
        assert self.store.get_all() == []
        new_todo = self.store.add(title="C")
        assert new_todo["id"] == 1


# ---------------------------------------------------------------------------
# Functional store (store.py)
# ---------------------------------------------------------------------------


class TestFunctionalStore:
    """Tests for the module-level functional store."""

    def setup_method(self) -> None:
        """Reset module-level state before every test."""
        functional_store.reset_store()

    def test_create_todo(self) -> None:
        """create_todo() should return a complete todo dict."""
        todo = functional_store.create_todo({"title": "Test"})
        assert todo["id"] == 1
        assert todo["title"] == "Test"
        assert todo["completed"] is False
        assert todo["description"] is None
        assert "created_at" in todo

    def test_get_all_todos(self) -> None:
        """get_all_todos() should return all created todos."""
        functional_store.create_todo({"title": "A"})
        functional_store.create_todo({"title": "B"})
        assert len(functional_store.get_all_todos()) == 2

    def test_get_todo_by_id(self) -> None:
        """get_todo_by_id() should retrieve the correct todo."""
        created = functional_store.create_todo({"title": "Find"})
        fetched = functional_store.get_todo_by_id(created["id"])
        assert fetched is not None
        assert fetched["title"] == "Find"

    def test_get_todo_by_id_missing(self) -> None:
        """get_todo_by_id() should return None for unknown id."""
        assert functional_store.get_todo_by_id(999) is None

    def test_update_todo(self) -> None:
        """update_todo() should partially update the todo."""
        created = functional_store.create_todo({"title": "Old"})
        updated = functional_store.update_todo(
            created["id"], {"title": "New", "completed": True}
        )
        assert updated is not None
        assert updated["title"] == "New"
        assert updated["completed"] is True

    def test_update_todo_missing(self) -> None:
        """update_todo() should return None for unknown id."""
        assert functional_store.update_todo(999, {"title": "X"}) is None

    def test_delete_todo(self) -> None:
        """delete_todo() should remove the todo and return True."""
        created = functional_store.create_todo({"title": "Delete"})
        assert functional_store.delete_todo(created["id"]) is True
        assert functional_store.get_todo_by_id(created["id"]) is None

    def test_delete_todo_missing(self) -> None:
        """delete_todo() should return False for unknown id."""
        assert functional_store.delete_todo(999) is False

    def test_reset_store(self) -> None:
        """reset_store() should clear all data and reset the counter."""
        functional_store.create_todo({"title": "X"})
        functional_store.reset_store()
        assert functional_store.get_all_todos() == []
        new = functional_store.create_todo({"title": "Y"})
        assert new["id"] == 1
