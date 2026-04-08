# Todo API — Architecture Plan

## Dependencies

| Package | Purpose |
|---------|---------|
| fastapi | Web framework for building the REST API |
| uvicorn | ASGI server to run the FastAPI application |
| pydantic | Data validation and serialization (bundled with FastAPI) |
| pytest | Test runner |
| httpx | Async HTTP client required by FastAPI `TestClient` |
| pytest-timeout | Timeout guard for test runs |

## Project Structure

```
.
├── main.py              # FastAPI application entry-point and lifespan
├── models.py            # Pydantic request/response schemas
├── routes.py            # API router with all endpoint handlers
├── storage.py           # In-memory dict-based todo store
├── requirements.txt     # Python dependencies
├── PLANNING.md          # This file — architectural decisions
└── tests/
    ├── __init__.py
    ├── test_models.py   # Unit tests for Pydantic schemas
    ├── test_storage.py  # Unit tests for in-memory store
    └── test_todos.py    # Integration tests for API endpoints
```

## Data Model

### Internal representation (stored in dict)

| Field | Type | Default | Notes |
|---|---|---|---|
| `id` | `int` | auto-increment | Assigned by `TodoStore._get_next_id()` |
| `title` | `str` | *(required)* | Must be non-empty |
| `description` | `Optional[str]` | `None` | Free-text, may be null |
| `completed` | `bool` | `False` | Toggled via update |
| `created_at` | `datetime` | UTC now | Set server-side, **not** client-overridable |

### Pydantic Schemas

- **`TodoCreate`** — request body for `POST /todos`
  - `title: str` (required, min_length=1)
  - `description: Optional[str] = None`

- **`TodoUpdate`** — request body for `PUT /todos/{id}`
  - `title: Optional[str] = None`
  - `description: Optional[str] = None`
  - `completed: Optional[bool] = None`

- **`TodoResponse`** — response body for all todo endpoints
  - `id: int`
  - `title: str`
  - `description: Optional[str]`
  - `completed: bool`
  - `created_at: datetime`

## In-Memory Storage

The `storage.py` module provides a `TodoStore` class:

- **Backing structure**: `dict[int, dict]` mapping todo ID → todo data dict.
- **ID generation**: An internal `_next_id: int` counter starting at 1. The `_get_next_id()` method returns the current value and increments it.
- **Singleton**: A module-level `todo_store = TodoStore()` instance is used by route handlers.
- **Ephemeral**: All data is lost when the process restarts. This is intentional for the MVP.

### Methods

| Method | Signature | Returns |
|---|---|---|
| `create` | `(title, description=None) -> dict` | New todo dict |
| `get_all` | `() -> list[dict]` | All todos, newest first |
| `get_by_id` | `(todo_id) -> dict \| None` | Single todo or None |
| `update` | `(todo_id, title?, description?, completed?) -> dict \| None` | Updated todo or None |
| `delete` | `(todo_id) -> bool` | True if deleted |
| `clear` | `() -> None` | Resets store and counter |

## API Endpoints

| Method | Path | Request Body | Response | Status | Description |
|---|---|---|---|---|---|
| `GET` | `/todos` | — | `list[TodoResponse]` | 200 | List all todos |
| `POST` | `/todos` | `TodoCreate` | `TodoResponse` | 201 | Create a new todo |
| `GET` | `/todos/{id}` | — | `TodoResponse` | 200 | Get a single todo |
| `PUT` | `/todos/{id}` | `TodoUpdate` | `TodoResponse` | 200 | Update a todo |
| `DELETE` | `/todos/{id}` | — | — | 204 | Delete a todo |

## Error Handling

| Status | Condition | Body |
|---|---|---|
| **404** | Todo with given ID not found (`GET`, `PUT`, `DELETE` by ID) | `{"detail": "Todo not found"}` |
| **422** | Request body fails Pydantic validation (automatic via FastAPI) | FastAPI default validation error response |

## Testing Strategy

Tests use `pytest` with FastAPI's `TestClient` (backed by `httpx`).

### Test functions (minimum set)

1. `test_create_todo` — POST /todos returns 201 with correct body
2. `test_create_todo_missing_title` — POST /todos with no title returns 422
3. `test_list_todos_empty` — GET /todos on empty store returns []
4. `test_list_todos_nonempty` — GET /todos returns all created todos
5. `test_get_todo_by_id` — GET /todos/{id} returns the correct todo
6. `test_get_todo_not_found` — GET /todos/{id} with bad ID returns 404
7. `test_update_todo` — PUT /todos/{id} updates fields and returns 200
8. `test_update_todo_not_found` — PUT /todos/{id} with bad ID returns 404
9. `test_delete_todo` — DELETE /todos/{id} returns 204
10. `test_delete_todo_not_found` — DELETE /todos/{id} with bad ID returns 404
