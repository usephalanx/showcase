"""Tests for the database layer defined in database.py."""

from __future__ import annotations

import os
import tempfile
from typing import Generator

import pytest

import database


@pytest.fixture(autouse=True)
def _use_temp_db() -> Generator[None, None, None]:
    """Redirect the database to a temporary file for each test."""
    fd, db_path = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    original_path = database.DATABASE_PATH
    database.DATABASE_PATH = db_path
    database.init_db()
    yield
    database.DATABASE_PATH = original_path
    try:
        os.unlink(db_path)
    except OSError:
        pass


class TestInitDb:
    """Tests for init_db()."""

    def test_creates_table(self) -> None:
        """init_db should create the todos table."""
        with database.get_db_connection() as conn:
            cursor = conn.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name='todos';"
            )
            assert cursor.fetchone() is not None

    def test_idempotent(self) -> None:
        """Calling init_db twice should not raise."""
        database.init_db()
        database.init_db()


class TestCreateTodo:
    """Tests for create_todo()."""

    def test_create_returns_dict(self) -> None:
        """create_todo should return a dict with expected keys."""
        result = database.create_todo("Test item")
        assert isinstance(result, dict)
        assert result["title"] == "Test item"
        assert result["completed"] is False
        assert "id" in result
        assert "created_at" in result

    def test_create_empty_title_raises(self) -> None:
        """create_todo with empty title should raise ValueError."""
        with pytest.raises(ValueError, match="empty"):
            database.create_todo("")

    def test_create_whitespace_title_raises(self) -> None:
        """create_todo with whitespace-only title should raise ValueError."""
        with pytest.raises(ValueError, match="empty"):
            database.create_todo("   ")


class TestGetAllTodos:
    """Tests for get_all_todos()."""

    def test_empty_when_none_exist(self) -> None:
        """get_all_todos should return empty list when table is empty."""
        result = database.get_all_todos()
        assert result == []

    def test_returns_inserted_items(self) -> None:
        """get_all_todos should return all created items."""
        database.create_todo("A")
        database.create_todo("B")
        result = database.get_all_todos()
        assert len(result) == 2


class TestUpdateTodoCompleted:
    """Tests for update_todo_completed()."""

    def test_update_sets_completed(self) -> None:
        """update_todo_completed should update the completed field."""
        todo = database.create_todo("Update test")
        updated = database.update_todo_completed(todo["id"], True)
        assert updated is not None
        assert updated["completed"] is True

    def test_update_nonexistent_returns_none(self) -> None:
        """update_todo_completed on missing id should return None."""
        result = database.update_todo_completed(99999, True)
        assert result is None


class TestDeleteTodo:
    """Tests for delete_todo()."""

    def test_delete_existing(self) -> None:
        """delete_todo should return True for an existing item."""
        todo = database.create_todo("Delete me")
        assert database.delete_todo(todo["id"]) is True

    def test_delete_nonexistent(self) -> None:
        """delete_todo should return False for a non-existent id."""
        assert database.delete_todo(99999) is False

    def test_delete_removes_from_list(self) -> None:
        """After deletion the item should not appear in get_all_todos."""
        todo = database.create_todo("Ephemeral")
        database.delete_todo(todo["id"])
        ids = [t["id"] for t in database.get_all_todos()]
        assert todo["id"] not in ids
