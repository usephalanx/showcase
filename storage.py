"""In-memory dictionary-based storage for todo items.

Provides a TodoStore class that keeps todos in a plain Python dict
with an auto-incrementing integer ID counter.  Storage is ephemeral
and resets when the process restarts.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional


class TodoStore:
    """In-memory store for todo items backed by a Python dict.

    Each todo is stored as a dict with keys: id, title, description,
    completed, created_at.  An internal counter provides monotonically
    increasing unique IDs.
    """

    def __init__(self) -> None:
        """Initialise the store with an empty dict and counter starting at 1."""
        self._todos: Dict[int, Dict[str, Any]] = {}
        self._next_id: int = 1

    def _get_next_id(self) -> int:
        """Return the next available ID and increment the counter.

        Returns:
            The next unique integer ID.
        """
        current_id = self._next_id
        self._next_id += 1
        return current_id

    def create(
        self,
        title: str,
        description: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Create a new todo item and return it.

        Args:
            title: The title of the todo item.
            description: An optional description.

        Returns:
            A dictionary representing the newly created todo.
        """
        todo_id = self._get_next_id()
        now = datetime.now(timezone.utc)
        todo: Dict[str, Any] = {
            "id": todo_id,
            "title": title,
            "description": description,
            "completed": False,
            "created_at": now,
        }
        self._todos[todo_id] = todo
        return dict(todo)

    def get_all(self) -> List[Dict[str, Any]]:
        """Return all todo items ordered by creation time descending.

        Returns:
            A list of todo dictionaries.
        """
        todos = sorted(
            self._todos.values(),
            key=lambda t: t["created_at"],
            reverse=True,
        )
        return [dict(t) for t in todos]

    def get_by_id(self, todo_id: int) -> Optional[Dict[str, Any]]:
        """Return a single todo by its ID, or None if not found.

        Args:
            todo_id: The unique ID of the todo to retrieve.

        Returns:
            A dictionary representing the todo, or None.
        """
        todo = self._todos.get(todo_id)
        if todo is None:
            return None
        return dict(todo)

    def update(
        self,
        todo_id: int,
        title: Optional[str] = None,
        description: Optional[str] = ...,  # type: ignore[assignment]
        completed: Optional[bool] = None,
    ) -> Optional[Dict[str, Any]]:
        """Update fields of an existing todo item.

        Only fields that are not None (and not the sentinel for
        description) are updated, supporting partial updates.

        Args:
            todo_id: The ID of the todo to update.
            title: New title, or None to leave unchanged.
            description: New description, or the sentinel (Ellipsis default)
                         to leave unchanged.  Pass None explicitly to clear.
            completed: New completed status, or None to leave unchanged.

        Returns:
            A dictionary of the updated todo, or None if not found.
        """
        todo = self._todos.get(todo_id)
        if todo is None:
            return None

        if title is not None:
            todo["title"] = title
        if description is not ...:
            todo["description"] = description
        if completed is not None:
            todo["completed"] = completed

        return dict(todo)

    def delete(self, todo_id: int) -> bool:
        """Delete a todo by its ID.

        Args:
            todo_id: The ID of the todo to delete.

        Returns:
            True if the todo was found and deleted, False otherwise.
        """
        if todo_id in self._todos:
            del self._todos[todo_id]
            return True
        return False

    def clear(self) -> None:
        """Remove all todos and reset the ID counter."""
        self._todos.clear()
        self._next_id = 1


# Module-level singleton instance for use by the application.
todo_store = TodoStore()
