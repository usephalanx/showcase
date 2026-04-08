"""Tests for the in-memory TodoStorage backend."""

from __future__ import annotations

import pytest

from app.storage import TodoStorage


@pytest.fixture()
def store() -> TodoStorage:
    """Return a fresh TodoStorage instance for each test."""
    return TodoStorage()


class TestCreate:
    """Tests for TodoStorage.create."""

    def test_create_returns_todo_with_id(self, store: TodoStorage) -> None:
        """Created todo should have an auto-assigned id."""
        todo = store.create({"title": "Buy milk"})
        assert todo["id"] == 1
        assert todo["title"] == "Buy milk"
        assert todo["description"] == ""
        assert todo["completed"] is False

    def test_create_increments_id(self, store: TodoStorage) -> None:
        """Each created todo should receive a unique incrementing id."""
        t1 = store.create({"title": "First"})
        t2 = store.create({"title": "Second"})
        assert t1["id"] == 1
        assert t2["id"] == 2

    def test_create_with_description(self, store: TodoStorage) -> None:
        """Created todo should preserve an explicit description."""
        todo = store.create({"title": "Task", "description": "Details"})
        assert todo["description"] == "Details"


class TestGetAll:
    """Tests for TodoStorage.get_all."""

    def test_empty_store(self, store: TodoStorage) -> None:
        """An empty store should return an empty list."""
        assert store.get_all() == []

    def test_returns_all_items(self, store: TodoStorage) -> None:
        """get_all should return every created todo."""
        store.create({"title": "A"})
        store.create({"title": "B"})
        assert len(store.get_all()) == 2


class TestGetById:
    """Tests for TodoStorage.get_by_id."""

    def test_existing_id(self, store: TodoStorage) -> None:
        """get_by_id should return the correct todo."""
        created = store.create({"title": "Find me"})
        found = store.get_by_id(created["id"])
        assert found is not None
        assert found["title"] == "Find me"

    def test_missing_id_returns_none(self, store: TodoStorage) -> None:
        """get_by_id should return None for a non-existent id."""
        assert store.get_by_id(999) is None


class TestUpdate:
    """Tests for TodoStorage.update."""

    def test_update_title(self, store: TodoStorage) -> None:
        """Updating the title should change only that field."""
        todo = store.create({"title": "Old"})
        updated = store.update(todo["id"], {"title": "New"})
        assert updated is not None
        assert updated["title"] == "New"
        assert updated["completed"] is False

    def test_update_completed(self, store: TodoStorage) -> None:
        """Updating completed should change only that field."""
        todo = store.create({"title": "Task"})
        updated = store.update(todo["id"], {"completed": True})
        assert updated is not None
        assert updated["completed"] is True
        assert updated["title"] == "Task"

    def test_update_ignores_none_values(self, store: TodoStorage) -> None:
        """Fields set to None should not overwrite existing values."""
        todo = store.create({"title": "Keep", "description": "Original"})
        updated = store.update(todo["id"], {"title": None, "description": None})
        assert updated is not None
        assert updated["title"] == "Keep"
        assert updated["description"] == "Original"

    def test_update_missing_returns_none(self, store: TodoStorage) -> None:
        """Updating a non-existent id should return None."""
        assert store.update(999, {"title": "Nope"}) is None


class TestDelete:
    """Tests for TodoStorage.delete."""

    def test_delete_existing(self, store: TodoStorage) -> None:
        """Deleting an existing todo should return True and remove it."""
        todo = store.create({"title": "Bye"})
        assert store.delete(todo["id"]) is True
        assert store.get_by_id(todo["id"]) is None

    def test_delete_missing_returns_false(self, store: TodoStorage) -> None:
        """Deleting a non-existent id should return False."""
        assert store.delete(999) is False


class TestClear:
    """Tests for TodoStorage.clear."""

    def test_clear_empties_store(self, store: TodoStorage) -> None:
        """clear should remove all todos and reset the counter."""
        store.create({"title": "A"})
        store.create({"title": "B"})
        store.clear()
        assert store.get_all() == []
        # Counter resets, so next id should be 1 again
        todo = store.create({"title": "After clear"})
        assert todo["id"] == 1
