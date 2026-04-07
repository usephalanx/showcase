"""Tests for app.storage in-memory TodoStorage."""

from __future__ import annotations

import pytest

from app.models import TodoCreate, TodoUpdate
from app.storage import TodoStorage


@pytest.fixture()
def store() -> TodoStorage:
    """Return a fresh TodoStorage instance for each test."""
    return TodoStorage()


# ---------------------------------------------------------------------------
# get_all
# ---------------------------------------------------------------------------


class TestGetAll:
    """Tests for TodoStorage.get_all."""

    def test_empty_store_returns_empty_list(self, store: TodoStorage) -> None:
        """get_all returns an empty list when no items exist."""
        assert store.get_all() == []

    def test_returns_all_created_items(self, store: TodoStorage) -> None:
        """get_all returns every item that has been created."""
        store.create(TodoCreate(title="First"))
        store.create(TodoCreate(title="Second"))
        result = store.get_all()
        assert len(result) == 2
        titles = {item.title for item in result}
        assert titles == {"First", "Second"}


# ---------------------------------------------------------------------------
# get_by_id
# ---------------------------------------------------------------------------


class TestGetById:
    """Tests for TodoStorage.get_by_id."""

    def test_returns_none_for_nonexistent_id(self, store: TodoStorage) -> None:
        """get_by_id returns None when the ID does not exist."""
        assert store.get_by_id(999) is None

    def test_returns_correct_item(self, store: TodoStorage) -> None:
        """get_by_id returns the item matching the given ID."""
        created = store.create(TodoCreate(title="Test"))
        fetched = store.get_by_id(created.id)
        assert fetched is not None
        assert fetched.id == created.id
        assert fetched.title == "Test"


# ---------------------------------------------------------------------------
# create
# ---------------------------------------------------------------------------


class TestCreate:
    """Tests for TodoStorage.create."""

    def test_create_assigns_incrementing_ids(self, store: TodoStorage) -> None:
        """Each created item receives a unique, incrementing ID."""
        first = store.create(TodoCreate(title="A"))
        second = store.create(TodoCreate(title="B"))
        assert first.id == 1
        assert second.id == 2

    def test_create_defaults_completed_to_false(self, store: TodoStorage) -> None:
        """Newly created items have completed=False."""
        item = store.create(TodoCreate(title="Test"))
        assert item.completed is False

    def test_create_stores_description(self, store: TodoStorage) -> None:
        """The description field is persisted when provided."""
        item = store.create(
            TodoCreate(title="Test", description="Details here")
        )
        assert item.description == "Details here"

    def test_create_description_defaults_to_none(self, store: TodoStorage) -> None:
        """The description field defaults to None when omitted."""
        item = store.create(TodoCreate(title="Test"))
        assert item.description is None


# ---------------------------------------------------------------------------
# update
# ---------------------------------------------------------------------------


class TestUpdate:
    """Tests for TodoStorage.update."""

    def test_update_nonexistent_returns_none(self, store: TodoStorage) -> None:
        """update returns None when the ID does not exist."""
        result = store.update(999, TodoUpdate(title="Nope"))
        assert result is None

    def test_update_title(self, store: TodoStorage) -> None:
        """update modifies the title when provided."""
        created = store.create(TodoCreate(title="Old"))
        updated = store.update(created.id, TodoUpdate(title="New"))
        assert updated is not None
        assert updated.title == "New"

    def test_update_completed(self, store: TodoStorage) -> None:
        """update modifies the completed status when provided."""
        created = store.create(TodoCreate(title="Task"))
        updated = store.update(created.id, TodoUpdate(completed=True))
        assert updated is not None
        assert updated.completed is True

    def test_update_description(self, store: TodoStorage) -> None:
        """update modifies the description when provided."""
        created = store.create(TodoCreate(title="Task"))
        updated = store.update(created.id, TodoUpdate(description="Added"))
        assert updated is not None
        assert updated.description == "Added"

    def test_update_preserves_unset_fields(self, store: TodoStorage) -> None:
        """Fields not included in the update payload remain unchanged."""
        created = store.create(
            TodoCreate(title="Keep me", description="Keep this too")
        )
        updated = store.update(created.id, TodoUpdate(completed=True))
        assert updated is not None
        assert updated.title == "Keep me"
        assert updated.description == "Keep this too"
        assert updated.completed is True

    def test_update_multiple_fields_at_once(self, store: TodoStorage) -> None:
        """Multiple fields can be updated in a single call."""
        created = store.create(TodoCreate(title="Original"))
        updated = store.update(
            created.id,
            TodoUpdate(title="Changed", description="New desc", completed=True),
        )
        assert updated is not None
        assert updated.title == "Changed"
        assert updated.description == "New desc"
        assert updated.completed is True


# ---------------------------------------------------------------------------
# delete
# ---------------------------------------------------------------------------


class TestDelete:
    """Tests for TodoStorage.delete."""

    def test_delete_nonexistent_returns_false(self, store: TodoStorage) -> None:
        """delete returns False when the ID does not exist."""
        assert store.delete(999) is False

    def test_delete_existing_returns_true(self, store: TodoStorage) -> None:
        """delete returns True when the item is successfully removed."""
        created = store.create(TodoCreate(title="Doomed"))
        assert store.delete(created.id) is True

    def test_delete_removes_item_from_store(self, store: TodoStorage) -> None:
        """After deletion the item is no longer retrievable."""
        created = store.create(TodoCreate(title="Gone"))
        store.delete(created.id)
        assert store.get_by_id(created.id) is None
        assert len(store.get_all()) == 0

    def test_delete_same_id_twice_returns_false(self, store: TodoStorage) -> None:
        """Deleting the same ID a second time returns False."""
        created = store.create(TodoCreate(title="Once"))
        assert store.delete(created.id) is True
        assert store.delete(created.id) is False
