"""SQLAlchemy ORM models for the Task Manager application.

This module defines the database-level representation of domain entities.
It is intentionally kept separate from the Pydantic API schemas
(:mod:`backend.schemas`) to maintain a clean boundary between the
persistence layer and the HTTP interface.
"""

from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy import Column, Integer, String, DateTime

from backend.database import Base


class Task(Base):  # type: ignore[misc]
    """ORM model for a task stored in the ``tasks`` table.

    Attributes:
        id: Auto-incrementing integer primary key.
        title: Short summary of the task (required).
        description: Longer description (defaults to empty string).
        status: Current status — ``'pending'`` or ``'done'``.
        created_at: UTC timestamp recording when the task was created.
    """

    __tablename__ = "tasks"

    id: int = Column(Integer, primary_key=True, autoincrement=True, index=True)
    title: str = Column(String, nullable=False)
    description: str = Column(String, nullable=False, default="")
    status: str = Column(String, nullable=False, default="pending")
    created_at: datetime = Column(
        DateTime,
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )
