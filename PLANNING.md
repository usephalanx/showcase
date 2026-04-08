# Todo API — Planning Document

## Overview

A simple RESTful Todo API built with FastAPI, using an in-memory dictionary
as the persistence layer. Designed for development and testing purposes.

## Data Model

### Todo Item

| Field       | Type            | Required | Default | Notes                      |
|-------------|-----------------|----------|---------|----------------------------|
| id          | int             | auto     | —       | Auto-incremented integer   |
| title       | str             | yes      | —       | Min length 1               |
| description | Optional[str]   | no       | None    | Free-text description      |
| completed   | bool            | no       | False   | Completion flag            |
| created_at  | str (ISO 8601)  | auto     | —       | UTC timestamp at creation  |

## API Endpoints

| Method | Path             | Status | Description              |
|--------|------------------|--------|--------------------------|
| GET    | /                | 200    | Health / welcome message |
| POST   | /todos           | 201    | Create a new todo        |
| GET    | /todos           | 200    | List all todos           |
| GET    | /todos/{todo_id} | 200    | Get a single todo        |
| PUT    | /todos/{todo_id} | 200    | Update an existing todo  |
| DELETE | /todos/{todo_id} | 204    | Delete a todo            |

### Error Responses

- **404 Not Found** — returned by GET /todos/{id}, PUT /todos/{id}, and
  DELETE /todos/{id} when the requested todo does not exist.
- **422 Unprocessable Entity** — returned by FastAPI when the request body
  fails Pydantic validation.

## Project Structure

```
.
├── main.py          # FastAPI app entry point, mounts router
├── models.py        # Pydantic request/response schemas
├── storage.py       # In-memory TodoStore class
├── routes.py        # APIRouter with all CRUD handlers
├── conftest.py      # Root pytest configuration
├── requirements.txt # Pinned Python dependencies
├── tests/
│   ├── __init__.py
│   └── test_routes.py  # Full endpoint test suite
└── PLANNING.md      # This file
```

## Design Decisions

1. **In-memory store** — chosen for simplicity; no external dependencies.
   Data is lost on restart, which is acceptable for dev/test.
2. **Auto-increment ID** — a simple counter in `TodoStore` ensures unique,
   predictable IDs without external libraries.
3. **Partial updates via PUT** — only fields supplied in the request body
   are changed; `None` values are skipped.
4. **DELETE returns 204** — follows REST conventions; no body is returned.
5. **Store instance on the router module** — keeps the store accessible for
   both route handlers and test fixtures (via import + `.reset()`).
