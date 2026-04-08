"""Tests for app.models module.

Verifies the Todo SQLAlchemy model definition, column attributes,
defaults, and basic CRUD operations against the in-memory database.
"""

from __future__ import annotations

from datetime import datetime

import pytest
from sqlalchemy import inspect, text
from sqlalchemy.orm import Session

from app.database import Base, SessionLocal, engine
from app.models import Todo


@pytest.fixture(autouse=True)
def _setup_tables() -> None:
    """Create all tables before each test and drop them after."""
    Base.metadata.create_all(bind=engine)
    yield  # type: ignore[misc]
    Base.metadata.drop_all(bind=engine)


@pytest.fixture()
def db_session() -> Session:
    """Provide a fresh database session for a single test."""
    session = SessionLocal()
    try:
        yield session  # type: ignore[misc]
    finally:
        session.close()


# ---------------------------------------------------------------------------
# Schema / column definition tests
# ---------------------------------------------------------------------------


class TestTodoTableSchema:
    """Verify the 'todos' table schema matches the specification."""

    def test_table_name(self) -> None:
        """Model should map to the 'todos' table."""
        assert Todo.__tablename__ == "todos"

    def test_table_exists_after_create_all(self) -> None:
        """After create_all the 'todos' table must exist in the DB."""
        inspector = inspect(engine)
        table_names = inspector.get_table_names()
        assert "todos" in table_names

    def test_columns_present(self) -> None:
        """Table must contain the five required columns."""
        inspector = inspect(engine)
        columns = {col["name"] for col in inspector.get_columns("todos")}
        assert columns == {"id", "title", "description", "completed", "created_at"}

    def test_id_is_primary_key(self) -> None:
        """The 'id' column must be the primary key."""
        inspector = inspect(engine)
        pk = inspector.get_pk_constraint("todos")
        assert "id" in pk["constrained_columns"]

    def test_title_not_nullable(self) -> None:
        """The 'title' column must be NOT NULL."""
        inspector = inspect(engine)
        cols = {c["name"]: c for c in inspector.get_columns("todos")}
        assert cols["title"]["nullable"] is False

    def test_description_nullable(self) -> None:
        """The 'description' column must be nullable."""
        inspector = inspect(engine)
        cols = {c["name"]: c for c in inspector.get_columns("todos")}
        assert cols["description"]["nullable"] is True


# ---------------------------------------------------------------------------
# CRUD / default-value tests
# ---------------------------------------------------------------------------


class TestTodoDefaults:
    """Verify default column values when creating Todo instances."""

    def test_completed_defaults_to_false(self, db_session: Session) -> None:
        """A new Todo should have completed=False by default."""
        todo = Todo(title="Test item")
        db_session.add(todo)
        db_session.commit()
        db_session.refresh(todo)
        assert todo.completed is False

    def test_description_defaults_to_none(self, db_session: Session) -> None:
        """A new Todo without a description should have description=None."""
        todo = Todo(title="No description")
        db_session.add(todo)
        db_session.commit()
        db_session.refresh(todo)
        assert todo.description is None

    def test_created_at_is_set_automatically(self, db_session: Session) -> None:
        """created_at should be populated automatically on insert."""
        before = datetime.utcnow()
        todo = Todo(title="Timestamped")
        db_session.add(todo)
        db_session.commit()
        db_session.refresh(todo)
        after = datetime.utcnow()

        assert todo.created_at is not None
        assert isinstance(todo.created_at, datetime)
        assert before <= todo.created_at <= after

    def test_id_is_autoincremented(self, db_session: Session) -> None:
        """Sequential inserts should yield incrementing ids."""
        todo1 = Todo(title="First")
        todo2 = Todo(title="Second")
        db_session.add_all([todo1, todo2])
        db_session.commit()
        db_session.refresh(todo1)
        db_session.refresh(todo2)
        assert todo1.id is not None
        assert todo2.id is not None
        assert todo2.id > todo1.id


# ---------------------------------------------------------------------------
# CRUD operation tests
# ---------------------------------------------------------------------------


class TestTodoCRUD:
    """Verify basic create / read / update / delete operations."""

    def test_create_and_read(self, db_session: Session) -> None:
        """Creating a Todo and reading it back should return matching data."""
        todo = Todo(title="Buy milk", description="2% milk from store")
        db_session.add(todo)
        db_session.commit()

        fetched = db_session.query(Todo).filter_by(id=todo.id).first()
        assert fetched is not None
        assert fetched.title == "Buy milk"
        assert fetched.description == "2% milk from store"
        assert fetched.completed is False

    def test_update_todo(self, db_session: Session) -> None:
        """Updating a Todo's fields should persist the changes."""
        todo = Todo(title="Old title")
        db_session.add(todo)
        db_session.commit()

        todo.title = "New title"
        todo.completed = True
        db_session.commit()
        db_session.refresh(todo)

        assert todo.title == "New title"
        assert todo.completed is True

    def test_delete_todo(self, db_session: Session) -> None:
        """Deleting a Todo should remove it from the database."""
        todo = Todo(title="To delete")
        db_session.add(todo)
        db_session.commit()
        todo_id = todo.id

        db_session.delete(todo)
        db_session.commit()

        assert db_session.query(Todo).filter_by(id=todo_id).first() is None

    def test_query_all(self, db_session: Session) -> None:
        """Querying all Todos should return every inserted row."""
        db_session.add_all(
            [Todo(title="A"), Todo(title="B"), Todo(title="C")]
        )
        db_session.commit()

        todos = db_session.query(Todo).all()
        assert len(todos) == 3


# ---------------------------------------------------------------------------
# Repr test
# ---------------------------------------------------------------------------


class TestTodoRepr:
    """Verify the __repr__ of the Todo model."""

    def test_repr(self, db_session: Session) -> None:
        """__repr__ should contain id, title, and completed."""
        todo = Todo(title="Repr test")
        db_session.add(todo)
        db_session.commit()
        db_session.refresh(todo)

        r = repr(todo)
        assert "Repr test" in r
        assert str(todo.id) in r
        assert "False" in r
