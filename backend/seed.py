"""Seed script to populate the database with sample tasks.

Creates 5 sample tasks spanning all workflow statuses (todo, in-progress,
done) with various due dates.  The script is idempotent in the sense that
it initialises the database tables before inserting — but it does **not**
clear existing rows, so running it multiple times will create duplicates.

Usage:
    python -m backend.seed
"""

from __future__ import annotations

import sys
from datetime import date, timedelta

from backend.database import SessionLocal, init_db
from backend.models import Task

# ---------------------------------------------------------------------------
# Sample task definitions
# ---------------------------------------------------------------------------

SAMPLE_TASKS: list[dict[str, object]] = [
    {
        "title": "Set up project repository",
        "status": "done",
        "due_date": date.today() - timedelta(days=7),
    },
    {
        "title": "Design database schema",
        "status": "done",
        "due_date": date.today() - timedelta(days=3),
    },
    {
        "title": "Implement REST API endpoints",
        "status": "in-progress",
        "due_date": date.today() + timedelta(days=2),
    },
    {
        "title": "Build frontend task list view",
        "status": "todo",
        "due_date": date.today() + timedelta(days=7),
    },
    {
        "title": "Write end-to-end tests",
        "status": "todo",
        "due_date": None,
    },
]


def seed() -> None:
    """Insert sample tasks into the database.

    Ensures the database tables exist before inserting rows.  Prints a
    summary of each created task to stdout.
    """
    init_db()

    db = SessionLocal()
    try:
        for task_data in SAMPLE_TASKS:
            task = Task(
                title=task_data["title"],
                status=task_data["status"],
                due_date=task_data["due_date"],
            )
            db.add(task)
            db.flush()  # populate task.id before printing
            print(
                f"  Created task #{task.id}: "
                f"{task.title!r} "
                f"[{task.status}] "
                f"(due: {task.due_date or 'none'})"
            )
        db.commit()
        print(f"\n✔ Successfully seeded {len(SAMPLE_TASKS)} tasks.")
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    print("Seeding database with sample tasks...\n")
    try:
        seed()
    except Exception as exc:
        print(f"\n✘ Seeding failed: {exc}", file=sys.stderr)
        sys.exit(1)
