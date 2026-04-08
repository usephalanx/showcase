"""In-memory storage backend for todo items.

Uses a module-level dictionary and an auto-incrementing counter.
Data is **not** persistent and resets when the process restarts.
"""

from __future__ import annotations

from typing import Dict, List, Optional


class TodoStorage:
    """Simple in-memory store for todo items.

    Attributes:
        _todos: Mapping of todo id to todo data dictionaries.
        _counter: Auto-incrementing id counter.
    """

    def __init__(self) -> None:
        """Initialise an empty store."""
        self._todos: Dict[int, dict] = {}
        self._counter: int = 0

    # -- helpers -------------------------------------------------------------

    def _next_id(self) -> int:
        """Return the next unique id and increment the counter."""
        self._counter += 1
        return self._counter

    # -- public API ----------------------------------------------------------

    def get_all(self) -> List[dict]:
        """Return a list of all todo items."""
        return list(self._todos.values())

    def get_by_id(self, todo_id: int) -> Optional[dict]:
        """Return a single todo by *todo_id*, or ``None`` if not found."""
        return self._todos.get(todo_id)

    def create(self, data: dict) -> dict:
        """Create a new todo from *data* and return it with an assigned id.

        *data* should contain ``title`` and optionally ``description`` keys.
        The ``id`` is auto-generated and ``completed`` defaults to ``False``.

        Args:
            data: Dictionary with at least a ``title`` key.

        Returns:
            The newly created todo dictionary including its assigned ``id``.
        """
        todo_id = self._next_id()
        todo: dict = {
            "id": todo_id,
            "title": data["title"],
            "description": data.get("description", ""),
            "completed": False,
        }
        self._todos[todo_id] = todo
        return todo

    def update(self, todo_id: int, data: dict) -> Optional[dict]:
        """Update an existing todo with the non-``None`` values in *data*.

        Returns the updated todo dict, or ``None`` if *todo_id* does not exist.

        Args:
            todo_id: The id of the todo to update.
            data: Dictionary of fields to update.  ``None`` values are ignored.

        Returns:
            The updated todo dictionary, or ``None`` if not found.
        """
        todo = self._todos.get(todo_id)
        if todo is None:
            return None

        for key in ("title", "description", "completed"):
            if key in data and data[key] is not None:
                todo[key] = data[key]

        return todo

    def delete(self, todo_id: int) -> bool:
        """Delete a todo by *todo_id*.  Returns ``True`` if it existed.

        Args:
            todo_id: The id of the todo to delete.

        Returns:
            ``True`` if the todo was found and deleted, ``False`` otherwise.
        """
        if todo_id in self._todos:
            del self._todos[todo_id]
            return True
        return False

    def clear(self) -> None:
        """Remove all todos and reset the counter.  Useful for tests."""
        self._todos.clear()
        self._counter = 0


# Module-level singleton used by the route handlers.
storage = TodoStorage()
