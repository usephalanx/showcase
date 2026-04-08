"""API route endpoints for the Todo resource.

Defines an ``APIRouter`` with the following endpoints:

- ``GET /todos`` – List all todos with optional ``skip``/``limit`` pagination.
- ``GET /todos/{todo_id}`` – Retrieve a single todo by ID (404 if missing).
- ``POST /todos`` – Create a new todo (returns 201).
- ``PUT /todos/{todo_id}`` – Update an existing todo (404 if missing).
- ``DELETE /todos/{todo_id}`` – Delete a todo (returns 204, 404 if missing).

All endpoints use ``Depends(get_db)`` for database session injection.
"""

from __future__ import annotations

from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.crud import create_todo, delete_todo, get_todo, get_todos, update_todo
from app.database import get_db
from app.schemas import TodoCreate, TodoResponse, TodoUpdate

router = APIRouter(
    prefix="/todos",
    tags=["todos"],
)


@router.get(
    "",
    response_model=List[TodoResponse],
    status_code=status.HTTP_200_OK,
    summary="List all todos",
)
def list_todos(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
) -> List[TodoResponse]:
    """Return a paginated list of todo items.

    Args:
        skip: Number of records to skip (offset). Defaults to ``0``.
        limit: Maximum number of records to return. Defaults to ``100``.
        db: SQLAlchemy database session (injected).

    Returns:
        A list of :class:`~app.schemas.TodoResponse` objects.
    """
    return get_todos(db, skip=skip, limit=limit)


@router.get(
    "/{todo_id}",
    response_model=TodoResponse,
    status_code=status.HTTP_200_OK,
    summary="Get a single todo",
)
def read_todo(
    todo_id: int,
    db: Session = Depends(get_db),
) -> TodoResponse:
    """Retrieve a single todo item by its primary key.

    Args:
        todo_id: The integer ID of the desired todo.
        db: SQLAlchemy database session (injected).

    Returns:
        The matching :class:`~app.schemas.TodoResponse`.

    Raises:
        HTTPException: 404 if no todo with the given ID exists.
    """
    db_todo = get_todo(db, todo_id=todo_id)
    if db_todo is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found",
        )
    return db_todo


@router.post(
    "",
    response_model=TodoResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new todo",
)
def create_todo_endpoint(
    todo: TodoCreate,
    db: Session = Depends(get_db),
) -> TodoResponse:
    """Create and persist a new todo item.

    The ``id`` and ``created_at`` fields are set automatically by the
    server and returned in the response.

    Args:
        todo: Validated :class:`~app.schemas.TodoCreate` request body.
        db: SQLAlchemy database session (injected).

    Returns:
        The newly created :class:`~app.schemas.TodoResponse`.
    """
    return create_todo(db, todo=todo)


@router.put(
    "/{todo_id}",
    response_model=TodoResponse,
    status_code=status.HTTP_200_OK,
    summary="Update an existing todo",
)
def update_todo_endpoint(
    todo_id: int,
    todo: TodoUpdate,
    db: Session = Depends(get_db),
) -> TodoResponse:
    """Partially update an existing todo item.

    Only the fields provided in the request body are modified; omitted
    fields remain unchanged.

    Args:
        todo_id: The integer ID of the todo to update.
        todo: Validated :class:`~app.schemas.TodoUpdate` request body.
        db: SQLAlchemy database session (injected).

    Returns:
        The updated :class:`~app.schemas.TodoResponse`.

    Raises:
        HTTPException: 404 if no todo with the given ID exists.
    """
    db_todo = update_todo(db, todo_id=todo_id, todo=todo)
    if db_todo is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found",
        )
    return db_todo


@router.delete(
    "/{todo_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a todo",
)
def delete_todo_endpoint(
    todo_id: int,
    db: Session = Depends(get_db),
) -> None:
    """Delete a todo item by its primary key.

    Args:
        todo_id: The integer ID of the todo to delete.
        db: SQLAlchemy database session (injected).

    Raises:
        HTTPException: 404 if no todo with the given ID exists.
    """
    deleted = delete_todo(db, todo_id=todo_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found",
        )
