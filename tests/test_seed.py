"""Tests for the seed_data function."""

from __future__ import annotations

from sqlalchemy.orm import Session

from backend.app.models import Project, Task
from backend.app.seed import seed_data


class TestSeedData:
    """Tests for seed_data()."""

    def test_seeds_empty_database(self, db: Session) -> None:
        """Should populate an empty database with 2 projects and 5 tasks."""
        seed_data(db)

        projects = db.query(Project).all()
        tasks = db.query(Task).all()

        assert len(projects) == 2
        assert len(tasks) == 5

    def test_project_names(self, db: Session) -> None:
        """Seeded projects should have the expected names."""
        seed_data(db)

        names = {p.name for p in db.query(Project).all()}
        assert "Website Redesign" in names
        assert "Mobile App Launch" in names

    def test_tasks_per_project(self, db: Session) -> None:
        """Each project should have at least 2 tasks."""
        seed_data(db)

        for project in db.query(Project).all():
            task_count = (
                db.query(Task).filter(Task.project_id == project.id).count()
            )
            assert task_count >= 2, (
                f"Project '{project.name}' has only {task_count} tasks"
            )

    def test_task_statuses(self, db: Session) -> None:
        """Seeded tasks should only contain valid statuses."""
        seed_data(db)

        valid_statuses = {"todo", "in_progress", "done"}
        for task in db.query(Task).all():
            assert task.status in valid_statuses

    def test_task_priorities(self, db: Session) -> None:
        """Seeded tasks should only contain valid priorities."""
        seed_data(db)

        valid_priorities = {"low", "medium", "high"}
        for task in db.query(Task).all():
            assert task.priority in valid_priorities

    def test_idempotent_no_duplicates(self, db: Session) -> None:
        """Calling seed_data twice should not create duplicate rows."""
        seed_data(db)
        seed_data(db)

        assert db.query(Project).count() == 2
        assert db.query(Task).count() == 5

    def test_skips_when_projects_exist(self, db: Session) -> None:
        """Should skip seeding if projects already exist."""
        existing = Project(name="Existing", status="active")
        db.add(existing)
        db.commit()

        seed_data(db)

        assert db.query(Project).count() == 1  # Only the manually-added one
        assert db.query(Task).count() == 0

    def test_skips_when_tasks_exist(self, db: Session) -> None:
        """Should skip seeding if tasks already exist (edge case)."""
        project = Project(name="P", status="active")
        db.add(project)
        db.commit()
        db.refresh(project)

        task = Task(project_id=project.id, title="T")
        db.add(task)
        db.commit()

        seed_data(db)

        # Nothing extra should have been added.
        assert db.query(Project).count() == 1
        assert db.query(Task).count() == 1

    def test_seed_task_due_dates(self, db: Session) -> None:
        """All seeded tasks should have a non-null due_date."""
        seed_data(db)

        for task in db.query(Task).all():
            assert task.due_date is not None, (
                f"Task '{task.title}' is missing a due_date"
            )
