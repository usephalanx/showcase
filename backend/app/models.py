"""SQLAlchemy ORM models for the Todo application."""

from __future__ import annotations

import enum
from datetime import date, datetime
from typing import Optional

from sqlalchemy import Date, DateTime, Enum, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class TaskStatus(str, enum.Enum):
    """Allowed status values for a Task."""

    TODO = "todo"
    IN_PROGRESS = "in-progress"
    DONE = "done"


class Task(Base):
    """Represents a single task / todo item.

    Attributes:
        id: Auto-incrementing primary key.
        title: Short description of the task (required).
        status: Current workflow status (todo | in-progress | done).
        due_date: Optional target completion date.
        created_at: Timestamp of row creation (set by the database).
        updated_at: Timestamp of last modification (auto-updated).
    """

    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )
    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
    status: Mapped[str] = mapped_column(
        Enum(TaskStatus, values_callable=lambda e: [m.value for m in e]),
        nullable=False,
        default=TaskStatus.TODO.value,
        server_default=TaskStatus.TODO.value,
    )
    due_date: Mapped[Optional[date]] = mapped_column(
        Date,
        nullable=True,
        default=None,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=func.now(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    def __repr__(self) -> str:
        """Return a developer-friendly string representation."""
        return (
            f"<Task(id={self.id!r}, title={self.title!r}, "
            f"status={self.status!r})>"
        )
