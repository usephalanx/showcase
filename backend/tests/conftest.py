"""Shared pytest fixtures for Kanban backend tests.

Provides an in-memory SQLite database and a FastAPI TestClient that
uses the test database session.
"""

from __future__ import annotations

from typing import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from database import Base, get_db
from main import app

SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///"

test_engine = create_engine(
    SQLALCHEMY_TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
)

TestSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=test_engine,
)


@pytest.fixture(autouse=True)
def setup_database() -> Generator[None, None, None]:
    """Create all tables before each test and drop them afterwards."""
    import models as _models  # noqa: F401 — register models

    Base.metadata.create_all(bind=test_engine)
    yield
    Base.metadata.drop_all(bind=test_engine)


@pytest.fixture()
def db_session() -> Generator[Session, None, None]:
    """Yield a database session scoped to a single test."""
    session = TestSessionLocal()
    try:
        yield session
    finally:
        session.close()


def _override_get_db() -> Generator[Session, None, None]:
    """Dependency override that yields test sessions."""
    session = TestSessionLocal()
    try:
        yield session
    finally:
        session.close()


app.dependency_overrides[get_db] = _override_get_db


@pytest.fixture()
def client() -> Generator[TestClient, None, None]:
    """Yield a FastAPI TestClient configured with the test database."""
    with TestClient(app, raise_server_exceptions=True) as c:
        yield c
