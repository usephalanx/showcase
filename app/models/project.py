"""Project model definition.

Represents a project entity which groups related tasks together.
"""

from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy import DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Project(Base):
    """SQLAlchemy model for the ``projects`` table.

    Attributes:
        id: Auto-incrementing primary key.
        name: Human-readable project name.
        description: Longer description of the project.
        created_at: UTC timestamp of when the project was created.
        tasks: One-to-many relationship with :class:`Task`.
    """

    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(String(1024), nullable=False, default="")
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )

    tasks = relationship("Task", back_populates="project", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        """Return developer-friendly string representation."""
        return f"<Project(id={self.id}, name={self.name!r})>"
