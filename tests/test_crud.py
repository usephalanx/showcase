"""Tests for app.crud CRUD operations.

Uses a dedicated in-memory SQLite database for each test function so
that tests are fully isolated and repeatable.
"""

from __future__ import annotations

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.database import Base
from app.crud import create_todo, delete_todo, get_todo, get_todos, update_todo
from app.models import Todo  # noqa: F401 – register model on Base
from app.schemas import TodoCreate, TodoUpdate


@pytest.fixture()
def db() -> Session:  # type: ignore[misc]
    """Yield a fresh SQLAlchemy session backed by an in-memory SQLite DB."""
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
    )
    Base.metadata.create_all(bind=engine)
    testing_session_local = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine,
    )
    session = testing_session_local()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)


# ---------------------------------------------------------------------------
# get_todos
# ---------------------------------------------------------------------------


class TestGetTodos:
    """Tests for the get_todos function."""

    def test_returns_empty_list_when_no_todos(self, db: Session) -> None:
        """An empty database should yield an empty list."""
        result = get_todos(db)
        assert result == []

    def test_returns_all_todos(self, db: Session) -> None:
        """All persisted todos are returned when no pagination is applied."""
        create_todo(db, TodoCreate(title="First"))
        create_todo(db, TodoCreate(title="Second"))
        create_todo(db, TodoCreate(title="Third"))

        result = get_todos(db)
        assert len(result) == 3

    def test_skip_parameter(self, db: Session) -> None:
        """The skip parameter should offset returned rows."""
        for i in range(5):
            create_todo(db, TodoCreate(title=f"Todo {i}"))

        result = get_todos(db, skip=3)
        assert len(result) == 2

    def test_limit_parameter(self, db: Session) -> None:
        """The limit parameter should cap the number of returned rows."""
        for i in range(5):
            create_todo(db, TodoCreate(title=f"Todo {i}"))

        result = get_todos(db, limit=2)
        assert len(result) == 2

    def test_skip_and_limit_combined(self, db: Session) -> None:
        """Skip and limit work together for proper pagination."""
        for i in range(10):
            create_todo(db, TodoCreate(title=f"Todo {i}"))

        result = get_todos(db, skip=2, limit=3)
        assert len(result) == 3


# ---------------------------------------------------------------------------
# get_todo
# ---------------------------------------------------------------------------


class TestGetTodo:
    """Tests for the get_todo function."""

    def test_returns_existing_todo(self, db: Session) -> None:
        """A valid id should return the corresponding Todo."""
        created = create_todo(db, TodoCreate(title="My Todo", description="Details"))
        result = get_todo(db, created.id)

        assert result is not None
        assert result.id == created.id
        assert result.title == "My Todo"
        assert result.description == "Details"
        assert result.completed is False

    def test_returns_none_for_missing_id(self, db: Session) -> None:
        """A non-existent id should return None."""
        result = get_todo(db, 999)
        assert result is None


# ---------------------------------------------------------------------------
# create_todo
# ---------------------------------------------------------------------------


class TestCreateTodo:
    """Tests for the create_todo function."""

    def test_creates_todo_with_title_only(self, db: Session) -> None:
        """A todo can be created with just a title."""
        todo = create_todo(db, TodoCreate(title="Buy groceries"))

        assert todo.id is not None
        assert todo.title == "Buy groceries"
        assert todo.description is None
        assert todo.completed is False
        assert todo.created_at is not None

    def test_creates_todo_with_description(self, db: Session) -> None:
        """A todo can be created with both title and description."""
        todo = create_todo(
            db,
            TodoCreate(title="Read book", description="Chapter 3"),
        )

        assert todo.title == "Read book"
        assert todo.description == "Chapter 3"

    def test_created_todo_is_persisted(self, db: Session) -> None:
        """The created todo should be retrievable from the DB."""
        todo = create_todo(db, TodoCreate(title="Persisted"))
        fetched = get_todo(db, todo.id)

        assert fetched is not None
        assert fetched.title == "Persisted"

    def test_auto_increment_ids(self, db: Session) -> None:
        """Successive creates should yield incrementing ids."""
        first = create_todo(db, TodoCreate(title="First"))
        second = create_todo(db, TodoCreate(title="Second"))

        assert second.id > first.id


