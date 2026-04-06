# Todo Application — Architecture Document

## 1. Overview

A full-stack Todo/Task management application consisting of:

- **Backend** — Python FastAPI application with SQLite persistence via SQLAlchemy.
- **Frontend** — React single-page application bootstrapped with Vite and written in TypeScript.
- **Database** — SQLite file-based database (`tasks.db`).

The backend exposes a RESTful JSON API consumed by the frontend.

## 2. Backend Architecture

The backend follows a layered structure:

| Layer | Responsibility | Key files |
|-------|---------------|-----------|
| **Router / Endpoints** | HTTP request handling, validation | `backend/main.py` |
| **Schemas** | Pydantic request/response models | `backend/schemas.py` |
| **Models** | SQLAlchemy ORM table definitions | `backend/models.py` |
| **Database** | Engine creation, session management | `backend/database.py` |

Middleware:

- **CORSMiddleware** — allows the frontend dev-server origin.

Server: `uvicorn backend.main:app --reload --port 8000`

## 3. Database Schema

Table: **tasks**

| Column | Type | Constraints |
|--------|------|-------------|
| `id` | INTEGER | PRIMARY KEY AUTOINCREMENT |
| `title` | VARCHAR(255) | NOT NULL |
| `status` | VARCHAR(20) | NOT NULL DEFAULT `'todo'`, CHECK IN (`'todo'`, `'in-progress'`, `'done'`) |
| `due_date` | DATE | NULLABLE |
| `created_at` | DATETIME | DEFAULT CURRENT_TIMESTAMP |
| `updated_at` | DATETIME | DEFAULT CURRENT_TIMESTAMP, updated on every modification |

## 4. API Endpoints

All endpoints are prefixed at the root (`/`).

### `GET /tasks`

Retrieve all tasks. Optional query parameters:

| Param | Type | Description |
|-------|------|-------------|
| `status` | string | Filter by status (`todo`, `in-progress`, `done`) |
| `sort_by` | string | Sort field (e.g. `created_at`, `due_date`) |

**Response** `200 OK` — `Task[]`

### `GET /tasks/{id}`

Retrieve a single task by its id.

**Response** `200 OK` — `Task`
**Error** `404 Not Found`

### `POST /tasks`

Create a new task.

**Request body:**

```json
{
  "title": "string (required)",
  "status": "todo | in-progress | done (optional, default todo)",
  "due_date": "YYYY-MM-DD | null (optional)"
}
```

**Response** `201 Created` — `Task`

### `PUT /tasks/{id}`

Update an existing task.

**Request body (all fields optional):**

```json
{
  "title": "string",
  "status": "todo | in-progress | done",
  "due_date": "YYYY-MM-DD | null"
}
```

**Response** `200 OK` — `Task`
**Error** `404 Not Found`

### `DELETE /tasks/{id}`

Delete a task.

**Response** `200 OK` — `{"detail": "Task deleted"}`
**Error** `404 Not Found`

### Task JSON shape

```json
{
  "id": 1,
  "title": "Buy groceries",
  "status": "todo",
  "due_date": "2025-03-01",
  "created_at": "2025-01-15T10:30:00",
  "updated_at": "2025-01-15T10:30:00"
}
```

## 5. Frontend Architecture

**Stack:** React 18 + Vite + TypeScript + Axios

### Component Tree

```
App
└── HomePage
    ├── TaskForm
    └── TaskList
        └── TaskCard
            └── StatusBadge
```

### State Management

React built-in hooks (`useState`, `useEffect`) manage local component state.
API calls are made via the Axios service in `frontend/src/api.ts`.

### Key Frontend Files

| File | Purpose |
|------|---------|
| `src/main.tsx` | Entry point — mounts `<App />` into DOM |
| `src/App.tsx` | Root component, routing shell |
| `src/types.ts` | TypeScript interfaces (`Task`, `TaskCreate`, `TaskUpdate`) |
| `src/api.ts` | Axios instance & API helper functions |
| `src/components/HomePage.tsx` | Main page layout |
| `src/components/TaskList.tsx` | Renders list of `TaskCard` components |
| `src/components/TaskCard.tsx` | Single task display with actions |
| `src/components/TaskForm.tsx` | Create / edit task form |
| `src/components/StatusBadge.tsx` | Coloured status indicator |

## 6. File Structure

```
/
├── backend/
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   └── requirements.txt
├── frontend/
│   ├── index.html
│   ├── package.json
│   ├── tsconfig.json
│   ├── vite.config.ts
│   └── src/
│       ├── main.tsx
│       ├── App.tsx
│       ├── types.ts
│       ├── api.ts
│       └── components/
│           ├── HomePage.tsx
│           ├── TaskList.tsx
│           ├── TaskCard.tsx
│           ├── TaskForm.tsx
│           └── StatusBadge.tsx
├── tests/
│   └── ...
├── ARCHITECTURE.md
├── RUNNING.md
└── docker-compose.yml
```

## 7. CORS Configuration

The FastAPI backend enables CORS via `CORSMiddleware`:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

The allowed origin `http://localhost:5173` corresponds to the default Vite dev-server address.

## 8. Development Workflow

### Backend

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

Interactive API docs available at http://localhost:8000/docs.

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Opens at http://localhost:5173.

### Docker (recommended)

See [RUNNING.md](RUNNING.md) for Docker Compose instructions.
