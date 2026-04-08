# Todo API — Planning & Architecture

## Overview

A simple RESTful Todo API built with FastAPI, using in-memory storage.

## Data Model

### Todo Item

| Field       | Type            | Required | Default | Notes                        |
|-------------|-----------------|----------|---------|------------------------------|
| id          | int             | auto     | —       | Auto-incremented primary key |
| title       | str             | yes      | —       | Min length 1                 |
| description | Optional[str]   | no       | None    | Longer description           |
| completed   | bool            | no       | False   | Completion status            |
| created_at  | str (ISO 8601)  | auto     | now()   | UTC timestamp                |

## Pydantic Schemas

- **TodoCreate** — `title` (required), `description` (optional), `completed` (optional, default False)
- **TodoUpdate** — all fields optional: `title`, `description`, `completed`
- **TodoResponse** — full representation: `id`, `title`, `description`, `completed`, `created_at`

## In-Memory Store Design

- Python `dict[int, dict]` keyed by todo id.
- Module-level auto-increment counter (`_counter: int`).
- Class-based (`TodoStore`) for encapsulation and easy reset in tests.
- `reset()` method clears state between test runs.
- **Not thread-safe** — acceptable for development/testing.

## API Endpoints

| Method | Path              | Request Body | Response          | Status | Description          |
|--------|-------------------|--------------|-------------------|--------|----------------------|
| GET    | /                 | —            | `{"message": …}`  | 200    | Health / welcome     |
| POST   | /todos            | TodoCreate   | TodoResponse      | 201    | Create a todo        |
| GET    | /todos            | —            | List[TodoResponse] | 200   | List all todos       |
| GET    | /todos/{todo_id}  | —            | TodoResponse      | 200    | Get single todo      |
| PUT    | /todos/{todo_id}  | TodoUpdate   | TodoResponse      | 200    | Update a todo        |
| DELETE | /todos/{todo_id}  | —            | `{"detail": …}`   | 200    | Delete a todo        |

### Error Responses

- **404** — Todo not found (GET/PUT/DELETE by id)
- **422** — Validation error (malformed request body)

## Project Structure

```
├── main.py            # FastAPI app entry point
├── models.py          # Pydantic request/response models
├── storage.py         # In-memory TodoStore class
├── store.py           # Module-level functional store interface
├── routes.py          # APIRouter with CRUD endpoints
├── requirements.txt   # Python dependencies
├── PLANNING.md        # This file
├── conftest.py        # Root pytest configuration
└── tests/
    ├── __init__.py
    ├── test_models.py     # Unit tests for Pydantic models
    ├── test_store.py      # Unit tests for store module
    └── test_api.py        # Integration tests for API endpoints
```

## Design Decisions

1. **In-memory storage** — simplicity; no external dependencies for dev/test.
2. **Auto-increment ID** — monotonically increasing integer; simple and predictable.
3. **Class-based store** — encapsulates state; `reset()` enables isolated tests.
4. **Module-level store (`store.py`)** — thin functional wrapper for alternative import style.
5. **`created_at` as ISO 8601 string** — avoids datetime serialisation issues in JSON.
6. **Partial updates via `exclude_unset`** — only supplied fields are changed on PUT.
