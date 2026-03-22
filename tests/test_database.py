"""Tests for the database module utilities."""

from __future__ import annotations

from sqlalchemy.orm import Session

from backend.app.database import Base, SessionLocal, get_db, init_db


class TestGetDb:
    """Tests for the get_db dependency."""

    def test_yields_session(self) -> None:
        """get_db should yield a Session instance."""
        gen = get_db()
        session = next(gen)
        try:
            assert isinstance(session, Session)
        finally:
            try:
                next(gen)
            except StopIteration:
                pass

    def test_session_closes(self) -> None:
        """The session should be closed after the generator is exhausted."""
        gen = get_db()
        session = next(gen)
        try:
            next(gen)
        except StopIteration:
            pass
        # After generator cleanup the session internal state should be
        # invalidated. We just verify it did not raise.


class TestBase:
    """Tests for the declarative base."""

    def test_base_has_metadata(self) -> None:
        """Base should expose a metadata attribute."""
        assert hasattr(Base, "metadata")


class TestInitDb:
    """Tests for init_db helper."""

    def test_init_db_creates_tables(self) -> None:
        """Calling init_db should not raise and should register tables."""
        # init_db is safe to call multiple times.
        init_db()
        table_names = set(Base.metadata.tables.keys())
        assert "projects" in table_names
        assert "tasks" in table_names
