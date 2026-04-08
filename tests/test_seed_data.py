"""Tests for the seed_data module.

Verifies that :func:`seed_data.seed` correctly inserts the expected
sample todos into a fresh in-memory database, and that the inserted
records have the right fields and values.
"""

from __future__ import annotations

from typing import Generator

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.database import Base
from app.models import Todo
from seed_data import SAMPLE_TODOS, seed


@pytest.fixture()
def db_session() -> Generator[Session, None, None]:
    """Provide a clean in-memory SQLite session for each test."""
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
    )
    Base.metadata.create_all(bind=engine)
    testing_session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = testing_session()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)


class TestSeed:
    """Tests for the seed function."""

    def test_seed_returns_correct_count(self, db_session: Session) -> None:
        """seed() should return the same number of todos as SAMPLE_TODOS."""
        result = seed(db_session)
        assert len(result) == len(SAMPLE_TODOS)

    def test_seed_items_have_ids(self, db_session: Session) -> None:
        """Every seeded todo should have a non-None integer id."""
        result = seed(db_session)
        for todo in result:
            assert todo.id is not None
            assert isinstance(todo.id, int)

    def test_seed_items_have_created_at(self, db_session: Session) -> None:
        """Every seeded todo should have a created_at timestamp."""
        result = seed(db_session)
        for todo in result:
            assert todo.created_at is not None

    def test_seed_titles_match(self, db_session: Session) -> None:
        """Seeded todo titles should match the sample data."""
        result = seed(db_session)
        expected_titles = [item["title"] for item in SAMPLE_TODOS]
        actual_titles = [todo.title for todo in result]
        assert actual_titles == expected_titles

    def test_seed_descriptions_match(self, db_session: Session) -> None:
        """Seeded todo descriptions should match the sample data."""
        result = seed(db_session)
        for todo, sample in zip(result, SAMPLE_TODOS):
            assert todo.description == sample["description"]

    def test_seed_completed_flags_match(self, db_session: Session) -> None:
        """Seeded todo completed flags should match the sample data."""
        result = seed(db_session)
        for todo, sample in zip(result, SAMPLE_TODOS):
            assert todo.completed == sample["completed"]

    def test_seed_persists_to_database(self, db_session: Session) -> None:
        """After seeding, querying the database should return all items."""
        seed(db_session)
        count = db_session.query(Todo).count()
        assert count == len(SAMPLE_TODOS)

    def test_seed_twice_doubles_records(self, db_session: Session) -> None:
        """Calling seed() twice should insert records cumulatively."""
        seed(db_session)
        seed(db_session)
        count = db_session.query(Todo).count()
        assert count == len(SAMPLE_TODOS) * 2

    def test_seed_contains_completed_and_incomplete(self, db_session: Session) -> None:
        """Sample data should include at least one completed and one incomplete todo."""
        result = seed(db_session)
        completed = [t for t in result if t.completed]
        incomplete = [t for t in result if not t.completed]
        assert len(completed) >= 1, "Expected at least one completed todo in seed data"
        assert len(incomplete) >= 1, "Expected at least one incomplete todo in seed data"

    def test_seed_contains_item_without_description(self, db_session: Session) -> None:
        """Sample data should include at least one todo with no description."""
        result = seed(db_session)
        none_descriptions = [t for t in result if t.description is None]
        assert len(none_descriptions) >= 1, (
            "Expected at least one todo with description=None in seed data"
        )

    def test_sample_todos_titles_non_empty(self) -> None:
        """All sample todo titles should be non-empty strings."""
        for item in SAMPLE_TODOS:
            assert isinstance(item["title"], str)
            assert len(item["title"]) >= 1
