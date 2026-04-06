"""SQLAlchemy ORM models for the Todo application.

Defines the ``Task`` model which maps to the ``tasks`` table in the
SQLite database.
"""

from __future__ import annotations

import enum

from sqlalchemy import Column, Date, Enum, Integer, String

from app.database import Base


class TaskStatus(str, enum.Enum):
    """Allowed values for a task's status field."""

    TODO = "todo"
    IN_PROGRESS = "in-progress"
    DONE = "done"


class Task(Base):
    """SQLAlchemy model representing a task in the todo list.

    Attributes:
        id: Primary key, auto-incremented integer.
        title: Non-nullable title string.
        status: Current status (todo, in-progress, done). Defaults to 'todo'.
        due_date: Optional date by which the task should be completed.
    """

    __tablename__ = "tasks"

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    title: str = Column(String, nullable=False)
    status: str = Column(
        Enum(TaskStatus),
        nullable=False,
        default=TaskStatus.TODO,
        server_default=TaskStatus.TODO.value,
    )
    due_date = Column(Date, nullable=True)

    def __repr__(self) -> str:
        """Return a developer-friendly string representation."""
        return (
            f"<Task(id={self.id!r}, title={self.title!r}, "
            f"status={self.status!r}, due_date={self.due_date!r})>"
        )
