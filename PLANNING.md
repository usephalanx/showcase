# Todo App — Architecture & Design Plan

This document is the single source of truth for the Todo application's
architecture, data models, API contract, and frontend component hierarchy.

---

## Overview

A full-stack task management application consisting of:

- **Backend** — FastAPI + SQLAlchemy ORM + SQLite
- **Frontend** — React + TypeScript + Vite

---

## Folder Structure

```
/
├── PLANNING.md
├── requirements.txt
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py          # FastAPI application entry point & lifespan
│   │   ├── database.py       # SQLAlchemy engine, SessionLocal, Base
│   │   ├── models.py         # SQLAlchemy ORM models
│   │   ├── schemas.py        # Pydantic request/response schemas
│   │   ├── crud.py           # Database CRUD helper functions
│   │   └── routers/
│   │       ├── __init__.py
│   │       └── tasks.py      # /api/tasks router
│   └── tests/
│       ├── __init__.py
│       ├── test_models.py
│       ├── test_database.py
│       └── test_schemas.py
├── frontend/
│   ├── index.html
│   ├── package.json
│   ├── tsconfig.json
│   ├── vite.config.ts
│   └── src/
│       ├── App.tsx
│       ├── main.tsx
│       ├── types/
│       │   └── task.ts
│       ├── services/
│       │   └── api.ts
│       └── components/
│           ├── Layout.tsx
│           ├── TaskList.tsx
│           ├── TaskItem.tsx
│           ├── TaskForm.tsx
│           └── TaskFilter.tsx
└── SETUP.md
```

---

## Data Models

### SQLAlchemy — `Task`

| Column       | Type                  | Constraints                          |
|--------------|-----------------------|--------------------------------------|
| `id`         | Integer               | Primary Key, autoincrement           |
| `title`      | String(255)           | NOT NULL                             |
| `status`     | String(20)            | NOT NULL, enum: `todo`, `in-progress`, `done`; default `todo` |
| `due_date`   | Date                  | Nullable                             |
| `created_at` | DateTime              | NOT NULL, server default `now()`     |
| `updated_at` | DateTime              | NOT NULL, server default `now()`, onupdate `now()` |

---

## Pydantic Schemas

### `TaskCreate` (request body — POST)

| Field      | Type            | Required | Notes              |
|------------|-----------------|----------|-----------------------|
| `title`    | `str`           | Yes      | min_length=1          |
| `status`   | `str`           | No       | default `"todo"`      |
| `due_date` | `date \| None`  | No       | default `None`        |

### `TaskUpdate` (request body — PUT, requires all fields; PATCH, all optional)

| Field      | Type            | Required (PUT) | Required (PATCH) |
|------------|-----------------|----------------|------------------|
| `title`    | `str`           | Yes            | No               |
| `status`   | `str`           | Yes            | No               |
| `due_date` | `date \| None`  | Yes            | No               |

### `TaskResponse` (response body)

| Field        | Type            | Notes         |
|--------------|-----------------|---------------|
| `id`         | `int`           | read-only     |
| `title`      | `str`           |               |
| `status`     | `str`           |               |
| `due_date`   | `date \| None`  |               |
| `created_at` | `datetime`      | read-only     |
| `updated_at` | `datetime`      | read-only     |

> **Note:** `created_at` and `updated_at` are **read-only**. They are never
> accepted in create or update request bodies.

---

## API Contract

Base path: `/api`

### 1. List Tasks

```
GET /api/tasks?status=todo
```

- **Query params:** `status` (optional) — filter by status. Returns 422 if
  value is not one of `todo`, `in-progress`, `done`.
- **Response:** `200 OK` — `TaskResponse[]`

### 2. Get Task by ID

```
GET /api/tasks/{task_id}
```

- **Path params:** `task_id` (int)
- **Response:** `200 OK` — `TaskResponse`
- **Errors:** `404 Not Found`

### 3. Create Task

```
POST /api/tasks
Content-Type: application/json

{"title": "Buy groceries", "due_date": "2025-01-15"}
```

- **Request body:** `TaskCreate`
- **Response:** `201 Created` — `TaskResponse`
- **Errors:** `422 Unprocessable Entity`

### 4. Full Update Task

```
PUT /api/tasks/{task_id}
Content-Type: application/json

{"title": "Updated", "status": "done", "due_date": null}
```

- **Request body:** `TaskUpdate` (all fields required)
- **Response:** `200 OK` — `TaskResponse`
- **Errors:** `404`, `422`

### 5. Partial Update Task

```
PATCH /api/tasks/{task_id}
Content-Type: application/json

{"status": "in-progress"}
```

- **Request body:** `TaskUpdate` (fields are optional)
- **Response:** `200 OK` — `TaskResponse`
- **Errors:** `404`, `422`

### 6. Delete Task

```
DELETE /api/tasks/{task_id}
```

- **Response:** `200 OK` — `{"detail": "Task deleted successfully"}`
- **Errors:** `404 Not Found`

---

## Error Responses

All errors follow this shape:

```json
{"detail": "Human-readable message"}
```

Standard HTTP status codes:

| Code | Meaning                 |
|------|-------------------------|
| 200  | Success                 |
| 201  | Created                 |
| 404  | Resource not found      |
| 422  | Validation error        |
| 500  | Internal server error   |

---

## Component Hierarchy (Frontend)

```
App
└── Layout
    ├── TaskForm          # create / edit a task
    ├── TaskFilter        # filter by status
    └── TaskList
        └── TaskItem      # single task row (edit, delete, status toggle)
```

---

## Frontend Services

`src/services/api.ts` wraps all HTTP calls:

- `fetchTasks(status?: string): Promise<Task[]>`
- `fetchTask(id: number): Promise<Task>`
- `createTask(data: TaskCreate): Promise<Task>`
- `updateTask(id: number, data: TaskUpdate): Promise<Task>`
- `patchTask(id: number, data: Partial<TaskUpdate>): Promise<Task>`
- `deleteTask(id: number): Promise<void>`

---

## Configuration

| Variable          | Default              | Description               |
|-------------------|----------------------|---------------------------|
| `DATABASE_URL`    | `sqlite:///./tasks.db` | SQLAlchemy connection URL |
| `BACKEND_PORT`    | `8000`               | Uvicorn listen port       |
| `FRONTEND_PORT`   | `5173`               | Vite dev-server port      |

---

## Development Workflow

1. `pip install -r requirements.txt`
2. `cd backend && uvicorn app.main:app --reload`
3. `cd frontend && npm install && npm run dev`
4. Run tests: `cd backend && python -m pytest tests/ -v`
