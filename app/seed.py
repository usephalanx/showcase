"""Seed data for the Todo API.

Provides a ``seed_todos`` function that populates the in-memory storage
with a handful of sample todo items.  This is called automatically on
application startup via the FastAPI lifespan so that the API has demo
data available immediately.
"""

from __future__ import annotations

from typing import List

from app.storage import TodoStorage

# ---------------------------------------------------------------------------
# Sample data
# ---------------------------------------------------------------------------

SAMPLE_TODOS: List[dict] = [
    {
        "title": "Buy groceries",
        "description": "Milk, eggs, bread, and coffee",
    },
    {
        "title": "Read a book",
        "description": "Finish reading 'Designing Data-Intensive Applications'",
    },
    {
        "title": "Write unit tests",
        "description": "Add tests for the new todo endpoints",
    },
]


def seed_todos(storage: TodoStorage) -> List[dict]:
    """Populate *storage* with sample todos if it is currently empty.

    This function is idempotent within a single process lifetime: if the
    store already contains items (e.g. from a previous call) it does
    nothing and returns an empty list.

    Args:
        storage: The :class:`~app.storage.TodoStorage` instance to
            populate.

    Returns:
        A list of the newly created todo dictionaries, or an empty list
        if the store was not empty.
    """
    if storage.get_all():
        return []

    created: List[dict] = []
    for todo_data in SAMPLE_TODOS:
        created.append(storage.create(todo_data))
    return created
