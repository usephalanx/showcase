#!/usr/bin/env python3
"""Seed the database with sample Todo items for quick testing.

Usage
-----
::

    python seed_data.py

The script creates the database tables (if they don't already exist)
and inserts a handful of representative todos covering various
combinations of title, description, and completion status.

Because the default configuration uses an **in-memory** SQLite database,
this script is most useful when imported programmatically (e.g. from
tests) via :func:`seed` rather than run as a standalone process against
a live server.  To persist seeded data to a running server, either
change ``SQLALCHEMY_DATABASE_URL`` in ``app/database.py`` to a
file-based SQLite path or call the ``POST /todos`` endpoint directly.
"""

from __future__ import annotations

from typing import List

from sqlalchemy.orm import Session

from app.database import Base, SessionLocal, engine
from app.models import Todo

# ---------------------------------------------------------------------------
# Sample data
# ---------------------------------------------------------------------------

SAMPLE_TODOS: List[dict] = [
    {
        "title": "Buy groceries",
        "description": "Milk, eggs, bread, and fresh vegetables from the farmers market.",
        "completed": False,
    },
    {
        "title": "Read a book",
        "description": "Finish reading 'Designing Data-Intensive Applications' by Martin Kleppmann.",
        "completed": False,
    },
    {
        "title": "Morning jog",
        "description": "Run 5 km around the park before breakfast.",
        "completed": True,
    },
    {
        "title": "Write unit tests",
        "description": "Add pytest coverage for the new CRUD endpoints.",
        "completed": False,
    },
    {
        "title": "Clean the kitchen",
        "description": None,
        "completed": True,
    },
    {
        "title": "Plan weekend trip",
        "description": "Research destinations, book accommodation, and create a packing list.",
        "completed": False,
    },
    {
        "title": "Update resume",
        "description": "Add recent project experience and refresh the skills section.",
        "completed": False,
    },
]


def seed(db: Session) -> List[Todo]:
    """Insert sample todos into the database.

    Args:
        db: An active SQLAlchemy database session.

    Returns:
        A list of the newly created :class:`~app.models.Todo` instances
        with server-set fields (``id``, ``created_at``) populated.
    """
    created: List[Todo] = []
    for item in SAMPLE_TODOS:
        todo = Todo(
            title=item["title"],
            description=item["description"],
            completed=item["completed"],
        )
        db.add(todo)
        created.append(todo)

    db.commit()
    for todo in created:
        db.refresh(todo)

    return created


def main() -> None:
    """Entry point: create tables and seed sample data."""
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        todos = seed(db)
        print(f"Seeded {len(todos)} sample todos:")
        for todo in todos:
            status = "✓" if todo.completed else "✗"
            print(f"  [{status}] {todo.id}: {todo.title}")
    finally:
        db.close()


if __name__ == "__main__":
    main()
