"""Tests for SQLAlchemy ORM models (Project and Task)."""

from __future__ import annotations

import datetime

import pytest
from sqlalchemy import inspect
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from backend.app.models import Project, Task


# ---------------------------------------------------------------------------
# Project model tests
# ---------------------------------------------------------------------------


class TestProjectModel:
    """Tests for the Project ORM model."""

    def test_create_project_defaults(self, db: Session) -> None:
        """A project created with only a name should get sensible defaults."""
        project = Project(name="Test Project")
        db.add(project)
        db.commit()
        db.refresh(project)

        assert project.id is not None
        assert project.name == "Test Project"
        assert project.description is None
        assert project.status == "active"
        assert project.created_at is not None

    def test_create_project_with_all_fields(self, db: Session) -> None:
        """A project can be created with all fields specified."""
        project = Project(
            name="Full Project",
            description="A complete project",
            status="completed",
        )
        db.add(project)
        db.commit()
        db.refresh(project)

        assert project.name == "Full Project"
        assert project.description == "A complete project"
        assert project.status == "completed"

    def test_project_name_not_null(self, db: Session) -> None:
        """Inserting a project without a name must raise an IntegrityError."""
        project = Project(name=None)  # type: ignore[arg-type]
        db.add(project)
        with pytest.raises(IntegrityError):
            db.commit()

    def test_project_repr(self, db: Session) -> None:
        """The __repr__ method should include id, name, and status."""
        project = Project(name="Repr Test")
        db.add(project)
        db.commit()
        db.refresh(project)

        text = repr(project)
        assert "Repr Test" in text
        assert "active" in text

    def test_project_tasks_relationship(self, db: Session) -> None:
        """A project should expose its child tasks via the relationship."""
        project = Project(name="With Tasks")
        db.add(project)
        db.commit()
        db.refresh(project)

        task = Task(project_id=project.id, title="Child Task")
        db.add(task)
        db.commit()
        db.refresh(project)

        assert len(project.tasks) == 1
        assert project.tasks[0].title == "Child Task"


# ---------------------------------------------------------------------------
# Task model tests
# ---------------------------------------------------------------------------


class TestTaskModel:
    """Tests for the Task ORM model."""

    def _make_project(self, db: Session) -> Project:
        """Helper that creates and returns a persisted project."""
        project = Project(name="Parent Project")
        db.add(project)
        db.commit()
        db.refresh(project)
        return project

    def test_create_task_defaults(self, db: Session) -> None:
        """A task created with only project_id and title gets defaults."""
        project = self._make_project(db)
        task = Task(project_id=project.id, title="Default Task")
        db.add(task)
        db.commit()
        db.refresh(task)

        assert task.id is not None
        assert task.project_id == project.id
        assert task.title == "Default Task"
        assert task.status == "todo"
        assert task.priority == "medium"
        assert task.due_date is None

    def test_create_task_with_all_fields(self, db: Session) -> None:
        """A task can be created with all fields specified."""
        project = self._make_project(db)
        due = datetime.date(2025, 6, 15)
        task = Task(
            project_id=project.id,
            title="Full Task",
            status="in_progress",
            priority="high",
            due_date=due,
        )
        db.add(task)
        db.commit()
        db.refresh(task)

        assert task.status == "in_progress"
        assert task.priority == "high"
        assert task.due_date == due

    def test_task_title_not_null(self, db: Session) -> None:
        """Inserting a task without a title must raise an IntegrityError."""
        project = self._make_project(db)
        task = Task(project_id=project.id, title=None)  # type: ignore[arg-type]
        db.add(task)
        with pytest.raises(IntegrityError):
            db.commit()

    def test_task_requires_valid_project(self, db: Session) -> None:
        """A task referencing a non-existent project must raise an error."""
        task = Task(project_id=99999, title="Orphan Task")
        db.add(task)
        with pytest.raises(IntegrityError):
            db.commit()

    def test_cascade_delete(self, db: Session) -> None:
        """Deleting a project should cascade-delete its tasks."""
        project = self._make_project(db)
        task1 = Task(project_id=project.id, title="Task A")
        task2 = Task(project_id=project.id, title="Task B")
        db.add_all([task1, task2])
        db.commit()

        assert db.query(Task).count() == 2

        db.delete(project)
        db.commit()

        assert db.query(Task).count() == 0
        assert db.query(Project).count() == 0

    def test_task_repr(self, db: Session) -> None:
        """The __repr__ method should include id, title, status, priority."""
        project = self._make_project(db)
        task = Task(project_id=project.id, title="Repr Task")
        db.add(task)
        db.commit()
        db.refresh(task)

        text = repr(task)
        assert "Repr Task" in text
        assert "todo" in text
        assert "medium" in text

    def test_task_project_relationship(self, db: Session) -> None:
        """A task should be able to navigate back to its parent project."""
        project = self._make_project(db)
        task = Task(project_id=project.id, title="Nav Task")
        db.add(task)
        db.commit()
        db.refresh(task)

        assert task.project is not None
        assert task.project.name == "Parent Project"


# ---------------------------------------------------------------------------
# Table structure tests
# ---------------------------------------------------------------------------


class TestTableStructure:
    """Validate table columns and constraints via introspection."""

    def test_projects_table_columns(self, engine) -> None:
        """The projects table should have the expected columns."""
        insp = inspect(engine)
        columns = {col["name"] for col in insp.get_columns("projects")}
        expected = {"id", "name", "description", "status", "created_at"}
        assert expected == columns

    def test_tasks_table_columns(self, engine) -> None:
        """The tasks table should have the expected columns."""
        insp = inspect(engine)
        columns = {col["name"] for col in insp.get_columns("tasks")}
        expected = {"id", "project_id", "title", "status", "priority", "due_date"}
        assert expected == columns

    def test_tasks_foreign_key(self, engine) -> None:
        """The tasks table should have a FK to projects.id."""
        insp = inspect(engine)
        fks = insp.get_foreign_keys("tasks")
        assert len(fks) == 1
        assert fks[0]["referred_table"] == "projects"
        assert fks[0]["referred_columns"] == ["id"]
