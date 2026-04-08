"""API routes for Todo CRUD operations.

Provides an APIRouter with five endpoints:
- POST   /todos       — create a new todo
- GET    /todos       — list all todos
- GET    /todos/{id}  — retrieve a single todo
- PUT    /todos/{id}  — update an existing todo
- DELETE /todos/{id}  — delete a todo

All endpoints use the in-memory TodoStore from storage.py and the
Pydantic models from models.py.
"""

from __future__ import annotations

from fastapi import APIRouter, HTTPException

from models import TodoCreate, TodoResponse, TodoUpdate
from storage import TodoStore

router = APIRouter()

# Module-level store instance shared by all route handlers.
store = TodoStore()


@router.post("/todos", response_model=TodoResponse, status_code=201, tags=["todos"])
async def create_todo(payload: TodoCreate) -> TodoResponse:
    """Create a new todo item and return its full representation."""
    todo = store.add(
        title=payload.title,
        description=payload.description,
        completed=payload.completed if payload.completed is not None else False,
    )
    return TodoResponse(**todo)


@router.get("/todos", response_model=list[TodoResponse], tags=["todos"])
async def list_todos() -> list[TodoResponse]:
    """Return a list of all todo items."""
    todos = store.get_all()
    return [TodoResponse(**t) for t in todos]


@router.get("/todos/{todo_id}", response_model=TodoResponse, tags=["todos"])
async def get_todo(todo_id: int) -> TodoResponse:
    """Retrieve a single todo item by its ID.

    Raises:
        HTTPException: 404 if the todo is not found.
    """
    todo = store.get(todo_id)
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return TodoResponse(**todo)


@router.put("/todos/{todo_id}", response_model=TodoResponse, tags=["todos"])
async def update_todo(todo_id: int, payload: TodoUpdate) -> TodoResponse:
    """Update an existing todo item.

    Only fields present in the request body are changed.

    Raises:
        HTTPException: 404 if the todo is not found.
    """
    todo = store.update(
        todo_id=todo_id,
        title=payload.title,
        description=payload.description,
        completed=payload.completed,
    )
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return TodoResponse(**todo)


@router.delete("/todos/{todo_id}", status_code=200, tags=["todos"])
async def delete_todo(todo_id: int) -> dict:
    """Delete a todo item by its ID.

    Raises:
        HTTPException: 404 if the todo is not found.
    """
    deleted = store.delete(todo_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Todo not found")
    return {"detail": "Todo deleted successfully"}
