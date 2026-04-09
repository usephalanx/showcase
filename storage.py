"""In-memory storage layer for Todo items.

Provides a thread-safe (GIL-protected) dictionary-based store with
auto-incrementing integer IDs and ISO-8601 timestamps.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional


class TodoStore:
    """Simple in-memory store for todo items."""

    def __init__(self) -> None:
        """Initialise an empty store with a zero counter."""
        self._todos: Dict[int, Dict[str, Any]] = {}
        self._counter: int = 0

    def add(
        self,
        title: str,
        description: Optional[str] = None,
        completed: bool = False,
    ) -> Dict[str, Any]:
        """Add a new todo and return its full dictionary representation.

        Args:
            title: The title of the todo item.
            description: Optional longer description.
            completed: Initial completion status.

        Returns:
            A dictionary representing the created todo.
        """
        self._counter += 1
        todo: Dict[str, Any] = {
            "id": self._counter,
            "title": title,
            "description": description,
            "completed": completed,
            "created_at": datetime.now(timezone.utc).isoformat(),
        }
        self._todos[self._counter] = todo
        return dict(todo)

    def get_all(self) -> List[Dict[str, Any]]:
        """Return a list of all todos ordered by id ascending."""
        return [dict(t) for t in self._todos.values()]

    def get(self, todo_id: int) -> Optional[Dict[str, Any]]:
        """Return a single todo by *todo_id*, or ``None`` if not found."""
        todo = self._todos.get(todo_id)
        return dict(todo) if todo is not None else None

    def update(
        self,
        todo_id: int,
        title: Optional[str] = None,
        description: Optional[str] = None,
        completed: Optional[bool] = None,
    ) -> Optional[Dict[str, Any]]:
        """Update fields of an existing todo.

        Only non-``None`` arguments are applied.

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
        """Remove a todo by *todo_id*.

        Returns:
            ``True`` if the item was deleted, ``False`` if it did not exist.
        """
        return self._todos.pop(todo_id, None) is not None
