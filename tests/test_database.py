"""Tests for the SQLite database layer (database.py).

Covers: init_db, get_all_todos, create_todo, update_todo, delete_todo,
edge cases with empty titles, nonexistent IDs, and row-to-dict conversion.
"""

from __future__ import annotations

import sqlite3
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "healthcheck" / "e36e389f"))


class TestInitDb:
    """Tests for database initialisation."""

    def test_init_db_creates_todos_table(self, _tmp_database: Path) -> None:
        """init_db creates the 'todos' table."""
        import database

        conn = database.get_db_connection()
        try:
            cursor = conn.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name='todos';"
            )
            assert cursor.fetchone() is not None
        finally:
            conn.close()

    def test_init_db_is_idempotent(self, _tmp_database: Path) -> None:
        """Calling init_db twice does not raise."""
        import database

        # Should not raise
        database.init_db()
        database.init_db()


class TestCreateTodo:
    """Tests for database.create_todo()."""

    def test_create_todo_returns_dict(self, _tmp_database: Path) -> None:
        """create_todo returns a dictionary with expected keys."""
        import database

        result = database.create_todo("Test item")
        assert isinstance(result, dict)
        assert "id" in result
        assert "title" in result
        assert "completed" in result
        assert "created_at" in result

    def test_create_todo_stores_title(self, _tmp_database: Path) -> None:
        """The returned todo has the correct title."""
        import database

        result = database.create_todo("My task")
        assert result["title"] == "My task"

    def test_create_todo_defaults_completed_false(self, _tmp_database: Path) -> None:
        """New todos are not completed by default."""
        import database

        result = database.create_todo("Task")
        assert result["completed"] is False

    def test_create_todo_empty_title_raises(self, _tmp_database: Path) -> None:
        """Creating a todo with empty title raises ValueError."""
        import database

        with pytest.raises(ValueError, match="title must not be empty"):
            database.create_todo("")

    def test_create_todo_whitespace_title_raises(self, _tmp_database: Path) -> None:
        """Creating a todo with whitespace-only title raises ValueError."""
        import database

        with pytest.raises(ValueError, match="title must not be empty"):
            database.create_todo("   ")

    def test_create_todo_assigns_unique_ids(self, _tmp_database: Path) -> None:
        """Each created todo gets a unique id."""
        import database

        t1 = database.create_todo("First")
        t2 = database.create_todo("Second")
        assert t1["id"] != t2["id"]


class TestGetAllTodos:
    """Tests for database.get_all_todos()."""

    def test_get_all_empty(self, _tmp_database: Path) -> None:
        """Returns empty list when no todos exist."""
        import database

        result = database.get_all_todos()
        assert result == []

    def test_get_all_returns_created_items(self, _tmp_database: Path) -> None:
        """Returns all previously created todos."""
        import database

        database.create_todo("A")
        database.create_todo("B")
        result = database.get_all_todos()
        assert len(result) == 2

    def test_get_all_ordered_by_created_at_desc(self, _tmp_database: Path) -> None:
        """Todos are ordered newest first."""
        import database

        database.create_todo("Old")
        database.create_todo("New")
        result = database.get_all_todos()
        # The most recently created should come first
        assert result[0]["title"] == "New"
        assert result[1]["title"] == "Old"

    def test_get_all_completed_is_bool(self, _tmp_database: Path) -> None:
        """The completed field in returned dicts is a Python bool."""
        import database

        database.create_todo("Task")
        result = database.get_all_todos()
        assert isinstance(result[0]["completed"], bool)


class TestUpdateTodo:
    """Tests for database.update_todo()."""

    def test_update_todo_completed(self, _tmp_database: Path) -> None:
        """Setting completed to True is reflected in the returned dict."""
        import database

        created = database.create_todo("Task")
        updated = database.update_todo(created["id"], True)
        assert updated is not None
        assert updated["completed"] is True

    def test_update_todo_unmark_completed(self, _tmp_database: Path) -> None:
        """Setting completed back to False works."""
        import database

        created = database.create_todo("Task")
        database.update_todo(created["id"], True)
        updated = database.update_todo(created["id"], False)
        assert updated is not None
        assert updated["completed"] is False

    def test_update_nonexistent_returns_none(self, _tmp_database: Path) -> None:
        """Updating a non-existent todo returns None."""
        import database

        result = database.update_todo(99999, True)
        assert result is None


class TestDeleteTodo:
    """Tests for database.delete_todo()."""

    def test_delete_existing_todo(self, _tmp_database: Path) -> None:
        """Deleting an existing todo returns True."""
        import database

        created = database.create_todo("Delete me")
        result = database.delete_todo(created["id"])
        assert result is True

    def test_delete_removes_from_database(self, _tmp_database: Path) -> None:
        """After deletion, the todo is no longer in get_all_todos()."""
        import database

        created = database.create_todo("Bye")
        database.delete_todo(created["id"])
        all_todos = database.get_all_todos()
        ids = [t["id"] for t in all_todos]
        assert created["id"] not in ids

    def test_delete_nonexistent_returns_false(self, _tmp_database: Path) -> None:
        """Deleting a non-existent todo returns False."""
        import database

        result = database.delete_todo(99999)
        assert result is False
