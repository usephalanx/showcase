"""Seed script for the Todo application.

Inserts 5 sample tasks with varied statuses and due dates into the
SQLite database for demonstration purposes.  Tables are created
automatically if they do not already exist.

Usage:
    python seed.py
"""

from __future__ import annotations

import sys
from datetime import date, timedelta

from app.database import Base, SessionLocal, engine
from app.models import Task, TaskStatus


def create_tables() -> None:
    """Create all database tables if they do not already exist."""
    Base.metadata.create_all(bind=engine)


def seed_tasks() -> list[Task]:
    """Insert sample tasks into the database and return them.

    Creates 5 tasks with different statuses and due dates to showcase
    the application's filtering and display capabilities.

    Returns:
        A list of the newly created Task instances.
    """
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

    db = SessionLocal()
    try:
        db.add_all(sample_tasks)
        db.commit()
        for task in sample_tasks:
            db.refresh(task)
        return sample_tasks
    finally:
        db.close()


def main() -> None:
    """Run the seed script: create tables and insert sample data."""
    create_tables()
    tasks = seed_tasks()

    print(f"Successfully seeded {len(tasks)} tasks:")
    print("-" * 60)
    for task in tasks:
        due = task.due_date.isoformat() if task.due_date else "No due date"
        status_val = task.status.value if isinstance(task.status, TaskStatus) else task.status
        print(f"  [{task.id}] {task.title}")
        print(f"       Status: {status_val}  |  Due: {due}")
    print("-" * 60)
    print("Done.")


if __name__ == "__main__":
    main()
