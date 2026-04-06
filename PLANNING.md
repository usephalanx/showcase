# Todo Application — Architecture & Design Plan

This document serves as the single source of truth for the Todo application
architecture, covering both the **FastAPI + SQLite** backend and the
**React + TypeScript + Vite** frontend.

---

## Overview

A full-stack task management application that exposes a RESTful API for
CRUD operations on tasks and provides a React-based single-page frontend.

### Technology Stack

| Layer      | Technology                        | Version  |
|------------|-----------------------------------|----------|
| Backend    | Python                            | ≥ 3.11   |
| Framework  | FastAPI                           | ≥ 0.110 |
| ORM        | SQLAlchemy                        | ≥ 2.0    |
| Validation | Pydantic                          | ≥ 2.0    |
| Database   | SQLite                            | 3.x      |
| Frontend   | React + TypeScript + Vite         | 18 / 5   |
| Testing    | pytest, React Testing Library     | latest   |

---

## Folder Structure

```
/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py              # FastAPI entry-point & lifespan
│   │   ├── database.py          # Engine, session, Base, init_db
│   │   ├── models.py            # SQLAlchemy ORM models
│   │   ├── schemas.py           # Pydantic request/response schemas
│   │   ├── crud.py              # Data-access helper functions
│   │   └── routers/
│   │       ├── __init__.py
│   │       └── tasks.py         # /api/tasks endpoints
│   ├── tests/
│   │   ├── __init__.py
│   │   ├── conftest.py          # Shared fixtures
│   │   ├── test_schemas.py      # Schema validation tests
│   │   ├── test_models.py       # ORM model tests
│   │   └── test_tasks.py        # Router / integration tests
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── App.tsx
│   │   ├── main.tsx
│   │   ├── components/
│   │   │   ├── Layout.tsx
│   │   │   ├── TaskList.tsx
│   │   │   ├── TaskItem.tsx
│   │   │   ├── TaskForm.tsx
│   │   │   └── TaskFilter.tsx
│   │   ├── services/
│   │   │   └── api.ts           # Axios/fetch wrapper
│   │   └── types/
│   │       └── task.ts          # TypeScript interfaces
│   ├── index.html
│   ├── package.json
│   ├── tsconfig.json
│   └── vite.config.ts
├── PLANNING.md
└── README.md
```

---

## Data Models

### SQLAlchemy — `Task` (backend/app/models.py)

| Column       | Type                                    | Constraints                        |
|--------------|-----------------------------------------|------------------------------------|
| `id`         | `Integer`                               | Primary key, auto-increment        |
| `title`      | `String(255)`                           | NOT NULL                           |
| `status`     | `Enum('todo','in-progress','done')`     | NOT NULL, default `'todo'`         |
| `due_date`   | `Date`                                  | Nullable, default `None`           |
| `created_at` | `DateTime`                              | NOT NULL, server_default `now()`   |
| `updated_at` | `DateTime`                              | NOT NULL, server_default `now()`, onupdate `now()` |

### Status Enum Values

- `todo` — Task has not been started
- `in-progress` — Task is currently being worked on
- `done` — Task has been completed

---

## Pydantic Schemas

### `TaskCreate` (POST request body)

| Field      | Type                | Required | Default  |
|------------|---------------------|----------|----------|
| `title`    | `str` (1–255 chars) | Yes      | —        |
| `status`   | `TaskStatusEnum`    | No       | `"todo"` |
| `due_date` | `Optional[date]`    | No       | `None`   |

### `TaskUpdate` (PUT request body)

| Field      | Type                | Required | Default |
|------------|---------------------|----------|---------|
| `title`    | `str` (1–255 chars) | Yes      | —       |
| `status`   | `TaskStatusEnum`    | Yes      | —       |
| `due_date` | `Optional[date]`    | No       | `None`  |

### `TaskPatch` (PATCH request body)

| Field      | Type                        | Required | Default |
|------------|-----------------------------|----------|---------|
| `title`    | `Optional[str]` (1–255)     | No       | `None`  |
| `status`   | `Optional[TaskStatusEnum]`  | No       | `None`  |
| `due_date` | `Optional[date]`            | No       | `None`  |

### `TaskResponse` (all responses)

| Field        | Type               | Notes              |
|--------------|--------------------|--------------------||
| `id`         | `int`              | Read-only          |
| `title`      | `str`              |                    |
| `status`     | `TaskStatusEnum`   |                    |
| `due_date`   | `Optional[date]`   | Nullable           |
| `created_at` | `datetime`         | Read-only          |
| `updated_at` | `datetime`         | Read-only          |

