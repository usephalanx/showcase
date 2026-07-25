"""FastAPI application for the Todo backend.

Exposes REST endpoints for CRUD operations on todo items and serves
an HTML frontend at the root path.
"""

from __future__ import annotations

from contextlib import asynccontextmanager
from pathlib import Path
from typing import AsyncIterator, List

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field

import database


# ---------------------------------------------------------------------------
# Pydantic models
# ---------------------------------------------------------------------------


class TodoCreate(BaseModel):
    """Request body for creating a new todo item."""

    title: str = Field(..., min_length=1, description="Title of the todo item")


class TodoResponse(BaseModel):
    """Response body representing a single todo item."""

    id: int
    title: str
    completed: bool
    created_at: str


# ---------------------------------------------------------------------------
# Application lifespan (replaces deprecated @app.on_event)
# ---------------------------------------------------------------------------


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncIterator[None]:
    """Initialise the database on application startup."""
    database.init_db()
    yield


app = FastAPI(
    title="Todo API",
    description="A simple Todo REST API backed by SQLite.",
    version="1.0.0",
    lifespan=lifespan,
)


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------


@app.get("/", response_class=HTMLResponse, tags=["frontend"])
async def serve_index() -> HTMLResponse:
    """Serve the HTML frontend page."""
    html_path = Path(__file__).parent / "static" / "index.html"
    if not html_path.exists():
        raise HTTPException(status_code=404, detail="Frontend page not found")
    content = html_path.read_text(encoding="utf-8")
    return HTMLResponse(content=content, status_code=200)


@app.get("/api/todos", response_model=List[TodoResponse], tags=["todos"])
async def list_todos() -> List[TodoResponse]:
    """Return a list of all todo items ordered by creation date descending."""
    rows = database.get_all_todos()
    return [TodoResponse(**row) for row in rows]


@app.post("/api/todos", response_model=TodoResponse, status_code=201, tags=["todos"])
async def create_todo(payload: TodoCreate) -> TodoResponse:
    """Create a new todo item and return it."""
    try:
        row = database.create_todo(payload.title)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    return TodoResponse(**row)


@app.patch("/api/todos/{todo_id}", response_model=TodoResponse, tags=["todos"])
async def toggle_todo(todo_id: int) -> TodoResponse:
    """Toggle the completed status of an existing todo item."""
    conn = database.get_db_connection()
    try:
        cursor = conn.execute(
            "SELECT completed FROM todos WHERE id = ?;", (todo_id,)
        )
        existing = cursor.fetchone()
    finally:
        conn.close()

    if existing is None:
        raise HTTPException(status_code=404, detail="Todo not found")

    new_completed = not bool(existing["completed"])
    updated = database.update_todo(todo_id, new_completed)

    if updated is None:  # pragma: no cover – defensive check
        raise HTTPException(status_code=404, detail="Todo not found")

    return TodoResponse(**updated)


@app.delete("/api/todos/{todo_id}", status_code=200, tags=["todos"])
async def delete_todo(todo_id: int) -> dict:
    """Delete a todo item by its id."""
    deleted = database.delete_todo(todo_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Todo not found")
    return {"detail": "Todo deleted successfully"}
