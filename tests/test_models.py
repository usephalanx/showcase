"""Tests for SQLAlchemy ORM models.

Covers creation, relationships, constraints, cascading deletes,
and the many-to-many Card <-> Category association.
"""

from __future__ import annotations

from datetime import datetime, timezone

import pytest
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

import models


# -----------------------------------------------------------------------
# Board tests
# -----------------------------------------------------------------------


class TestBoard:
    """Tests for the Board model."""

    def test_create_board(self, db_session: Session) -> None:
        """A board can be created with all fields."""
        board = models.Board(
            title="My Board",
            slug="my-board",
            description="Desc",
            meta_title="MT",
            meta_description="MD",
        )
        db_session.add(board)
        db_session.commit()

        assert board.id is not None
        assert board.title == "My Board"
        assert board.slug == "my-board"
        assert board.description == "Desc"
        assert board.meta_title == "MT"
        assert board.meta_description == "MD"

    def test_board_timestamps(self, sample_board: models.Board) -> None:
        """Board should have created_at and updated_at timestamps."""
        assert isinstance(sample_board.created_at, datetime)
        assert isinstance(sample_board.updated_at, datetime)

    def test_board_slug_unique(self, db_session: Session, sample_board: models.Board) -> None:
        """Duplicate slugs raise IntegrityError."""
        dup = models.Board(title="Dup", slug=sample_board.slug)
        db_session.add(dup)
        with pytest.raises(IntegrityError):
            db_session.commit()

    def test_board_repr(self, sample_board: models.Board) -> None:
        """Board repr includes id and slug."""
        r = repr(sample_board)
        assert "Board" in r
        assert sample_board.slug in r

    def test_board_optional_fields(self, db_session: Session) -> None:
        """Board can be created without optional fields."""
        board = models.Board(title="Minimal", slug="minimal")
        db_session.add(board)
        db_session.commit()

        assert board.description is None
        assert board.meta_title is None
        assert board.meta_description is None


# -----------------------------------------------------------------------
# Column tests
# -----------------------------------------------------------------------


class TestColumn:
    """Tests for the Column model."""

    def test_create_column(self, db_session: Session, sample_board: models.Board) -> None:
        """A column can be created and linked to a board."""
        col = models.Column(board_id=sample_board.id, title="In Progress", position=1)
        db_session.add(col)
        db_session.commit()

        assert col.id is not None
        assert col.board_id == sample_board.id
        assert col.title == "In Progress"
        assert col.position == 1

    def test_column_board_relationship(self, db_session: Session, sample_column: models.Column, sample_board: models.Board) -> None:
        """Column.board should reference the parent Board."""
        assert sample_column.board.id == sample_board.id

    def test_board_columns_relationship(self, db_session: Session, sample_board: models.Board) -> None:
        """Board.columns should contain added columns in position order."""
        col_a = models.Column(board_id=sample_board.id, title="A", position=1)
        col_b = models.Column(board_id=sample_board.id, title="B", position=0)
        db_session.add_all([col_a, col_b])
        db_session.commit()
        db_session.refresh(sample_board)

        titles = [c.title for c in sample_board.columns]
        assert titles == ["B", "A"]

    def test_column_unique_position_per_board(
        self, db_session: Session, sample_column: models.Column, sample_board: models.Board,
    ) -> None:
        """Two columns in the same board cannot share a position."""
        dup = models.Column(
            board_id=sample_board.id, title="Dup", position=sample_column.position,
        )
        db_session.add(dup)
        with pytest.raises(IntegrityError):
            db_session.commit()

    def test_column_repr(self, sample_column: models.Column) -> None:
        """Column repr includes title and position."""
        r = repr(sample_column)
        assert "Column" in r
        assert sample_column.title in r


# -----------------------------------------------------------------------
# Card tests
# -----------------------------------------------------------------------


