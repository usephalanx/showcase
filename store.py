"""Module-level functional interface to in-memory Todo storage.

Wraps a module-level ``dict`` and auto-incrementing counter, exposing
plain functions for CRUD operations.  This complements the class-based
``TodoStore`` in ``storage.py`` and serves as the store layer described
in the project specification.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Dict, List, Optional

# ---------------------------------------------------------------------------
# Module-level state
# ---------------------------------------------------------------------------

todos: Dict[int, dict] = {}
_counter: int = 0


# ---------------------------------------------------------------------------
# CRUD helpers
# ---------------------------------------------------------------------------


def create_todo(todo_data: dict) -> dict:
    """Create a new todo item and return its full representation.

    ``todo_data`` should contain at least a ``title`` key.  Optional keys:
    ``description`` (defaults to ``None``) and ``completed`` (defaults to
    ``False``).

    Args:
        todo_data: Dictionary with the fields for the new todo.

    Returns:
        A dictionary representing the newly created todo, including the
        auto-generated ``id`` and ``created_at`` timestamp.
    """
    global _counter  # noqa: PLW0603
    _counter += 1
    todo_id = _counter
    now = datetime.now(timezone.utc).isoformat()
    todo: dict = {
        "id": todo_id,
        "title": todo_data["title"],
        "description": todo_data.get("description"),
        "completed": todo_data.get("completed", False),
        "created_at": now,
    }
    todos[todo_id] = todo
    return dict(todo)


def get_all_todos() -> List[dict]:
    """Return a list of all stored todo items.

    Returns:
        A list of todo dictionaries (copies).
    """
    return [dict(t) for t in todos.values()]


def get_todo_by_id(todo_id: int) -> Optional[dict]:
    """Retrieve a single todo by its ID.

    Args:
        todo_id: The integer ID of the todo.

    Returns:
        A copy of the todo dict, or ``None`` if not found.
    """
    todo = todos.get(todo_id)
    if todo is None:
        return None
    return dict(todo)


def update_todo(todo_id: int, update_data: dict) -> Optional[dict]:
    """Partially update an existing todo.

    Only keys present in *update_data* whose values are not ``None`` are
    applied.

    Args:
        todo_id: The integer ID of the todo to update.
        update_data: Dictionary of fields to change.

    Returns:
        The updated todo dict, or ``None`` if the ID does not exist.
    """
    todo = todos.get(todo_id)
    if todo is None:
        return None
    for key in ("title", "description", "completed"):
        if key in update_data and update_data[key] is not None:
            todo[key] = update_data[key]
    return dict(todo)


def delete_todo(todo_id: int) -> bool:
    """Remove a todo by its ID.

    Args:
        todo_id: The integer ID of the todo to delete.

    Returns:
        ``True`` if the todo was found and deleted, ``False`` otherwise.
    """
    if todo_id in todos:
        del todos[todo_id]
        return True
    return False


def reset_store() -> None:
    """Clear all todos and reset the auto-increment counter.

    Intended for use in test fixtures to guarantee a clean state between
    test cases.
    """
    global _counter  # noqa: PLW0603
    todos.clear()
    _counter = 0
