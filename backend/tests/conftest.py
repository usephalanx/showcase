"""Shared pytest fixtures for backend tests.

Provides an in-memory SQLite database, a session factory, and a
FastAPI test client that overrides the production database dependency.
"""

from __future__ import annotations

from typing import Generator

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.database import Base, get_db
from app.main import app

# Use an in-memory SQLite database for tests.
TEST_DATABASE_URL = "sqlite:///"

test_engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
)

TestSessionLocal: sessionmaker[Session] = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=test_engine,
)


@pytest.fixture(autouse=True)
def setup_database() -> Generator[None, None, None]:
    """Create all tables before each test and drop them afterwards."""
    import app.models  # noqa: F401 – register models

    Base.metadata.create_all(bind=test_engine)
    yield
    Base.metadata.drop_all(bind=test_engine)


@pytest.fixture()
def db_session() -> Generator[Session, None, None]:
    """Yield a test database session and rollback after the test."""
    session = TestSessionLocal()
    try:
        yield session
    finally:
        session.rollback()
        session.close()


@pytest.fixture()
def client(db_session: Session) -> Generator:
    """Provide a TestClient whose DB dependency is overridden."""
    from fastapi.testclient import TestClient

    def _override_get_db() -> Generator[Session, None, None]:
        """Yield the test session instead of the production one."""
        yield db_session

    app.dependency_overrides[get_db] = _override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


@pytest.fixture()
def auth_headers(client) -> dict[str, str]:  # type: ignore[type-arg]
    """Register a test user, log in, and return Authorization headers."""
    client.post(
        "/auth/register",
        json={"username": "testuser", "password": "testpassword123"},
    )
    response = client.post(
        "/auth/login",
        json={"username": "testuser", "password": "testpassword123"},
    )
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}
