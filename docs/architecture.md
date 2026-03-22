# Architecture

## Project File Structure

```
.
├── database.py          # SQLite database access layer
├── main.py              # FastAPI application and route handlers
├── models.py            # Pydantic data-validation models
├── static/
│   └── index.html       # Single-file HTML/JS/CSS frontend
├── requirements.txt     # Python dependencies
├── docs/
│   ├── architecture.md  # This file
│   └── api-spec.md      # REST API specification
└── tests/
    ├── test_database.py           # Unit tests for database layer
    └── test_docs_completeness.py  # Structural tests for docs
```

## Technology Stack

| Layer       | Technology            | Notes                                    |
|-------------|-----------------------|------------------------------------------|
| Language    | Python 3.11+          |                                          |
| Web framework | FastAPI             | ASGI, async route handlers               |
| Server      | uvicorn               | ASGI server                              |
| Database    | SQLite (stdlib sqlite3) | File-based, zero-config                |
| Validation  | Pydantic v2           | Request/response models                  |
| Frontend    | Vanilla HTML/JS/CSS   | Served as a static file from `GET /`     |

## SQLite Schema

The application uses a single table:

```sql
CREATE TABLE IF NOT EXISTS todos (
    id         INTEGER   PRIMARY KEY AUTOINCREMENT,
    title      TEXT      NOT NULL,
    completed  BOOLEAN   NOT NULL DEFAULT 0,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
```

### Column Details

| Column       | Type      | Constraints                          | Description                         |
|--------------|-----------|--------------------------------------|-------------------------------------|
| `id`         | INTEGER   | PRIMARY KEY AUTOINCREMENT            | Unique identifier                   |
| `title`      | TEXT      | NOT NULL                             | Title of the todo item              |
| `completed`  | BOOLEAN   | NOT NULL DEFAULT 0                   | Completion flag (0 = false, 1 = true) |
| `created_at` | TIMESTAMP | NOT NULL DEFAULT CURRENT_TIMESTAMP   | Row creation time (SQLite-managed)  |

- `created_at` defaults to `CURRENT_TIMESTAMP` on the SQLite side, keeping the schema self-contained.
- `completed` defaults to `0` (false) so new todos are always incomplete.

## Startup / Shutdown Lifecycle

1. **Startup** — FastAPI lifespan event calls `database.init_db()`, which
   creates the `todos` table if it does not already exist.
2. **Runtime** — Each request handler calls synchronous `database.*`
   functions. Connections are obtained via a context manager
   (`get_db_connection`) that ensures they are always closed.
3. **Shutdown** — No special teardown is needed; SQLite connections are
   short-lived and closed after each operation.

## Component Diagram

```
┌──────────┐       HTTP        ┌─────────────────────┐
│          │ ◄───────────────► │  FastAPI (main.py)  │
│ Browser  │                   │                     │
│          │   GET / (HTML)    │  Route handlers     │
└──────────┘   /api/* (JSON)   │  Pydantic models    │
                               └─────────┬───────────┘
                                         │
                                         │ function calls
                                         ▼
                               ┌─────────────────────┐
                               │  database.py        │
                               │                     │
                               │  get_db_connection() │
                               │  init_db()          │
                               │  get_all_todos()    │
                               │  create_todo()      │
                               │  update_todo_completed() │
                               │  delete_todo()      │
                               └─────────┬───────────┘
                                         │
                                         │ sqlite3
                                         ▼
                               ┌─────────────────────┐
                               │  todos.db (SQLite)  │
                               └─────────────────────┘
```
