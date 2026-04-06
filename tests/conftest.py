"""Shared pytest fixtures for the Todo backend test suite.

Provides an in-memory SQLite database, a fresh DB session per test,
and a FastAPI TestClient wired to use that session instead of the
production database.
"""

from __future__ import annotations

from typing import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base, get_db
from app.main import app
from app.models import Task, TaskStatus  # noqa: F401 – register models on Base

# In-memory SQLite engine shared across a single test via StaticPool
TEST_SQLALCHEMY_DATABASE_URL = "sqlite://"


@pytest.fixture(name="engine")
def fixture_engine():
    """Create a new in-memory SQLite engine for each test."""
    engine = create_engine(
        TEST_SQLALCHEMY_DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)
    engine.dispose()


@pytest.fixture(name="db_session")
def fixture_db_session(engine) -> Generator[Session, None, None]:
    """Yield a SQLAlchemy session bound to the in-memory engine."""
    TestingSessionLocal = sessionmaker(
        autocommit=False, autoflush=False, bind=engine
    )
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture(name="client")
def fixture_client(db_session: Session) -> Generator[TestClient, None, None]:
    """Provide a TestClient whose dependency on ``get_db`` is overridden.

    Every request made through this client will use the in-memory
    SQLite session so tests are fast and fully isolated.
    """

    def _override_get_db() -> Generator[Session, None, None]:
        """Yield the test database session."""
        try:
            yield db_session
        finally:
            pass  # session lifecycle managed by the fixture

    app.dependency_overrides[get_db] = _override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


@pytest.fixture(name="sample_task")
def fixture_sample_task(client: TestClient) -> dict:
    """Create and return a single task via the API for use in tests."""
    payload = {"title": "Sample task", "status": "todo", "due_date": "2025-12-31"}
    response = client.post("/tasks", json=payload)
    assert response.status_code == 201
    return response.json()
