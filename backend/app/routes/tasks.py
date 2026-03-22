"""Task API routes.

Provides CRUD endpoints for tasks, including a dedicated PATCH endpoint
for status-only updates and optional query-parameter filtering.
"""

from __future__ import annotations

from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from sqlalchemy.orm import Session

from backend.app.database import get_db
from backend.app.models import Project, Task
from backend.app.schemas import (
    TaskCreate,
    TaskPriority,
    TaskResponse,
    TaskStatus,
    TaskStatusUpdate,
    TaskUpdate,
)

router = APIRouter(prefix="/api/tasks", tags=["tasks"])


@router.get("", response_model=List[TaskResponse])
def list_tasks(
    project_id: Optional[int] = Query(None, description="Filter by project ID"),
    task_status: Optional[TaskStatus] = Query(
        None, alias="status", description="Filter by task status"
    ),
    priority: Optional[TaskPriority] = Query(
        None, description="Filter by priority"
    ),
    db: Session = Depends(get_db),
) -> List[Task]:
    """Return all tasks, optionally filtered by project_id, status, or priority."""
    query = db.query(Task)
    if project_id is not None:
        query = query.filter(Task.project_id == project_id)
    if task_status is not None:
        query = query.filter(Task.status == task_status.value)
    if priority is not None:
        query = query.filter(Task.priority == priority.value)
    return query.order_by(Task.id.asc()).all()


@router.post("", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(
    payload: TaskCreate, db: Session = Depends(get_db)
) -> Task:
    """Create a new task.

    The referenced ``project_id`` must exist; otherwise a 400 error is returned.
    """
    project = db.query(Project).filter(Project.id == payload.project_id).first()
    if project is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Project with id {payload.project_id} does not exist",
        )

    task = Task(
        project_id=payload.project_id,
        title=payload.title,
        status=payload.status.value,
        priority=payload.priority.value,
        due_date=payload.due_date,
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


@router.get("/{task_id}", response_model=TaskResponse)
def get_task(task_id: int, db: Session = Depends(get_db)) -> Task:
    """Return a single task by ID or 404."""
    task = db.query(Task).filter(Task.id == task_id).first()
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} not found",
        )
    return task


@router.put("/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: int,
    payload: TaskUpdate,
    db: Session = Depends(get_db),
) -> Task:
    """Fully update an existing task. Only provided fields are changed."""
    task = db.query(Task).filter(Task.id == task_id).first()
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} not found",
        )

    update_data = payload.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        if field in ("status", "priority") and value is not None:
            setattr(task, field, value.value if hasattr(value, "value") else value)
        else:
            setattr(task, field, value)

    db.commit()
    db.refresh(task)
    return task


@router.patch("/{task_id}/status", response_model=TaskResponse)
def update_task_status(
    task_id: int,
    payload: TaskStatusUpdate,
    db: Session = Depends(get_db),
) -> Task:
    """Update only the status of an existing task."""
    task = db.query(Task).filter(Task.id == task_id).first()
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} not found",
        )

    task.status = payload.status.value
    db.commit()
    db.refresh(task)
    return task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task_id: int, db: Session = Depends(get_db)
) -> Response:
    """Delete a task by ID."""
    task = db.query(Task).filter(Task.id == task_id).first()
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} not found",
        )
    db.delete(task)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
