# Todo API — Planning Document

## Overview

A lightweight RESTful Todo API built with **FastAPI** and backed by an
in-memory Python dictionary.  Designed for learning, prototyping, and
automated testing — not for production persistence.

## Data Model

### Todo

| Field        | Type            | Default         | Notes                        |
|--------------|-----------------|-----------------|------------------------------|
| id           | int             | auto-increment  | Primary key, assigned by store |
| title        | str             | *(required)*    | Must be at least 1 character |
| description  | Optional[str]   | None            | Free-text description        |
| completed    | bool            | False           | Completion status            |
| created_at   | str (ISO 8601)  | UTC now         | Set once at creation time    |

## API Endpoints

| Method | Path              | Request Body | Success Status | Response Body        |
|--------|-------------------|--------------|----------------|----------------------|
| GET    | `/`               | —            | 200            | `{"message": "..."}` |
| POST   | `/todos`          | TodoCreate   | 201            | TodoResponse         |
| GET    | `/todos`          | —            | 200            | List[TodoResponse]   |
| GET    | `/todos/{todo_id}`| —            | 200            | TodoResponse         |
| PUT    | `/todos/{todo_id}`| TodoUpdate   | 200            | TodoResponse         |
| DELETE | `/todos/{todo_id}`| —            | 204            | *(empty)*            |

### Error Responses

- **404 Not Found** — returned by GET, PUT, DELETE when `todo_id` does
  not exist. Body: `{"detail": "Todo not found"}`.
- **422 Unprocessable Entity** — returned automatically by FastAPI when
  the request body fails Pydantic validation.

## Project Structure

```
.
├── main.py          # FastAPI app creation, router mounting, uvicorn entry point
├── routes.py        # APIRouter with all five CRUD endpoints
├── models.py        # Pydantic request/response schemas
├── storage.py       # In-memory TodoStore class
├── requirements.txt # Python dependency pins
├── conftest.py      # Root pytest configuration
├── tests/
│   ├── test_main.py # Tests for the root endpoint and app wiring
│   └── ...          # Additional test modules
├── PLANNING.md      # This file
└── RUNNING.md       # How to install and run
```

## Design Decisions

1. **In-memory storage** — chosen for simplicity; no external database
   dependency.  The `TodoStore` class encapsulates all state so it can
   be swapped for a persistent backend later.

2. **Auto-incrementing integer IDs** — simple, predictable, easy to test.
   A production system might use UUIDs.

3. **Module-level store instance in routes.py** — the store is
   instantiated once when the module is imported.  Tests reset it via
   `store.reset()` to ensure isolation.

4. **Partial updates via PUT with optional fields** — `TodoUpdate` has
   all-optional fields; only non-`None` values are applied.  This keeps
   the endpoint count low while supporting partial changes.

5. **204 No Content for DELETE** — follows REST conventions; the
   response body is empty on successful deletion.
