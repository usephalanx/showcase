"""API router for Todo CRUD endpoints.

Defines all REST endpoints for managing todo items:
- GET    /todos            – list all todos
- GET    /todos/{todo_id}  – retrieve a single todo
- POST   /todos            – create a new todo
- PUT    /todos/{todo_id}  – update an existing todo
- DELETE /todos/{todo_id}  – delete a todo
"""

from __future__ import annotations

from typing import List

from fastapi import APIRouter, HTTPException, status

from app.models import TodoCreate, TodoResponse, TodoUpdate
from app.storage import storage

router = APIRouter()


@router.get("/todos", response_model=List[TodoResponse], tags=["todos"])
async def list_todos() -> List[TodoResponse]:
    """Return all todo items.

    Returns:
        A list of all todos currently in storage.  Returns an empty
        list when no todos exist.
    """
    return storage.get_all()


@router.get("/todos/{todo_id}", response_model=TodoResponse, tags=["todos"])
async def get_todo(todo_id: int) -> TodoResponse:
    """Return a single todo item by its ID.

    Args:
        todo_id: The unique identifier of the requested todo.

    Returns:
        The matching TodoResponse.

    Raises:
        HTTPException: 404 if no todo with the given ID exists.
    """
    todo = storage.get_by_id(todo_id)
    if todo is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found",
        )
    return todo


@router.post(
    "/todos",
    response_model=TodoResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["todos"],
)
async def create_todo(payload: TodoCreate) -> TodoResponse:
    """Create a new todo item.

    Args:
        payload: The creation payload containing title and optional
                 description.

    Returns:
        The newly created TodoResponse with a 201 status code.
    """
    return storage.create(payload)


@router.put("/todos/{todo_id}", response_model=TodoResponse, tags=["todos"])
async def update_todo(todo_id: int, payload: TodoUpdate) -> TodoResponse:
    """Update an existing todo item.

    Only fields provided in the request body are updated; omitted
    fields remain unchanged.

    Args:
        todo_id: The unique identifier of the todo to update.
        payload: The update payload with optional fields.

    Returns:
        The updated TodoResponse.

    Raises:
        HTTPException: 404 if no todo with the given ID exists.
    """
    todo = storage.update(todo_id, payload)
    if todo is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found",
        )
    return todo


@router.delete(
    "/todos/{todo_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["todos"],
)
async def delete_todo(todo_id: int) -> None:
    """Delete a todo item by its ID.

    Args:
        todo_id: The unique identifier of the todo to delete.

    Raises:
        HTTPException: 404 if no todo with the given ID exists.
    """
    deleted = storage.delete(todo_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found",
        )