class TestCard:
    """Tests for the Card model."""

    def test_create_card(self, db_session: Session, sample_column: models.Column) -> None:
        """A card can be created with all fields."""
        card = models.Card(
            column_id=sample_column.id,
            title="New Card",
            description="Details",
            slug="new-card",
            position=0,
        )
        db_session.add(card)
        db_session.commit()

        assert card.id is not None
        assert card.slug == "new-card"

    def test_card_timestamps(self, sample_card: models.Card) -> None:
        """Card should have created_at and updated_at timestamps."""
        assert isinstance(sample_card.created_at, datetime)
        assert isinstance(sample_card.updated_at, datetime)

    def test_card_slug_unique(self, db_session: Session, sample_card: models.Card, sample_column: models.Column) -> None:
        """Duplicate card slugs raise IntegrityError."""
        dup = models.Card(
            column_id=sample_column.id,
            title="Dup",
            slug=sample_card.slug,
            position=1,
        )
        db_session.add(dup)
        with pytest.raises(IntegrityError):
            db_session.commit()

    def test_card_column_relationship(self, sample_card: models.Card, sample_column: models.Column) -> None:
        """Card.column should point to the parent column."""
        assert sample_card.column.id == sample_column.id

    def test_column_cards_relationship(
        self, db_session: Session, sample_column: models.Column,
    ) -> None:
        """Column.cards should contain cards ordered by position."""
        card_b = models.Card(column_id=sample_column.id, title="B", slug="b", position=2)
        card_a = models.Card(column_id=sample_column.id, title="A", slug="a", position=1)
        db_session.add_all([card_b, card_a])
        db_session.commit()
        db_session.refresh(sample_column)

        slugs = [c.slug for c in sample_column.cards]
        assert slugs == ["a", "b"]

    def test_card_repr(self, sample_card: models.Card) -> None:
        """Card repr includes slug."""
        r = repr(sample_card)
        assert "Card" in r
        assert sample_card.slug in r


# -----------------------------------------------------------------------
# Category tests
# -----------------------------------------------------------------------


class TestCategory:
    """Tests for the Category model."""

    def test_create_category(self, db_session: Session) -> None:
        """A category can be created with all fields."""
        cat = models.Category(name="Feature", slug="feature", description="Features")
        db_session.add(cat)
        db_session.commit()

        assert cat.id is not None
        assert cat.name == "Feature"
        assert cat.slug == "feature"

    def test_category_slug_unique(self, db_session: Session, sample_category: models.Category) -> None:
        """Duplicate category slugs raise IntegrityError."""
        dup = models.Category(name="Dup", slug=sample_category.slug)
        db_session.add(dup)
        with pytest.raises(IntegrityError):
            db_session.commit()

    def test_category_hierarchy(self, db_session: Session, sample_category: models.Category) -> None:
        """A category can have a parent."""
        child = models.Category(
            name="UI Bug", slug="ui-bug", parent_id=sample_category.id,
        )
        db_session.add(child)
        db_session.commit()
        db_session.refresh(child)
        db_session.refresh(sample_category)

        assert child.parent_id == sample_category.id
        assert child.parent.id == sample_category.id
        assert any(c.id == child.id for c in sample_category.children)

    def test_category_deep_hierarchy(self, db_session: Session) -> None:
        """Categories can be nested multiple levels."""
        root = models.Category(name="Root", slug="root")
        db_session.add(root)
        db_session.commit()

        parent = root
        for i in range(1, 5):
            child = models.Category(
                name=f"Level-{i}", slug=f"level-{i}", parent_id=parent.id,
            )
            db_session.add(child)
            db_session.commit()
            parent = child

        # Walk up from deepest
        current = parent
        depth = 0
        while current.parent_id is not None:
            current = current.parent
            depth += 1
        assert depth == 4

    def test_category_repr(self, sample_category: models.Category) -> None:
        """Category repr includes slug."""
        r = repr(sample_category)
        assert "Category" in r
        assert sample_category.slug in r


