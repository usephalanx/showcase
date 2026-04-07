# Todo API — Architecture Plan

## Overview

A FastAPI-based Todo CRUD API with in-memory dict storage. The API
exposes RESTful endpoints for managing todo items. Storage is ephemeral
and resets on server restart.

## Project Structure

```
app/
├── __init__.py   # Package marker
├── main.py       # FastAPI application entry point, includes router
├── models.py     # Pydantic schemas: TodoCreate, TodoUpdate, TodoResponse
├── storage.py    # In-memory storage class with dict and auto-incrementing ID
└── routes.py     # API route definitions
tests/
├── test_models.py
├── test_storage.py
└── test_planning_doc.py
PLANNING.md       # This file
```

## Data Model

Each todo item has the following fields:

| Field         | Type            | Description                          |
|---------------|-----------------|--------------------------------------|
| `id`          | `int`           | Auto-generated unique identifier     |
| `title`       | `str`           | Title of the todo item (required)    |
| `description` | `str \| None`   | Optional longer description          |
| `completed`   | `bool`          | Completion status (default: `False`) |

## Pydantic Schemas

### TodoCreate

Used in `POST /todos` request bodies.

- `title: str` — required, min length 1
- `description: str | None = None` — optional

### TodoUpdate

Used in `PUT /todos/{id}` request bodies. All fields optional; only
provided fields are updated (partial update semantics).

- `title: str | None = None`
- `description: str | None = None`
- `completed: bool | None = None`

### TodoResponse

Returned from all endpoints that produce todo data.

- `id: int`
- `title: str`
- `description: str | None`
- `completed: bool`

## API Endpoints

| Method   | Path              | Description              | Success | Error |
|----------|-------------------|--------------------------|---------|-------|
| `GET`    | `/todos`          | List all todo items      | 200     | —     |
| `GET`    | `/todos/{id}`     | Get a single todo by ID  | 200     | 404   |
| `POST`   | `/todos`          | Create a new todo item   | 201     | 422   |
| `PUT`    | `/todos/{id}`     | Update an existing todo  | 200     | 404   |
| `DELETE` | `/todos/{id}`     | Delete a todo by ID      | 200     | 404   |

## Storage

The storage layer uses a Python **dict** (`dict[int, dict]`) as the
in-memory data store. An auto-incrementing integer counter (`_next_id`)
assigns unique IDs to new items.

The `TodoStorage` class exposes five methods:

- `get_all() -> list[TodoResponse]`
- `get_by_id(todo_id: int) -> TodoResponse | None`
- `create(todo: TodoCreate) -> TodoResponse`
- `update(todo_id: int, todo: TodoUpdate) -> TodoResponse | None`
- `delete(todo_id: int) -> bool`

**Note:** Storage is ephemeral. All data is lost when the server process
restarts.

## Error Handling

- **404 Not Found** — returned by `GET /todos/{id}`, `PUT /todos/{id}`,
  and `DELETE /todos/{id}` when no todo with the given ID exists.
- **422 Unprocessable Entity** — returned by `POST /todos` and
  `PUT /todos/{id}` when the request body fails validation.
