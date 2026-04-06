"""Shared test fixtures."""

from __future__ import annotations

from typing import Generator

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.database import Base

# Use an in-memory SQLite database for tests.
TEST_DATABASE_URL = "sqlite:///"


@pytest.fixture()
def db_engine():
    """Create a fresh in-memory SQLAlchemy engine for each test."""
    engine = create_engine(
        TEST_DATABASE_URL,
        connect_args={"check_same_thread": False},
    )
    # Ensure all models are registered.
    import app.models  # noqa: F401

    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)
    engine.dispose()


@pytest.fixture()
def db_session(db_engine) -> Generator[Session, None, None]:
    """Yield a transactional database session that is rolled back after use."""
    testing_session_local = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=db_engine,
    )
    session = testing_session_local()
    try:
        yield session
    finally:
        session.rollback()
        session.close()
