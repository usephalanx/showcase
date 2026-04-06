"""Shared test fixtures for the Kanban backend test suite."""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Generator

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

# Make the backend package importable from the tests directory.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "backend"))

from database import Base  # noqa: E402
import models  # noqa: E402, F401 — register models with Base


@pytest.fixture()
def db_session() -> Generator[Session, None, None]:
    """Provide a transactional in-memory SQLite session for each test.

    Tables are created fresh before the test and dropped afterward.
    """
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
    )
    Base.metadata.create_all(bind=engine)
    testing_session_local = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine,
    )
    session = testing_session_local()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)
