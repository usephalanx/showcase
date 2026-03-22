"""SQLite database layer for the Todo application.

Provides connection management, schema initialization, and CRUD helper
functions for the 'todos' table.  Uses a file-based SQLite database
(todos.db) with check_same_thread=False for thread safety.
"""

from __future__ import annotations

import sqlite3
from typing import Any, Dict, List, Optional

DATABASE_PATH: str = "todos.db"


def get_db_connection() -> sqlite3.Connection:
    """Return a new SQLite connection with row-factory enabled.

    The connection is created with ``check_same_thread=False`` so it can
    be safely shared across threads (e.g. in an ASGI server).

    Returns:
        sqlite3.Connection: A connection to the SQLite database.
    """
    conn = sqlite3.connect(DATABASE_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    """Initialise the database by creating the 'todos' table if it does not exist.

    Schema
    ------
    - id : INTEGER PRIMARY KEY AUTOINCREMENT
    - title : TEXT NOT NULL
    - completed : BOOLEAN NOT NULL DEFAULT 0
    - created_at : TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
    """
    conn = get_db_connection()
    try:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS todos (
                id         INTEGER   PRIMARY KEY AUTOINCREMENT,
                title      TEXT      NOT NULL,
                completed  BOOLEAN   NOT NULL DEFAULT 0,
                created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
            );
            """
        )
        conn.commit()
    finally:
        conn.close()


def _row_to_dict(row: sqlite3.Row) -> Dict[str, Any]:
    """Convert a sqlite3.Row to a plain dictionary.

    The ``completed`` column is stored as 0/1 in SQLite and is
    normalised to a Python ``bool`` here.

    Args:
        row: A single database row.

    Returns:
        A dictionary representation of the row.
    """
    d = dict(row)
    d["completed"] = bool(d["completed"])
    return d


def get_all_todos() -> List[Dict[str, Any]]:
    """Retrieve every todo from the database ordered by creation time (desc).

    Returns:
        A list of dictionaries, each representing a todo item.
    """
    conn = get_db_connection()
    try:
        cursor = conn.execute("SELECT * FROM todos ORDER BY created_at DESC;")
        rows = cursor.fetchall()
        return [_row_to_dict(row) for row in rows]
    finally:
        conn.close()


def create_todo(title: str) -> Dict[str, Any]:
    """Insert a new todo and return it.

    Args:
        title: The title text of the todo item.  Must not be empty.

    Returns:
        A dictionary representing the newly created todo.

    Raises:
        ValueError: If *title* is empty or whitespace-only.
    """
    if not title or not title.strip():
        raise ValueError("title must not be empty")

    conn = get_db_connection()
    try:
        cursor = conn.execute(
            "INSERT INTO todos (title) VALUES (?);",
            (title,),
        )
        conn.commit()
        todo_id = cursor.lastrowid

        cursor = conn.execute("SELECT * FROM todos WHERE id = ?;", (todo_id,))
        row = cursor.fetchone()
        return _row_to_dict(row)
    finally:
        conn.close()


def update_todo(todo_id: int, completed: bool) -> Optional[Dict[str, Any]]:
    """Update the ``completed`` status of an existing todo.

    Args:
        todo_id: The primary-key id of the todo to update.
        completed: The new completion status.

    Returns:
        A dictionary of the updated todo, or ``None`` if no todo with
        the given *todo_id* exists.
    """
    conn = get_db_connection()
    try:
        cursor = conn.execute(
            "UPDATE todos SET completed = ? WHERE id = ?;",
            (int(completed), todo_id),
        )
        conn.commit()

        if cursor.rowcount == 0:
            return None

        cursor = conn.execute("SELECT * FROM todos WHERE id = ?;", (todo_id,))
        row = cursor.fetchone()
        return _row_to_dict(row)
    finally:
        conn.close()


def delete_todo(todo_id: int) -> bool:
    """Delete a todo by its id.

    Args:
        todo_id: The primary-key id of the todo to delete.

    Returns:
        ``True`` if a row was deleted, ``False`` if no matching row existed.
    """
    conn = get_db_connection()
    try:
        cursor = conn.execute("DELETE FROM todos WHERE id = ?;", (todo_id,))
        conn.commit()
        return cursor.rowcount > 0
    finally:
        conn.close()
