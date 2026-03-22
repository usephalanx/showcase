"""Tests for backend/database.py — schema creation, user CRUD, board seeding."""

from __future__ import annotations

import os
import sqlite3
import sys
import tempfile
from typing import Generator

import pytest

# Ensure the backend package is importable
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "backend"))

import database


@pytest.fixture(autouse=True)
def _use_temp_db(tmp_path: object) -> Generator[None, None, None]:
    """Redirect the database to a temporary file for each test."""
    fd, path = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    database.DATABASE_PATH = path
    database.init_db()
    yield
    os.unlink(path)


# ---------------------------------------------------------------------------
# Schema tests
# ---------------------------------------------------------------------------


def test_init_db_creates_tables() -> None:
    """init_db should create users, boards, columns, and cards tables."""
    conn = database.get_db_connection()
    try:
        cursor = conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;"
        )
        tables = {row["name"] for row in cursor.fetchall()}
    finally:
        conn.close()

    assert "users" in tables
    assert "boards" in tables
    assert "columns" in tables
    assert "cards" in tables


def test_users_table_columns() -> None:
    """The users table should have the expected columns."""
    conn = database.get_db_connection()
    try:
        cursor = conn.execute("PRAGMA table_info(users);")
        cols = {row["name"] for row in cursor.fetchall()}
    finally:
        conn.close()

    assert cols == {"id", "username", "email", "hashed_password", "created_at"}


def test_boards_table_columns() -> None:
    """The boards table should have the expected columns."""
    conn = database.get_db_connection()
    try:
        cursor = conn.execute("PRAGMA table_info(boards);")
        cols = {row["name"] for row in cursor.fetchall()}
    finally:
        conn.close()

    assert cols == {"id", "user_id", "title", "created_at"}


def test_columns_table_columns() -> None:
    """The columns table should have the expected columns."""
    conn = database.get_db_connection()
    try:
        cursor = conn.execute("PRAGMA table_info(columns);")
        cols = {row["name"] for row in cursor.fetchall()}
    finally:
        conn.close()

    assert cols == {"id", "board_id", "title", "position"}


def test_cards_table_columns() -> None:
    """The cards table should have the expected columns."""
    conn = database.get_db_connection()
    try:
        cursor = conn.execute("PRAGMA table_info(cards);")
        cols = {row["name"] for row in cursor.fetchall()}
    finally:
        conn.close()

    assert cols == {"id", "column_id", "title", "description", "position", "created_at"}


# ---------------------------------------------------------------------------
# User CRUD tests
# ---------------------------------------------------------------------------


def test_create_user() -> None:
    """create_user should insert a user and return the row."""
    user = database.create_user("alice", "alice@example.com", "hashed_pw")
    assert user["username"] == "alice"
    assert user["email"] == "alice@example.com"
    assert user["hashed_password"] == "hashed_pw"
    assert "id" in user
    assert "created_at" in user


def test_create_user_duplicate_username() -> None:
    """Creating a user with an existing username should raise IntegrityError."""
    database.create_user("bob", "bob@example.com", "pw1")
    with pytest.raises(sqlite3.IntegrityError):
        database.create_user("bob", "bob2@example.com", "pw2")


def test_create_user_duplicate_email() -> None:
    """Creating a user with an existing email should raise IntegrityError."""
    database.create_user("charlie", "charlie@example.com", "pw1")
    with pytest.raises(sqlite3.IntegrityError):
        database.create_user("charlie2", "charlie@example.com", "pw2")


def test_get_user_by_username() -> None:
    """get_user_by_username should find an existing user."""
    database.create_user("dave", "dave@example.com", "pw")
    user = database.get_user_by_username("dave")
    assert user is not None
    assert user["email"] == "dave@example.com"


def test_get_user_by_username_not_found() -> None:
    """get_user_by_username should return None for missing users."""
    assert database.get_user_by_username("nonexistent") is None


def test_get_user_by_email() -> None:
    """get_user_by_email should find an existing user."""
    database.create_user("eve", "eve@example.com", "pw")
    user = database.get_user_by_email("eve@example.com")
    assert user is not None
    assert user["username"] == "eve"


def test_get_user_by_email_not_found() -> None:
    """get_user_by_email should return None for missing emails."""
    assert database.get_user_by_email("ghost@example.com") is None


def test_get_user_by_id() -> None:
    """get_user_by_id should find an existing user."""
    user = database.create_user("frank", "frank@example.com", "pw")
    found = database.get_user_by_id(user["id"])
    assert found is not None
    assert found["username"] == "frank"


def test_get_user_by_id_not_found() -> None:
    """get_user_by_id should return None for missing ids."""
    assert database.get_user_by_id(999) is None


# ---------------------------------------------------------------------------
# Board & default column seeding tests
# ---------------------------------------------------------------------------


def test_create_board_seeds_default_columns() -> None:
    """create_board should create the board and seed 4 default columns."""
    user = database.create_user("grace", "grace@example.com", "pw")
    board = database.create_board(user["id"], "My Board")

    assert board["title"] == "My Board"
    assert board["user_id"] == user["id"]

    cols = database.get_columns_by_board(board["id"])
    assert len(cols) == 4
    assert [c["title"] for c in cols] == ["Backlog", "In Progress", "Review", "Done"]
    assert [c["position"] for c in cols] == [0, 1, 2, 3]


def test_get_boards_by_user() -> None:
    """get_boards_by_user should return all boards for a user."""
    user = database.create_user("hank", "hank@example.com", "pw")
    database.create_board(user["id"], "Board 1")
    database.create_board(user["id"], "Board 2")

    boards = database.get_boards_by_user(user["id"])
    assert len(boards) == 2
    titles = {b["title"] for b in boards}
    assert titles == {"Board 1", "Board 2"}


def test_get_board_by_id() -> None:
    """get_board_by_id should return the correct board."""
    user = database.create_user("ivan", "ivan@example.com", "pw")
    board = database.create_board(user["id"], "Test Board")
    found = database.get_board_by_id(board["id"])
    assert found is not None
    assert found["title"] == "Test Board"


def test_get_board_by_id_not_found() -> None:
    """get_board_by_id should return None for missing boards."""
    assert database.get_board_by_id(999) is None


# ---------------------------------------------------------------------------
# Cards helpers
# ---------------------------------------------------------------------------


def test_get_cards_by_column_empty() -> None:
    """get_cards_by_column should return an empty list for a column with no cards."""
    user = database.create_user("judy", "judy@example.com", "pw")
    board = database.create_board(user["id"], "B")
    cols = database.get_columns_by_board(board["id"])
    cards = database.get_cards_by_column(cols[0]["id"])
    assert cards == []


def test_init_db_idempotent() -> None:
    """Calling init_db multiple times should not raise errors."""
    database.init_db()
    database.init_db()
    # Simply assert no exception is raised
