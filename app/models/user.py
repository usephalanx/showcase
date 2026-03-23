"""User model definition.

Represents a user entity for authentication and authorisation.
"""

from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy import DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class User(Base):
    """SQLAlchemy model for the ``users`` table.

    Attributes:
        id: Auto-incrementing primary key.
        username: Unique username for authentication.
        hashed_password: Bcrypt-hashed password string.
        created_at: UTC timestamp of when the user was created.
    """

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(
        String(150), unique=True, nullable=False, index=True
    )
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )

    def __repr__(self) -> str:
        """Return developer-friendly string representation."""
        return f"<User(id={self.id}, username={self.username!r})>"
