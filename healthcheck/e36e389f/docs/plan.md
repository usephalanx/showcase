# Todo Application — Architecture & API Contract

## Overview

A minimal full-stack Todo application backed by SQLite, served via FastAPI,
with a vanilla HTML/JS frontend.

## Tech Stack

| Layer    | Technology              |
| -------- | ----------------------- |
| Backend  | Python 3.11+, FastAPI   |
| Database | SQLite 3 (stdlib)       |
| Server   | Uvicorn                 |
| Frontend | Vanilla HTML/CSS/JS     |

### Dependencies

- **fastapi**
- **uvicorn**
- Python standard library **sqlite3**

## File Structure

```
.
├── main.py            # FastAPI application and route handlers
├── models.py          # Pydantic request/response models
├── database.py        # SQLite connection management and CRUD helpers
├── static/
│   └── index.html     # Single-page frontend
├── requirements.txt   # Python dependencies
├── docs/
│   └── plan.md        # This document
└── tests/
    └── test_database.py
```

## SQLite Schema

```sql
CREATE TABLE IF NOT EXISTS todos (
    id         INTEGER   PRIMARY KEY AUTOINCREMENT,
    title      TEXT      NOT NULL,
    completed  BOOLEAN   NOT NULL DEFAULT 0,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
```

- `completed` is stored as `0`/`1` in SQLite and serialised as `bool` in JSON.
- `created_at` uses SQLite's `CURRENT_TIMESTAMP` (i.e. `datetime('now')`).

## Data Models (Pydantic)

### TodoCreate

```python
class TodoCreate(BaseModel):
    title: str
```

### TodoUpdate

```python
class TodoUpdate(BaseModel):
    completed: bool
```

### TodoResponse

```python
class TodoResponse(BaseModel):
    id: int
    title: str
    completed: bool
    created_at: str
```

## API Endpoints

| Method   | Path                 | Request Body | Response Body       | Status        |
| -------- | -------------------- | ------------ | ------------------- | ------------- |
| `GET`    | `/`                  | —            | HTML page           | 200           |
| `GET`    | `/api/todos`         | —            | `TodoResponse[]`    | 200           |
| `POST`   | `/api/todos`         | `TodoCreate` | `TodoResponse`      | 201           |
| `PATCH`  | `/api/todos/{id}`    | `TodoUpdate` | `TodoResponse`      | 200 / 404     |
| `DELETE` | `/api/todos/{id}`    | —            | `{"ok": true}`      | 200 / 404     |

> **Note:** `PATCH` updates the `completed` field only — title editing is not supported.

## Database Module (`database.py`)

### Functions

| Function                          | Description                                  |
| --------------------------------- | -------------------------------------------- |
| `get_db_connection()`             | Returns `sqlite3.Connection` with `sqlite3.Row` row-factory and `check_same_thread=False` |
| `init_db()`                       | Creates the `todos` table if it doesn't exist |
| `get_all_todos()`                 | Returns all todos as a list of dicts          |
| `create_todo(title: str)`         | Inserts a new todo; returns the created dict  |
| `update_todo(id: int, completed: bool)` | Updates completed status; returns dict or `None` |
| `delete_todo(id: int)`            | Deletes a todo; returns `True`/`False`        |

Database file path: `todos.db`

## Main Application Module (`main.py`)

### Handler Functions

| Function         | Endpoint                |
| ---------------- | ----------------------- |
| `serve_index`    | `GET /`                 |
| `list_todos`     | `GET /api/todos`        |
| `create_todo`    | `POST /api/todos`       |
| `toggle_todo`    | `PATCH /api/todos/{id}` |
| `delete_todo`    | `DELETE /api/todos/{id}`|

## Frontend

A single `static/index.html` file providing a minimal UI to list, add,
toggle, and delete todos via `fetch()` calls to the API.

## Error Handling

- **404** — Returned when `PATCH` or `DELETE` targets a non-existent todo id.
- **422** — Automatically returned by FastAPI for request validation failures.

## Running the App

```bash
pip install -r requirements.txt
python -c "from database import init_db; init_db()"
uvicorn main:app --reload
```

## Test Strategy

All database functions are tested in `tests/test_database.py` using a
temporary SQLite database (via `tempfile`) so the real `todos.db` is
never modified.

Key test functions:

- `test_init_db_creates_todos_table`
- `test_init_db_is_idempotent`
- `test_init_db_schema_columns`
- `test_create_todo_returns_dict_with_expected_keys`
- `test_create_todo_auto_increments_id`
- `test_create_todo_empty_title_raises`
- `test_get_all_todos_empty`
- `test_get_all_todos_returns_all`
- `test_update_todo_marks_completed`
- `test_update_todo_nonexistent_returns_none`
- `test_delete_todo_existing`
- `test_delete_todo_nonexistent_returns_false`
- `test_connection_check_same_thread_false`
