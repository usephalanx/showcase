"""Shared test fixtures for the Todo application test suite.

Provides an in-memory SQLite database, a test DB session, and a
pre-configured ``TestClient`` that overrides the production DB
dependency so no real database is touched during tests.
"""

from __future__ import annotations

from typing import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from backend.database import Base, get_db
from backend.main import app

SQLALCHEMY_DATABASE_URL = "sqlite:///"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
)

TestingSessionLocal: sessionmaker[Session] = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


@pytest.fixture(autouse=True)
def setup_database() -> Generator[None, None, None]:
    """Create all tables before each test and drop them afterwards."""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture()
def db_session() -> Generator[Session, None, None]:
    """Yield a SQLAlchemy session connected to the test database."""
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture()
def client(db_session: Session) -> Generator[TestClient, None, None]:
    """Yield a FastAPI TestClient with the DB dependency overridden."""

    def _override_get_db() -> Generator[Session, None, None]:
        """Provide the test session instead of the production session."""
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = _override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()
