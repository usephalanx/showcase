"""Unit tests for the in-memory TodoStorage backend."""

from __future__ import annotations

import pytest

from app.storage import TodoStorage


@pytest.fixture()
def store() -> TodoStorage:
    """Return a fresh TodoStorage instance for each test."""
    return TodoStorage()


class TestGetAll:
    """Tests for TodoStorage.get_all."""

    def test_empty_store(self, store: TodoStorage) -> None:
        """A new store has no items."""
        assert store.get_all() == []

    def test_returns_all_items(self, store: TodoStorage) -> None:
        """All created items are returned."""
        store.create({"title": "A"})
        store.create({"title": "B"})
        assert len(store.get_all()) == 2


class TestGetById:
    """Tests for TodoStorage.get_by_id."""

    def test_existing_item(self, store: TodoStorage) -> None:
        """Returns the item when it exists."""
        created = store.create({"title": "Find me"})
        result = store.get_by_id(created["id"])
        assert result is not None
        assert result["title"] == "Find me"

    def test_missing_item(self, store: TodoStorage) -> None:
        """Returns None for a non-existent id."""
        assert store.get_by_id(42) is None


class TestCreate:
    """Tests for TodoStorage.create."""

    def test_assigns_id(self, store: TodoStorage) -> None:
        """Created item receives an auto-incremented id."""
        item = store.create({"title": "New"})
        assert item["id"] == 1

    def test_defaults(self, store: TodoStorage) -> None:
        """Description defaults to empty string, completed to False."""
        item = store.create({"title": "Defaults"})
        assert item["description"] == ""
        assert item["completed"] is False

    def test_with_description(self, store: TodoStorage) -> None:
        """Provided description is stored."""
        item = store.create({"title": "Desc", "description": "Detail"})
        assert item["description"] == "Detail"

    def test_sequential_ids(self, store: TodoStorage) -> None:
        """Successive creates produce incrementing ids."""
        a = store.create({"title": "A"})
        b = store.create({"title": "B"})
        assert b["id"] == a["id"] + 1


class TestUpdate:
    """Tests for TodoStorage.update."""

    def test_update_title(self, store: TodoStorage) -> None:
        """Updating title works."""
        item = store.create({"title": "Old"})
        updated = store.update(item["id"], {"title": "New"})
        assert updated is not None
        assert updated["title"] == "New"

    def test_update_completed(self, store: TodoStorage) -> None:
        """Updating completed status works."""
        item = store.create({"title": "Task"})
        updated = store.update(item["id"], {"completed": True})
        assert updated is not None
        assert updated["completed"] is True

    def test_partial_update_leaves_other_fields(self, store: TodoStorage) -> None:
        """Unspecified fields remain unchanged."""
        item = store.create({"title": "Keep", "description": "Detail"})
        updated = store.update(item["id"], {"completed": True})
        assert updated is not None
        assert updated["title"] == "Keep"
        assert updated["description"] == "Detail"

    def test_update_missing_returns_none(self, store: TodoStorage) -> None:
        """Updating a non-existent id returns None."""
        assert store.update(999, {"title": "Nope"}) is None

    def test_update_ignores_none_values(self, store: TodoStorage) -> None:
        """None values in the data dict are not applied."""
        item = store.create({"title": "Original"})
        updated = store.update(item["id"], {"title": None, "completed": True})
        assert updated is not None
        assert updated["title"] == "Original"
        assert updated["completed"] is True


class TestDelete:
    """Tests for TodoStorage.delete."""

    def test_delete_existing(self, store: TodoStorage) -> None:
        """Deleting an existing item returns True."""
        item = store.create({"title": "Bye"})
        assert store.delete(item["id"]) is True
        assert store.get_by_id(item["id"]) is None

    def test_delete_missing(self, store: TodoStorage) -> None:
        """Deleting a non-existent id returns False."""
        assert store.delete(999) is False


class TestClear:
    """Tests for TodoStorage.clear."""

    def test_clear_resets_store(self, store: TodoStorage) -> None:
        """Clear removes all items and resets the counter."""
        store.create({"title": "A"})
        store.create({"title": "B"})
        store.clear()
        assert store.get_all() == []
        new_item = store.create({"title": "C"})
        assert new_item["id"] == 1
