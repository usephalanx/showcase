"""API route definitions for the Todo application.

This module defines the :data:`router` that is included by the main
application.  All CRUD endpoints for tasks are registered here.
"""

from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.models import Task
from backend.schemas import TaskCreate, TaskResponse, TaskStatus, TaskUpdate

router = APIRouter()


@router.get("/health", tags=["health"])
async def health_check() -> dict[str, str]:
    """Return a simple health-check response.

    Returns:
        A JSON object with a ``status`` key set to ``ok``.
    """
    return {"status": "ok"}


@router.get(
    "/tasks",
    response_model=list[TaskResponse],
    tags=["tasks"],
    summary="List all tasks",
)
def list_tasks(
    status: Optional[TaskStatus] = Query(
        default=None,
        description="Filter tasks by workflow status",
    ),
    db: Session = Depends(get_db),
) -> list[Task]:
    """Return all tasks, optionally filtered by status.

    Args:
        status: If provided, only tasks matching this status are returned.
        db: SQLAlchemy session provided by dependency injection.

    Returns:
        A list of :class:`Task` instances serialised as
        :class:`TaskResponse`.
    """
    query = db.query(Task)
    if status is not None:
        query = query.filter(Task.status == status.value)
    return query.order_by(Task.created_at.desc()).all()


@router.get(
    "/tasks/{task_id}",
    response_model=TaskResponse,
    tags=["tasks"],
    summary="Get a single task",
)
def get_task(
    task_id: int,
    db: Session = Depends(get_db),
) -> Task:
    """Retrieve a single task by its primary key.

    Args:
        task_id: The ID of the task to retrieve.
        db: SQLAlchemy session provided by dependency injection.

    Returns:
        The matching :class:`Task` instance.

    Raises:
        HTTPException: 404 if no task with the given ID exists.
    """
    task = db.query(Task).filter(Task.id == task_id).first()
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} not found",
        )
    return task


@router.post(
    "/tasks",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["tasks"],
    summary="Create a new task",
)
def create_task(
    payload: TaskCreate,
    db: Session = Depends(get_db),
) -> Task:
    """Create a new task from the supplied payload.

    Args:
        payload: Validated request body containing the new task data.
        db: SQLAlchemy session provided by dependency injection.

    Returns:
        The newly created :class:`Task` instance.
    """
    task = Task(
        title=payload.title,
        status=payload.status.value,
        due_date=payload.due_date,
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


@router.put(
    "/tasks/{task_id}",
    response_model=TaskResponse,
    tags=["tasks"],
    summary="Update an existing task",
)
def update_task(
    task_id: int,
    payload: TaskUpdate,
    db: Session = Depends(get_db),
) -> Task:
    """Update one or more fields on an existing task.

    Only fields that are explicitly provided (not ``None``) in the
    request body will be updated.

    Args:
        task_id: The ID of the task to update.
        payload: Validated request body with optional updated fields.
        db: SQLAlchemy session provided by dependency injection.

    Returns:
        The updated :class:`Task` instance.

    Raises:
        HTTPException: 404 if no task with the given ID exists.
    """
    task = db.query(Task).filter(Task.id == task_id).first()
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} not found",
        )

    update_data = payload.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        if field == "status" and value is not None:
            setattr(task, field, value.value if isinstance(value, TaskStatus) else value)
        else:
            setattr(task, field, value)

    db.commit()
    db.refresh(task)
    return task


@router.delete(
    "/tasks/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["tasks"],
    summary="Delete a task",
)
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
) -> None:
    """Delete a task by its primary key.

    Args:
        task_id: The ID of the task to delete.
        db: SQLAlchemy session provided by dependency injection.

    Raises:
        HTTPException: 404 if no task with the given ID exists.
    """
    task = db.query(Task).filter(Task.id == task_id).first()
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} not found",
        )
    db.delete(task)
    db.commit()
