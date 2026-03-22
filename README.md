# Task Manager API

A FastAPI backend for managing tasks, backed by SQLite via SQLAlchemy.

## Architecture

### Database Schema

```sql
CREATE TABLE tasks (
    id          INTEGER   PRIMARY KEY AUTOINCREMENT,
    title       VARCHAR   NOT NULL,
    description VARCHAR   NOT NULL DEFAULT '',
    status      VARCHAR   NOT NULL DEFAULT 'pending',
    created_at  DATETIME  NOT NULL DEFAULT (CURRENT_TIMESTAMP)
);
```

- **id**: Auto-incrementing integer primary key.
- **title**: Required non-empty string (max 200 chars enforced at API level).
- **description**: Optional string, defaults to empty.
- **status**: One of `'pending'`, `'done'`. Defaults to `'pending'`.
- **created_at**: UTC timestamp, set automatically on row creation.

### API Endpoints

| Method | Path             | Description                        |
|--------|------------------|------------------------------------|
| POST   | `/tasks`         | Create a new task                  |
| GET    | `/tasks`         | List all tasks (newest first)      |
| PATCH  | `/tasks/{id}`    | Update a task's status             |

#### POST /tasks

**Request body:**
```json
{
  "title": "Buy groceries",
  "description": "Milk, eggs, bread"
}
```

**Response (201):**
```json
{
  "id": 1,
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "status": "pending",
  "created_at": "2024-01-15T10:30:00"
}
```

#### GET /tasks

**Response (200):**
```json
[
  {
    "id": 1,
    "title": "Buy groceries",
    "description": "Milk, eggs, bread",
    "status": "pending",
    "created_at": "2024-01-15T10:30:00"
  }
]
```

#### PATCH /tasks/{id}

**Request body:**
```json
{
  "status": "done"
}
```

**Response (200):**
```json
{
  "id": 1,
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "status": "done",
  "created_at": "2024-01-15T10:30:00"
}
```

**Response (404):**
```json
{
  "detail": "Task not found"
}
```

### CORS Configuration

CORS middleware is configured to allow **all origins** for local development:
- `allow_origins=["*"]`
- `allow_methods=["*"]`
- `allow_headers=["*"]`

### Directory Structure

```
.
├── README.md
├── requirements.txt
├── backend/
│   ├── __init__.py
│   ├── database.py      # SQLAlchemy engine, session, table creation
│   ├── models.py         # SQLAlchemy ORM model for Task
│   ├── schemas.py        # Pydantic request/response schemas
│   └── main.py           # FastAPI app, routes, CORS, lifespan
└── tests/
    ├── __init__.py
    └── test_main.py      # Integration tests using TestClient
```

## Setup & Run

```bash
pip install -r requirements.txt
uvicorn backend.main:app --reload
```

The API will be available at `http://127.0.0.1:8000`.
Interactive docs at `http://127.0.0.1:8000/docs`.

## Running Tests

```bash
pytest tests/ -v
```
