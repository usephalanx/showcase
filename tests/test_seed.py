"""Tests for the database seed script (backend/seed.py).

Each test uses an isolated in-memory SQLite database so that no
state leaks between test runs and no on-disk database file is required.
"""

from __future__ import annotations

from datetime import date
from typing import Generator

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from backend.database import Base
from backend.models import Task
from backend.seed import SAMPLE_TASKS, seed

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture(autouse=True)
def _patch_database(monkeypatch: pytest.MonkeyPatch) -> Generator[None, None, None]:
    """Replace the production database with an in-memory SQLite instance.

    This patches both ``backend.seed`` and ``backend.database`` so that
    the seed function and all its transitive imports use the test engine.
    """
    engine = create_engine("sqlite:///:memory:", echo=False)
    Base.metadata.create_all(bind=engine)
    TestSession: sessionmaker[Session] = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine,
    )

    # Patch SessionLocal in both the database module and the seed module
    monkeypatch.setattr("backend.database.SessionLocal", TestSession)
    monkeypatch.setattr("backend.seed.SessionLocal", TestSession)

    # Patch init_db to be a no-op (tables already created above)
    monkeypatch.setattr("backend.seed.init_db", lambda: None)

    yield

    engine.dispose()


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


def test_seed_creates_correct_number_of_tasks() -> None:
    """Verify that seed() inserts exactly 5 tasks."""
    seed()

    from backend.database import SessionLocal

    db = SessionLocal()
    try:
        count = db.query(Task).count()
        assert count == 5, f"Expected 5 tasks, got {count}"
    finally:
        db.close()


def test_seed_covers_all_statuses() -> None:
    """Verify that all three statuses (todo, in-progress, done) are present."""
    seed()

    from backend.database import SessionLocal

    db = SessionLocal()
    try:
        statuses = {row.status for row in db.query(Task.status).distinct().all()}
        assert statuses == {"todo", "in-progress", "done"}
    finally:
        db.close()


def test_seed_has_tasks_with_due_dates_and_without() -> None:
    """Verify that at least one task has a due_date and one does not."""
    seed()

    from backend.database import SessionLocal

    db = SessionLocal()
    try:
        tasks = db.query(Task).all()
        has_due_date = any(t.due_date is not None for t in tasks)
        has_no_due_date = any(t.due_date is None for t in tasks)
        assert has_due_date, "Expected at least one task with a due_date"
        assert has_no_due_date, "Expected at least one task without a due_date"
    finally:
        db.close()


def test_seed_task_titles_are_non_empty() -> None:
    """Verify that every seeded task has a non-empty title."""
    seed()

    from backend.database import SessionLocal

    db = SessionLocal()
    try:
        tasks = db.query(Task).all()
        for task in tasks:
            assert task.title and task.title.strip(), (
                f"Task #{task.id} has an empty title"
            )
    finally:
        db.close()


def test_sample_tasks_constant_has_five_entries() -> None:
    """Verify the SAMPLE_TASKS constant itself contains exactly 5 items."""
    assert len(SAMPLE_TASKS) == 5


def test_sample_tasks_statuses_are_valid() -> None:
    """Verify every entry in SAMPLE_TASKS uses a valid status string."""
    valid_statuses = {"todo", "in-progress", "done"}
    for task_data in SAMPLE_TASKS:
        assert task_data["status"] in valid_statuses, (
            f"Invalid status {task_data['status']!r} in SAMPLE_TASKS"
        )


def test_sample_tasks_due_dates_are_valid_types() -> None:
    """Verify due_date in SAMPLE_TASKS is either a date or None."""
    for task_data in SAMPLE_TASKS:
        due = task_data["due_date"]
        assert due is None or isinstance(due, date), (
            f"Expected date or None, got {type(due)}"
        )


def test_seed_idempotent_table_creation() -> None:
    """Verify that calling seed() twice does not raise and doubles the rows."""
    seed()
    seed()  # second call should not fail

    from backend.database import SessionLocal

    db = SessionLocal()
    try:
        count = db.query(Task).count()
        assert count == 10, (
            f"Expected 10 tasks after seeding twice, got {count}"
        )
    finally:
        db.close()
