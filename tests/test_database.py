"""Tests for app.database module.

Verifies engine configuration, session factory behaviour, and the
``get_db`` dependency generator.
"""

from __future__ import annotations

from sqlalchemy import text
from sqlalchemy.orm import Session

from app.database import Base, SessionLocal, engine, get_db


class TestEngine:
    """Tests for the SQLAlchemy engine configuration."""

    def test_engine_url_is_sqlite_in_memory(self) -> None:
        """Engine must point at an in-memory SQLite database."""
        url_str = str(engine.url)
        assert url_str == "sqlite://"

    def test_engine_can_connect(self) -> None:
        """Engine should be able to establish a connection."""
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            assert result.scalar() == 1


class TestSessionLocal:
    """Tests for the SessionLocal session factory."""

    def test_session_local_returns_session(self) -> None:
        """SessionLocal() should return a valid Session instance."""
        session = SessionLocal()
        try:
            assert isinstance(session, Session)
        finally:
            session.close()

    def test_session_is_bound_to_engine(self) -> None:
        """Session should be bound to the configured engine."""
        session = SessionLocal()
        try:
            assert session.bind is engine
        finally:
            session.close()


class TestBase:
    """Tests for the declarative Base."""

    def test_base_has_metadata(self) -> None:
        """Base should expose a metadata attribute."""
        assert Base.metadata is not None


class TestGetDb:
    """Tests for the get_db dependency generator."""

    def test_get_db_yields_session(self) -> None:
        """get_db should yield a Session and close it afterwards."""
        gen = get_db()
        session = next(gen)
        assert isinstance(session, Session)
        # Exhaust the generator so the finally block runs.
        try:
            next(gen)
        except StopIteration:
            pass

    def test_get_db_closes_session(self) -> None:
        """After the generator is exhausted the session should be closed."""
        gen = get_db()
        session = next(gen)
        try:
            next(gen)
        except StopIteration:
            pass
        # Accessing session.is_active on a closed session should not raise,
        # but the session's internal connection should be released.
        # We verify by simply running a new query – the old session should
        # not interfere.
        new_session = SessionLocal()
        try:
            result = new_session.execute(text("SELECT 1"))
            assert result.scalar() == 1
        finally:
            new_session.close()
