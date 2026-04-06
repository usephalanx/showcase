# Todo Application — Architecture Document

## 1. Overview

A full-stack Todo/Task management application consisting of:

- **Backend**: FastAPI (Python) REST API backed by SQLite via SQLAlchemy ORM.
- **Frontend**: React + Vite + TypeScript single-page application.
- **Database**: SQLite file-based database (`todo.db`).

The application allows users to create, read, update, and delete tasks
with workflow states (`todo`, `in-progress`, `done`) and optional due dates.

## 2. Backend Architecture

The backend is a FastAPI application structured as follows:

```
backend/
├── __init__.py          # Package marker
├── database.py          # SQLAlchemy engine, session factory, get_db dependency
├── models.py            # SQLAlchemy ORM models (Task)
├── schemas.py           # Pydantic request/response schemas
├── main.py              # FastAPI app, lifespan, CORS, route registration
└── crud.py              # CRUD helper functions
```

**Key components**:

- **database.py** — Creates the SQLAlchemy `engine` (SQLite with
  `check_same_thread=False`), a `SessionLocal` session factory, and a
  `get_db()` generator for FastAPI dependency injection.
- **models.py** — Defines the `Task` ORM model mapped to the `tasks` table.
- **schemas.py** — Defines `TaskCreate`, `TaskUpdate`, and `TaskResponse`
  Pydantic models with validation and `from_attributes` (ORM mode) support.
- **main.py** — Instantiates the FastAPI app, configures CORS middleware,
  registers route handlers, and runs `init_db()` at startup.
- **crud.py** — Contains database query functions used by route handlers.

## 3. Database Schema

The `tasks` table has the following schema:

| Column       | Type          | Constraints                                                |
|-------------|---------------|------------------------------------------------------------|
| `id`        | INTEGER       | PRIMARY KEY AUTOINCREMENT                                  |
| `title`     | VARCHAR(255)  | NOT NULL                                                   |
| `status`    | VARCHAR(20)   | NOT NULL, DEFAULT `'todo'`, CHECK IN (`'todo'`, `'in-progress'`, `'done'`) |
| `due_date`  | DATE          | NULLABLE                                                   |
| `created_at`| DATETIME      | NOT NULL, DEFAULT CURRENT_TIMESTAMP                        |
| `updated_at`| DATETIME      | NOT NULL, DEFAULT CURRENT_TIMESTAMP, ON UPDATE CURRENT_TIMESTAMP |

## 4. API Endpoints

### `GET /tasks`

Retrieve all tasks. Supports optional query parameters:

- `status` (string) — filter by status (`todo`, `in-progress`, `done`)
- `sort_by` (string) — sort field (`created_at`, `due_date`, `title`)

**Response**: `200 OK` — `TaskResponse[]`

### `GET /tasks/{id}`

Retrieve a single task by primary key.

**Response**: `200 OK` — `TaskResponse`
**Error**: `404 Not Found` — if no task with the given id exists.

### `POST /tasks`

Create a new task.

**Request body** (`TaskCreate`):
```json
{
  "title": "string (required, 1-255 chars)",
  "status": "string (optional, default 'todo')",
  "due_date": "string|null (optional, ISO 8601 date)"
}
```

**Response**: `201 Created` — `TaskResponse`
**Error**: `422 Unprocessable Entity` — on validation failure.

### `PUT /tasks/{id}`

Update an existing task (partial updates supported).

**Request body** (`TaskUpdate`):
```json
{
  "title": "string|null (optional)",
  "status": "string|null (optional)",
  "due_date": "string|null (optional)"
}
```

**Response**: `200 OK` — `TaskResponse`
**Error**: `404 Not Found` — if no task with the given id exists.

### `DELETE /tasks/{id}`

Delete a task by primary key.

**Response**: `200 OK` — `{"detail": "Task deleted successfully"}`
**Error**: `404 Not Found` — if no task with the given id exists.

## 5. Frontend Architecture

The frontend is a React application scaffolded with Vite and TypeScript.

### Component Tree

```
App
└── HomePage
    ├── TaskForm
    └── TaskList
        └── TaskCard
            └── StatusBadge
```

### Components

- **App** — Top-level component; provides routing and layout.
- **HomePage** — Main page; fetches tasks and holds application state.
- **TaskForm** — Form for creating or editing a task.
- **TaskList** — Renders a list of `TaskCard` components.
- **TaskCard** — Displays a single task with title, status badge, and due date.
- **StatusBadge** — Visual indicator for the task's workflow state.

### State Management

State is managed with React hooks (`useState`, `useEffect`). API calls
are made via `fetch` or an Axios-based API client.

## 6. File Structure

```
.
├── ARCHITECTURE.md
├── RUNNING.md
├── backend/
│   ├── __init__.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── main.py
│   └── crud.py
├── frontend/
│   ├── index.html
│   ├── package.json
│   ├── tsconfig.json
│   ├── vite.config.ts
│   └── src/
│       ├── main.tsx
│       ├── App.tsx
│       ├── api/
│       │   └── client.ts
│       ├── components/
│       │   ├── HomePage.tsx
│       │   ├── TaskForm.tsx
│       │   ├── TaskList.tsx
│       │   ├── TaskCard.tsx
│       │   └── StatusBadge.tsx
│       └── types/
│           └── task.ts
├── tests/
│   ├── __init__.py
│   ├── test_database.py
│   ├── test_models.py
│   └── test_schemas.py
├── docker-compose.yml
├── Dockerfile.backend
└── Dockerfile.frontend
```

## 7. CORS Configuration

The FastAPI backend uses `CORSMiddleware` to allow cross-origin requests
from the frontend development server:

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

The allowed origin is `http://localhost:5173` (Vite's default dev server
port). For production, this should be updated to the actual deployment URL.

## 8. Development Workflow

### Backend

```bash
cd backend
pip install fastapi uvicorn sqlalchemy pydantic
uvicorn main:app --reload --port 8000
```

API documentation is available at http://localhost:8000/docs (Swagger UI)
and http://localhost:8000/redoc (ReDoc).

### Frontend

```bash
cd frontend
npm install
npm run dev
```

The frontend dev server starts at http://localhost:5173.

### Docker (recommended)

See [RUNNING.md](./RUNNING.md) for Docker Compose instructions.
