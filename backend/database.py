"""SQLite database layer for the Kanban board application.

Provides connection management, schema initialization with tables for
users, boards, columns, and cards. Includes an init_db() function that
creates all tables and a helper to seed default columns on board creation.
"""

from __future__ import annotations

import os
import sqlite3
from datetime import datetime
from typing import Any, Dict, List, Optional

DATABASE_PATH: str = os.environ.get("KANBAN_DB_PATH", "kanban.db")

DEFAULT_COLUMNS: List[str] = ["Backlog", "In Progress", "Review", "Done"]


def get_db_connection() -> sqlite3.Connection:
    """Return a new SQLite connection with row-factory enabled.

    The connection is created with ``check_same_thread=False`` so it can
    be safely shared across threads (e.g. in an ASGI server).  Foreign
    key enforcement is enabled on every connection.

    Returns:
        sqlite3.Connection: A connection to the SQLite database.
    """
    conn = sqlite3.connect(DATABASE_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def init_db() -> None:
    """Initialise the database by creating all required tables.

    Tables created:
    - users (id, username, email, hashed_password, created_at)
    - boards (id, user_id FK, title, created_at)
    - columns (id, board_id FK, title, position)
    - cards (id, column_id FK, title, description, position, created_at)
    """
    conn = get_db_connection()
    try:
        conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS users (
                id              INTEGER   PRIMARY KEY AUTOINCREMENT,
                username        TEXT      NOT NULL UNIQUE,
                email           TEXT      NOT NULL UNIQUE,
                hashed_password TEXT      NOT NULL,
                created_at      TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS boards (
                id         INTEGER   PRIMARY KEY AUTOINCREMENT,
                user_id    INTEGER   NOT NULL,
                title      TEXT      NOT NULL,
                created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            );

            CREATE TABLE IF NOT EXISTS columns (
                id       INTEGER PRIMARY KEY AUTOINCREMENT,
                board_id INTEGER NOT NULL,
                title    TEXT    NOT NULL,
                position INTEGER NOT NULL DEFAULT 0,
                FOREIGN KEY (board_id) REFERENCES boards(id) ON DELETE CASCADE
            );

            CREATE TABLE IF NOT EXISTS cards (
                id          INTEGER   PRIMARY KEY AUTOINCREMENT,
                column_id   INTEGER   NOT NULL,
                title       TEXT      NOT NULL,
                description TEXT      NOT NULL DEFAULT '',
                position    INTEGER   NOT NULL DEFAULT 0,
                created_at  TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (column_id) REFERENCES columns(id) ON DELETE CASCADE
            );
            """
        )
        conn.commit()
    finally:
        conn.close()


def _row_to_dict(row: Optional[sqlite3.Row]) -> Optional[Dict[str, Any]]:
    """Convert a sqlite3.Row to a plain dictionary.

    Args:
        row: A single database row, or None.

    Returns:
        A dictionary representation of the row, or None.
    """
    if row is None:
        return None
    return dict(row)


# ---------------------------------------------------------------------------
# User helpers
# ---------------------------------------------------------------------------


def create_user(username: str, email: str, hashed_password: str) -> Dict[str, Any]:
    """Insert a new user and return the created record.

    Args:
        username: Unique username.
        email: Unique email address.
        hashed_password: Pre-hashed password string.

    Returns:
        A dictionary representing the new user row.

    Raises:
        sqlite3.IntegrityError: If username or email already exists.
    """
    conn = get_db_connection()
    try:
        cursor = conn.execute(
            "INSERT INTO users (username, email, hashed_password) VALUES (?, ?, ?);",
            (username, email, hashed_password),
        )
        conn.commit()
        user_id = cursor.lastrowid
        cursor = conn.execute("SELECT * FROM users WHERE id = ?;", (user_id,))
        return _row_to_dict(cursor.fetchone())  # type: ignore[return-value]
    finally:
        conn.close()


def get_user_by_username(username: str) -> Optional[Dict[str, Any]]:
    """Retrieve a user by username.

    Args:
        username: The username to look up.

    Returns:
        A dictionary of user data or None if not found.
    """
    conn = get_db_connection()
    try:
        cursor = conn.execute("SELECT * FROM users WHERE username = ?;", (username,))
        return _row_to_dict(cursor.fetchone())
    finally:
        conn.close()


def get_user_by_email(email: str) -> Optional[Dict[str, Any]]:
    """Retrieve a user by email.

    Args:
        email: The email address to look up.

    Returns:
        A dictionary of user data or None if not found.
    """
    conn = get_db_connection()
    try:
        cursor = conn.execute("SELECT * FROM users WHERE email = ?;", (email,))
        return _row_to_dict(cursor.fetchone())
    finally:
        conn.close()


def get_user_by_id(user_id: int) -> Optional[Dict[str, Any]]:
    """Retrieve a user by primary key.

    Args:
        user_id: The id of the user.

    Returns:
        A dictionary of user data or None if not found.
    """
    conn = get_db_connection()
    try:
        cursor = conn.execute("SELECT * FROM users WHERE id = ?;", (user_id,))
        return _row_to_dict(cursor.fetchone())
    finally:
        conn.close()


# ---------------------------------------------------------------------------
# Board helpers
# ---------------------------------------------------------------------------


def create_board(user_id: int, title: str) -> Dict[str, Any]:
    """Create a new board and seed it with default columns.

    The default columns created are: Backlog, In Progress, Review, Done
    (positions 0-3).

    Args:
        user_id: The owning user's id.
        title: The board title.

    Returns:
        A dictionary representing the newly created board.
    """
    conn = get_db_connection()
    try:
        cursor = conn.execute(
            "INSERT INTO boards (user_id, title) VALUES (?, ?);",
            (user_id, title),
        )
        board_id = cursor.lastrowid

        for position, col_title in enumerate(DEFAULT_COLUMNS):
            conn.execute(
                "INSERT INTO columns (board_id, title, position) VALUES (?, ?, ?);",
                (board_id, col_title, position),
            )

        conn.commit()

        cursor = conn.execute("SELECT * FROM boards WHERE id = ?;", (board_id,))
        return _row_to_dict(cursor.fetchone())  # type: ignore[return-value]
    finally:
        conn.close()


def get_boards_by_user(user_id: int) -> List[Dict[str, Any]]:
    """Retrieve all boards belonging to a user.

    Args:
        user_id: The owner's user id.

    Returns:
        A list of board dictionaries ordered by creation date descending.
    """
    conn = get_db_connection()
    try:
        cursor = conn.execute(
            "SELECT * FROM boards WHERE user_id = ? ORDER BY created_at DESC;",
            (user_id,),
        )
        return [_row_to_dict(row) for row in cursor.fetchall()]  # type: ignore[misc]
    finally:
        conn.close()


def get_board_by_id(board_id: int) -> Optional[Dict[str, Any]]:
    """Retrieve a single board by id.

    Args:
        board_id: The board's primary key.

    Returns:
        A board dictionary or None.
    """
    conn = get_db_connection()
    try:
        cursor = conn.execute("SELECT * FROM boards WHERE id = ?;", (board_id,))
        return _row_to_dict(cursor.fetchone())
    finally:
        conn.close()


# ---------------------------------------------------------------------------
# Column helpers
# ---------------------------------------------------------------------------


def get_columns_by_board(board_id: int) -> List[Dict[str, Any]]:
    """Retrieve all columns for a board ordered by position.

    Args:
        board_id: The board's primary key.

    Returns:
        A list of column dictionaries.
    """
    conn = get_db_connection()
    try:
        cursor = conn.execute(
            "SELECT * FROM columns WHERE board_id = ? ORDER BY position ASC;",
            (board_id,),
        )
        return [_row_to_dict(row) for row in cursor.fetchall()]  # type: ignore[misc]
    finally:
        conn.close()


# ---------------------------------------------------------------------------
# Card helpers
# ---------------------------------------------------------------------------


def get_cards_by_column(column_id: int) -> List[Dict[str, Any]]:
    """Retrieve all cards for a column ordered by position.

    Args:
        column_id: The column's primary key.

    Returns:
        A list of card dictionaries.
    """
    conn = get_db_connection()
    try:
        cursor = conn.execute(
            "SELECT * FROM cards WHERE column_id = ? ORDER BY position ASC;",
            (column_id,),
        )
        return [_row_to_dict(row) for row in cursor.fetchall()]  # type: ignore[misc]
    finally:
        conn.close()
