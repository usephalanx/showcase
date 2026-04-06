"""Shared test fixtures for the Kanban backend test suite.

Provides an in-memory SQLite database, a session factory, and
pre-populated fixtures for boards, columns, cards, and categories.
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Generator

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

# Make sure the backend package is on the path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "backend"))

from database import Base  # noqa: E402
import models  # noqa: E402, F401


@pytest.fixture(scope="function")
def db_engine():
    """Create a fresh in-memory SQLite engine for each test."""
    engine = create_engine("sqlite:///:memory:", echo=False)
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)
    engine.dispose()


@pytest.fixture(scope="function")
def db_session(db_engine) -> Generator[Session, None, None]:
    """Provide a transactional database session that rolls back after each test."""
    TestingSessionLocal = sessionmaker(bind=db_engine, autocommit=False, autoflush=False)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.rollback()
        session.close()


@pytest.fixture()
def sample_board(db_session: Session) -> models.Board:
    """Create and return a sample Board."""
    board = models.Board(
        title="Test Board",
        slug="test-board",
        description="A board for testing.",
        meta_title="Test Board — Kanban",
        meta_description="A test board description for SEO.",
    )
    db_session.add(board)
    db_session.commit()
    db_session.refresh(board)
    return board


@pytest.fixture()
def sample_column(db_session: Session, sample_board: models.Board) -> models.Column:
    """Create and return a sample Column in the sample board."""
    column = models.Column(
        board_id=sample_board.id,
        title="To Do",
        position=0,
    )
    db_session.add(column)
    db_session.commit()
    db_session.refresh(column)
    return column


@pytest.fixture()
def sample_card(db_session: Session, sample_column: models.Column) -> models.Card:
    """Create and return a sample Card in the sample column."""
    card = models.Card(
        column_id=sample_column.id,
        title="Test Card",
        description="Card description.",
        slug="test-card",
        position=0,
    )
    db_session.add(card)
    db_session.commit()
    db_session.refresh(card)
    return card


@pytest.fixture()
def sample_category(db_session: Session) -> models.Category:
    """Create and return a root sample Category."""
    category = models.Category(
        name="Bug",
        slug="bug",
        description="Bug reports.",
    )
    db_session.add(category)
    db_session.commit()
    db_session.refresh(category)
    return category
