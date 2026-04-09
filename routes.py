"""API routes for Todo CRUD operations and Hello endpoint.

Provides an APIRouter with endpoints:
- GET    /hello       — return a greeting message
- POST   /todos       — create a new todo
- GET    /todos       — list all todos
- GET    /todos/{id}  — retrieve a single todo
- PUT    /todos/{id}  — update an existing todo
- DELETE /todos/{id}  — delete a todo

All todo endpoints use the in-memory TodoStore from storage.py and the
Pydantic models from models.py.
"""

from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, HTTPException, Query

from models import TodoCreate, TodoResponse, TodoUpdate
from storage import TodoStore

router = APIRouter()

# Module-level store instance shared by all route handlers.
store = TodoStore()


# ---------------------------------------------------------------------------
# Hello endpoint
# ---------------------------------------------------------------------------


@router.get("/hello", tags=["hello"])
async def hello(name: Optional[str] = Query(None, description="Name to greet")) -> dict:
    """Return a JSON greeting message.

    If the *name* query parameter is provided and non-empty, the greeting
    addresses that name.  Otherwise it defaults to ``"World"``.

    Args:
        name: Optional name to include in the greeting.

    Returns:
        A dict with a single ``message`` key.
    """
    if name is None or name.strip() == "":
        greeting_name = "World"
    else:
        greeting_name = name
    return {"message": f"Hello, {greeting_name}!"}


# ---------------------------------------------------------------------------
# Todo endpoints
# ---------------------------------------------------------------------------


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
