# Architecture — Todo API

## Overview

A lightweight RESTful Todo API built with **FastAPI** and backed by an
in-memory Python dictionary.  The application is intended for
demonstration and prototyping; data does **not** persist across server
restarts.

## Technology Choices

| Layer          | Technology              |
| -------------- | ----------------------- |
| Web framework  | FastAPI                 |
| Data validation| Pydantic v2             |
| ASGI server    | Uvicorn                 |
| Testing        | pytest + httpx          |

## Project Structure

```
.
├── app/
│   ├── __init__.py          # Package marker
│   ├── main.py              # FastAPI application & lifespan
│   ├── models.py            # Pydantic request/response schemas
│   ├── seed.py              # Sample data seeded on startup
│   ├── storage.py           # In-memory storage backend
│   └── routes/
│       ├── __init__.py      # Sub-package marker
│       └── todos.py         # CRUD route handlers
├── tests/
│   ├── __init__.py
│   ├── test_seed.py         # Seed-data tests
│   └── test_todos.py        # Endpoint integration tests
├── ARCHITECTURE.md           # This file
├── RUNNING.md                # Setup & run instructions
└── requirements.txt          # Python dependencies
```

## Data Model

Each todo item is stored as a plain Python dictionary with the
following shape:

| Field         | Type   | Required | Default | Notes                        |
| ------------- | ------ | -------- | ------- | ---------------------------- |
| `id`          | `int`  | auto     | —       | Auto-generated, read-only    |
| `title`       | `str`  | yes      | —       | Min length 1                 |
| `description` | `str`  | no       | `""`    | Optional longer description  |
| `completed`   | `bool` | no       | `False` | Completion status            |

### Pydantic Schemas

- **`TodoCreate`** — used for `POST /todos`
  - `title` (str, required, min_length=1)
  - `description` (str, optional, default `""`)

- **`TodoUpdate`** — used for `PUT /todos/{id}`
  - `title` (Optional[str])
  - `description` (Optional[str])
  - `completed` (Optional[bool])
  - All fields are optional to support **partial updates**.  Only fields
    explicitly present in the request body are applied.

- **`TodoResponse`** — returned by all endpoints that produce a todo
  - `id` (int)
  - `title` (str)
  - `description` (str)
  - `completed` (bool)

The `id` field is **read-only** and never accepted in create or update
payloads.

## API Endpoints

| #  | Method   | Path            | Request Body  | Success Response           | Error Responses |
| -- | -------- | --------------- | ------------- | -------------------------- | --------------- |
| 1  | `GET`    | `/todos`        | —             | `200` `List[TodoResponse]` | —               |
| 2  | `GET`    | `/todos/{id}`   | —             | `200` `TodoResponse`       | `404`           |
| 3  | `POST`   | `/todos`        | `TodoCreate`  | `201` `TodoResponse`       | `422`           |
| 4  | `PUT`    | `/todos/{id}`   | `TodoUpdate`  | `200` `TodoResponse`       | `404`, `422`    |
| 5  | `DELETE` | `/todos/{id}`   | —             | `204` No Content           | `404`           |

Additionally a `GET /health` endpoint returns `{"status": "ok"}`.

## In-Memory Storage

The storage layer lives in `app/storage.py` and is implemented as the
`TodoStorage` class.

- **`_todos`** — `dict[int, dict]` mapping todo ids to todo
  dictionaries.
- **`_counter`** — `int` auto-incrementing id counter.

### Storage Helper Methods

| Method                             | Returns             | Description                        |
| ---------------------------------- | ------------------- | ---------------------------------- |
| `get_all() -> list[dict]`          | All todos           | Returns every stored todo          |
| `get_by_id(id) -> dict \| None`    | One todo or `None`  | Lookup by id                       |
| `create(data) -> dict`             | Created todo        | Assigns id, sets completed=False   |
| `update(id, data) -> dict \| None` | Updated todo / None | Partial update, ignores None vals  |
| `delete(id) -> bool`               | True / False        | True if found and deleted          |
| `clear() -> None`                  | None                | Resets store and counter           |

A **module-level singleton** (`storage`) is instantiated at import time
and shared by the route handlers.

> **Note:** Data is **not persistent**.  All todos are lost when the
> process stops.

## Seed Data

`app/seed.py` defines a `seed_todos(storage)` function that populates
the store with a handful of sample items when the store is empty.  It
is called automatically during the FastAPI **lifespan** startup event
(see `app/main.py`).

The function is idempotent: if the store already contains items it
returns immediately without inserting duplicates.

## Error Handling

- **404 Not Found** — returned when `GET`, `PUT`, or `DELETE` targets a
  non-existent todo id.  Body: `{"detail": "Todo not found"}`.
- **422 Unprocessable Entity** — returned automatically by FastAPI /
  Pydantic when the request body fails validation (e.g. missing
  `title`, `title` is empty string).

## Testing Strategy

Tests live in the `tests/` directory and are run with `pytest`.

### Planned Test Cases

| Test function                             | Description                           |
| ----------------------------------------- | ------------------------------------- |
| `test_create_todo`                        | POST creates and returns a todo       |
| `test_list_todos`                         | GET /todos returns all items          |
| `test_get_todo_by_id`                     | GET /todos/{id} returns correct item  |
| `test_get_todo_not_found_returns_404`     | GET /todos/{id} with bad id → 404     |
| `test_update_todo`                        | PUT updates fields correctly          |
| `test_update_todo_not_found_returns_404`  | PUT with bad id → 404                 |
| `test_delete_todo`                        | DELETE returns 204                    |
| `test_delete_todo_not_found_returns_404`  | DELETE with bad id → 404              |
| `test_create_todo_missing_title_returns_422` | POST without title → 422           |
| `test_seed_populates_empty_store`         | Seed function adds items to empty store |
| `test_seed_skips_non_empty_store`         | Seed function is idempotent           |
