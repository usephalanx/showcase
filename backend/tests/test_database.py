"""Tests for database configuration and initialisation."""

from __future__ import annotations

from sqlalchemy import inspect
from sqlalchemy.orm import Session

from app.database import Base


def test_tables_created(db_session: Session) -> None:
    """All expected tables exist after init_db runs."""
    inspector = inspect(db_session.bind)
    tables = inspector.get_table_names()
    assert "projects" in tables
    assert "tasks" in tables


def test_projects_columns(db_session: Session) -> None:
    """The projects table has the expected columns."""
    inspector = inspect(db_session.bind)
    columns = {col["name"] for col in inspector.get_columns("projects")}
    assert columns >= {"id", "name", "description", "created_at"}


def test_tasks_columns(db_session: Session) -> None:
    """The tasks table has the expected columns."""
    inspector = inspect(db_session.bind)
    columns = {col["name"] for col in inspector.get_columns("tasks")}
    assert columns >= {
        "id",
        "project_id",
        "title",
        "description",
        "status",
        "priority",
        "due_date",
        "created_at",
    }


def test_tasks_foreign_key(db_session: Session) -> None:
    """The tasks table has a foreign key referencing projects."""
    inspector = inspect(db_session.bind)
    fks = inspector.get_foreign_keys("tasks")
    referred_tables = {fk["referred_table"] for fk in fks}
    assert "projects" in referred_tables
