# API Specification

## Base URL

All API endpoints are prefixed with `/api`. The frontend is served at
the root path `/`.

---

## Endpoints

### `GET /` — Serve Frontend

| Property        | Value                            |
|-----------------|----------------------------------|
| Handler         | `serve_frontend`                 |
| Content-Type    | `text/html`                      |
| Success Status  | `200 OK`                         |

Returns the contents of `static/index.html`.

---

### `GET /api/todos` — List All Todos

| Property        | Value                            |
|-----------------|----------------------------------|
| Handler         | `list_todos`                     |
| Content-Type    | `application/json`               |
| Success Status  | `200 OK`                         |

**Response Body** (array of `TodoResponse`):

```json
[
  {
    "id": 1,
    "title": "Buy groceries",
    "completed": false,
    "created_at": "2024-01-15 10:30:00"
  }
]
```

Returns an empty array `[]` when no todos exist — never `null` or an error.

---

### `POST /api/todos` — Create a Todo

| Property        | Value                            |
|-----------------|----------------------------------|
| Handler         | `create_todo`                    |
| Content-Type    | `application/json`               |
| Success Status  | `201 Created`                    |

**Request Body** (`TodoCreate`):

```json
{
  "title": "Buy groceries"
}
```

- `title` must be between 1 and 500 characters (validated by Pydantic).

**Response Body** (`TodoResponse`):

```json
{
  "id": 1,
  "title": "Buy groceries",
  "completed": false,
  "created_at": "2024-01-15 10:30:00"
}
```

**Errors:**

| Status | Condition                    | Body                                |
|--------|------------------------------|-------------------------------------|
| 422    | Empty or missing title       | `{"detail": "..."}`                 |

---

### `PATCH /api/todos/{id}` — Update Completion Status

| Property        | Value                            |
|-----------------|----------------------------------|
| Handler         | `update_todo`                    |
| Content-Type    | `application/json`               |
| Success Status  | `200 OK`                         |

**Path Parameters:**

- `id` — positive integer, primary key of the todo.

**Request Body** (`TodoUpdate`):

```json
{
  "completed": true
}
```

**Response Body** (`TodoResponse`):

```json
{
  "id": 1,
  "title": "Buy groceries",
  "completed": true,
  "created_at": "2024-01-15 10:30:00"
}
```

**Errors:**

| Status | Condition         | Body                              |
|--------|-------------------|-----------------------------------|
| 404    | Todo not found    | `{"detail": "Todo not found"}`    |

---

### `DELETE /api/todos/{id}` — Delete a Todo

| Property        | Value                            |
|-----------------|----------------------------------|
| Handler         | `delete_todo`                    |
| Success Status  | `204 No Content`                 |

**Path Parameters:**

- `id` — positive integer, primary key of the todo.

Response body is **empty** on success (204).

**Errors:**

| Status | Condition         | Body                              |
|--------|-------------------|-----------------------------------|
| 404    | Todo not found    | `{"detail": "Todo not found"}`    |

---

## Pydantic Models

```python
class TodoCreate(BaseModel):
    """Request body for creating a new todo."""
    title: str = Field(..., min_length=1, max_length=500)

class TodoUpdate(BaseModel):
    """Request body for updating a todo's completion status."""
    completed: bool

class TodoResponse(BaseModel):
    """Response body representing a single todo item."""
    id: int
    title: str
    completed: bool
    created_at: str
```

---

## Database Functions (`database.py`)

| Function                                  | Returns                     | Description                              |
|-------------------------------------------|-----------------------------|------------------------------------------|
| `init_db() -> None`                       | `None`                      | Creates `todos` table if not exists      |
| `get_db_connection() -> Iterator[Connection]` | Context manager yielding `sqlite3.Connection` | Provides managed DB connection |
| `get_all_todos() -> List[Dict]`           | List of todo dicts          | Fetches all rows, ordered by created_at DESC |
| `create_todo(title: str) -> Dict`         | Created todo dict           | Inserts a new todo                       |
| `update_todo_completed(id, completed) -> Optional[Dict]` | Updated todo or `None` | Updates completion status     |
| `delete_todo(id: int) -> bool`            | `True` / `False`            | Deletes a todo by primary key            |

### CREATE TABLE Statement

```sql
CREATE TABLE IF NOT EXISTS todos (
    id         INTEGER   PRIMARY KEY AUTOINCREMENT,
    title      TEXT      NOT NULL,
    completed  BOOLEAN   NOT NULL DEFAULT 0,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
```

---

## Error Response Format

All errors return a JSON body with the following shape:

```json
{
  "detail": "Human-readable error message"
}
```

| HTTP Status | Meaning                                   |
|-------------|-------------------------------------------|
| 400         | Bad request / malformed input             |
| 404         | Resource not found                        |
| 422         | Unprocessable entity (validation failure) |
