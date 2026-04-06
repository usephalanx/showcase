"""Tests for database connection setup, initialization, and session management."""

from __future__ import annotations

from typing import Generator

import pytest
from sqlalchemy import create_engine, event, inspect, text
from sqlalchemy.orm import Session, sessionmaker

from models import Base, Board


@pytest.fixture()
def memory_engine():
    """Create an in-memory SQLite engine with foreign keys enabled."""
    engine = create_engine("sqlite:///:memory:", echo=False)

    @event.listens_for(engine, "connect")
    def _set_pragma(dbapi_conn, rec):
        """Enable foreign keys and WAL mode for in-memory DB."""
        cursor = dbapi_conn.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()

    return engine


class TestDatabaseInit:
    """Tests for database initialization and schema creation."""

    def test_create_all_creates_tables(self, memory_engine) -> None:
        """Test that Base.metadata.create_all creates all expected tables."""
        Base.metadata.create_all(bind=memory_engine)
        inspector = inspect(memory_engine)
        tables = inspector.get_table_names()

        assert "boards" in tables
        assert "columns" in tables
        assert "cards" in tables
        assert "tags" in tables
        assert "card_tags" in tables

    def test_create_all_idempotent(self, memory_engine) -> None:
        """Test that calling create_all twice doesn't raise errors."""
        Base.metadata.create_all(bind=memory_engine)
        Base.metadata.create_all(bind=memory_engine)
        inspector = inspect(memory_engine)
        tables = inspector.get_table_names()
        assert "boards" in tables

    def test_boards_table_columns(self, memory_engine) -> None:
        """Test that the boards table has the correct columns."""
        Base.metadata.create_all(bind=memory_engine)
        inspector = inspect(memory_engine)
        columns = {col["name"] for col in inspector.get_columns("boards")}

        expected = {
            "id", "title", "slug", "description",
            "meta_title", "meta_description",
            "created_at", "updated_at",
        }
        assert expected.issubset(columns)

    def test_columns_table_columns(self, memory_engine) -> None:
        """Test that the columns table has the correct columns."""
        Base.metadata.create_all(bind=memory_engine)
        inspector = inspect(memory_engine)
        columns = {col["name"] for col in inspector.get_columns("columns")}

        expected = {"id", "board_id", "title", "position"}
        assert expected.issubset(columns)

    def test_cards_table_columns(self, memory_engine) -> None:
        """Test that the cards table has the correct columns."""
        Base.metadata.create_all(bind=memory_engine)
        inspector = inspect(memory_engine)
        columns = {col["name"] for col in inspector.get_columns("cards")}

        expected = {
            "id", "column_id", "title", "description",
            "slug", "position", "created_at", "updated_at",
        }
        assert expected.issubset(columns)

    def test_tags_table_columns(self, memory_engine) -> None:
        """Test that the tags table has the correct columns."""
        Base.metadata.create_all(bind=memory_engine)
        inspector = inspect(memory_engine)
        columns = {col["name"] for col in inspector.get_columns("tags")}

        expected = {"id", "name", "slug", "color"}
        assert expected.issubset(columns)

    def test_card_tags_table_columns(self, memory_engine) -> None:
        """Test that the card_tags association table has the correct columns."""
        Base.metadata.create_all(bind=memory_engine)
        inspector = inspect(memory_engine)
        columns = {col["name"] for col in inspector.get_columns("card_tags")}

        expected = {"card_id", "tag_id"}
        assert expected.issubset(columns)


class TestForeignKeyEnforcement:
    """Tests that foreign key constraints are enforced."""

    def test_foreign_keys_enabled(self, memory_engine) -> None:
        """Test that PRAGMA foreign_keys is ON."""
        Base.metadata.create_all(bind=memory_engine)
        with memory_engine.connect() as conn:
            result = conn.execute(text("PRAGMA foreign_keys"))
            value = result.scalar()
            assert value == 1


class TestSessionFactory:
    """Tests for session factory behavior."""

    def test_session_can_add_and_query(self, memory_engine) -> None:
        """Test that a session created from the engine works for CRUD."""
        Base.metadata.create_all(bind=memory_engine)
        TestSession = sessionmaker(bind=memory_engine)
        session = TestSession()

        board = Board(title="Test", slug="test")
        session.add(board)
        session.commit()

        result = session.query(Board).filter_by(slug="test").first()
        assert result is not None
        assert result.title == "Test"
        session.close()


class TestArchitectureDocumentation:
    """Tests that architecture documentation files exist and are complete."""

    def test_architecture_md_exists(self) -> None:
        """Verify ARCHITECTURE.md exists at repo root and is non-empty."""
        from pathlib import Path
        arch_path = Path("ARCHITECTURE.md")
        assert arch_path.exists(), "ARCHITECTURE.md does not exist"
        content = arch_path.read_text(encoding="utf-8")
        assert len(content) > 100, "ARCHITECTURE.md is too short"

    def test_architecture_has_all_sections(self) -> None:
        """Parse ARCHITECTURE.md and assert it contains all required sections."""
        from pathlib import Path
        content = Path("ARCHITECTURE.md").read_text(encoding="utf-8")

        required_sections = [
            "Tech Stack",
            "Data Models",
            "API Endpoints",
            "URL Structure",
            "Meta Tag Strategy",
            "Frontend Component Tree",
            "Database Schema",
            "Directory Structure",
        ]

        for section in required_sections:
            assert section in content, (
                f"ARCHITECTURE.md is missing required section: {section}"
            )

    def test_running_md_exists(self) -> None:
        """Verify RUNNING.md exists at repo root and is non-empty."""
        from pathlib import Path
        running_path = Path("RUNNING.md")
        assert running_path.exists(), "RUNNING.md does not exist"
        content = running_path.read_text(encoding="utf-8")
        assert len(content) > 50, "RUNNING.md is too short"
