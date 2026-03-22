"""SQLAlchemy ORM models for Project and Task entities.

All models inherit from the shared ``Base`` declarative class defined in
``database.py``.
"""

from __future__ import annotations

import datetime
from typing import List, Optional

from sqlalchemy import (
    CheckConstraint,
    Date,
    DateTime,
    ForeignKey,
    Integer,
    String,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.database import Base


class Project(Base):
    """A project that contains zero or more tasks.

    Attributes:
        id:          Auto-incrementing primary key.
        name:        Human-readable project name (required).
        description: Optional longer description of the project.
        status:      One of 'active', 'completed', or 'archived'.
        created_at:  Timestamp set automatically on creation.
        tasks:       ORM relationship to child :class:`Task` instances.
    """

    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(
        String(500), nullable=True
    )
    status: Mapped[str] = mapped_column(
        String(20), nullable=False, default="active"
    )
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now()
    )

    # Relationships
    tasks: Mapped[List["Task"]] = relationship(
        "Task",
        back_populates="project",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    __table_args__ = (
        CheckConstraint(
            "status IN ('active', 'completed', 'archived')",
            name="ck_project_status",
        ),
    )

    def __repr__(self) -> str:
        """Return developer-friendly string representation."""
        return f"<Project(id={self.id}, name={self.name!r}, status={self.status!r})>"


class Task(Base):
    """A task that belongs to a single project.

    Attributes:
        id:         Auto-incrementing primary key.
        project_id: Foreign key referencing :attr:`Project.id`.
        title:      Short description of the task (required).
        status:     One of 'todo', 'in_progress', or 'done'.
        priority:   One of 'low', 'medium', or 'high'.
        due_date:   Optional date by which the task should be completed.
        project:    ORM relationship back to the parent :class:`Project`.
    """

    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )
    project_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("projects.id", ondelete="CASCADE"),
        nullable=False,
    )
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    status: Mapped[str] = mapped_column(
        String(20), nullable=False, default="todo"
    )
    priority: Mapped[str] = mapped_column(
        String(10), nullable=False, default="medium"
    )
    due_date: Mapped[Optional[datetime.date]] = mapped_column(
        Date, nullable=True
    )

    # Relationships
    project: Mapped["Project"] = relationship(
        "Project", back_populates="tasks"
    )

    __table_args__ = (
        CheckConstraint(
            "status IN ('todo', 'in_progress', 'done')",
            name="ck_task_status",
        ),
        CheckConstraint(
            "priority IN ('low', 'medium', 'high')",
            name="ck_task_priority",
        ),
    )

    def __repr__(self) -> str:
        """Return developer-friendly string representation."""
        return (
            f"<Task(id={self.id}, title={self.title!r}, "
            f"status={self.status!r}, priority={self.priority!r})>"
        )
