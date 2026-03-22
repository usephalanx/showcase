"""Unit tests for the database module.

Each test function uses a temporary database file so that tests are
isolated and do not interfere with production data.
"""

from __future__ import annotations

import os
import sqlite3
import tempfile
from typing import Generator

import pytest

import database


@pytest.fixture(autouse=True)
def _use_temp_db(tmp_path: object) -> Generator[None, None, None]:
    """Override DATABASE_PATH to use a temporary file for each test."""
    fd, path = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    original_path = database.DATABASE_PATH
    database.DATABASE_PATH = path
    try:
        yield
    finally:
        database.DATABASE_PATH = original_path
        if os.path.exists(path):
            os.unlink(path)


class TestInitDb:
    """Tests for init_db()."""

    def test_creates_todos_table(self) -> None:
        """init_db should create the todos table."""
        database.init_db()

        with database.get_db_connection() as conn:
            cursor = conn.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name='todos';"
            )
            assert cursor.fetchone() is not None

    def test_idempotent(self) -> None:
        """Calling init_db twice should not raise an error."""
        database.init_db()
        database.init_db()  # should not raise

    def test_table_columns(self) -> None:
        """The todos table should have the expected columns."""
        database.init_db()

        with database.get_db_connection() as conn:
            cursor = conn.execute("PRAGMA table_info(todos);")
            columns = {row["name"] for row in cursor.fetchall()}

        assert columns == {"id", "title", "completed", "created_at"}


class TestGetDbConnection:
    """Tests for the get_db_connection context manager."""

    def test_returns_connection(self) -> None:
        """The context manager should yield a sqlite3.Connection."""
        with database.get_db_connection() as conn:
            assert isinstance(conn, sqlite3.Connection)

    def test_connection_has_row_factory(self) -> None:
        """The connection should use sqlite3.Row as row_factory."""
        with database.get_db_connection() as conn:
            assert conn.row_factory is sqlite3.Row

    def test_connection_closed_after_exit(self) -> None:
        """The connection should be closed after exiting the context."""
        with database.get_db_connection() as conn:
            pass
        # Attempting to use a closed connection raises ProgrammingError
        with pytest.raises(Exception):
            conn.execute("SELECT 1;")


class TestGetAllTodos:
    """Tests for get_all_todos()."""

    def test_empty_table(self) -> None:
        """Should return an empty list when the table has no rows."""
        database.init_db()
        result = database.get_all_todos()
        assert result == []

    def test_returns_all_rows(self) -> None:
        """Should return every todo in the table."""
        database.init_db()
        database.create_todo("First")
        database.create_todo("Second")

        result = database.get_all_todos()
        assert len(result) == 2

    def test_order_descending(self) -> None:
        """Todos should be ordered by created_at descending."""
        database.init_db()
        database.create_todo("First")
        database.create_todo("Second")

        result = database.get_all_todos()
        # The most recently created todo should appear first
        assert result[0]["title"] == "Second"
        assert result[1]["title"] == "First"

    def test_completed_is_bool(self) -> None:
        """The completed field should be a Python bool, not int."""
        database.init_db()
        database.create_todo("Test")

        result = database.get_all_todos()
        assert isinstance(result[0]["completed"], bool)
        assert result[0]["completed"] is False


class TestCreateTodo:
    """Tests for create_todo()."""

    def test_returns_dict_with_expected_keys(self) -> None:
        """Created todo should contain id, title, completed, created_at."""
        database.init_db()
        result = database.create_todo("Buy milk")

        assert "id" in result
        assert "title" in result
        assert "completed" in result
        assert "created_at" in result

    def test_title_stored_correctly(self) -> None:
        """The returned title should match the input."""
        database.init_db()
        result = database.create_todo("Buy milk")
        assert result["title"] == "Buy milk"

    def test_completed_defaults_to_false(self) -> None:
        """New todos should have completed = False."""
        database.init_db()
        result = database.create_todo("Buy milk")
        assert result["completed"] is False

    def test_id_is_autoincrement(self) -> None:
        """Each new todo should get a unique, incrementing id."""
        database.init_db()
        first = database.create_todo("First")
        second = database.create_todo("Second")
        assert second["id"] > first["id"]

    def test_created_at_is_populated(self) -> None:
        """created_at should be a non-empty string."""
        database.init_db()
        result = database.create_todo("Test")
        assert result["created_at"]
        assert isinstance(result["created_at"], str)

    def test_empty_title_raises(self) -> None:
        """An empty string should raise ValueError."""
        database.init_db()
        with pytest.raises(ValueError, match="title must not be empty"):
            database.create_todo("")

    def test_whitespace_title_raises(self) -> None:
        """A whitespace-only string should raise ValueError."""
        database.init_db()
        with pytest.raises(ValueError, match="title must not be empty"):
            database.create_todo("   ")


class TestUpdateTodoCompleted:
    """Tests for update_todo_completed()."""

    def test_mark_completed(self) -> None:
        """Should set completed to True."""
        database.init_db()
        todo = database.create_todo("Test")

        updated = database.update_todo_completed(todo["id"], True)
        assert updated is not None
        assert updated["completed"] is True

    def test_mark_not_completed(self) -> None:
        """Should set completed back to False."""
        database.init_db()
        todo = database.create_todo("Test")
        database.update_todo_completed(todo["id"], True)

        updated = database.update_todo_completed(todo["id"], False)
        assert updated is not None
        assert updated["completed"] is False

    def test_nonexistent_id_returns_none(self) -> None:
        """Should return None when the todo does not exist."""
        database.init_db()
        result = database.update_todo_completed(9999, True)
        assert result is None

    def test_preserves_title(self) -> None:
        """Updating completed should not change the title."""
        database.init_db()
        todo = database.create_todo("Keep this title")

        updated = database.update_todo_completed(todo["id"], True)
        assert updated is not None
        assert updated["title"] == "Keep this title"


class TestDeleteTodo:
    """Tests for delete_todo()."""

    def test_delete_existing(self) -> None:
        """Should return True when deleting an existing todo."""
        database.init_db()
        todo = database.create_todo("To be deleted")

        result = database.delete_todo(todo["id"])
        assert result is True

    def test_delete_nonexistent(self) -> None:
        """Should return False when the todo does not exist."""
        database.init_db()
        result = database.delete_todo(9999)
        assert result is False

    def test_todo_removed_from_table(self) -> None:
        """After deletion the todo should not appear in get_all_todos."""
        database.init_db()
        todo = database.create_todo("To be deleted")
        database.delete_todo(todo["id"])

        all_todos = database.get_all_todos()
        ids = [t["id"] for t in all_todos]
        assert todo["id"] not in ids

    def test_delete_idempotent(self) -> None:
        """Deleting the same id twice should return False the second time."""
        database.init_db()
        todo = database.create_todo("Test")
        database.delete_todo(todo["id"])

        result = database.delete_todo(todo["id"])
        assert result is False


class TestRowToDict:
    """Tests for the _row_to_dict helper."""

    def test_converts_row(self) -> None:
        """Should convert a sqlite3.Row to a dict with bool completed."""
        database.init_db()
        todo = database.create_todo("Test")

        assert isinstance(todo, dict)
        assert isinstance(todo["completed"], bool)

    def test_completed_true_conversion(self) -> None:
        """completed=1 in the DB should become True in the dict."""
        database.init_db()
        todo = database.create_todo("Test")
        updated = database.update_todo_completed(todo["id"], True)
        assert updated is not None
        assert updated["completed"] is True
        assert type(updated["completed"]) is bool
