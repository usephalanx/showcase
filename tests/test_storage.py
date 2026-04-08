"""Unit tests for the TodoStore in-memory storage layer."""

from __future__ import annotations

import pytest

from storage import TodoStore


@pytest.fixture()
def store() -> TodoStore:
    """Return a fresh TodoStore instance."""
    return TodoStore()


class TestAdd:
    """Tests for TodoStore.add()."""

    def test_add_returns_dict_with_id(self, store: TodoStore) -> None:
        """Adding a todo should return a dict containing an integer id."""
        todo = store.add(title="Test")
        assert isinstance(todo, dict)
        assert todo["id"] == 1

    def test_add_sets_defaults(self, store: TodoStore) -> None:
        """Default values for description and completed should be applied."""
        todo = store.add(title="Test")
        assert todo["description"] is None
        assert todo["completed"] is False

    def test_add_auto_increments(self, store: TodoStore) -> None:
        """Consecutive adds should produce incrementing IDs."""
        t1 = store.add(title="A")
        t2 = store.add(title="B")
        assert t2["id"] == t1["id"] + 1

    def test_add_with_all_fields(self, store: TodoStore) -> None:
        """All supplied fields should be stored."""
        todo = store.add(title="X", description="Desc", completed=True)
        assert todo["title"] == "X"
        assert todo["description"] == "Desc"
        assert todo["completed"] is True

    def test_add_includes_created_at(self, store: TodoStore) -> None:
        """The returned dict should contain a created_at timestamp."""
        todo = store.add(title="Timestamped")
        assert "created_at" in todo
        assert isinstance(todo["created_at"], str)


class TestGet:
    """Tests for TodoStore.get()."""

    def test_get_existing(self, store: TodoStore) -> None:
        """Getting an existing todo by ID should return its data."""
        added = store.add(title="Find me")
        found = store.get(added["id"])
        assert found is not None
        assert found["title"] == "Find me"

    def test_get_nonexistent_returns_none(self, store: TodoStore) -> None:
        """Getting a non-existent ID should return None."""
        assert store.get(999) is None

    def test_get_returns_copy(self, store: TodoStore) -> None:
        """Modifications to the returned dict should not affect the store."""
        added = store.add(title="Original")
        found = store.get(added["id"])
        assert found is not None
        found["title"] = "Mutated"
        assert store.get(added["id"])["title"] == "Original"  # type: ignore[index]


class TestGetAll:
    """Tests for TodoStore.get_all()."""

    def test_get_all_empty(self, store: TodoStore) -> None:
        """An empty store should return an empty list."""
        assert store.get_all() == []

    def test_get_all_multiple(self, store: TodoStore) -> None:
        """All stored todos should be returned."""
        store.add(title="A")
        store.add(title="B")
        all_todos = store.get_all()
        assert len(all_todos) == 2


class TestUpdate:
    """Tests for TodoStore.update()."""

    def test_update_title(self, store: TodoStore) -> None:
        """Updating the title should change only the title."""
        added = store.add(title="Old")
        updated = store.update(added["id"], title="New")
        assert updated is not None
        assert updated["title"] == "New"
        assert updated["completed"] is False

    def test_update_completed(self, store: TodoStore) -> None:
        """Updating completed should toggle the flag."""
        added = store.add(title="Toggle")
        updated = store.update(added["id"], completed=True)
        assert updated is not None
        assert updated["completed"] is True

    def test_update_description(self, store: TodoStore) -> None:
        """Updating description should set the new value."""
        added = store.add(title="Desc test")
        updated = store.update(added["id"], description="New desc")
        assert updated is not None
        assert updated["description"] == "New desc"

    def test_update_nonexistent_returns_none(self, store: TodoStore) -> None:
        """Updating a non-existent ID should return None."""
        assert store.update(999, title="Nope") is None

    def test_update_none_values_keep_existing(self, store: TodoStore) -> None:
        """Passing None for fields should leave them unchanged."""
        added = store.add(title="Keep", description="Same")
        updated = store.update(added["id"])
        assert updated is not None
        assert updated["title"] == "Keep"
        assert updated["description"] == "Same"


class TestDelete:
    """Tests for TodoStore.delete()."""

    def test_delete_existing(self, store: TodoStore) -> None:
        """Deleting an existing todo should return True."""
        added = store.add(title="Delete me")
        assert store.delete(added["id"]) is True
        assert store.get(added["id"]) is None

    def test_delete_nonexistent_returns_false(self, store: TodoStore) -> None:
        """Deleting a non-existent ID should return False."""
        assert store.delete(999) is False


class TestReset:
    """Tests for TodoStore.reset()."""

    def test_reset_clears_data_and_counter(self, store: TodoStore) -> None:
        """After reset, store should be empty and IDs restart at 1."""
        store.add(title="A")
        store.add(title="B")
        store.reset()
        assert store.get_all() == []
        new = store.add(title="After reset")
        assert new["id"] == 1
