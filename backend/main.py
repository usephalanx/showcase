"""FastAPI application entry point for the Task Manager API.

Configures CORS middleware, sets up the database on startup via a
lifespan context manager, and exposes three REST endpoints for
creating, listing, and updating tasks.
"""

from __future__ import annotations

from contextlib import asynccontextmanager
from typing import AsyncIterator, List

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from backend.database import get_db, init_db
from backend.models import Task
from backend.schemas import TaskCreate, TaskResponse, TaskUpdate


# ---------------------------------------------------------------------------
# Application lifespan
# ---------------------------------------------------------------------------


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncIterator[None]:
    """Initialise the database tables on application startup."""
    init_db()
    yield


# ---------------------------------------------------------------------------
# FastAPI app
# ---------------------------------------------------------------------------

app = FastAPI(
    title="Task Manager API",
    description="A simple task management REST API backed by SQLite.",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS — allow all origins for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------


@app.post("/tasks", response_model=TaskResponse, status_code=201, tags=["tasks"])
async def create_task(
    payload: TaskCreate,
    db: Session = Depends(get_db),
) -> TaskResponse:
    """Create a new task with status 'pending' and return it."""
    task = Task(
        title=payload.title,
        description=payload.description,
        status="pending",
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    return TaskResponse.model_validate(task)


@app.get("/tasks", response_model=List[TaskResponse], tags=["tasks"])
async def list_tasks(
    db: Session = Depends(get_db),
) -> List[TaskResponse]:
    """Return all tasks ordered by created_at descending."""
    tasks = db.query(Task).order_by(Task.created_at.desc()).all()
    return [TaskResponse.model_validate(t) for t in tasks]


@app.patch("/tasks/{task_id}", response_model=TaskResponse, tags=["tasks"])
async def update_task_status(
    task_id: int,
    payload: TaskUpdate,
    db: Session = Depends(get_db),
) -> TaskResponse:
    """Update the status of an existing task.

    Returns 404 if no task with the given *task_id* exists.
    """
    task = db.query(Task).filter(Task.id == task_id).first()
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    task.status = payload.status  # type: ignore[assignment]
    db.commit()
    db.refresh(task)
    return TaskResponse.model_validate(task)
