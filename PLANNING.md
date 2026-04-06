# Todo App — Architecture & Design Plan

This document serves as the single source of truth for the full-stack Todo application.

---

## Overview

A full-stack task management application with a **FastAPI + SQLite** backend and a
**React + TypeScript + Vite** frontend. Users can create, read, update, and delete
tasks, each of which carries a title, status, and optional due date.

**Technology Stack:**

| Layer      | Technology                        | Version  |
| ---------- | --------------------------------- | -------- |
| Backend    | Python / FastAPI                  | 3.11+ / 0.110+ |
| ORM        | SQLAlchemy                        | 2.0+     |
| Database   | SQLite                            | 3        |
| Validation | Pydantic                          | 2.0+     |
| Frontend   | React / TypeScript / Vite         | 18 / 5.4+ / 5.2+ |
| HTTP       | Axios                             | 1.7+     |
| Styling    | Plain CSS (minimal, system fonts) | —        |

---

## Folder Structure

```
/
├── PLANNING.md
├── backend/
│   ├── main.py               # FastAPI app entry-point
│   ├── database.py           # SQLAlchemy engine & session
│   ├── models.py             # SQLAlchemy ORM models
│   ├── schemas.py            # Pydantic request / response schemas
│   ├── crud.py               # Data-access helpers
│   └── routers/
│       └── tasks.py          # /api/tasks router
├── frontend/
│   ├── index.html
│   ├── package.json
│   ├── tsconfig.json
│   ├── tsconfig.node.json
│   ├── vite.config.ts
│   └── src/
│       ├── main.tsx          # React DOM entry-point
│       ├── App.tsx           # Root component
│       ├── index.css         # Global styles
│       ├── types/
│       │   └── task.ts       # TypeScript interfaces
│       ├── services/
│       │   └── api.ts        # Axios instance & API helpers
│       └── components/
│           ├── Layout.tsx
│           ├── TaskList.tsx
│           ├── TaskItem.tsx
│           ├── TaskForm.tsx
│           └── TaskFilter.tsx
└── tests/
    ├── test_planning.py      # Structural tests for PLANNING.md
    └── test_frontend_structure.py  # Structural tests for frontend files
```

---

## Data Models

### SQLAlchemy — `Task`

| Column       | Type            | Constraints                          |
| ------------ | --------------- | ------------------------------------ |
| `id`         | `Integer`       | Primary key, auto-increment          |
| `title`      | `String(255)`   | Not null                             |
| `status`     | `String(20)`    | Not null, one of `todo`, `in-progress`, `done`; default `todo` |
| `due_date`   | `Date`          | Nullable                             |
| `created_at` | `DateTime`      | Not null, server default `utcnow`    |
| `updated_at` | `DateTime`      | Not null, server default `utcnow`, onupdate `utcnow` |

> **Note:** `created_at` and `updated_at` are **read-only** — they are never
> accepted in create or update request bodies.

---

## Pydantic Schemas

### `TaskCreate` (request body for `POST`)

```python
class TaskCreate(BaseModel):
    title: str                          # required
    status: str = "todo"                # optional, default "todo"
    due_date: date | None = None        # optional, nullable
```

### `TaskUpdate` (request body for `PUT` — full replacement)

```python
class TaskUpdate(BaseModel):
    title: str                          # required
    status: str                         # required
    due_date: date | None = None        # optional, nullable
```

### `TaskPatch` (request body for `PATCH` — partial update)

```python
class TaskPatch(BaseModel):
    title: str | None = None
    status: str | None = None
    due_date: date | None = None
```

### `TaskResponse` (response body)

```python
class TaskResponse(BaseModel):
    id: int
    title: str
    status: str
    due_date: date | None
    created_at: datetime
    updated_at: datetime
```

**Status validation:** All schemas that include a `status` field validate it
against the allowed set `{"todo", "in-progress", "done"}`. An invalid value
returns a `422 Unprocessable Entity` response.

---

## API Contract

All endpoints are prefixed with **`/api`**.

### 1. `GET /api/tasks`

List all tasks, optionally filtered by status.

