# Todo API — Architecture

## Overview

A simple RESTful Todo API built with **FastAPI** and **Pydantic v2**.  Data is
stored in-memory (no database) and resets on process restart.  The API exposes
standard CRUD operations on todo items.

## Technology Choices

| Component      | Technology            |
|----------------|-----------------------|
| Framework      | FastAPI               |
| Validation     | Pydantic v2           |
| Server         | Uvicorn               |
| Testing        | pytest + httpx        |
| Python         | 3.11+                 |

## Project Structure

```
app/
├── __init__.py           # Package marker
├── main.py               # FastAPI application entry point
├── models.py             # Pydantic request/response schemas
├── storage.py            # In-memory storage backend
└── routes/
    ├── __init__.py       # Routes sub-package marker
    └── todos.py          # CRUD route handlers for /todos
tests/
├── __init__.py           # Test package marker
├── test_models.py        # Tests for Pydantic schemas
└── test_storage.py       # Tests for in-memory storage
```

## Data Model

Each todo item has the following fields:

| Field         | Type   | Notes                                      |
|---------------|--------|--------------------------------------------|
| `id`          | `int`  | Auto-generated, read-only, unique          |
| `title`       | `str`  | Required, minimum 1 character              |
| `description` | `str`  | Optional, defaults to empty string `""`    |
| `completed`   | `bool` | Defaults to `False` on creation            |

The `id` field is **never** accepted in create or update requests — it is
assigned by the storage layer.

## Pydantic Schemas

### `TodoCreate` (request body for POST)

- `title`: `str` — required, min length 1
- `description`: `str` — optional, defaults to `""`

### `TodoUpdate` (request body for PUT)

All fields are **optional** to support partial updates:

- `title`: `Optional[str]` — min length 1 when provided
- `description`: `Optional[str]`
- `completed`: `Optional[bool]`

### `TodoResponse` (response body)

- `id`: `int`
- `title`: `str`
- `description`: `str`
- `completed`: `bool`

## API Endpoints

| Method   | Path             | Request Body | Response            | Status  |
|----------|------------------|--------------|---------------------|---------|
| `GET`    | `/todos`         | —            | `List[TodoResponse]`| `200`   |
| `GET`    | `/todos/{id}`    | —            | `TodoResponse`      | `200`   |
| `POST`   | `/todos`         | `TodoCreate` | `TodoResponse`      | `201`   |
| `PUT`    | `/todos/{id}`    | `TodoUpdate` | `TodoResponse`      | `200`   |
| `DELETE` | `/todos/{id}`    | —            | No body             | `204`   |

### Error Responses

- `404 Not Found` — returned by GET (single), PUT, and DELETE when the
  requested `id` does not exist.  Body: `{"detail": "Todo not found"}`.
- `422 Unprocessable Entity` — returned when the request body fails
  Pydantic validation (e.g. missing `title` on create).

## In-Memory Storage

The storage layer (`app/storage.py`) uses a `TodoStorage` class:

- **`_todos`**: `dict[int, dict]` — mapping of todo id → todo data dictionary.
- **`_counter`**: `int` — auto-incrementing counter for generating unique ids.

### Storage API

| Method                           | Returns               | Description                                  |
|----------------------------------|-----------------------|----------------------------------------------|
| `get_all()`                      | `list[dict]`          | Return all todos                             |
| `get_by_id(todo_id: int)`        | `dict \| None`        | Return one todo or `None`                    |
| `create(data: dict)`             | `dict`                | Create a todo with auto-assigned id          |
| `update(todo_id: int, data: dict)` | `dict \| None`      | Partial update; `None` values are ignored    |
| `delete(todo_id: int)`           | `bool`                | `True` if deleted, `False` if not found      |
| `clear()`                        | `None`                | Reset store and counter (for tests)          |

A module-level **singleton** instance `storage` is exported for use by route
handlers.

> **Note:** Data is not persistent.  Restarting the server clears all todos.

## Testing Strategy

Tests are located in the `tests/` directory and run with `pytest`.

### Planned Test Functions

- `test_create_todo` — POST creates a todo and returns 201
- `test_list_todos` — GET /todos returns all items
- `test_get_todo_by_id` — GET /todos/{id} returns the correct item
- `test_get_todo_not_found_returns_404` — GET /todos/{id} with bad id → 404
- `test_update_todo` — PUT /todos/{id} updates fields correctly
- `test_update_todo_not_found_returns_404` — PUT /todos/{id} with bad id → 404
- `test_delete_todo` — DELETE /todos/{id} returns 204
- `test_delete_todo_not_found_returns_404` — DELETE /todos/{id} with bad id → 404
- `test_create_todo_missing_title_returns_422` — POST without title → 422
