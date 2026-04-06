"""Tests for backend.models module.

Verifies the Task SQLAlchemy model: table name, column names, types,
defaults, constraints, and that instances can be persisted and
retrieved.
"""

from __future__ import annotations

from datetime import date, datetime

import pytest
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import Session, sessionmaker

from backend.database import Base
from backend.models import Task


@pytest.fixture()
def db_session() -> Session:
    """Create an in-memory database and yield a session."""
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


class TestTaskTableStructure:
    """Verify the tasks table has the expected schema."""

    def test_table_name(self) -> None:
        """Task model should map to the 'tasks' table."""
        assert Task.__tablename__ == "tasks"

    def test_column_names(self) -> None:
        """Task model should have the expected columns."""
        mapper = inspect(Task)
        column_names = {col.key for col in mapper.mapper.column_attrs}
        expected = {"id", "title", "status", "due_date", "created_at", "updated_at"}
        assert expected == column_names

    def test_id_is_primary_key(self) -> None:
        """The id column should be a primary key."""
        mapper = inspect(Task)
        pk_cols = [col.name for col in mapper.mapper.primary_key]
        assert "id" in pk_cols

    def test_title_is_not_nullable(self) -> None:
        """The title column should not allow NULL."""
        col = Task.__table__.columns["title"]
        assert col.nullable is False

    def test_status_default_is_todo(self) -> None:
        """The status column should default to 'todo'."""
        col = Task.__table__.columns["status"]
        assert col.default.arg == "todo"

    def test_due_date_is_nullable(self) -> None:
        """The due_date column should allow NULL."""
        col = Task.__table__.columns["due_date"]
        assert col.nullable is True

    def test_status_not_nullable(self) -> None:
        """The status column should not allow NULL."""
        col = Task.__table__.columns["status"]
        assert col.nullable is False


class TestTaskCRUD:
    """Verify Task instances can be created, read, and updated."""

    def test_create_task_defaults(self, db_session: Session) -> None:
        """A new task should receive default status and timestamps."""
        task = Task(title="Write tests")
        db_session.add(task)
        db_session.commit()
        db_session.refresh(task)

        assert task.id is not None
        assert task.title == "Write tests"
        assert task.status == "todo"
        assert task.due_date is None
        assert task.created_at is not None
        assert task.updated_at is not None

    def test_create_task_with_all_fields(self, db_session: Session) -> None:
        """A task created with explicit values should retain them."""
        target_date = date(2025, 12, 31)
        task = Task(
            title="Ship feature",
            status="in-progress",
            due_date=target_date,
        )
        db_session.add(task)
        db_session.commit()
        db_session.refresh(task)

        assert task.title == "Ship feature"
        assert task.status == "in-progress"
        assert task.due_date == target_date

    def test_create_task_done_status(self, db_session: Session) -> None:
        """A task can be created with status 'done'."""
        task = Task(title="Completed item", status="done")
        db_session.add(task)
        db_session.commit()
        db_session.refresh(task)

        assert task.status == "done"

    def test_query_task_by_id(self, db_session: Session) -> None:
        """A persisted task should be retrievable by primary key."""
        task = Task(title="Find me")
        db_session.add(task)
        db_session.commit()

        fetched = db_session.get(Task, task.id)
        assert fetched is not None
        assert fetched.title == "Find me"

    def test_update_task_status(self, db_session: Session) -> None:
        """Updating the status column should persist correctly."""
        task = Task(title="Move me")
        db_session.add(task)
        db_session.commit()

        task.status = "done"
        db_session.commit()
        db_session.refresh(task)

        assert task.status == "done"

    def test_delete_task(self, db_session: Session) -> None:
        """A deleted task should no longer be retrievable."""
        task = Task(title="Delete me")
        db_session.add(task)
        db_session.commit()
        task_id = task.id

        db_session.delete(task)
        db_session.commit()

        assert db_session.get(Task, task_id) is None

    def test_repr(self, db_session: Session) -> None:
        """__repr__ should include id, title, and status."""
        task = Task(title="Repr test")
        db_session.add(task)
        db_session.commit()
        db_session.refresh(task)

        r = repr(task)
        assert "Repr test" in r
        assert "todo" in r

    def test_multiple_tasks(self, db_session: Session) -> None:
        """Multiple tasks should be independently queryable."""
        t1 = Task(title="First")
        t2 = Task(title="Second", status="in-progress")
        t3 = Task(title="Third", status="done")
        db_session.add_all([t1, t2, t3])
        db_session.commit()

        all_tasks = db_session.query(Task).all()
        assert len(all_tasks) == 3

        in_progress = (
            db_session.query(Task).filter(Task.status == "in-progress").all()
        )
        assert len(in_progress) == 1
        assert in_progress[0].title == "Second"
