"""SQLAlchemy ORM models for the Todo application.

Defines the ``tasks`` table and the :class:`Task` model used throughout
the backend.
"""

from __future__ import annotations

from datetime import date, datetime
from typing import Optional

from sqlalchemy import CheckConstraint, Column, Date, DateTime, Integer, String, func

from backend.database import Base


class Task(Base):
    """SQLAlchemy model representing a single task.

    Attributes:
        id: Auto-incrementing primary key.
        title: Short description of the task (required, max 255 chars).
        status: Workflow state — one of ``'todo'``, ``'in-progress'``,
            or ``'done'``.  Defaults to ``'todo'``.
        due_date: Optional calendar date by which the task should be
            completed.
        created_at: Timestamp recorded when the row is first inserted.
        updated_at: Timestamp that is refreshed on every update.
    """

    __tablename__ = "tasks"

    id: int = Column(Integer, primary_key=True, autoincrement=True, index=True)
    title: str = Column(String(255), nullable=False)
    status: str = Column(
        String(20),
        nullable=False,
        default="todo",
        server_default="todo",
    )
    due_date: Optional[date] = Column(Date, nullable=True)
    created_at: datetime = Column(
        DateTime,
        nullable=False,
        default=func.now(),
        server_default=func.now(),
    )
    updated_at: datetime = Column(
        DateTime,
        nullable=False,
        default=func.now(),
        server_default=func.now(),
        onupdate=func.now(),
    )

    __table_args__ = (
        CheckConstraint(
            "status IN ('todo', 'in-progress', 'done')",
            name="ck_tasks_status",
        ),
    )

    def __repr__(self) -> str:
        """Return a developer-friendly string representation."""
        return (
            f"<Task(id={self.id!r}, title={self.title!r}, "
            f"status={self.status!r})>"
        )