# -----------------------------------------------------------------------
# Card <-> Category many-to-many
# -----------------------------------------------------------------------


class TestCardCategory:
    """Tests for the Card-Category many-to-many relationship."""

    def test_assign_category_to_card(
        self, db_session: Session, sample_card: models.Card, sample_category: models.Category,
    ) -> None:
        """A category can be added to a card."""
        sample_card.categories.append(sample_category)
        db_session.commit()
        db_session.refresh(sample_card)

        assert sample_category in sample_card.categories

    def test_card_accessible_from_category(
        self, db_session: Session, sample_card: models.Card, sample_category: models.Category,
    ) -> None:
        """A card can be accessed from its category's cards list."""
        sample_card.categories.append(sample_category)
        db_session.commit()
        db_session.refresh(sample_category)

        assert sample_card in sample_category.cards

    def test_multiple_categories_per_card(
        self, db_session: Session, sample_card: models.Card, sample_category: models.Category,
    ) -> None:
        """A card can belong to multiple categories."""
        cat2 = models.Category(name="Enhancement", slug="enhancement")
        db_session.add(cat2)
        db_session.commit()

        sample_card.categories.extend([sample_category, cat2])
        db_session.commit()
        db_session.refresh(sample_card)

        assert len(sample_card.categories) == 2

    def test_remove_category_from_card(
        self, db_session: Session, sample_card: models.Card, sample_category: models.Category,
    ) -> None:
        """Removing a category from a card does not delete the category."""
        sample_card.categories.append(sample_category)
        db_session.commit()

        sample_card.categories.remove(sample_category)
        db_session.commit()
        db_session.refresh(sample_card)

        assert sample_category not in sample_card.categories
        # Category still exists
        cat = db_session.get(models.Category, sample_category.id)
        assert cat is not None


# -----------------------------------------------------------------------
# Cascade delete tests
# -----------------------------------------------------------------------


class TestCascadeDelete:
    """Tests for cascade delete behaviour."""

    def test_delete_board_cascades_to_columns(
        self, db_session: Session, sample_board: models.Board, sample_column: models.Column,
    ) -> None:
        """Deleting a board removes its columns."""
        col_id = sample_column.id
        db_session.delete(sample_board)
        db_session.commit()

        assert db_session.get(models.Column, col_id) is None

    def test_delete_board_cascades_to_cards(
        self, db_session: Session, sample_board: models.Board, sample_card: models.Card,
    ) -> None:
        """Deleting a board removes its columns' cards."""
        card_id = sample_card.id
        db_session.delete(sample_board)
        db_session.commit()

        assert db_session.get(models.Card, card_id) is None

    def test_delete_column_cascades_to_cards(
        self, db_session: Session, sample_column: models.Column, sample_card: models.Card,
    ) -> None:
        """Deleting a column removes its cards."""
        card_id = sample_card.id
        db_session.delete(sample_column)
        db_session.commit()

        assert db_session.get(models.Card, card_id) is None

    def test_delete_card_removes_junction_rows(
        self,
        db_session: Session,
        sample_card: models.Card,
        sample_category: models.Category,
    ) -> None:
        """Deleting a card removes card_categories rows but not the category."""
        sample_card.categories.append(sample_category)
        db_session.commit()

        cat_id = sample_category.id
        db_session.delete(sample_card)
        db_session.commit()

        # Category still exists
        assert db_session.get(models.Category, cat_id) is not None

    def test_delete_category_removes_junction_rows(
        self,
        db_session: Session,
        sample_card: models.Card,
        sample_category: models.Category,
    ) -> None:
        """Deleting a category removes card_categories rows but not the card."""
        sample_card.categories.append(sample_category)
        db_session.commit()

        card_id = sample_card.id
        db_session.delete(sample_category)
        db_session.commit()

        # Card still exists
        card = db_session.get(models.Card, card_id)
        assert card is not None
        assert len(card.categories) == 0
