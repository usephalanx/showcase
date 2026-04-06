"""Tests for the Task SQLAlchemy model.

Uses an in-memory SQLite database to validate schema, defaults, and
constraints.
"""

from __future__ import annotations

import datetime

from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker

from app.database import Base
from app.models import Task, TaskStatus

# In-memory engine for isolated test runs
_engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
_TestSession = sessionmaker(autocommit=False, autoflush=False, bind=_engine)


def _setup_tables() -> None:
    """Ensure all tables exist in the in-memory database."""
    Base.metadata.create_all(bind=_engine)


def test_task_table_name() -> None:
    """The Task model should map to the 'tasks' table."""
    assert Task.__tablename__ == "tasks"


def test_task_columns_exist() -> None:
    """The tasks table should have id, title, status, and due_date columns."""
    _setup_tables()
    inspector = inspect(_engine)
    columns = {col["name"] for col in inspector.get_columns("tasks")}
    assert "id" in columns
    assert "title" in columns
    assert "status" in columns
    assert "due_date" in columns


def test_task_id_is_primary_key() -> None:
    """The id column should be the primary key."""
    _setup_tables()
    inspector = inspect(_engine)
    pk_columns = inspector.get_pk_constraint("tasks")["constrained_columns"]
    assert "id" in pk_columns


def test_task_default_status() -> None:
    """A new task should default to 'todo' status."""
    _setup_tables()
    session = _TestSession()
    try:
        task = Task(title="Test task")
        session.add(task)
        session.commit()
        session.refresh(task)
        assert task.status == TaskStatus.TODO or task.status == "todo"
    finally:
        session.close()


def test_task_due_date_nullable() -> None:
    """A task should be creatable without a due_date."""
    _setup_tables()
    session = _TestSession()
    try:
        task = Task(title="No deadline")
        session.add(task)
        session.commit()
        session.refresh(task)
        assert task.due_date is None
    finally:
        session.close()


def test_task_with_due_date() -> None:
    """A task should accept a valid due_date."""
    _setup_tables()
    session = _TestSession()
    try:
        target_date = datetime.date(2025, 12, 31)
        task = Task(title="Year end task", due_date=target_date)
        session.add(task)
        session.commit()
        session.refresh(task)
        assert task.due_date == target_date
    finally:
        session.close()


def test_task_status_values() -> None:
    """TaskStatus enum should contain exactly todo, in-progress, and done."""
    values = {member.value for member in TaskStatus}
    assert values == {"todo", "in-progress", "done"}


def test_task_autoincrement_id() -> None:
    """Task ids should auto-increment."""
    _setup_tables()
    session = _TestSession()
    try:
        t1 = Task(title="First")
        t2 = Task(title="Second")
        session.add_all([t1, t2])
        session.commit()
        session.refresh(t1)
        session.refresh(t2)
        assert t2.id > t1.id
    finally:
        session.close()


def test_task_repr() -> None:
    """The __repr__ method should return a meaningful string."""
    task = Task(id=1, title="Repr test", status=TaskStatus.TODO)
    r = repr(task)
    assert "Task" in r
    assert "Repr test" in r


def test_task_title_not_null() -> None:
    """Inserting a task without a title should raise an error."""
    _setup_tables()
    session = _TestSession()
    import pytest
    from sqlalchemy.exc import IntegrityError

    try:
        task = Task(title=None)  # type: ignore[arg-type]
        session.add(task)
        with pytest.raises(IntegrityError):
            session.commit()
    finally:
        session.rollback()
        session.close()


def test_task_in_progress_status() -> None:
    """A task should accept 'in-progress' as status."""
    _setup_tables()
    session = _TestSession()
    try:
        task = Task(title="WIP task", status=TaskStatus.IN_PROGRESS)
        session.add(task)
        session.commit()
        session.refresh(task)
        assert task.status == TaskStatus.IN_PROGRESS or task.status == "in-progress"
    finally:
        session.close()


def test_task_done_status() -> None:
    """A task should accept 'done' as status."""
    _setup_tables()
    session = _TestSession()
    try:
        task = Task(title="Completed task", status=TaskStatus.DONE)
        session.add(task)
        session.commit()
        session.refresh(task)
        assert task.status == TaskStatus.DONE or task.status == "done"
    finally:
        session.close()
