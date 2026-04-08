# Todo API — Architecture

## Overview

A simple RESTful Todo API built with **FastAPI** and backed by an
**in-memory Python dictionary**.  Data is **not** persistent and resets
when the process restarts.

## Project Structure

```
app/
├── __init__.py          # Package marker
├── main.py              # FastAPI application entry point
├── models.py            # Pydantic request/response schemas
├── storage.py           # In-memory storage backend
└── routes/
    ├── __init__.py      # Sub-package marker
    └── todos.py         # CRUD route handlers
tests/
├── __init__.py
├── conftest.py          # Shared fixtures (TestClient, storage reset)
├── test_todos.py        # Integration tests for endpoints
└── test_storage.py      # Unit tests for TodoStorage
```

## Technology Choices

| Concern        | Choice                            |
| -------------- | --------------------------------- |
| Framework      | FastAPI                           |
| Validation     | Pydantic v2                       |
| Server         | Uvicorn                           |
| Testing        | pytest + `fastapi.testclient`     |

## Data Model

Each todo item has the following fields:

| Field         | Type   | Notes                                     |
| ------------- | ------ | ----------------------------------------- |
| `id`          | `int`  | Auto-generated, read-only                 |
| `title`       | `str`  | Required, min length 1                    |
| `description` | `str`  | Optional, defaults to `""`                |
| `completed`   | `bool` | Defaults to `False`                       |

### Pydantic Schemas

- **`TodoCreate`** — `title` (required), `description` (optional, default `""`).
- **`TodoUpdate`** — `title`, `description`, `completed` — all optional to
  support partial updates.  Only fields explicitly sent in the request body
  are applied (`exclude_unset=True`).
- **`TodoResponse`** — `id`, `title`, `description`, `completed`.

## API Endpoints

All endpoints are prefixed with `/todos`.

| Method   | Path            | Request Body  | Success Code | Response Body          |
| -------- | --------------- | ------------- | ------------ | ---------------------- |
| `GET`    | `/todos`        | —             | 200          | `List[TodoResponse]`   |
| `GET`    | `/todos/{id}`   | —             | 200          | `TodoResponse`         |
| `POST`   | `/todos`        | `TodoCreate`  | 201          | `TodoResponse`         |
| `PUT`    | `/todos/{id}`   | `TodoUpdate`  | 200          | `TodoResponse`         |
| `DELETE` | `/todos/{id}`   | —             | 204          | No body                |

### Error Responses

| Condition               | Status | Detail             |
| ----------------------- | ------ | ------------------ |
| Todo not found          | 404    | `"Todo not found"` |
| Validation failure      | 422    | Pydantic errors    |

## In-Memory Storage

The storage layer (`app/storage.py`) uses:

- A Python `dict[int, dict]` (`_todos`) mapping todo ids to data dicts.
- An `int` counter (`_counter`) for auto-incrementing ids.

### Helper Functions

| Method                              | Returns             | Description                              |
| ----------------------------------- | ------------------- | ---------------------------------------- |
| `get_all()`                         | `list[dict]`        | Return all todos                         |
| `get_by_id(id: int)`               | `dict \| None`      | Return one todo or `None`                |
| `create(data: dict)`               | `dict`              | Create and return a new todo             |
| `update(id: int, data: dict)`      | `dict \| None`      | Update and return, or `None` if missing  |
| `delete(id: int)`                  | `bool`              | `True` if deleted, `False` if not found  |
| `clear()`                          | `None`              | Reset store and counter (for tests)      |

A module-level singleton `storage = TodoStorage()` is imported by the
route handlers.

> **Note:** Data is ephemeral.  Restarting the server clears all todos.

## Testing Strategy

Tests live in the `tests/` directory and use `pytest`.

### Integration Tests (`test_todos.py`)

- `test_create_todo` — POST returns 201 with correct body
- `test_create_todo_default_description` — description defaults to `""`
- `test_create_todo_missing_title_returns_422` — validation error
- `test_create_todo_empty_title_returns_422` — min_length enforced
- `test_list_todos_empty` — empty store returns `[]`
- `test_list_todos` — returns all created todos
- `test_get_todo_by_id` — returns correct todo
- `test_get_todo_not_found_returns_404` — 404 for missing id
- `test_update_todo` — partial update works
- `test_update_todo_not_found_returns_404` — 404 for missing id
- `test_delete_todo` — returns 204, todo is removed
- `test_delete_todo_not_found_returns_404` — 404 for missing id

### Unit Tests (`test_storage.py`)

- Tests for each `TodoStorage` method including edge cases
- `clear()` resets both the dict and the counter
