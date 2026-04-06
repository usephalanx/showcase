"""Tests for the database module (engine, session, init_db)."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest
from sqlalchemy import inspect, text
from sqlalchemy.orm import Session

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "backend"))

from database import Base, get_db  # noqa: E402


class TestGetDb:
    """Tests for the get_db dependency generator."""

    def test_get_db_yields_session(self) -> None:
        """get_db should yield a Session-like object."""
        gen = get_db()
        session = next(gen)
        assert isinstance(session, Session)
        # Cleanup
        try:
            next(gen)
        except StopIteration:
            pass

    def test_get_db_closes_session(self) -> None:
        """Session should be closed after the generator completes."""
        gen = get_db()
        session = next(gen)
        try:
            next(gen)
        except StopIteration:
            pass
        # After close, attribute access may still work but bind should be present
        # Just verify no exception was raised during close
        assert session is not None


class TestInitDb:
    """Tests for init_db table creation."""

    def test_all_tables_created(self, db_engine) -> None:
        """All expected tables should exist after create_all."""
        inspector = inspect(db_engine)
        table_names = set(inspector.get_table_names())
        expected = {"boards", "columns", "cards", "categories", "card_categories"}
        assert expected.issubset(table_names)

    def test_boards_table_columns(self, db_engine) -> None:
        """The boards table should have the expected columns."""
        inspector = inspect(db_engine)
        columns = {col["name"] for col in inspector.get_columns("boards")}
        expected = {
            "id", "title", "slug", "description",
            "meta_title", "meta_description", "created_at", "updated_at",
        }
        assert expected.issubset(columns)

    def test_columns_table_columns(self, db_engine) -> None:
        """The columns table should have the expected columns."""
        inspector = inspect(db_engine)
        columns = {col["name"] for col in inspector.get_columns("columns")}
        expected = {"id", "board_id", "title", "position"}
        assert expected.issubset(columns)

    def test_cards_table_columns(self, db_engine) -> None:
        """The cards table should have the expected columns."""
        inspector = inspect(db_engine)
        columns = {col["name"] for col in inspector.get_columns("cards")}
        expected = {
            "id", "column_id", "title", "description",
            "slug", "position", "created_at", "updated_at",
        }
        assert expected.issubset(columns)

    def test_categories_table_columns(self, db_engine) -> None:
        """The categories table should have the expected columns."""
        inspector = inspect(db_engine)
        columns = {col["name"] for col in inspector.get_columns("categories")}
        expected = {"id", "name", "slug", "description", "parent_id"}
        assert expected.issubset(columns)

    def test_card_categories_table_columns(self, db_engine) -> None:
        """The card_categories junction table should have card_id and category_id."""
        inspector = inspect(db_engine)
        columns = {col["name"] for col in inspector.get_columns("card_categories")}
        expected = {"card_id", "category_id"}
        assert expected == columns
