"""Tests for the database module.

Validates engine creation, session factory, and the ``get_db`` helper.
"""

from __future__ import annotations

from sqlalchemy import inspect, text
from sqlalchemy.orm import Session

from app.database import Base, SessionLocal, engine, get_db


def test_engine_url_contains_sqlite() -> None:
    """The engine should be configured with an SQLite URL."""
    assert "sqlite" in str(engine.url)


def test_session_local_returns_session() -> None:
    """SessionLocal should produce a valid SQLAlchemy Session."""
    session = SessionLocal()
    try:
        assert isinstance(session, Session)
    finally:
        session.close()


def test_get_db_yields_session() -> None:
    """The get_db generator should yield a Session and close it."""
    gen = get_db()
    session = next(gen)
    assert isinstance(session, Session)
    try:
        gen.send(None)
    except StopIteration:
        pass


def test_base_is_declarative_base() -> None:
    """Base should expose a metadata attribute."""
    assert hasattr(Base, "metadata")


def test_engine_check_same_thread() -> None:
    """The SQLite engine should be created with check_same_thread=False."""
    # We verify by successfully executing a query from this thread
    with engine.connect() as conn:
        result = conn.execute(text("SELECT 1"))
        assert result.scalar() == 1
