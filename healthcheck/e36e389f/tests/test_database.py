"""Tests for the database module.

Each test uses a temporary SQLite database so that the real todos.db is
never touched and tests remain fully isolated.
"""

from __future__ import annotations

import os
import tempfile
from typing import Generator

import pytest

import database


@pytest.fixture(autouse=True)
def _use_temp_db(tmp_path: object) -> Generator[None, None, None]:
    """Redirect DATABASE_PATH to a temporary file for each test."""
    fd, path = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    original = database.DATABASE_PATH
    database.DATABASE_PATH = path
    try:
        yield
    finally:
        database.DATABASE_PATH = original
        if os.path.exists(path):
            os.unlink(path)


# ------------------------------------------------------------------
# init_db
# ------------------------------------------------------------------


def test_init_db_creates_todos_table() -> None:
    """init_db should create the 'todos' table."""
    database.init_db()
    conn = database.get_db_connection()
    try:
        cursor = conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='todos';"
        )
        assert cursor.fetchone() is not None
    finally:
        conn.close()


def test_init_db_is_idempotent() -> None:
    """Calling init_db twice must not raise."""
    database.init_db()
    database.init_db()  # should not raise


def test_init_db_schema_columns() -> None:
    """The todos table must have the expected columns."""
    database.init_db()
    conn = database.get_db_connection()
    try:
        cursor = conn.execute("PRAGMA table_info(todos);")
        columns = {row["name"]: row for row in cursor.fetchall()}
    finally:
        conn.close()

    assert "id" in columns
    assert "title" in columns
    assert "completed" in columns
    assert "created_at" in columns

    # title must be NOT NULL
    assert columns["title"]["notnull"] == 1
    # completed must be NOT NULL with default 0
    assert columns["completed"]["notnull"] == 1


# ------------------------------------------------------------------
# get_db_connection
# ------------------------------------------------------------------


def test_get_db_connection_row_factory() -> None:
    """Connections should use sqlite3.Row as row_factory."""
    import sqlite3

    conn = database.get_db_connection()
    try:
        assert conn.row_factory is sqlite3.Row
    finally:
        conn.close()


# ------------------------------------------------------------------
# create_todo
# ------------------------------------------------------------------


def test_create_todo_returns_dict_with_expected_keys() -> None:
    """create_todo should return a dict with id, title, completed, created_at."""
    database.init_db()
    todo = database.create_todo("Buy milk")

    assert isinstance(todo, dict)
    assert todo["title"] == "Buy milk"
    assert todo["completed"] is False
    assert "id" in todo
    assert "created_at" in todo


def test_create_todo_auto_increments_id() -> None:
    """Each new todo should receive a unique, incrementing id."""
    database.init_db()
    t1 = database.create_todo("First")
    t2 = database.create_todo("Second")
    assert t2["id"] > t1["id"]


def test_create_todo_empty_title_raises() -> None:
    """An empty title should raise ValueError."""
    database.init_db()
    with pytest.raises(ValueError, match="title must not be empty"):
        database.create_todo("")


def test_create_todo_whitespace_title_raises() -> None:
    """A whitespace-only title should raise ValueError."""
    database.init_db()
    with pytest.raises(ValueError, match="title must not be empty"):
        database.create_todo("   ")


# ------------------------------------------------------------------
# get_all_todos
# ------------------------------------------------------------------


def test_get_all_todos_empty() -> None:
    """get_all_todos on an empty table returns an empty list."""
    database.init_db()
    assert database.get_all_todos() == []


def test_get_all_todos_returns_all() -> None:
    """All created todos should appear in get_all_todos."""
    database.init_db()
    database.create_todo("A")
    database.create_todo("B")
    database.create_todo("C")

    todos = database.get_all_todos()
    assert len(todos) == 3
    titles = {t["title"] for t in todos}
    assert titles == {"A", "B", "C"}


def test_get_all_todos_completed_is_bool() -> None:
    """The completed field should be a Python bool, not an int."""
    database.init_db()
    database.create_todo("Check type")
    todo = database.get_all_todos()[0]
    assert isinstance(todo["completed"], bool)


# ------------------------------------------------------------------
# update_todo
# ------------------------------------------------------------------


def test_update_todo_marks_completed() -> None:
    """update_todo should flip the completed flag."""
    database.init_db()
    todo = database.create_todo("Do laundry")
    updated = database.update_todo(todo["id"], True)

    assert updated is not None
    assert updated["completed"] is True


def test_update_todo_marks_incomplete() -> None:
    """update_todo should be able to set completed back to False."""
    database.init_db()
    todo = database.create_todo("Do laundry")
    database.update_todo(todo["id"], True)
    updated = database.update_todo(todo["id"], False)

    assert updated is not None
    assert updated["completed"] is False


def test_update_todo_nonexistent_returns_none() -> None:
    """Updating a non-existent todo should return None."""
    database.init_db()
    result = database.update_todo(9999, True)
    assert result is None


def test_update_todo_preserves_title() -> None:
    """Updating completed should not change the title."""
    database.init_db()
    todo = database.create_todo("Keep me")
    updated = database.update_todo(todo["id"], True)

    assert updated is not None
    assert updated["title"] == "Keep me"


# ------------------------------------------------------------------
# delete_todo
# ------------------------------------------------------------------


def test_delete_todo_existing() -> None:
    """Deleting an existing todo should return True."""
    database.init_db()
    todo = database.create_todo("Delete me")
    assert database.delete_todo(todo["id"]) is True


def test_delete_todo_removes_from_db() -> None:
    """After deletion the todo should no longer appear in get_all_todos."""
    database.init_db()
    todo = database.create_todo("Gone")
    database.delete_todo(todo["id"])
    assert database.get_all_todos() == []


def test_delete_todo_nonexistent_returns_false() -> None:
    """Deleting a non-existent todo should return False."""
    database.init_db()
    assert database.delete_todo(9999) is False


def test_delete_todo_only_removes_target() -> None:
    """Deleting one todo should not affect others."""
    database.init_db()
    t1 = database.create_todo("Keep")
    t2 = database.create_todo("Remove")

    database.delete_todo(t2["id"])

    remaining = database.get_all_todos()
    assert len(remaining) == 1
    assert remaining[0]["id"] == t1["id"]


# ------------------------------------------------------------------
# Thread safety
# ------------------------------------------------------------------


def test_connection_check_same_thread_false() -> None:
    """Connections must be usable from threads other than the creating one."""
    import threading

    database.init_db()
    errors: list[str] = []

    def _worker() -> None:
        try:
            conn = database.get_db_connection()
            conn.execute("SELECT 1;")
            conn.close()
        except Exception as exc:
            errors.append(str(exc))

    t = threading.Thread(target=_worker)
    t.start()
    t.join()
    assert errors == []
