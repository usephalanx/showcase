# Todo App — Architecture Plan

## Technology Stack

| Layer          | Choice                                  |
|----------------|-----------------------------------------|
| Web framework  | FastAPI 0.110+                          |
| ASGI server    | uvicorn 0.23+                           |
| ORM            | SQLAlchemy 2.0+                         |
| Validation     | Pydantic v2                             |
| Database       | SQLite in-memory (`sqlite:///:memory:`) |
| Testing        | pytest + httpx                          |

> **Note:** The SQLite in-memory database is **ephemeral** — all data is
> lost when the process restarts.

---

## Project Structure

```
.
├── app/
│   ├── __init__.py          # Package marker
│   ├── main.py              # FastAPI app, CORS middleware, router inclusion
│   ├── database.py          # SQLAlchemy engine, SessionLocal, Base, get_db
│   ├── models.py            # SQLAlchemy ORM models
│   ├── schemas.py           # Pydantic request/response schemas
│   └── routers/
│       ├── __init__.py      # Aggregated APIRouter
│       └── todos.py         # CRUD endpoint handlers
├── tests/
│   ├── __init__.py
│   └── test_todos.py        # Full endpoint test suite
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── PLANNING.md              # This file
└── RUNNING.md               # How to run the project
```

---

## Data Model

SQLAlchemy ORM model (`app/models.py`):

| Column       | Type               | Constraints                          |
|--------------|--------------------|--------------------------------------|
| `id`         | `Integer`          | Primary key, autoincrement           |
| `title`      | `String(255)`      | `nullable=False`                     |
| `description`| `String(1024)`     | `nullable=True`                      |
| `completed`  | `Boolean`          | `default=False`                      |
| `created_at` | `DateTime`         | `default=datetime.utcnow`, server-set|

> `created_at` is **always server-set** and never accepted from client input.

---

## Pydantic Schemas

Defined in `app/schemas.py`.

### TodoCreate

```python
class TodoCreate(BaseModel):
    title: str          # min_length=1 — empty strings are rejected
    description: Optional[str] = None
    completed: bool = False
```

### TodoUpdate

```python
class TodoUpdate(BaseModel):
    title: Optional[str] = None        # min_length=1 when provided
    description: Optional[str] = None
    completed: Optional[bool] = None
```

> **Partial update semantics:** only provided (non-`None`) fields are
> written; `None` values are skipped.

### TodoResponse

```python
class TodoResponse(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    completed: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
```

---

## API Endpoints

All endpoints are prefixed with `/todos`.

| Method   | Path            | Status  | Description               |
|----------|-----------------|---------|---------------------------|
| `GET`    | `/todos`        | `200`   | List all todos            |
| `GET`    | `/todos/{id}`   | `200`/`404` | Get a single todo     |
| `POST`   | `/todos`        | `201`   | Create a new todo         |
| `PUT`    | `/todos/{id}`   | `200`/`404` | Update an existing todo|
| `DELETE` | `/todos/{id}`   | `204`/`404` | Delete a todo          |

---

## Database Layer

Defined in `app/database.py`.

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},   # Required for SQLite + FastAPI
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
```

### Dependency injection

```python
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

Used via `Depends(get_db)` in every router function.

---

## Router Functions

Defined in `app/routers/todos.py`.  Each function receives a
`db: Session = Depends(get_db)` parameter.

1. **list_todos** — `db.query(Todo).all()`
2. **get_todo** — `db.query(Todo).filter(Todo.id == id).first()`, raise 404 if `None`
3. **create_todo** — instantiate `Todo`, `db.add`, `db.commit`, `db.refresh`, return 201
4. **update_todo** — fetch existing, apply non-`None` fields from `TodoUpdate`, `db.commit`, return 200 or 404
5. **delete_todo** — fetch existing, `db.delete`, `db.commit`, return 204 or 404

---

## Application Startup

`app/main.py`:

1. Create `FastAPI()` instance.
2. Add `CORSMiddleware` (allow all origins for development).
3. Import `Base` and `engine` from `app.database`; call `Base.metadata.create_all(bind=engine)`.
4. Include `router` from `app.routers`.

---

## Error Handling

Missing resources return a consistent JSON error:

```python
raise HTTPException(status_code=404, detail="Todo not found")
```

Pydantic validation errors are handled automatically by FastAPI (422).

Title must have `min_length=1` to prevent empty-string titles.

---

## Testing Strategy

Tests live in `tests/test_todos.py` and use `httpx.AsyncClient` (or
`TestClient` from `starlette.testclient`).

- Override `get_db` dependency to use a **separate in-memory SQLite
  database** for test isolation.
- Cover all 5 endpoints with happy-path and error cases.
- Verify status codes, response bodies, and side effects.

---

## Docker Configuration

### Dockerfile

- Base image: `python:3.12-slim`
- Copy `requirements.txt`, `pip install`.
- Copy application code.
- `CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]`

### docker-compose.yml

- Single `app` service building from `.`.
- Map port `8000:8000`.
- Optional volume mount for live reload during development.
