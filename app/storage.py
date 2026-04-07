"""In-memory storage for Todo items.

Provides a class-based store backed by a Python dict with an
auto-incrementing integer ID counter.  Storage is ephemeral and
resets when the process restarts.

A module-level ``storage`` instance is provided for convenient use
across the application.  The instance is pre-populated with a handful
of seed todos so the demo is never empty on first launch.
"""

from __future__ import annotations

from typing import Dict, List, Optional

from app.models import TodoCreate, TodoResponse, TodoUpdate


class TodoStorage:
    """In-memory CRUD store for todo items.

    Attributes:
        _todos: Internal dict mapping todo id -> todo data dict.
        _next_id: Auto-incrementing counter for generating unique IDs.
    """

    def __init__(self) -> None:
        """Initialise an empty store with the ID counter starting at 1."""
        self._todos: Dict[int, dict] = {}
        self._next_id: int = 1

    def _allocate_id(self) -> int:
        """Return the next available ID and increment the counter.

        Returns:
            The newly allocated integer ID.
        """
        current_id = self._next_id
        self._next_id += 1
        return current_id

    def get_all(self) -> List[TodoResponse]:
        """Return all todo items in the store.

        Returns:
            A list of TodoResponse objects.  Returns an empty list when
            the store contains no items.
        """
        return [
            TodoResponse(**todo_data) for todo_data in self._todos.values()
        ]

    def get_by_id(self, todo_id: int) -> Optional[TodoResponse]:
        """Return a single todo item by its ID.

        Args:
            todo_id: The unique identifier of the todo to retrieve.

        Returns:
            A TodoResponse if found, or None if no item with the given
            ID exists.
        """
        todo_data = self._todos.get(todo_id)
        if todo_data is None:
            return None
        return TodoResponse(**todo_data)

    def create(self, todo: TodoCreate) -> TodoResponse:
        """Create a new todo item and return it.

        The item is assigned an auto-incrementing ID and its completed
        status defaults to False.

        Args:
            todo: The creation payload containing title and optional
                  description.

        Returns:
            A TodoResponse representing the newly created item.
        """
        new_id = self._allocate_id()
        todo_data: dict = {
            "id": new_id,
            "title": todo.title,
            "description": todo.description,
            "completed": False,
        }
        self._todos[new_id] = todo_data
        return TodoResponse(**todo_data)

    def update(self, todo_id: int, todo: TodoUpdate) -> Optional[TodoResponse]:
        """Update an existing todo item with the provided fields.

        Only fields that are explicitly set (not None) in the update
        payload will be modified; all other fields remain unchanged.

        Args:
            todo_id: The unique identifier of the todo to update.
            todo: The update payload with optional fields.

        Returns:
            A TodoResponse with the updated data, or None if no item
            with the given ID exists.
        """
        existing = self._todos.get(todo_id)
        if existing is None:
            return None

        update_fields = todo.model_dump(exclude_unset=True)
        for field, value in update_fields.items():
            existing[field] = value

        return TodoResponse(**existing)

    def delete(self, todo_id: int) -> bool:
        """Delete a todo item by its ID.

        Args:
            todo_id: The unique identifier of the todo to delete.

        Returns:
            True if the item was found and deleted, False if no item
            with the given ID exists.
        """
        if todo_id not in self._todos:
            return False
        del self._todos[todo_id]
        return True


def _build_seeded_storage() -> TodoStorage:
    """Create a TodoStorage instance pre-populated with demo items.

    Seed items give new users something to see immediately when they
    start the application for the first time.

    Returns:
        A TodoStorage containing a few example todo items.
    """
    store = TodoStorage()

    seed_items: List[TodoCreate] = [
        TodoCreate(
            title="Buy groceries",
            description="Milk, eggs, bread, and fresh vegetables",
        ),
        TodoCreate(
            title="Read FastAPI documentation",
            description="Review the official tutorial and advanced user guide",
        ),
        TodoCreate(
            title="Write unit tests",
            description="Achieve at least 90% coverage on the API routes",
        ),
    ]

    for item in seed_items:
        store.create(item)

    # Mark the second item as completed to showcase mixed state
    store.update(
        2,
        TodoUpdate(completed=True),
    )

    return store


storage: TodoStorage = _build_seeded_storage()
