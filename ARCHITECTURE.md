# Todo Application — Architecture Document

This document is the single source of truth for the full-stack Todo application.
Every implementation task references this file for data shapes, endpoint contracts,
component names, and file layout.

---

## 1. Overview

The Todo App is a full-stack task-management application built with:

| Layer    | Technology                          |
| -------- | ----------------------------------- |
| Backend  | **FastAPI** (Python 3.11+)          |
| Database | **SQLite** via **SQLAlchemy**        |
| Frontend | **React 18 + Vite + TypeScript**    |
| HTTP     | **axios** for API calls             |

Users can create, read, update, and delete tasks. Each task has a title, a
status (`todo`, `in-progress`, or `done`), and an optional due date.

---

## 2. Backend Architecture

### Framework & Middleware

* **FastAPI** application created in `backend/main.py`.
* **CORSMiddleware** configured to allow the frontend dev origin
  (`http://localhost:5173`).
* **SQLAlchemy** ORM with a synchronous SQLite engine.

### Key Modules

| Module              | Responsibility                              |
| ------------------- | ------------------------------------------- |
| `main.py`           | App factory, router mounting, lifespan hook |
| `database.py`       | Engine, `SessionLocal`, `Base`              |
| `models.py`         | SQLAlchemy ORM model (`Task`)               |
| `schemas.py`        | Pydantic request/response schemas           |
| `crud.py`           | Database CRUD helper functions              |
| `routers/tasks.py`  | `/tasks` API router                         |

### Pydantic Schemas

```text
TaskCreate   { title: str, status?: str = "todo", due_date?: str | null }
TaskUpdate   { title?: str, status?: str, due_date?: str | null }
TaskResponse { id: int, title: str, status: str, due_date: str | null, created_at: str, updated_at: str }
```

---

## 3. Database Schema

A single table named **`tasks`**:

| Column       | Type                | Constraints                                                        |
| ------------ | ------------------- | ------------------------------------------------------------------ |
| `id`         | INTEGER             | PRIMARY KEY AUTOINCREMENT                                          |
| `title`      | VARCHAR(255)        | NOT NULL                                                           |
| `status`     | VARCHAR(20)         | NOT NULL DEFAULT `'todo'`, CHECK IN (`'todo'`, `'in-progress'`, `'done'`) |
| `due_date`   | DATE                | NULLABLE                                                           |
| `created_at` | DATETIME            | NOT NULL DEFAULT CURRENT_TIMESTAMP                                 |
| `updated_at` | DATETIME            | NOT NULL DEFAULT CURRENT_TIMESTAMP, updated on every row mutation  |

### Status Enum

The **status** column accepts exactly three values:

1. `todo`
2. `in-progress`
3. `done`

This constraint is enforced at the database level (`CHECK`), the Pydantic
schema level (`Literal` / `enum`), and the TypeScript type level.

### `due_date` Nullability

`due_date` is **nullable / optional** across every layer:

* Database: the column allows `NULL`.
* Pydantic: `Optional[date] = None`.
* TypeScript: `due_date: string | null`.
* API JSON: the field may be `null` or omitted on creation.

---

## 4. API Endpoints

All endpoints are prefixed with `/tasks`.

### `GET /tasks`

Retrieve all tasks with optional filtering and sorting.

| Query Param | Type   | Description                                      |
| ----------- | ------ | ------------------------------------------------ |
| `status`    | string | Filter by status (`todo`, `in-progress`, `done`) |
| `sort_by`   | string | Sort field (`created_at`, `due_date`, `title`)   |

**Response** `200 OK`

```json
[
  {
    "id": 1,
    "title": "Buy groceries",
    "status": "todo",
    "due_date": "2025-03-01",
    "created_at": "2025-01-15T10:30:00",
    "updated_at": "2025-01-15T10:30:00"
  }
]
```

### `GET /tasks/{id}`

Retrieve a single task by its primary key.

**Response** `200 OK` — single task object.  
**Response** `404 Not Found` — `{"detail": "Task not found"}`.

### `POST /tasks`

Create a new task.

**Request Body**

```json
{
  "title": "Buy groceries",
  "status": "todo",
  "due_date": "2025-03-01"
}
```

`status` defaults to `"todo"` if omitted. `due_date` is optional (nullable).

**Response** `201 Created` — the created task object.

### `PUT /tasks/{id}`

Update an existing task (partial updates allowed).

**Request Body**

```json
{
  "title": "Buy organic groceries",
  "status": "in-progress",
  "due_date": null
}
```

**Response** `200 OK` — the updated task object.  
**Response** `404 Not Found` — `{"detail": "Task not found"}`.

### `DELETE /tasks/{id}`

Delete a task by its id.

**Response** `200 OK` — `{"detail": "Task deleted successfully"}`.  
**Response** `404 Not Found` — `{"detail": "Task not found"}`.

---

## 5. Frontend Architecture

### Tooling

* **Vite** dev server on port `5173`.
* **TypeScript** in strict mode.
* **axios** for HTTP communication with the backend.

### Component Tree

```
App
└── HomePage
    ├── TaskForm
    └── TaskList
        └── TaskCard
            └── StatusBadge
```

| Component     | Responsibility                                              |
| ------------- | ----------------------------------------------------------- |
| `App`         | Top-level layout and routing                                |
| `HomePage`    | Composes task form and list, owns top-level task state      |
| `TaskForm`    | Input form for creating / editing a task                    |
| `TaskList`    | Renders a list of `TaskCard` components                     |
| `TaskCard`    | Displays a single task's title, due date, and status badge  |
| `StatusBadge` | Visual indicator of a task's current status                 |

### State Management

State is managed via React hooks:

* `useState` — local component state for tasks array, form fields, loading flags.
* `useEffect` — data fetching on mount and after mutations.

No external state library is required at this scale.

### API Client

A thin `api.ts` module wraps **axios** with a pre-configured base URL
(`http://localhost:8000`) and exports typed functions:

```ts
getTasks(params?): Promise<Task[]>
getTask(id): Promise<Task>
createTask(data): Promise<Task>
updateTask(id, data): Promise<Task>
deleteTask(id): Promise<void>
```

---

## 6. File Structure

```
/
├── backend/
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── crud.py
│   └── routers/
│       └── tasks.py
├── frontend/
│   ├── index.html
│   ├── package.json
│   ├── tsconfig.json
│   ├── tsconfig.node.json
│   ├── vite.config.ts
│   └── src/
│       ├── main.tsx
│       ├── App.tsx
│       ├── api.ts
│       ├── types.ts
│       ├── components/
│       │   ├── HomePage.tsx
│       │   ├── TaskForm.tsx
│       │   ├── TaskList.tsx
│       │   ├── TaskCard.tsx
│       │   └── StatusBadge.tsx
│       └── vite-env.d.ts
├── tests/
│   └── test_architecture_doc.py
├── ARCHITECTURE.md
├── RUNNING.md
└── README.md
```

---

## 7. CORS Configuration

The FastAPI backend uses `CORSMiddleware` to allow cross-origin requests
from the Vite dev server:

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

> **Note:** The origin uses `http` (not `https`) because the local Vite
> dev server does not enable TLS by default.

---

## 8. Development Workflow

### Backend

```bash
cd backend
pip install fastapi uvicorn sqlalchemy
uvicorn main:app --reload --port 8000
```

Interactive API docs are available at `http://localhost:8000/docs`.

### Frontend

```bash
cd frontend
npm install
npm run dev
```

The Vite dev server starts on `http://localhost:5173`.

### Running Both Together

See [RUNNING.md](./RUNNING.md) for Docker Compose instructions that start
both services with a single command.