# ---------------------------------------------------------------------------
# update_todo
# ---------------------------------------------------------------------------


class TestUpdateTodo:
    """Tests for the update_todo function."""

    def test_update_title(self, db: Session) -> None:
        """Updating the title field should persist the change."""
        todo = create_todo(db, TodoCreate(title="Old Title"))
        updated = update_todo(db, todo.id, TodoUpdate(title="New Title"))

        assert updated is not None
        assert updated.title == "New Title"

    def test_update_description(self, db: Session) -> None:
        """Updating the description field should persist the change."""
        todo = create_todo(db, TodoCreate(title="Task", description="Old desc"))
        updated = update_todo(db, todo.id, TodoUpdate(description="New desc"))

        assert updated is not None
        assert updated.description == "New desc"
        # Title should be unchanged.
        assert updated.title == "Task"

    def test_update_completed(self, db: Session) -> None:
        """Updating the completed flag should persist the change."""
        todo = create_todo(db, TodoCreate(title="Task"))
        assert todo.completed is False

        updated = update_todo(db, todo.id, TodoUpdate(completed=True))

        assert updated is not None
        assert updated.completed is True

    def test_partial_update_leaves_other_fields(self, db: Session) -> None:
        """Fields not included in the update payload remain unchanged."""
        todo = create_todo(
            db,
            TodoCreate(title="Original", description="Keep me"),
        )
        updated = update_todo(db, todo.id, TodoUpdate(completed=True))

        assert updated is not None
        assert updated.title == "Original"
        assert updated.description == "Keep me"
        assert updated.completed is True

    def test_update_nonexistent_returns_none(self, db: Session) -> None:
        """Attempting to update a non-existent todo returns None."""
        result = update_todo(db, 999, TodoUpdate(title="Ghost"))
        assert result is None

    def test_update_multiple_fields(self, db: Session) -> None:
        """Multiple fields can be updated in a single call."""
        todo = create_todo(db, TodoCreate(title="Old", description="Old desc"))
        updated = update_todo(
            db,
            todo.id,
            TodoUpdate(title="New", description="New desc", completed=True),
        )

        assert updated is not None
        assert updated.title == "New"
        assert updated.description == "New desc"
        assert updated.completed is True


# ---------------------------------------------------------------------------
# delete_todo
# ---------------------------------------------------------------------------


class TestDeleteTodo:
    """Tests for the delete_todo function."""

    def test_delete_existing_todo(self, db: Session) -> None:
        """Deleting an existing todo should return True."""
        todo = create_todo(db, TodoCreate(title="Delete me"))
        result = delete_todo(db, todo.id)

        assert result is True

    def test_deleted_todo_no_longer_exists(self, db: Session) -> None:
        """After deletion the todo should not be retrievable."""
        todo = create_todo(db, TodoCreate(title="Gone soon"))
        delete_todo(db, todo.id)

        assert get_todo(db, todo.id) is None

    def test_delete_nonexistent_returns_false(self, db: Session) -> None:
        """Deleting a non-existent todo should return False."""
        result = delete_todo(db, 999)
        assert result is False

    def test_delete_does_not_affect_other_todos(self, db: Session) -> None:
        """Deleting one todo should leave other todos intact."""
        todo1 = create_todo(db, TodoCreate(title="Keep me"))
        todo2 = create_todo(db, TodoCreate(title="Delete me"))

        delete_todo(db, todo2.id)

        assert get_todo(db, todo1.id) is not None
        assert get_todo(db, todo2.id) is None
        assert len(get_todos(db)) == 1
