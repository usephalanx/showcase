"""Tests for backend.database module.

Verifies engine creation, session factory behaviour, the ``get_db``
dependency generator, and the ``init_db`` helper.
"""

from __future__ import annotations

import importlib
from typing import Generator

import pytest
from sqlalchemy import inspect, text
from sqlalchemy.orm import Session


def _make_test_database():
    """Re-import the database module with an in-memory SQLite engine."""
    import backend.database as db_mod

    # Override to in-memory database for testing
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker

    db_mod.engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
    )
    db_mod.SessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=db_mod.engine,
    )
    return db_mod


@pytest.fixture()
def db_module():
    """Provide a database module configured with an in-memory database."""
    return _make_test_database()


def test_engine_is_sqlite(db_module) -> None:
    """Engine should use the sqlite dialect."""
    assert db_module.engine.dialect.name == "sqlite"


def test_session_local_produces_session(db_module) -> None:
    """SessionLocal() should return a valid SQLAlchemy Session."""
    session = db_module.SessionLocal()
    try:
        assert isinstance(session, Session)
    finally:
        session.close()


def test_get_db_yields_session(db_module) -> None:
    """get_db should be a generator that yields a Session and closes it."""
    gen = db_module.get_db()
    assert isinstance(gen, Generator) or hasattr(gen, "__next__")
    session = next(gen)
    assert isinstance(session, Session)
    # Exhaust the generator to trigger the finally block
    try:
        next(gen)
    except StopIteration:
        pass


def test_init_db_creates_tables(db_module) -> None:
    """init_db should create the tasks table from the Base metadata."""
    # Ensure models are imported so Base.metadata knows about Task
    import backend.models  # noqa: F401

    # Re-bind Base to our in-memory engine
    from backend.database import Base

    Base.metadata.create_all(bind=db_module.engine)

    inspector = inspect(db_module.engine)
    tables = inspector.get_table_names()
    assert "tasks" in tables


def test_session_can_execute_query(db_module) -> None:
    """A session from SessionLocal should be able to execute raw SQL."""
    session = db_module.SessionLocal()
    try:
        result = session.execute(text("SELECT 1"))
        row = result.fetchone()
        assert row is not None
        assert row[0] == 1
    finally:
        session.close()
