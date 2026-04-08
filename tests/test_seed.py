"""Tests for the seed-data module.

Verifies that :func:`app.seed.seed_todos` correctly populates an empty
:class:`~app.storage.TodoStorage` and is idempotent when called
repeatedly.
"""

from __future__ import annotations

from app.seed import SAMPLE_TODOS, seed_todos
from app.storage import TodoStorage


def _fresh_storage() -> TodoStorage:
    """Return a new, empty TodoStorage instance."""
    return TodoStorage()


# -------------------------------------------------------------------
# Tests
# -------------------------------------------------------------------


def test_seed_populates_empty_store() -> None:
    """seed_todos should insert the sample items into an empty store."""
    store = _fresh_storage()
    created = seed_todos(store)

    assert len(created) == len(SAMPLE_TODOS)
    assert len(store.get_all()) == len(SAMPLE_TODOS)

    # Verify each created item has an id and the expected title
    titles = {item["title"] for item in created}
    expected_titles = {item["title"] for item in SAMPLE_TODOS}
    assert titles == expected_titles


def test_seed_items_have_correct_defaults() -> None:
    """Seeded items should have completed=False and a description."""
    store = _fresh_storage()
    created = seed_todos(store)

    for item in created:
        assert "id" in item
        assert isinstance(item["id"], int)
        assert item["completed"] is False
        assert isinstance(item["description"], str)


def test_seed_skips_non_empty_store() -> None:
    """seed_todos must be idempotent — no-op when the store has data."""
    store = _fresh_storage()

    first_run = seed_todos(store)
    assert len(first_run) == len(SAMPLE_TODOS)

    second_run = seed_todos(store)
    assert second_run == []
    # Count must not have grown
    assert len(store.get_all()) == len(SAMPLE_TODOS)


def test_seed_after_clear_repopulates() -> None:
    """After clearing the store, seed_todos should insert items again."""
    store = _fresh_storage()

    seed_todos(store)
    assert len(store.get_all()) == len(SAMPLE_TODOS)

    store.clear()
    assert len(store.get_all()) == 0

    created = seed_todos(store)
    assert len(created) == len(SAMPLE_TODOS)
    assert len(store.get_all()) == len(SAMPLE_TODOS)
