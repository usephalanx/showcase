"""CRUD operations for the Todo model.

Provides database-layer functions for creating, reading, updating, and
deleting Todo items.  Each function accepts a SQLAlchemy ``Session`` as
its first argument so that callers (typically FastAPI route handlers)
can inject the session via dependency injection.

Functions
---------
- ``get_todos`` – Retrieve a paginated list of todos.
- ``get_todo`` – Retrieve a single todo by primary key.
- ``create_todo`` – Persist a new todo from a ``TodoCreate`` schema.
- ``update_todo`` – Partially update an existing todo from a ``TodoUpdate`` schema.
- ``delete_todo`` – Remove a todo by primary key.
"""

from __future__ import annotations

from typing import List, Optional

from sqlalchemy.orm import Session

from app.models import Todo
from app.schemas import TodoCreate, TodoUpdate


def get_todos(db: Session, skip: int = 0, limit: int = 100) -> List[Todo]:
    """Return a paginated list of Todo items.

    Args:
        db: Active SQLAlchemy database session.
        skip: Number of rows to skip (offset).  Defaults to ``0``.
        limit: Maximum number of rows to return.  Defaults to ``100``.

    Returns:
        A list of :class:`~app.models.Todo` instances ordered by ``id``.
    """
    return db.query(Todo).offset(skip).limit(limit).all()


def get_todo(db: Session, todo_id: int) -> Optional[Todo]:
    """Return a single Todo by its primary key, or ``None`` if not found.

    Args:
        db: Active SQLAlchemy database session.
        todo_id: The integer primary key of the desired todo.

    Returns:
        The matching :class:`~app.models.Todo` instance, or ``None``.
    """
    return db.query(Todo).filter(Todo.id == todo_id).first()


def create_todo(db: Session, todo: TodoCreate) -> Todo:
    """Create and persist a new Todo item.

    The ``completed`` flag defaults to ``False`` and ``created_at`` is
    set automatically by the database column default.

    Args:
        db: Active SQLAlchemy database session.
        todo: A validated :class:`~app.schemas.TodoCreate` instance.

    Returns:
        The newly created :class:`~app.models.Todo` with server-set
        fields (``id``, ``created_at``) populated.
    """
    db_todo = Todo(
        title=todo.title,
        description=todo.description,
    )
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo


def update_todo(db: Session, todo_id: int, todo: TodoUpdate) -> Optional[Todo]:
    """Partially update an existing Todo item.

    Only fields that are explicitly provided (not ``None``) in *todo*
    are written to the database.  Fields omitted by the client remain
    unchanged.

    Args:
        db: Active SQLAlchemy database session.
        todo_id: The integer primary key of the todo to update.
        todo: A validated :class:`~app.schemas.TodoUpdate` instance
              containing the fields to change.

    Returns:
        The updated :class:`~app.models.Todo` instance, or ``None`` if
        no todo with the given *todo_id* exists.
    """
    db_todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if db_todo is None:
        return None

    update_data = todo.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_todo, field, value)

    db.commit()
    db.refresh(db_todo)
    return db_todo


def delete_todo(db: Session, todo_id: int) -> bool:
    """Delete a Todo item by primary key.

    Args:
        db: Active SQLAlchemy database session.
        todo_id: The integer primary key of the todo to delete.

    Returns:
        ``True`` if the todo existed and was deleted, ``False`` otherwise.
    """
    db_todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if db_todo is None:
        return False

    db.delete(db_todo)
    db.commit()
    return True
