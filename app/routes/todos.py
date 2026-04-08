"""CRUD route handlers for todo items."""

from __future__ import annotations

from typing import List

from fastapi import APIRouter, HTTPException, Response

from app.models import TodoCreate, TodoResponse, TodoUpdate
from app.storage import storage

router = APIRouter(prefix="/todos", tags=["todos"])


@router.get("", response_model=List[TodoResponse])
async def list_todos() -> List[TodoResponse]:
    """Return all todo items."""
    rows = storage.get_all()
    return [TodoResponse(**row) for row in rows]


@router.get("/{todo_id}", response_model=TodoResponse)
async def get_todo(todo_id: int) -> TodoResponse:
    """Return a single todo item by id."""
    todo = storage.get_by_id(todo_id)
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return TodoResponse(**todo)


@router.post("", response_model=TodoResponse, status_code=201)
async def create_todo(payload: TodoCreate) -> TodoResponse:
    """Create a new todo item."""
    todo = storage.create(payload.model_dump())
    return TodoResponse(**todo)


@router.put("/{todo_id}", response_model=TodoResponse)
async def update_todo(todo_id: int, payload: TodoUpdate) -> TodoResponse:
    """Update an existing todo item (partial update)."""
    updated = storage.update(todo_id, payload.model_dump(exclude_unset=True))
    if updated is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return TodoResponse(**updated)


@router.delete("/{todo_id}", status_code=204)
async def delete_todo(todo_id: int) -> Response:
    """Delete a todo item.  Returns 204 No Content on success."""
    deleted = storage.delete(todo_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Todo not found")
    return Response(status_code=204)
