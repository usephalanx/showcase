"""Shared pytest fixtures for the test suite.

Provides an in-memory SQLite database, session, and helper factories
that every test module can use.
"""

from __future__ import annotations

from typing import Generator

import pytest
from sqlalchemy import create_engine, event
from sqlalchemy.orm import Session, sessionmaker

from backend.app.database import Base

# We must import models so that Base.metadata knows about them.
import backend.app.models  # noqa: F401


@pytest.fixture(name="engine")
def fixture_engine():
    """Create an in-memory SQLite engine with foreign key support."""
    eng = create_engine("sqlite:///:memory:")

    @event.listens_for(eng, "connect")
    def _enable_fk(dbapi_connection, _connection_record):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON;")
        cursor.close()

    Base.metadata.create_all(bind=eng)
    return eng


@pytest.fixture(name="db")
def fixture_db(engine) -> Generator[Session, None, None]:
    """Yield a transactional SQLAlchemy session that is rolled back after each test."""
    _SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = _SessionLocal()
    try:
        yield session
    finally:
        session.rollback()
        session.close()