| Parameter | In    | Type   | Required | Notes                              |
| --------- | ----- | ------ | -------- | ---------------------------------- |
| `status`  | query | string | No       | Filter: `todo`, `in-progress`, `done`. Invalid value → 422 |

**Response:** `200 OK`
```json
[
  {
    "id": 1,
    "title": "Buy groceries",
    "status": "todo",
    "due_date": "2025-03-15",
    "created_at": "2025-01-01T00:00:00",
    "updated_at": "2025-01-01T00:00:00"
  }
]
```

### 2. `GET /api/tasks/{task_id}`

Retrieve a single task by ID.

**Response:** `200 OK` — single `TaskResponse` object.\
**Error:** `404 Not Found` if the task does not exist.

### 3. `POST /api/tasks`

Create a new task.

**Request body:** `TaskCreate`
```json
{
  "title": "Buy groceries",
  "status": "todo",
  "due_date": "2025-03-15"
}
```

**Response:** `201 Created` — the created `TaskResponse`.

### 4. `PUT /api/tasks/{task_id}`

Full replacement of a task. All mutable fields must be provided.

**Request body:** `TaskUpdate`
```json
{
  "title": "Buy organic groceries",
  "status": "in-progress",
  "due_date": null
}
```

**Response:** `200 OK` — the updated `TaskResponse`.\
**Error:** `404 Not Found` if the task does not exist.

### 5. `PATCH /api/tasks/{task_id}`

Partial update — only the provided fields are changed.

**Request body:** `TaskPatch`
```json
{
  "status": "done"
}
```

**Response:** `200 OK` — the updated `TaskResponse`.\
**Error:** `404 Not Found` if the task does not exist.

### 6. `DELETE /api/tasks/{task_id}`

Delete a task.

**Response:** `204 No Content`.\
**Error:** `404 Not Found` if the task does not exist.

---

## Error Responses

All error responses follow this format:

```json
{
  "detail": "Human-readable error message"
}
```

| Status | Meaning                 | Example cause                      |
| ------ | ----------------------- | ---------------------------------- |
| 404    | Not Found               | Task ID does not exist             |
| 422    | Unprocessable Entity    | Validation failure (bad status, missing title, invalid query param) |
| 500    | Internal Server Error   | Unexpected server error            |

---

## Component Hierarchy

```
App
└── Layout
    ├── TaskForm          — Create / edit a task
    ├── TaskFilter        — Filter by status
    └── TaskList
        └── TaskItem      — Single task row with actions (edit, delete, toggle status)
```

### Component Responsibilities

| Component    | Purpose                                                    |
| ------------ | ---------------------------------------------------------- |
| `App`        | Top-level provider, holds global state                     |
| `Layout`     | Page chrome — header, main content area                    |
| `TaskForm`   | Controlled form for creating / editing tasks               |
| `TaskFilter` | Dropdown or button group to set the active status filter   |
| `TaskList`   | Fetches & renders the filtered array of tasks              |
| `TaskItem`   | Displays a single task; exposes edit / delete / toggle     |

---

## Frontend Services

`src/services/api.ts` exposes an **Axios** instance pointed at `/api` (proxied
to `localhost:8000` during development via Vite config) and typed helper
functions:

```ts
getTasks(status?: string): Promise<Task[]>
getTask(id: number): Promise<Task>
createTask(data: TaskCreate): Promise<Task>
updateTask(id: number, data: TaskUpdate): Promise<Task>
patchTask(id: number, data: Partial<TaskUpdate>): Promise<Task>
deleteTask(id: number): Promise<void>
```

---

## Configuration

### Backend

- Database URL configured via env var `DATABASE_URL` (default `sqlite:///./tasks.db`).
- CORS configured to allow `http://localhost:5173` during development.

### Frontend

- Vite dev server on port **5173**.
- API proxy: requests to `/api` are forwarded to `http://localhost:8000`.

---

## Development Workflow

```bash
# Backend
cd backend
pip install fastapi uvicorn sqlalchemy pydantic
uvicorn main:app --reload --port 8000

# Frontend
cd frontend
npm install
npm run dev
```

The Vite dev server proxies `/api/*` to the FastAPI backend so there are no
CORS issues during local development.
