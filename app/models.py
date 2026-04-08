"""SQLAlchemy ORM models for the Todo application.

Defines the ``Todo`` model mapped to the ``todos`` table with the
following columns:

- **id** – Integer primary key with autoincrement.
- **title** – Non-nullable string (max 255 characters).
- **description** – Nullable string (max 1024 characters).
- **completed** – Boolean defaulting to ``False``.
- **created_at** – DateTime defaulting to ``datetime.utcnow``.
"""

from __future__ import annotations

from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Integer, String

from app.database import Base


class Todo(Base):
    """ORM model representing a single Todo item.

    Attributes:
        id: Unique auto-incrementing identifier.
        title: Short title of the todo (required).
        description: Optional longer description.
        completed: Whether the todo has been completed.
        created_at: Timestamp of when the todo was created (server-set).
    """

    __tablename__ = "todos"

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    title: str = Column(String(255), nullable=False)
    description: str | None = Column(String(1024), nullable=True)
    completed: bool = Column(Boolean, default=False, nullable=False)
    created_at: datetime = Column(DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self) -> str:
        """Return a developer-friendly string representation."""
        return (
            f"<Todo(id={self.id!r}, title={self.title!r}, "
            f"completed={self.completed!r})>"
        )
