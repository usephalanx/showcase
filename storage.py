"""In-memory dictionary-based storage for Todo items.

Provides a simple store backed by a Python dict with an auto-incrementing
integer counter.  Suitable for development and testing — not for production
use (data is lost on process restart and access is not thread-safe under
concurrent writes).
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Dict, List, Optional


class TodoStore:
    """Dict-backed todo storage with auto-incrementing IDs."""

    def __init__(self) -> None:
        """Initialise an empty store."""
        self._todos: Dict[int, dict] = {}
        self._counter: int = 0

    def _next_id(self) -> int:
        """Return the next unique integer ID and increment the counter."""
        self._counter += 1
        return self._counter

    def reset(self) -> None:
        """Clear all stored todos and reset the ID counter.

        Intended for use in test fixtures to ensure a clean state
        between test cases.
        """
        self._todos.clear()
        self._counter = 0

    def add(
        self,
        title: str,
        description: Optional[str] = None,
        completed: bool = False,
    ) -> dict:
        """Create a new todo and return its full representation.

        Args:
            title: The title of the todo item.
            description: An optional longer description.
            completed: Initial completion status (defaults to False).

        Returns:
            A dictionary representing the newly created todo.
        """
        todo_id = self._next_id()
        now = datetime.now(timezone.utc).isoformat()
        todo: dict = {
            "id": todo_id,
            "title": title,
            "description": description,
            "completed": completed,
            "created_at": now,
        }
        self._todos[todo_id] = todo
        return todo

    def get_all(self) -> List[dict]:
        """Return a list of all stored todos.

        Returns:
            A list of todo dictionaries ordered by insertion.
        """
        return list(self._todos.values())

    def get(self, todo_id: int) -> Optional[dict]:
        """Retrieve a single todo by its ID.

        Args:
            todo_id: The unique identifier of the todo.

        Returns:
            The todo dictionary, or ``None`` if not found.
        """
        return self._todos.get(todo_id)

    def update(
        self,
        todo_id: int,
        title: Optional[str] = None,
        description: Optional[str] = None,
        completed: Optional[bool] = None,
    ) -> Optional[dict]:
        """Partially update an existing todo.

        Only non-``None`` arguments are applied to the stored record.

        Args:
            todo_id: The unique identifier of the todo to update.
            title: New title (if provided).
            description: New description (if provided).
            completed: New completion status (if provided).

        Returns:
            The updated todo dictionary, or ``None`` if not found.
        """
        todo = self._todos.get(todo_id)
        if todo is None:
            return None

        if title is not None:
            todo["title"] = title
        if description is not None:
            todo["description"] = description
        if completed is not None:
            todo["completed"] = completed

        return todo

    def delete(self, todo_id: int) -> bool:
        """Remove a todo by its ID.

        Args:
            todo_id: The unique identifier of the todo to remove.

        Returns:
            ``True`` if the todo was found and removed, ``False`` otherwise.
        """
        if todo_id in self._todos:
            del self._todos[todo_id]
            return True
        return False
