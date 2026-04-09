"""In-memory storage layer for Todo items.

Provides a thread-safe (GIL-protected) dictionary-based store with
auto-incrementing integer IDs and ISO-8601 timestamps.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional


class TodoStore:
    """Simple in-memory store for todo items.

    Each todo is stored as a plain dictionary with keys:
    ``id``, ``title``, ``description``, ``completed``, ``created_at``.
    """

    def __init__(self) -> None:
        """Initialise an empty store."""
        self._todos: Dict[int, Dict[str, Any]] = {}
        self._next_id: int = 1

    def add(
        self,
        title: str,
        description: Optional[str] = None,
        completed: bool = False,
    ) -> Dict[str, Any]:
        """Add a new todo item and return it.

        Args:
            title: The title of the todo item.
            description: An optional longer description.
            completed: Whether the todo starts as completed.

        Returns:
            A dictionary representing the new todo.
        """
        todo_id = self._next_id
        self._next_id += 1
        now = datetime.now(timezone.utc).isoformat()
        todo: Dict[str, Any] = {
            "id": todo_id,
            "title": title,
            "description": description,
            "completed": completed,
            "created_at": now,
        }
        self._todos[todo_id] = todo
        return dict(todo)

    def get_all(self) -> List[Dict[str, Any]]:
        """Return a list of all todo items.

        Returns:
            A list of todo dictionaries.
        """
        return [dict(t) for t in self._todos.values()]

    def get(self, todo_id: int) -> Optional[Dict[str, Any]]:
        """Retrieve a single todo by its ID.

        Args:
            todo_id: The integer ID of the todo.

        Returns:
            The todo dictionary, or ``None`` if not found.
        """
        todo = self._todos.get(todo_id)
        if todo is None:
            return None
        return dict(todo)

    def update(
        self,
        todo_id: int,
        title: Optional[str] = None,
        description: Optional[str] = None,
        completed: Optional[bool] = None,
    ) -> Optional[Dict[str, Any]]:
        """Update fields of an existing todo.

        Only non-``None`` arguments are applied.

        Args:
            todo_id: The integer ID of the todo to update.
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
        return dict(todo)

    def delete(self, todo_id: int) -> bool:
        """Delete a todo by its ID.

        Args:
            todo_id: The integer ID of the todo to delete.

        Returns:
            ``True`` if the todo was deleted, ``False`` if not found.
        """
        if todo_id in self._todos:
            del self._todos[todo_id]
            return True
        return False
