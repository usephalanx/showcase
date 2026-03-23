"""Tests for SQLAlchemy ORM models."""

from __future__ import annotations

from datetime import date, datetime

from sqlalchemy.orm import Session

from app.models import Project, Task, TaskPriority, TaskStatus


class TestProjectModel:
    """Tests for the Project model."""

    def test_create_project(self, db_session: Session) -> None:
        """A project can be created with name and description."""
        project = Project(name="Test Project", description="A test project")
        db_session.add(project)
        db_session.commit()
        db_session.refresh(project)

        assert project.id is not None
        assert project.name == "Test Project"
        assert project.description == "A test project"
        assert isinstance(project.created_at, datetime)

    def test_project_repr(self, db_session: Session) -> None:
        """The Project repr includes id and name."""
        project = Project(name="Repr Test")
        db_session.add(project)
        db_session.commit()
        db_session.refresh(project)

        assert "Repr Test" in repr(project)

    def test_project_tasks_relationship(self, db_session: Session) -> None:
        """Tasks added to a project are accessible via the tasks relationship."""
        project = Project(name="With Tasks")
        db_session.add(project)
        db_session.commit()
        db_session.refresh(project)

        task = Task(project_id=project.id, title="Task 1")
        db_session.add(task)
        db_session.commit()
        db_session.refresh(project)

        assert len(project.tasks) == 1
        assert project.tasks[0].title == "Task 1"


class TestTaskModel:
    """Tests for the Task model."""

    def test_create_task_defaults(self, db_session: Session) -> None:
        """A task created with only required fields has correct defaults."""
        project = Project(name="P")
        db_session.add(project)
        db_session.commit()
        db_session.refresh(project)

        task = Task(project_id=project.id, title="Default Task")
        db_session.add(task)
        db_session.commit()
        db_session.refresh(task)

        assert task.id is not None
        assert task.status == TaskStatus.todo
        assert task.priority == TaskPriority.medium
        assert task.due_date is None
        assert isinstance(task.created_at, datetime)

    def test_create_task_all_fields(self, db_session: Session) -> None:
        """A task can be created with all fields specified."""
        project = Project(name="P")
        db_session.add(project)
        db_session.commit()
        db_session.refresh(project)

        task = Task(
            project_id=project.id,
            title="Full Task",
            description="A fully specified task",
            status=TaskStatus.in_progress,
            priority=TaskPriority.high,
            due_date=date(2025, 12, 31),
        )
        db_session.add(task)
        db_session.commit()
        db_session.refresh(task)

        assert task.status == TaskStatus.in_progress
        assert task.priority == TaskPriority.high
        assert task.due_date == date(2025, 12, 31)
        assert task.description == "A fully specified task"

    def test_task_project_relationship(self, db_session: Session) -> None:
        """A task's project back-reference works correctly."""
        project = Project(name="Parent")
        db_session.add(project)
        db_session.commit()
        db_session.refresh(project)

        task = Task(project_id=project.id, title="Child Task")
        db_session.add(task)
        db_session.commit()
        db_session.refresh(task)

        assert task.project.name == "Parent"

    def test_task_repr(self, db_session: Session) -> None:
        """The Task repr includes id, title, and status."""
        project = Project(name="P")
        db_session.add(project)
        db_session.commit()
        db_session.refresh(project)

        task = Task(project_id=project.id, title="Repr Task")
        db_session.add(task)
        db_session.commit()
        db_session.refresh(task)

        assert "Repr Task" in repr(task)

    def test_cascade_delete(self, db_session: Session) -> None:
        """Deleting a project cascades to its tasks."""
        project = Project(name="Cascade")
        db_session.add(project)
        db_session.commit()
        db_session.refresh(project)

        task = Task(project_id=project.id, title="Doomed")
        db_session.add(task)
        db_session.commit()

        task_id = task.id
        db_session.delete(project)
        db_session.commit()

        remaining = db_session.get(Task, task_id)
        assert remaining is None
