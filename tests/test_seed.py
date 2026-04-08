"""Tests for the seed data module.

Verifies that :func:`app.seed.seed_todos` correctly populates an empty
storage instance and is idempotent when the store already contains data.
"""

from __future__ import annotations

from app.seed import SAMPLE_TODOS, seed_todos
from app.storage import TodoStorage


def _fresh_storage() -> TodoStorage:
    """Return a new, empty :class:`TodoStorage` instance."""
    return TodoStorage()


class TestSeedTodos:
    """Unit tests for :func:`seed_todos`."""

    def test_seed_populates_empty_store(self) -> None:
        """Seeding an empty store should create all sample todos."""
        store = _fresh_storage()
        created = seed_todos(store)

        assert len(created) == len(SAMPLE_TODOS)
        assert len(store.get_all()) == len(SAMPLE_TODOS)

    def test_seed_returns_created_todos(self) -> None:
        """Each returned dict should have an id, title, description, and completed flag."""
        store = _fresh_storage()
        created = seed_todos(store)

        for todo in created:
            assert "id" in todo
            assert "title" in todo
            assert "description" in todo
            assert "completed" in todo
            assert todo["completed"] is False

    def test_seed_titles_match_sample_data(self) -> None:
        """Seeded todo titles should match the SAMPLE_TODOS definitions."""
        store = _fresh_storage()
        created = seed_todos(store)

        expected_titles = {t["title"] for t in SAMPLE_TODOS}
        actual_titles = {t["title"] for t in created}
        assert actual_titles == expected_titles

    def test_seed_is_idempotent(self) -> None:
        """Calling seed_todos twice should not duplicate items."""
        store = _fresh_storage()
        first = seed_todos(store)
        second = seed_todos(store)

        assert len(first) == len(SAMPLE_TODOS)
        assert second == []
        assert len(store.get_all()) == len(SAMPLE_TODOS)

    def test_seed_skips_nonempty_store(self) -> None:
        """If the store already has data, seed_todos should not add anything."""
        store = _fresh_storage()
        store.create({"title": "Existing item"})

        created = seed_todos(store)

        assert created == []
        assert len(store.get_all()) == 1

    def test_seed_assigns_sequential_ids(self) -> None:
        """Auto-generated ids should be sequential starting from 1."""
        store = _fresh_storage()
        created = seed_todos(store)

        ids = [t["id"] for t in created]
        assert ids == list(range(1, len(SAMPLE_TODOS) + 1))

    def test_seed_descriptions_match_sample_data(self) -> None:
        """Seeded todo descriptions should match the SAMPLE_TODOS definitions."""
        store = _fresh_storage()
        created = seed_todos(store)

        expected_descriptions = {t["description"] for t in SAMPLE_TODOS}
        actual_descriptions = {t["description"] for t in created}
        assert actual_descriptions == expected_descriptions
