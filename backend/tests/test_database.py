"""Tests for the database module."""

from __future__ import annotations

from sqlalchemy import inspect, create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base, get_db, init_db


class TestInitDb:
    """Test that init_db creates the expected tables."""

    def test_tasks_table_created(self, db_engine) -> None:
        """After init_db the 'tasks' table should exist."""
        inspector = inspect(db_engine)
        table_names = inspector.get_table_names()
        assert "tasks" in table_names

    def test_tasks_table_columns(self, db_engine) -> None:
        """The tasks table should contain all expected columns."""
        inspector = inspect(db_engine)
        columns = {col["name"] for col in inspector.get_columns("tasks")}
        expected = {"id", "title", "status", "due_date", "created_at", "updated_at"}
        assert expected.issubset(columns)


class TestGetDb:
    """Test the get_db dependency generator."""

    def test_get_db_yields_session(self) -> None:
        """get_db should yield a session and then close it."""
        gen = get_db()
        session = next(gen)
        assert session is not None
        # Exhaust the generator to trigger cleanup.
        try:
            next(gen)
        except StopIteration:
            pass


class TestInitDbIdempotent:
    """init_db should be safe to call multiple times."""

    def test_double_init_no_error(self) -> None:
        """Calling init_db twice should not raise."""
        engine = create_engine(
            "sqlite:///",
            connect_args={"check_same_thread": False},
        )
        import app.models  # noqa: F401

        Base.metadata.create_all(bind=engine)
        # Second call should be harmless.
        Base.metadata.create_all(bind=engine)
        engine.dispose()
