"""Shared test fixtures for the Kanban backend test suite.

Provides an in-memory SQLite database, a fresh session, and a
pre-configured FastAPI TestClient for each test function.
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

# Ensure backend package is on the path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "backend"))

from database import Base, get_db  # noqa: E402
from main import app  # noqa: E402
import models  # noqa: E402, F401 — register models

SQLALCHEMY_DATABASE_URL = "sqlite:///"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
)
TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


@pytest.fixture(autouse=True)
def _setup_database() -> Generator[None, None, None]:
    """Create all tables before each test and drop them after."""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture()
def db_session() -> Generator[Session, None, None]:
    """Provide a transactional database session for a test."""
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture()
def client(db_session: Session) -> Generator[TestClient, None, None]:
    """Provide a TestClient that uses the test database session."""

    def _override_get_db() -> Generator[Session, None, None]:
        """Yield the test-scoped database session."""
        yield db_session

    app.dependency_overrides[get_db] = _override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()
