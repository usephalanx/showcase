"""SQLAlchemy ORM models for the Kanban board application."""

from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


def _utcnow() -> datetime:
    """Return the current UTC datetime."""
    return datetime.now(timezone.utc)


class User(Base):
    """Application user account."""

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=_utcnow, nullable=False)

    boards: Mapped[list["Board"]] = relationship(
        "Board", back_populates="owner", cascade="all, delete-orphan"
    )


class Board(Base):
    """Kanban board belonging to a user."""

    __tablename__ = "boards"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=_utcnow, nullable=False)

    owner: Mapped["User"] = relationship("User", back_populates="boards")
    columns: Mapped[list["Column"]] = relationship(
        "Column", back_populates="board", cascade="all, delete-orphan", order_by="Column.position"
    )


class Column(Base):
    """A column within a board (e.g. 'To Do', 'In Progress', 'Done')."""

    __tablename__ = "columns"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    board_id: Mapped[int] = mapped_column(Integer, ForeignKey("boards.id", ondelete="CASCADE"), nullable=False, index=True)
    position: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    board: Mapped["Board"] = relationship("Board", back_populates="columns")
    cards: Mapped[list["Card"]] = relationship(
        "Card", back_populates="column", cascade="all, delete-orphan", order_by="Card.position"
    )


class Card(Base):
    """A card (task) within a column."""

    __tablename__ = "cards"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False, default="")
    column_id: Mapped[int] = mapped_column(Integer, ForeignKey("columns.id", ondelete="CASCADE"), nullable=False, index=True)
    position: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=_utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=_utcnow, onupdate=_utcnow, nullable=False)

    column: Mapped["Column"] = relationship("Column", back_populates="cards")
