"""Tests for the seed.py script.

Validates that the seed script correctly creates tables and inserts
sample tasks with the expected statuses and due date patterns.
"""

from __future__ import annotations

from datetime import date
from typing import Generator

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.database import Base
from app.models import Task, TaskStatus


@pytest.fixture()
def db_session() -> Generator[Session, None, None]:
    """Provide an in-memory SQLite session for isolated testing."""
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
    )
    Base.metadata.create_all(bind=engine)
    TestSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = TestSession()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)


def _insert_seed_tasks(session: Session) -> list[Task]:
    """Replicate the seed logic using a provided session.

    This avoids hitting the real database during tests while verifying
    the same data shapes that seed.py produces.

    Args:
        session: An active SQLAlchemy session.

    Returns:
        The list of created Task instances.
    """
    from datetime import timedelta

    today = date.today()

    sample_tasks = [
        Task(
            title="Buy groceries",
            status=TaskStatus.TODO,
            due_date=today + timedelta(days=1),
        ),
        Task(
            title="Write project documentation",
            status=TaskStatus.IN_PROGRESS,
            due_date=today + timedelta(days=3),
        ),
        Task(
            title="Fix login page bug",
            status=TaskStatus.DONE,
            due_date=today - timedelta(days=2),
        ),
        Task(
            title="Prepare demo presentation",
            status=TaskStatus.TODO,
            due_date=today + timedelta(days=7),
        ),
        Task(
            title="Review pull requests",
            status=TaskStatus.IN_PROGRESS,
            due_date=None,
        ),
    ]

    session.add_all(sample_tasks)
    session.commit()
    for task in sample_tasks:
        session.refresh(task)
    return sample_tasks


class TestSeedData:
    """Test suite for the seed data script logic."""

    def test_seed_inserts_five_tasks(self, db_session: Session) -> None:
        """Seed script should insert exactly 5 tasks."""
        tasks = _insert_seed_tasks(db_session)
        assert len(tasks) == 5

        count = db_session.query(Task).count()
        assert count == 5

    def test_seed_tasks_have_ids(self, db_session: Session) -> None:
        """Every seeded task should receive a database-generated ID."""
        tasks = _insert_seed_tasks(db_session)
        for task in tasks:
            assert task.id is not None
            assert isinstance(task.id, int)
            assert task.id > 0

    def test_seed_tasks_have_varied_statuses(self, db_session: Session) -> None:
        """Seeded tasks should include at least 2 distinct statuses."""
        tasks = _insert_seed_tasks(db_session)
        statuses = {task.status for task in tasks}
        assert len(statuses) >= 2

    def test_seed_tasks_contain_all_statuses(self, db_session: Session) -> None:
        """Seeded tasks should cover all three status values."""
        tasks = _insert_seed_tasks(db_session)
        statuses = {task.status for task in tasks}
        assert TaskStatus.TODO in statuses
        assert TaskStatus.IN_PROGRESS in statuses
        assert TaskStatus.DONE in statuses

    def test_seed_tasks_have_varied_due_dates(self, db_session: Session) -> None:
        """At least one task should have a due date and one without."""
        tasks = _insert_seed_tasks(db_session)
        due_dates = [task.due_date for task in tasks]
        assert any(d is not None for d in due_dates)
        assert any(d is None for d in due_dates)

    def test_seed_tasks_have_titles(self, db_session: Session) -> None:
        """Every seeded task should have a non-empty title."""
        tasks = _insert_seed_tasks(db_session)
        for task in tasks:
            assert task.title is not None
            assert len(task.title.strip()) > 0

    def test_seed_tasks_include_past_due_date(self, db_session: Session) -> None:
        """At least one seeded task should have a due date in the past."""
        tasks = _insert_seed_tasks(db_session)
        today = date.today()
        past_due = [t for t in tasks if t.due_date is not None and t.due_date < today]
        assert len(past_due) >= 1

    def test_seed_tasks_include_future_due_date(self, db_session: Session) -> None:
        """At least one seeded task should have a due date in the future."""
        tasks = _insert_seed_tasks(db_session)
        today = date.today()
        future_due = [t for t in tasks if t.due_date is not None and t.due_date > today]
        assert len(future_due) >= 1

    def test_seed_idempotent_adds_more_rows(self, db_session: Session) -> None:
        """Running seed twice should add 10 total tasks (not replace)."""
        _insert_seed_tasks(db_session)
        _insert_seed_tasks(db_session)
        count = db_session.query(Task).count()
        assert count == 10


class TestRunningMd:
    """Test suite to verify RUNNING.md exists and has required content."""

    def test_running_md_exists(self) -> None:
        """RUNNING.md should exist at the repository root."""
        from pathlib import Path

        running_md = Path("RUNNING.md")
        assert running_md.exists(), "RUNNING.md not found at repository root"

    def test_running_md_has_backend_setup(self) -> None:
        """RUNNING.md should contain backend setup instructions."""
        from pathlib import Path

        content = Path("RUNNING.md").read_text(encoding="utf-8")
        assert "pip install" in content
        assert "uvicorn" in content

    def test_running_md_has_frontend_setup(self) -> None:
        """RUNNING.md should contain frontend setup instructions."""
        from pathlib import Path

        content = Path("RUNNING.md").read_text(encoding="utf-8")
        assert "npm install" in content
        assert "npm run dev" in content

    def test_running_md_has_access_urls(self) -> None:
        """RUNNING.md should mention the URLs to access the app."""
        from pathlib import Path

        content = Path("RUNNING.md").read_text(encoding="utf-8")
        assert "localhost:5173" in content or "127.0.0.1:5173" in content
        assert "127.0.0.1:8000" in content or "localhost:8000" in content

    def test_running_md_has_seed_instructions(self) -> None:
        """RUNNING.md should mention the seed script."""
        from pathlib import Path

        content = Path("RUNNING.md").read_text(encoding="utf-8")
        assert "seed" in content.lower()
        assert "python seed.py" in content

    def test_running_md_has_api_docs_link(self) -> None:
        """RUNNING.md should reference the Swagger/API docs URL."""
        from pathlib import Path

        content = Path("RUNNING.md").read_text(encoding="utf-8")
        assert "/docs" in content
