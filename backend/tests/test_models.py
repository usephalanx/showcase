"""Tests for SQLAlchemy ORM models."""

from __future__ import annotations

from datetime import date, datetime

from app.models import Task, TaskStatus


class TestTaskModel:
    """Test suite for the Task ORM model."""

    def test_create_task_defaults(self, db_session) -> None:
        """A task created with only a title should have sensible defaults."""
        task = Task(title="Buy groceries")
        db_session.add(task)
        db_session.commit()
        db_session.refresh(task)

        assert task.id is not None
        assert task.title == "Buy groceries"
        assert task.status in (TaskStatus.TODO.value, TaskStatus.TODO)
        assert task.due_date is None
        assert isinstance(task.created_at, datetime)
        assert isinstance(task.updated_at, datetime)

    def test_create_task_with_all_fields(self, db_session) -> None:
        """A task can be created with every field specified."""
        due = date(2025, 12, 31)
        task = Task(
            title="Finish report",
            status=TaskStatus.IN_PROGRESS.value,
            due_date=due,
        )
        db_session.add(task)
        db_session.commit()
        db_session.refresh(task)

        assert task.title == "Finish report"
        assert task.status == "in-progress"
        assert task.due_date == due

    def test_status_enum_values(self) -> None:
        """TaskStatus enum contains exactly todo, in-progress, done."""
        values = {s.value for s in TaskStatus}
        assert values == {"todo", "in-progress", "done"}

    def test_task_repr(self, db_session) -> None:
        """__repr__ should return a useful string."""
        task = Task(title="Test repr")
        db_session.add(task)
        db_session.commit()
        db_session.refresh(task)

        repr_str = repr(task)
        assert "Test repr" in repr_str
        assert "Task" in repr_str

    def test_multiple_tasks_get_unique_ids(self, db_session) -> None:
        """Each persisted task should receive a unique auto-incremented id."""
        t1 = Task(title="First")
        t2 = Task(title="Second")
        db_session.add_all([t1, t2])
        db_session.commit()
        db_session.refresh(t1)
        db_session.refresh(t2)

        assert t1.id != t2.id

    def test_due_date_nullable(self, db_session) -> None:
        """due_date should accept None."""
        task = Task(title="No due date", due_date=None)
        db_session.add(task)
        db_session.commit()
        db_session.refresh(task)

        assert task.due_date is None

    def test_status_done(self, db_session) -> None:
        """A task can be created with status 'done'."""
        task = Task(title="Already done", status=TaskStatus.DONE.value)
        db_session.add(task)
        db_session.commit()
        db_session.refresh(task)

        assert task.status == "done"
