"""Dashboard API route.

Provides a single endpoint that returns aggregate statistics used by
the frontend dashboard page.
"""

from __future__ import annotations

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from backend.app.database import get_db
from backend.app.models import Project, Task

router = APIRouter(prefix="/api", tags=["dashboard"])


class DashboardResponse(BaseModel):
    """Response schema for the dashboard summary endpoint."""

    project_count: int
    open_task_count: int


@router.get("/dashboard", response_model=DashboardResponse)
def get_dashboard(db: Session = Depends(get_db)) -> DashboardResponse:
    """Return aggregate counts for the dashboard.

    ``project_count`` is the total number of projects.
    ``open_task_count`` is the number of tasks whose status is **not** ``done``.
    """
    project_count: int = db.query(Project).count()
    open_task_count: int = db.query(Task).filter(Task.status != "done").count()
    return DashboardResponse(
        project_count=project_count,
        open_task_count=open_task_count,
    )
