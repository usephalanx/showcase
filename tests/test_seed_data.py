"""Tests verifying that the module-level storage instance contains seed data."""

from __future__ import annotations

from app.models import TodoCreate, TodoUpdate
from app.storage import TodoStorage, _build_seeded_storage, storage


def test_module_storage_is_seeded() -> None:
    """The module-level storage instance must contain seed todos on import."""
    todos = storage.get_all()
    assert len(todos) > 0, "Module-level storage should not be empty"


def test_seed_count() -> None:
    """The seeded storage must contain exactly 3 demo items."""
    store = _build_seeded_storage()
    assert len(store.get_all()) == 3


def test_seed_titles() -> None:
    """Verify the titles of the three seed items."""
    store = _build_seeded_storage()
    titles = {todo.title for todo in store.get_all()}
    assert "Buy groceries" in titles
    assert "Read FastAPI documentation" in titles
    assert "Write unit tests" in titles


def test_seed_has_completed_item() -> None:
    """At least one seed item should be marked as completed."""
    store = _build_seeded_storage()
    completed = [todo for todo in store.get_all() if todo.completed]
    assert len(completed) >= 1, "Expected at least one completed seed todo"


def test_seed_ids_are_sequential() -> None:
    """Seed item IDs should be 1, 2, 3."""
    store = _build_seeded_storage()
    ids = sorted(todo.id for todo in store.get_all())
    assert ids == [1, 2, 3]


def test_seed_descriptions_populated() -> None:
    """All seed items should have non-None descriptions."""
    store = _build_seeded_storage()
    for todo in store.get_all():
        assert todo.description is not None, (
            f"Seed todo '{todo.title}' is missing a description"
        )


def test_fresh_storage_is_empty() -> None:
    """A freshly constructed TodoStorage (without seeding) must be empty."""
    store = TodoStorage()
    assert len(store.get_all()) == 0


def test_seed_next_id_continues_after_seeds() -> None:
    """Creating a new item after seeding must use id=4."""
    store = _build_seeded_storage()
    new_todo = store.create(TodoCreate(title="Fourth item"))
    assert new_todo.id == 4
