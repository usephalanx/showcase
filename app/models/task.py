"""Task model definition.

Represents an individual task belonging to a project, with status and
priority tracking.
"""

from __future__ import annotations

import enum
from datetime import date, datetime, timezone
from typing import Optional

from sqlalchemy import Date, DateTime, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class TaskStatus(str, enum.Enum):
    """Allowed status values for a task."""

    todo = "todo"
    in_progress = "in_progress"
    done = "done"


class TaskPriority(str, enum.Enum):
    """Allowed priority values for a task."""

    low = "low"
    medium = "medium"
    high = "high"


class Task(Base):
    """SQLAlchemy model for the ``tasks`` table.

    Attributes:
        id: Auto-incrementing primary key.
        project_id: Foreign key referencing :class:`Project`.
        title: Short summary of the task.
        status: Current workflow status (todo / in_progress / done).
        priority: Importance level (low / medium / high).
        due_date: Optional deadline for the task.
        created_at: UTC timestamp of when the task was created.
        project: Many-to-one relationship with :class:`Project`.
    """

    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    project_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("projects.id", ondelete="CASCADE"), nullable=False
    )
    title: Mapped[str] = mapped_column(String(512), nullable=False)
    status: Mapped[TaskStatus] = mapped_column(
        Enum(TaskStatus), nullable=False, default=TaskStatus.todo
    )
    priority: Mapped[TaskPriority] = mapped_column(
        Enum(TaskPriority), nullable=False, default=TaskPriority.medium
    )
    due_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True, default=None)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )

    project = relationship("Project", back_populates="tasks")

    def __repr__(self) -> str:
        """Return developer-friendly string representation."""
        return f"<Task(id={self.id}, title={self.title!r}, status={self.status})>"
