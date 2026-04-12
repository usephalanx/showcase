"""Tests for the in-memory TodoStore (storage.py).

Covers: add, get, get_all, update, delete, reset, edge cases.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from storage import TodoStore


class TestTodoStoreAdd:
    """Tests for TodoStore.add()."""

    def test_add_returns_dict_with_required_keys(self, todo_store: TodoStore) -> None:
        """Adding a todo returns a dict containing id, title, completed, created_at."""
        result = todo_store.add(title="Test todo")
        assert isinstance(result, dict)
        assert "id" in result
        assert "title" in result
        assert "completed" in result
        assert "created_at" in result

    def test_add_assigns_sequential_ids(self, todo_store: TodoStore) -> None:
        """IDs are auto-incremented starting from 1."""
        t1 = todo_store.add(title="First")
        t2 = todo_store.add(title="Second")
        assert t1["id"] == 1
        assert t2["id"] == 2

    def test_add_sets_title_correctly(self, todo_store: TodoStore) -> None:
        """The returned todo has the correct title."""
        result = todo_store.add(title="My Task")
        assert result["title"] == "My Task"

    def test_add_default_completed_is_false(self, todo_store: TodoStore) -> None:
        """Completed defaults to False when not specified."""
        result = todo_store.add(title="Task")
        assert result["completed"] is False

    def test_add_with_completed_true(self, todo_store: TodoStore) -> None:
        """Can create a todo that is already completed."""
        result = todo_store.add(title="Done task", completed=True)
        assert result["completed"] is True

    def test_add_with_description(self, todo_store: TodoStore) -> None:
        """A description is stored when provided."""
        result = todo_store.add(title="Task", description="Details here")
        assert result["description"] == "Details here"

    def test_add_without_description_defaults_to_none(
        self, todo_store: TodoStore
    ) -> None:
        """Description defaults to None."""
        result = todo_store.add(title="Task")
        assert result["description"] is None

    def test_add_sets_created_at_iso_format(self, todo_store: TodoStore) -> None:
        """created_at is a valid ISO 8601 string."""
        from datetime import datetime

        result = todo_store.add(title="Task")
        # Should not raise
        datetime.fromisoformat(result["created_at"])


class TestTodoStoreGet:
    """Tests for TodoStore.get()."""

    def test_get_existing_todo(self, todo_store: TodoStore) -> None:
        """Retrieving an existing todo returns the correct dict."""
        added = todo_store.add(title="Fetch me")
        fetched = todo_store.get(added["id"])
        assert fetched is not None
        assert fetched["title"] == "Fetch me"
        assert fetched["id"] == added["id"]

    def test_get_returns_copy(self, todo_store: TodoStore) -> None:
        """get() returns a copy, not the internal object."""
        added = todo_store.add(title="Original")
        fetched = todo_store.get(added["id"])
        assert fetched is not None
        fetched["title"] = "Modified"
        refetched = todo_store.get(added["id"])
        assert refetched is not None
        assert refetched["title"] == "Original"

    def test_get_nonexistent_returns_none(self, todo_store: TodoStore) -> None:
        """Getting a non-existent ID returns None."""
        result = todo_store.get(999)
        assert result is None


class TestTodoStoreGetAll:
    """Tests for TodoStore.get_all()."""

    def test_get_all_empty_store(self, todo_store: TodoStore) -> None:
        """An empty store returns an empty list."""
        assert todo_store.get_all() == []

    def test_get_all_returns_all_items(self, populated_store: TodoStore) -> None:
        """get_all returns every added item."""
        todos = populated_store.get_all()
        assert len(todos) == 3

    def test_get_all_returns_list_of_dicts(self, populated_store: TodoStore) -> None:
        """Each item in the list is a dictionary."""
        todos = populated_store.get_all()
        for t in todos:
            assert isinstance(t, dict)


class TestTodoStoreUpdate:
    """Tests for TodoStore.update()."""

    def test_update_title(self, todo_store: TodoStore) -> None:
        """Updating the title changes it."""
        added = todo_store.add(title="Old title")
        updated = todo_store.update(added["id"], title="New title")
        assert updated is not None
        assert updated["title"] == "New title"

    def test_update_completed(self, todo_store: TodoStore) -> None:
        """Toggling completed status works."""
        added = todo_store.add(title="Task", completed=False)
        updated = todo_store.update(added["id"], completed=True)
        assert updated is not None
        assert updated["completed"] is True

    def test_update_description(self, todo_store: TodoStore) -> None:
        """Updating description changes it."""
        added = todo_store.add(title="Task")
        updated = todo_store.update(added["id"], description="New desc")
        assert updated is not None
        assert updated["description"] == "New desc"

    def test_update_nonexistent_returns_none(self, todo_store: TodoStore) -> None:
        """Updating a non-existent todo returns None."""
        result = todo_store.update(999, title="Nope")
        assert result is None

    def test_update_preserves_unchanged_fields(self, todo_store: TodoStore) -> None:
        """Fields not passed to update remain unchanged."""
        added = todo_store.add(title="Keep", description="Keep this")
        updated = todo_store.update(added["id"], completed=True)
        assert updated is not None
        assert updated["title"] == "Keep"
        assert updated["description"] == "Keep this"


class TestTodoStoreDelete:
    """Tests for TodoStore.delete()."""

    def test_delete_existing_todo(self, todo_store: TodoStore) -> None:
        """Deleting an existing todo returns True."""
        added = todo_store.add(title="Delete me")
        assert todo_store.delete(added["id"]) is True

    def test_delete_removes_from_store(self, todo_store: TodoStore) -> None:
        """After deletion the todo is no longer retrievable."""
        added = todo_store.add(title="Delete me")
        todo_store.delete(added["id"])
        assert todo_store.get(added["id"]) is None

    def test_delete_nonexistent_returns_false(self, todo_store: TodoStore) -> None:
        """Deleting a non-existent todo returns False."""
        assert todo_store.delete(999) is False

    def test_delete_does_not_affect_other_todos(self, todo_store: TodoStore) -> None:
        """Deleting one todo leaves others intact."""
        t1 = todo_store.add(title="Stay")
        t2 = todo_store.add(title="Go away")
        todo_store.delete(t2["id"])
        assert todo_store.get(t1["id"]) is not None
        assert len(todo_store.get_all()) == 1


class TestTodoStoreReset:
    """Tests for TodoStore.reset()."""

    def test_reset_clears_all_todos(self, populated_store: TodoStore) -> None:
        """After reset the store is empty."""
        populated_store.reset()
        assert populated_store.get_all() == []

    def test_reset_resets_counter(self, populated_store: TodoStore) -> None:
        """After reset, new IDs start from 1 again."""
        populated_store.reset()
        new_todo = populated_store.add(title="Fresh")
        assert new_todo["id"] == 1
