"""API routes for the Todo application.

Defines CRUD endpoints for Task resources using an APIRouter.
All routes are prefixed with ``/tasks`` when registered in the main app.
"""

from __future__ import annotations

from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Task, TaskStatus
from app.schemas import TaskCreate, TaskResponse, TaskUpdate

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.get("", response_model=List[TaskResponse])
def list_tasks(
    status: Optional[str] = Query(
        default=None,
        description="Filter tasks by status (todo, in-progress, done)",
    ),
    db: Session = Depends(get_db),
) -> List[Task]:
    """Return all tasks, optionally filtered by status.

    Args:
        status: Optional status string to filter results.
        db: Database session provided by dependency injection.

    Returns:
        A list of Task model instances.
    """
    query = db.query(Task)
    if status is not None:
        # Validate that the provided status is a known enum value
        try:
            status_enum = TaskStatus(status)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY
                if hasattr(status, "HTTP_422_UNPROCESSABLE_ENTITY")
                else 422,
                detail=f"Invalid status '{status}'. "
                f"Allowed values: {[s.value for s in TaskStatus]}",
            )
        query = query.filter(Task.status == status_enum)
    return query.all()


@router.post("", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(
    task_in: TaskCreate,
    db: Session = Depends(get_db),
) -> Task:
    """Create a new task.

    Args:
        task_in: Validated request body with task data.
        db: Database session provided by dependency injection.

    Returns:
        The newly created Task instance.
    """
    task = Task(
        title=task_in.title,
        status=TaskStatus(task_in.status),
        due_date=task_in.due_date,
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


@router.get("/{task_id}", response_model=TaskResponse)
def get_task(
    task_id: int,
    db: Session = Depends(get_db),
) -> Task:
    """Retrieve a single task by its ID.

    Args:
        task_id: The primary-key identifier of the task.
        db: Database session provided by dependency injection.

    Returns:
        The matching Task instance.

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


@router.put("/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: int,
    task_in: TaskUpdate,
    db: Session = Depends(get_db),
) -> Task:
    """Update an existing task.

    Only fields provided in the request body (non-``None``) are updated.

    Args:
        task_id: The primary-key identifier of the task to update.
        task_in: Validated request body with optional updated fields.
        db: Database session provided by dependency injection.

    Returns:
        The updated Task instance.

    Raises:
        HTTPException: 404 if no task with the given ID exists.
    """
    task = db.query(Task).filter(Task.id == task_id).first()
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} not found",
        )

    update_data = task_in.dict(exclude_unset=True)
    for field, value in update_data.items():
        if value is not None:
            if field == "status":
                setattr(task, field, TaskStatus(value))
            else:
                setattr(task, field, value)

    db.commit()
    db.refresh(task)
    return task


@router.delete("/{task_id}", status_code=status.HTTP_200_OK)
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
) -> dict:
    """Delete a task by its ID.

    Args:
        task_id: The primary-key identifier of the task to delete.
        db: Database session provided by dependency injection.

    Returns:
        A confirmation message.

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
    return {"detail": f"Task with id {task_id} deleted successfully"}
