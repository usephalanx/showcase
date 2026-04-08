# Todo API — Architecture Plan

## Overview

A lightweight RESTful Todo API built with **FastAPI** and backed by an
in-memory Python dictionary for storage.  Designed for learning, prototyping,
and testing — not for production persistence.

## Project Structure

| File | Responsibility |
|---|---|
| `main.py` | FastAPI application factory, mount router, lifespan events |
| `models.py` | Pydantic request/response schemas |
| `routes.py` | `APIRouter` with all five CRUD endpoints |
| `storage.py` | Dict-based in-memory store with auto-incrementing ID counter |
| `tests/test_todos.py` | Pytest tests using FastAPI `TestClient` |

## Data Model

### Internal representation (stored in `dict[int, dict]`)

| Field | Type | Notes |
|---|---|---|
| `id` | `int` | Auto-incremented primary key |
| `title` | `str` | Required, non-empty |
| `description` | `Optional[str]` | May be `None` |
| `completed` | `bool` | Defaults to `False` |
| `created_at` | `str` | ISO-8601 UTC timestamp, set on creation |

### Pydantic models

**TodoCreate**

| Field | Type | Default |
|---|---|---|
| `title` | `str` | *required* (min_length=1) |
| `description` | `Optional[str]` | `None` |
| `completed` | `Optional[bool]` | `False` |

**TodoUpdate**

| Field | Type | Default |
|---|---|---|
| `title` | `Optional[str]` | `None` |
| `description` | `Optional[str]` | `None` |
| `completed` | `Optional[bool]` | `None` |

**TodoResponse**

| Field | Type | Default |
|---|---|---|
| `id` | `int` | — |
| `title` | `str` | — |
| `description` | `Optional[str]` | `None` |
| `completed` | `bool` | — |
| `created_at` | `str` | — |

## Storage

`storage.py` exposes a `TodoStore` class containing:

- `_todos: dict[int, dict]` — the data store.
- `_counter: int` — starts at `0`, incremented by `_next_id()`.

Public helpers:

- `add(title, description=None, completed=False) -> dict`
- `get(todo_id) -> Optional[dict]`
- `get_all() -> list[dict]`
- `update(todo_id, title=None, description=None, completed=None) -> Optional[dict]`
- `delete(todo_id) -> bool`
- `reset() -> None` — clears all data and resets the counter (for tests).

> **Concurrency caveat:** The plain `dict` is *not* thread-safe under
> concurrent writes.  This is acceptable for a single-worker dev server but
> must not be used in production with multiple workers.

## API Endpoints

| Method | Path | Request Body | Success Status | Response |
|---|---|---|---|---|
| `GET` | `/todos` | — | 200 | `list[TodoResponse]` |
| `GET` | `/todos/{todo_id}` | — | 200 | `TodoResponse` |
| `POST` | `/todos` | `TodoCreate` | 201 | `TodoResponse` |
| `PUT` | `/todos/{todo_id}` | `TodoUpdate` | 200 | `TodoResponse` |
| `DELETE` | `/todos/{todo_id}` | — | 204 | — |

## Error Handling

- **404 Not Found** — returned by `GET /todos/{id}`, `PUT /todos/{id}`, and
  `DELETE /todos/{id}` when the requested `todo_id` does not exist in the
  store.  Body: `{"detail": "Todo not found"}`.
- **422 Unprocessable Entity** — returned automatically by FastAPI/Pydantic
  when request validation fails.

## Design Decisions

1. **In-memory dict over SQLite:** Keeps the project zero-dependency beyond
   FastAPI itself, making it trivial to run and test.  Trade-off: no
   persistence across restarts.
2. **Separate `storage.py` module:** Isolates data access behind a clear
   interface so swapping to a database later requires changes in only one
   file.
3. **`reset()` helper on the store:** Enables deterministic test isolation
   without monkey-patching or fixture complexity.
4. **Returning copies from `get` / `get_all`:** Prevents callers from
   accidentally mutating the canonical store data.
5. **`TodoUpdate` with all-optional fields:** Supports true partial updates
   (PATCH semantics via PUT) — only supplied fields are changed.

## Test Strategy

Tests live in `tests/` and use `pytest` with FastAPI's `TestClient`.

| # | Test function | Covers |
|---|---|---|
| 1 | `test_create_todo` | POST /todos returns 201 with correct body |
| 2 | `test_create_todo_missing_title` | POST /todos with empty body returns 422 |
| 3 | `test_get_all_todos_empty` | GET /todos on fresh store returns [] |
| 4 | `test_get_all_todos` | GET /todos after adding items |
| 5 | `test_get_todo_by_id` | GET /todos/{id} returns correct item |
| 6 | `test_get_todo_not_found` | GET /todos/{id} returns 404 |
| 7 | `test_update_todo` | PUT /todos/{id} updates fields |
| 8 | `test_update_todo_not_found` | PUT /todos/{id} returns 404 |
| 9 | `test_delete_todo` | DELETE /todos/{id} returns 204 |
| 10 | `test_delete_todo_not_found` | DELETE /todos/{id} returns 404 |