> `created_at` and `updated_at` are **read-only**: they are never accepted
> in create or update request bodies.

---

## API Contract

Base path: `/api/tasks`

### 1. List Tasks

```
GET /api/tasks?status={status}
```

| Parameter | In    | Type              | Required | Description              |
|-----------|-------|-------------------|----------|--------------------------|
| `status`  | query | `TaskStatusEnum`  | No       | Filter by task status    |

**Response:** `200 OK`
```json
[
  {
    "id": 1,
    "title": "Buy groceries",
    "status": "todo",
    "due_date": "2025-06-15",
    "created_at": "2025-01-01T12:00:00",
    "updated_at": "2025-01-01T12:00:00"
  }
]
```

**Error — invalid status filter:** `422 Unprocessable Entity`

### 2. Get Task by ID

```
GET /api/tasks/{task_id}
```

| Parameter | In   | Type  | Required | Description         |
|-----------|------|-------|----------|---------------------|
| `task_id` | path | `int` | Yes      | Task primary key    |

**Response:** `200 OK` — single `TaskResponse`

**Error:** `404 Not Found`
```json
{"detail": "Task not found"}
```

### 3. Create Task

```
POST /api/tasks
```

**Request body:** `TaskCreate`
```json
{
  "title": "Buy groceries",
  "status": "todo",
  "due_date": "2025-06-15"
}
```

**Response:** `201 Created` — `TaskResponse`

**Error:** `422 Unprocessable Entity` (validation failure)

### 4. Full Update Task

```
PUT /api/tasks/{task_id}
```

**Request body:** `TaskUpdate` — all fields required

**Response:** `200 OK` — `TaskResponse`

**Errors:** `404 Not Found`, `422 Unprocessable Entity`

### 5. Partial Update Task

```
PATCH /api/tasks/{task_id}
```

**Request body:** `TaskPatch` — only supplied fields are updated

**Response:** `200 OK` — `TaskResponse`

**Errors:** `404 Not Found`, `422 Unprocessable Entity`

### 6. Delete Task

```
DELETE /api/tasks/{task_id}
```

**Response:** `204 No Content`

**Error:** `404 Not Found`

---

## Error Responses

All errors follow FastAPI's default format:

```json
{
  "detail": "Human-readable error message"
}
```

Or for validation errors (422):

```json
{
  "detail": [
    {
      "loc": ["body", "title"],
      "msg": "String should have at least 1 character",
      "type": "string_too_short"
    }
  ]
}
```

| Status Code | Meaning                  | When                                        |
|-------------|--------------------------|---------------------------------------------|
| 200         | OK                       | Successful GET, PUT, PATCH                  |
| 201         | Created                  | Successful POST                             |
| 204         | No Content               | Successful DELETE                           |
| 404         | Not Found                | Task with given ID does not exist           |
| 422         | Unprocessable Entity     | Request validation failure (bad enum, etc.) |

---

## Component Hierarchy

```
App
└── Layout
    ├── TaskForm          # Create new task
    ├── TaskFilter        # Filter by status
    └── TaskList          # List of tasks
        └── TaskItem      # Individual task with edit/delete actions
```

### Component Responsibilities

- **App** — Top-level routing and state provider
- **Layout** — Page layout wrapper (header, main content area)
- **TaskForm** — Form for creating new tasks (title, status, due_date)
- **TaskFilter** — Dropdown or button group to filter tasks by status
- **TaskList** — Renders an array of tasks, handles empty state
- **TaskItem** — Displays a single task; inline edit, status toggle, delete

---

## Frontend Services

### `api.ts`

```typescript
getTasks(status?: string): Promise<Task[]>
getTask(id: number): Promise<Task>
createTask(data: TaskCreate): Promise<Task>
updateTask(id: number, data: TaskUpdate): Promise<Task>
patchTask(id: number, data: Partial<TaskUpdate>): Promise<Task>
deleteTask(id: number): Promise<void>
```

### State Management

- React `useState` + `useEffect` for task list
- Optimistic updates for status toggles
- Error state for API failures

---

## Configuration

| Variable       | Default                        | Description             |
|----------------|--------------------------------|-------------------------|
| `DATABASE_URL` | `sqlite:///./tasks.db`         | SQLAlchemy database URL |
| `VITE_API_URL` | `http://localhost:8000`        | Backend URL for frontend|

---

## Development Workflow

### Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

### Testing

```bash
cd backend
python -m pytest tests/ -v
```
