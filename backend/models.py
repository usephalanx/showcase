"""SQLAlchemy ORM models for the Kanban application.

Models
------
- Board   : A Kanban board containing columns.
- Column  : A column within a board, holding cards.
- Card    : A task card within a column.
- Category: A hierarchical taxonomy for cards (self-referential).
- card_categories: Junction table linking cards to categories.
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
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


def _utcnow() -> datetime:
    """Return the current UTC time as a timezone-aware datetime."""
    return datetime.now(timezone.utc)


# ---------------------------------------------------------------------------
# Junction table: Card <-> Category (many-to-many)
# ---------------------------------------------------------------------------

card_categories = Table(
    "card_categories",
    Base.metadata,
    SAColumn("card_id", Integer, ForeignKey("cards.id", ondelete="CASCADE"), primary_key=True),
    SAColumn("category_id", Integer, ForeignKey("categories.id", ondelete="CASCADE"), primary_key=True),
)


# ---------------------------------------------------------------------------
# Board
# ---------------------------------------------------------------------------


class Board(Base):
    """A Kanban board that contains columns.

    Attributes:
        id: Primary key.
        title: Human-readable board title.
        slug: SEO-friendly URL slug (unique).
        description: Optional long description.
        meta_title: Optional SEO meta title override.
        meta_description: Optional SEO meta description override.
        created_at: Timestamp of creation (UTC).
        updated_at: Timestamp of last update (UTC).
        columns: Related Column objects (ordered by position).
    """

    __tablename__ = "boards"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    slug: Mapped[str] = mapped_column(String(280), nullable=False, unique=True, index=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    meta_title: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    meta_description: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=_utcnow, index=True,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=_utcnow, onupdate=_utcnow,
    )

    columns: Mapped[List["Column"]] = relationship(
        "Column",
        back_populates="board",
        cascade="all, delete-orphan",
        order_by="Column.position",
        passive_deletes=True,
    )

    def __repr__(self) -> str:
        """Return developer-friendly string representation."""
        return f"<Board(id={self.id}, slug='{self.slug}')>"


# ---------------------------------------------------------------------------
# Column
# ---------------------------------------------------------------------------


class Column(Base):
    """A column within a Kanban board.

    Attributes:
        id: Primary key.
        board_id: Foreign key to the parent board.
        title: Column heading.
        position: Ordering position within the board.
        created_at: Timestamp of creation (UTC).
        updated_at: Timestamp of last update (UTC).
        board: Parent Board object.
        cards: Related Card objects (ordered by position).
    """

    __tablename__ = "columns"
    __table_args__ = (
        UniqueConstraint("board_id", "position", name="uq_column_board_position"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    board_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("boards.id", ondelete="CASCADE"), nullable=False, index=True,
    )
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    position: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=_utcnow,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=_utcnow, onupdate=_utcnow,
    )

    board: Mapped["Board"] = relationship("Board", back_populates="columns")
    cards: Mapped[List["Card"]] = relationship(
        "Card",
        back_populates="column",
        cascade="all, delete-orphan",
        order_by="Card.position",
        passive_deletes=True,
    )

    def __repr__(self) -> str:
        """Return developer-friendly string representation."""
        return f"<Column(id={self.id}, title='{self.title}', position={self.position})>"


# ---------------------------------------------------------------------------
# Card
# ---------------------------------------------------------------------------


class Card(Base):
    """A task card within a column.

    Attributes:
        id: Primary key.
        column_id: Foreign key to the parent column.
        title: Card title.
        description: Optional rich-text description.
        position: Ordering position within the column.
        created_at: Timestamp of creation (UTC).
        updated_at: Timestamp of last update (UTC).
        column: Parent Column object.
        categories: Associated Category objects.
    """

    __tablename__ = "cards"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    column_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("columns.id", ondelete="CASCADE"), nullable=False, index=True,
    )
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    position: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=_utcnow,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=_utcnow, onupdate=_utcnow,
    )

    column: Mapped["Column"] = relationship("Column", back_populates="cards")
    categories: Mapped[List["Category"]] = relationship(
        "Category",
        secondary=card_categories,
        back_populates="cards",
    )

    def __repr__(self) -> str:
        """Return developer-friendly string representation."""
        return f"<Card(id={self.id}, title='{self.title}')>"


# ---------------------------------------------------------------------------
# Category
# ---------------------------------------------------------------------------


class Category(Base):
    """A hierarchical taxonomy category for cards.

    Attributes:
        id: Primary key.
        name: Category display name.
        slug: SEO-friendly URL slug (unique).
        parent_id: Optional self-referential FK for nesting.
        created_at: Timestamp of creation (UTC).
        updated_at: Timestamp of last update (UTC).
        parent: Parent Category (if nested).
        children: Child Category objects.
        cards: Associated Card objects.
    """

    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    slug: Mapped[str] = mapped_column(String(280), nullable=False, unique=True, index=True)
    parent_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("categories.id", ondelete="SET NULL"), nullable=True,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=_utcnow,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=_utcnow, onupdate=_utcnow,
    )

    parent: Mapped[Optional["Category"]] = relationship(
        "Category",
        remote_side="Category.id",
        back_populates="children",
    )
    children: Mapped[List["Category"]] = relationship(
        "Category",
        back_populates="parent",
        cascade="all, delete-orphan",
    )
    cards: Mapped[List["Card"]] = relationship(
        "Card",
        secondary=card_categories,
        back_populates="categories",
    )

    def __repr__(self) -> str:
        """Return developer-friendly string representation."""
        return f"<Category(id={self.id}, slug='{self.slug}')>"
