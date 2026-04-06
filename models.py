"""SQLAlchemy ORM models for the Kanban system.

Defines the following entities:
- Board: A kanban board with SEO metadata
- Column: A column within a board (e.g. "To Do", "In Progress", "Done")
- Card: A task card within a column
- Tag: A label/tag that can be applied to cards
- card_tags: Association table for the Card <-> Tag many-to-many relationship

All models use SQLAlchemy 2.0 declarative style with type-annotated columns.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import List, Optional

from sqlalchemy import (
    Column as SAColumn,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Table,
    Text,
    event,
)
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship,
)


def _utcnow() -> datetime:
    """Return the current UTC datetime.

    Returns:
        A timezone-aware datetime object representing the current UTC time.
    """
    return datetime.now(timezone.utc)


class Base(DeclarativeBase):
    """Declarative base class for all ORM models."""

    pass


# ---------------------------------------------------------------------------
# Association table for Card <-> Tag many-to-many
# ---------------------------------------------------------------------------

card_tags: Table = Table(
    "card_tags",
    Base.metadata,
    SAColumn(
        "card_id",
        Integer,
        ForeignKey("cards.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    SAColumn(
        "tag_id",
        Integer,
        ForeignKey("tags.id", ondelete="CASCADE"),
        primary_key=True,
    ),
)


# ---------------------------------------------------------------------------
# Board
# ---------------------------------------------------------------------------


class Board(Base):
    """A kanban board containing columns of cards.

    Attributes:
        id: Primary key.
        title: Display title of the board.
        slug: SEO-friendly URL slug (globally unique).
        description: Optional longer description.
        meta_title: Optional SEO title override (max ~70 chars).
        meta_description: Optional SEO description (max ~160 chars).
        created_at: Timestamp when the board was created.
        updated_at: Timestamp of the last update.
        columns: Relationship to child Column objects.
    """

    __tablename__ = "boards"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    slug: Mapped[str] = mapped_column(String(255), nullable=False, unique=True, index=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    meta_title: Mapped[Optional[str]] = mapped_column(String(70), nullable=True)
    meta_description: Mapped[Optional[str]] = mapped_column(String(160), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=_utcnow
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=_utcnow, onupdate=_utcnow
    )

    columns: Mapped[List["Column"]] = relationship(
        "Column",
        back_populates="board",
        cascade="all, delete-orphan",
        order_by="Column.position",
    )

    def __repr__(self) -> str:
        """Return a developer-friendly string representation."""
        return f"<Board(id={self.id}, slug={self.slug!r})>"


# ---------------------------------------------------------------------------
# Column
# ---------------------------------------------------------------------------


class Column(Base):
    """A column within a board that holds cards.

    Attributes:
        id: Primary key.
        board_id: Foreign key to the parent board.
        title: Display title of the column.
        position: Integer position for ordering (0-based).
        board: Relationship to the parent Board.
        cards: Relationship to child Card objects.
    """

    __tablename__ = "columns"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    board_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("boards.id", ondelete="CASCADE"), nullable=False
    )
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    position: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    board: Mapped["Board"] = relationship("Board", back_populates="columns")
    cards: Mapped[List["Card"]] = relationship(
        "Card",
        back_populates="column",
        cascade="all, delete-orphan",
        order_by="Card.position",
    )

    def __repr__(self) -> str:
        """Return a developer-friendly string representation."""
        return f"<Column(id={self.id}, title={self.title!r}, position={self.position})>"


# ---------------------------------------------------------------------------
# Card
# ---------------------------------------------------------------------------


class Card(Base):
    """A task card within a column.

    Attributes:
        id: Primary key.
        column_id: Foreign key to the parent column.
        title: Display title of the card.
        description: Optional detailed description.
        slug: SEO-friendly URL slug (globally unique).
        position: Integer position for ordering within the column (0-based).
        created_at: Timestamp when the card was created.
        updated_at: Timestamp of the last update.
        column: Relationship to the parent Column.
        tags: Many-to-many relationship to Tag objects via card_tags table.
    """

    __tablename__ = "cards"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    column_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("columns.id", ondelete="CASCADE"), nullable=False
    )
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    slug: Mapped[str] = mapped_column(String(255), nullable=False, unique=True, index=True)
    position: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=_utcnow
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=_utcnow, onupdate=_utcnow
    )

    column: Mapped["Column"] = relationship("Column", back_populates="cards")
    tags: Mapped[List["Tag"]] = relationship(
        "Tag",
        secondary=card_tags,
        back_populates="cards",
    )

    def __repr__(self) -> str:
        """Return a developer-friendly string representation."""
        return f"<Card(id={self.id}, slug={self.slug!r})>"


# ---------------------------------------------------------------------------
# Tag
# ---------------------------------------------------------------------------


class Tag(Base):
    """A label/tag that can be applied to cards.

    Attributes:
        id: Primary key.
        name: Display name of the tag.
        slug: SEO-friendly URL slug (globally unique).
        color: Hex color code for display (e.g. '#6b7280').
        cards: Many-to-many relationship to Card objects via card_tags table.
    """

    __tablename__ = "tags"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    slug: Mapped[str] = mapped_column(String(100), nullable=False, unique=True, index=True)
    color: Mapped[str] = mapped_column(String(7), nullable=False, default="#6b7280")

    cards: Mapped[List["Card"]] = relationship(
        "Card",
        secondary=card_tags,
        back_populates="tags",
    )

    def __repr__(self) -> str:
        """Return a developer-friendly string representation."""
        return f"<Tag(id={self.id}, name={self.name!r}, slug={self.slug!r})>"


# ---------------------------------------------------------------------------
# SQLite foreign key enforcement
# ---------------------------------------------------------------------------


@event.listens_for(Base.metadata, "after_create")
def _receive_after_create(target: Base.metadata, connection: object, **kwargs: object) -> None:
    """Placeholder event after table creation."""
    pass
