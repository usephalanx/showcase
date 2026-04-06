"""Pytest fixtures for Kanban backend tests.

Provides an in-memory SQLite database, test session, and FastAPI
test client with dependency overrides.
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

# Ensure backend package is importable
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "backend"))

from database import Base, get_db  # noqa: E402
from main import app  # noqa: E402
import models  # noqa: E402, F401 — register models with Base


TEST_DATABASE_URL = "sqlite:///"

test_engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
)

TestSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=test_engine,
)


@pytest.fixture(autouse=True)
def setup_database() -> Generator[None, None, None]:
    """Create all tables before each test and drop them after.

    Yields:
        Control to the test function.
    """
    Base.metadata.create_all(bind=test_engine)
    yield
    Base.metadata.drop_all(bind=test_engine)


@pytest.fixture()
def db_session() -> Generator[Session, None, None]:
    """Provide a transactional database session for tests.

    Yields:
        A SQLAlchemy session bound to the test database.
    """
    session = TestSessionLocal()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture()
def client(db_session: Session) -> Generator[TestClient, None, None]:
    """Provide a FastAPI TestClient with the test DB session injected.

    Args:
        db_session: The test database session fixture.

    Yields:
        A TestClient instance.
    """

    def _override_get_db() -> Generator[Session, None, None]:
        """Override the get_db dependency to use the test session."""
        yield db_session

    app.dependency_overrides[get_db] = _override_get_db
    with TestClient(app) as tc:
        yield tc
    app.dependency_overrides.clear()
