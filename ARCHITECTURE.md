# Todo API — Architecture

## Overview

A RESTful Todo API built with **FastAPI** using **in-memory storage**.
Designed for simplicity and ease of testing.

## Technology Choices

| Concern        | Choice                   |
|----------------|-------------------------|
| Framework      | FastAPI                  |
| Validation     | Pydantic v2              |
| Server         | Uvicorn                  |
| Testing        | pytest + httpx           |
| Storage        | In-memory Python dict    |

## Project Structure

```
.
├── app/
│   ├── __init__.py
│   ├── main.py          # FastAPI app, CORS, router inclusion
│   ├── models.py         # Pydantic schemas
│   ├── routes/
│   │   ├── __init__.py
│   │   └── todos.py      # /todos endpoint handlers
│   └── storage.py        # In-memory storage module
├── tests/
│   ├── __init__.py
│   ├── test_main.py      # App-level tests
│   └── test_todos.py     # Todo CRUD tests
├── pyproject.toml
├── ARCHITECTURE.md
└── RUNNING.md
```

## Data Model

### Todo Item

| Field         | Type   | Constraints                            |
|---------------|--------|----------------------------------------|
| `id`          | `int`  | Auto-generated, read-only              |
| `title`       | `str`  | Required, min length 1                 |
| `description` | `str`  | Optional, defaults to `""`             |
| `completed`   | `bool` | Defaults to `False`                    |

### Pydantic Schemas

- **`TodoCreate`** — request body for `POST /todos`
  - `title: str` (required)
  - `description: str = ""`

- **`TodoUpdate`** — request body for `PUT /todos/{id}`
  - `title: str | None = None`
  - `description: str | None = None`
  - `completed: bool | None = None`
  - All fields are **optional** to support partial updates.

- **`TodoResponse`** — response body for all todo endpoints
  - `id: int`
  - `title: str`
  - `description: str`
  - `completed: bool`

> The `id` field is **never** accepted in create or update requests.

## API Endpoints

| Method   | Path              | Request Body  | Success Response          | Error Responses |
|----------|-------------------|---------------|---------------------------|-----------------|
| `GET`    | `/todos`          | —             | `200` `List[TodoResponse]`| —               |
| `GET`    | `/todos/{id}`     | —             | `200` `TodoResponse`      | `404`           |
| `POST`   | `/todos`          | `TodoCreate`  | `201` `TodoResponse`      | `422`           |
| `PUT`    | `/todos/{id}`     | `TodoUpdate`  | `200` `TodoResponse`      | `404`           |
| `DELETE` | `/todos/{id}`     | —             | `204` No Content          | `404`           |

### Notes

- `DELETE` returns **204 No Content** with no response body on success.
- `POST` returns **201 Created**.
- `422 Unprocessable Entity` is returned when required fields (e.g. `title`) are missing.

## In-Memory Storage

Storage lives in `app/storage.py` as module-level state:

```python
_todos: dict[int, dict] = {}
_counter: int = 0
```

### Helper Functions

| Function                          | Returns              | Description                          |
|-----------------------------------|----------------------|--------------------------------------|
| `get_all() -> list[dict]`        | List of all todos    | Returns all stored todo dicts        |
| `get_by_id(id: int) -> dict \| None` | Single todo or None | Lookup by id                         |
| `create(data: dict) -> dict`     | Created todo         | Auto-assigns id, stores and returns  |
| `update(id: int, data: dict) -> dict \| None` | Updated todo or None | Partial update of existing todo |
| `delete(id: int) -> bool`        | True if deleted      | Returns False if id not found        |

> **Note:** In-memory storage is **not persistent**. All data is lost on
> server restart. This is intentional for this project scope.

## Error Handling

- `404 Not Found` — returned when a todo with the given id does not exist
  (GET by id, PUT, DELETE).
- `422 Unprocessable Entity` — returned when request validation fails
  (e.g. missing required `title` on POST).

## Testing Strategy

All tests use `httpx.AsyncClient` or `fastapi.testclient.TestClient`.

| Test Function                            | Validates                                  |
|------------------------------------------|--------------------------------------------|
| `test_create_todo`                       | POST /todos creates and returns 201        |
| `test_list_todos`                        | GET /todos returns list of all todos       |
| `test_get_todo_by_id`                    | GET /todos/{id} returns the correct todo   |
| `test_get_todo_not_found_returns_404`    | GET /todos/{id} returns 404 for bad id     |
| `test_update_todo`                       | PUT /todos/{id} updates fields correctly   |
| `test_update_todo_not_found_returns_404` | PUT /todos/{id} returns 404 for bad id     |
| `test_delete_todo`                       | DELETE /todos/{id} returns 204             |
| `test_delete_todo_not_found_returns_404` | DELETE /todos/{id} returns 404 for bad id  |
| `test_create_todo_missing_title_returns_422` | POST /todos without title returns 422  |
