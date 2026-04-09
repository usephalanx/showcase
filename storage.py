"""In-memory dictionary-based Todo storage.

Provides a simple thread-safe (GIL-protected) storage layer for todo
items.  Each item is stored as a plain dictionary keyed by integer ID.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional


class TodoStore:
    """In-memory store for todo items backed by a Python dictionary."""

    def __init__(self) -> None:
        """Initialise an empty store with a starting ID counter of 1."""
        self._todos: Dict[int, Dict[str, Any]] = {}
        self._next_id: int = 1

    def add(
        self,
        title: str,
        description: Optional[str] = None,
        completed: bool = False,
    ) -> Dict[str, Any]:
        """Create a new todo item and return its dictionary representation.

        Args:
            title: The title of the todo item.
            description: An optional longer description.
            completed: Initial completion status (defaults to False).

        Returns:
            A dictionary representing the newly created todo.
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
        """Retrieve a single todo item by its ID.

        Args:
            todo_id: The integer ID of the todo to retrieve.

        Returns:
            A dictionary representing the todo, or None if not found.
        """
        todo = self._todos.get(todo_id)
        return dict(todo) if todo is not None else None

    def update(
        self,
        todo_id: int,
        title: Optional[str] = None,
        description: Optional[str] = None,
        completed: Optional[bool] = None,
    ) -> Optional[Dict[str, Any]]:
        """Update fields of an existing todo item.

        Only non-None arguments are applied.

        Args:
            todo_id: The integer ID of the todo to update.
            title: New title, or None to keep current.
            description: New description, or None to keep current.
            completed: New completion status, or None to keep current.

        Returns:
            The updated todo dictionary, or None if the ID was not found.
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
        """Delete a todo item by its ID.

        Args:
            todo_id: The integer ID of the todo to delete.

        Returns:
            True if the item was deleted, False if it was not found.
        """
        if todo_id in self._todos:
            del self._todos[todo_id]
            return True
        return False
