# Todo Application – Architecture Plan

## Technology Stack

| Layer          | Technology                                   |
|----------------|----------------------------------------------|
| Web framework  | FastAPI 0.110+                               |
| ORM            | SQLAlchemy 2.0+                              |
| Validation     | Pydantic v2                                  |
| Database       | SQLite in-memory (`sqlite://`)               |
| ASGI server    | uvicorn                                      |
| Testing        | pytest + httpx + fastapi.testclient           |

> **Note:** The SQLite in-memory database is ephemeral — all data is lost
> when the process restarts.

## Project Structure

```
.
├── app/
│   ├── __init__.py
│   ├── main.py          # FastAPI application factory & lifespan
│   ├── database.py      # Engine, SessionLocal, Base, get_db
│   ├── models.py        # SQLAlchemy ORM models
│   ├── schemas.py       # Pydantic request/response schemas
│   └── routers/
│       ├── __init__.py
│       └── todos.py     # /todos CRUD endpoints
├── tests/
│   ├── __init__.py
│   ├── test_database.py
│   ├── test_models.py
│   ├── test_main_startup.py
│   └── test_todos.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── PLANNING.md          # ← you are here
└── RUNNING.md
```

## Database Layer

The database module (`app/database.py`) exposes:

- **`engine`** – `create_engine("sqlite://", connect_args={"check_same_thread": False})`
- **`SessionLocal`** – `sessionmaker(autocommit=False, autoflush=False, bind=engine)`
- **`Base`** – `declarative_base()` used by all models
- **`get_db()`** – generator dependency for FastAPI `Depends(get_db)`

`connect_args={"check_same_thread": False}` is **required** because SQLite
by default only allows the creating thread to access the connection, but
FastAPI/uvicorn may serve requests from a different thread.

## Data Model

### `todos` table (SQLAlchemy model: `Todo`)

| Column      | Type          | Constraints                              |
|-------------|---------------|------------------------------------------|
| id          | Integer       | PRIMARY KEY, AUTOINCREMENT               |
| title       | String(255)   | NOT NULL                                 |
| description | String(1024)  | NULLABLE                                 |
| completed   | Boolean       | NOT NULL, DEFAULT False                  |
| created_at  | DateTime      | NOT NULL, DEFAULT `datetime.utcnow`      |

> `created_at` is **server-set** and is never accepted from client input.

## Pydantic Schemas

### `TodoCreate` (POST body)

| Field       | Type            | Constraints                  |
|-------------|-----------------|------------------------------|
| title       | str             | required, min_length=1       |
| description | Optional[str]   | default None                 |
| completed   | bool            | default False                |

> Title must have a **minimum length of 1** to prevent empty-string titles.

### `TodoUpdate` (PUT body)

| Field       | Type            | Constraints                  |
|-------------|-----------------|------------------------------|
| title       | Optional[str]   | min_length=1 if provided     |
| description | Optional[str]   | default None                 |
| completed   | Optional[bool]  | default None                 |

> Uses **partial update semantics**: only provided (non-None) fields are
> written; fields not supplied in the JSON body remain unchanged.

### `TodoResponse` (all responses)

| Field       | Type            |
|-------------|-----------------|
| id          | int             |
| title       | str             |
| description | Optional[str]   |
| completed   | bool            |
| created_at  | datetime        |

Config: `from_attributes = True` (Pydantic v2 orm_mode equivalent).

## API Endpoints

| Method | Path            | Status | Description            |
|--------|-----------------|--------|------------------------|
| GET    | `/todos`        | 200    | List all todos         |
| GET    | `/todos/{id}`   | 200    | Get one todo           |
| POST   | `/todos`        | 201    | Create a new todo      |
| PUT    | `/todos/{id}`   | 200    | Update an existing todo|
| DELETE | `/todos/{id}`   | 204    | Delete a todo          |

## Router Functions

Each endpoint handler receives the DB session via
`db: Session = Depends(get_db)` and delegates to straight SQLAlchemy
queries (no repository layer needed at this scale).

## Application Startup

```python
@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield
```

This ensures all tables are created when the process starts.

## Error Handling

Missing resources raise:

```python
raise HTTPException(status_code=404, detail="Todo not found")
```

Validation errors are handled automatically by FastAPI / Pydantic (422).

## Testing Strategy

- Use `fastapi.testclient.TestClient` for synchronous integration tests.
- Each test file recreates tables via `Base.metadata.create_all` /
  `Base.metadata.drop_all` in an `autouse` fixture.
- Unit tests verify column definitions, defaults, and constraints.
- Integration tests hit every endpoint and cover 404 / validation paths.

## Docker Configuration

A `Dockerfile` builds a slim Python image; `docker-compose.yml` maps
port 8000 and runs `uvicorn app.main:app --host 0.0.0.0 --port 8000`.
