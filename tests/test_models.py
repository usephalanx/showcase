"""Tests for SQLAlchemy ORM models."""

from __future__ import annotations

from datetime import date, datetime, timezone

from sqlalchemy.orm import Session

from app.models.project import Project
from app.models.task import Task, TaskPriority, TaskStatus


def test_project_defaults(db_session: Session) -> None:
    """A new Project gets auto-generated id and created_at."""
    project = Project(name="Defaults", description="Testing defaults")
    db_session.add(project)
    db_session.commit()
    db_session.refresh(project)

    assert project.id is not None
    assert isinstance(project.created_at, datetime)
    assert project.name == "Defaults"


def test_task_defaults(db_session: Session) -> None:
    """A new Task gets default status=todo and priority=medium."""
    project = Project(name="Parent")
    db_session.add(project)
    db_session.commit()
    db_session.refresh(project)

    task = Task(project_id=project.id, title="Default task")
    db_session.add(task)
    db_session.commit()
    db_session.refresh(task)

    assert task.id is not None
    assert task.status == TaskStatus.todo
    assert task.priority == TaskPriority.medium
    assert task.due_date is None
    assert isinstance(task.created_at, datetime)


def test_task_with_due_date(db_session: Session) -> None:
    """A Task can store a due_date."""
    project = Project(name="Dated")
    db_session.add(project)
    db_session.commit()
    db_session.refresh(project)

    task = Task(
        project_id=project.id,
        title="Has due date",
        due_date=date(2025, 6, 15),
    )
    db_session.add(task)
    db_session.commit()
    db_session.refresh(task)

    assert task.due_date == date(2025, 6, 15)


def test_project_task_relationship(db_session: Session) -> None:
    """Project.tasks relationship returns associated tasks."""
    project = Project(name="Relational")
    db_session.add(project)
    db_session.commit()
    db_session.refresh(project)

    t1 = Task(project_id=project.id, title="T1")
    t2 = Task(project_id=project.id, title="T2")
    db_session.add_all([t1, t2])
    db_session.commit()
    db_session.refresh(project)

    assert len(project.tasks) == 2
    titles = {t.title for t in project.tasks}
    assert titles == {"T1", "T2"}


def test_task_project_backref(db_session: Session) -> None:
    """Task.project relationship returns the parent project."""
    project = Project(name="BackRef")
    db_session.add(project)
    db_session.commit()
    db_session.refresh(project)

    task = Task(project_id=project.id, title="Child")
    db_session.add(task)
    db_session.commit()
    db_session.refresh(task)

    assert task.project.name == "BackRef"


def test_project_repr(db_session: Session) -> None:
    """Project.__repr__ contains id and name."""
    project = Project(name="ReprTest")
    db_session.add(project)
    db_session.commit()
    db_session.refresh(project)

    r = repr(project)
    assert "ReprTest" in r
    assert str(project.id) in r


def test_task_repr(db_session: Session) -> None:
    """Task.__repr__ contains id, title, and status."""
    project = Project(name="P")
    db_session.add(project)
    db_session.commit()
    db_session.refresh(project)

    task = Task(project_id=project.id, title="ReprTask")
    db_session.add(task)
    db_session.commit()
    db_session.refresh(task)

    r = repr(task)
    assert "ReprTask" in r
    assert "todo" in r
