# Architecture Overview

## 1. Project Layout

```
backend/
├── app/
│   ├── __init__.py          # Package marker
│   ├── main.py              # FastAPI application & lifespan
│   ├── database.py          # SQLAlchemy engine, session, Base
│   ├── models.py            # ORM models (Project, Task)
│   ├── schemas.py           # Pydantic request/response schemas
│   ├── routers/             # API route modules (future)
│   │   ├── __init__.py
│   │   ├── projects.py
│   │   ├── tasks.py
│   │   └── auth.py
│   └── services/            # Business logic layer (future)
│       └── __init__.py
├── tests/
│   ├── __init__.py
│   ├── conftest.py          # Shared fixtures
│   ├── test_models.py
│   ├── test_schemas.py
│   ├── test_database.py
│   └── test_health.py
├── init_db.py               # CLI script to create tables
└── requirements.txt         # Python dependencies

frontend/                    # (future)
├── src/
│   ├── components/
│   │   ├── ProjectsGrid.tsx
│   │   ├── ProjectDetail.tsx
│   │   ├── TaskBoard.tsx
│   │   ├── TaskCard.tsx
│   │   └── AddTaskForm.tsx
│   ├── contexts/
│   │   └── AuthContext.tsx
│   ├── hooks/
│   │   └── useProjects.ts
│   ├── pages/
│   ├── App.tsx
│   └── main.tsx
├── index.html
└── package.json
```

## 2. Backend Structure

### Layers

| Layer      | Responsibility                              |
| ---------- | ------------------------------------------- |
| Routers    | HTTP endpoint definitions, request parsing  |
| Schemas    | Pydantic validation and serialisation       |
| Services   | Business logic, orchestration               |
| Models     | SQLAlchemy ORM table definitions             |
| Database   | Engine, session factory, connection pooling  |

### Database

- **Engine**: SQLite via SQLAlchemy 2.0 (`create_engine`).
- **Sessions**: `sessionmaker` yields sessions injected through `Depends(get_db)`.
- **Migrations**: `init_db()` calls `Base.metadata.create_all`.

### Authentication Flow (future)

1. Client sends `POST /api/auth/login` with `{username, password}`.
2. Backend verifies credentials using `passlib` + `bcrypt`.
3. On success, a JWT access token is generated with `python-jose`.
4. Subsequent requests include `Authorization: Bearer <token>`.
5. A FastAPI dependency (`get_current_user`) decodes and validates the token.

```
┌────────┐   POST /auth/login    ┌─────────┐
│ Client │ ──────────────────►   │ FastAPI │
│        │ ◄──────────────────   │         │
│        │   { access_token }    │         │
│        │                       │         │
│        │   GET /api/projects   │         │
│        │   Authorization:      │         │
│        │   Bearer <token>      │         │
│        │ ──────────────────►   │         │
│        │ ◄──────────────────   │         │
│        │   [project list]      │         │
└────────┘                       └─────────┘
```

## 3. Frontend Structure (future)

- **React 18** + **Vite** for fast dev builds.
- **react-router-dom v6** for client-side routing.
- **TanStack Query** (React Query) for server-state management.
- **React Context + useReducer** for auth state.
- **Tailwind CSS** for styling with a custom colour palette.

### Routing Plan

| Path                  | Component      | Auth? |
| --------------------- | -------------- | ----- |
| `/login`              | LoginPage      | No    |
| `/register`           | RegisterPage   | No    |
| `/projects`           | ProjectsGrid   | Yes   |
| `/projects/:id`       | ProjectDetail  | Yes   |

## 4. Data Flow Diagrams

### Project Creation

```
User ──► AddProjectForm ──► POST /api/projects ──► Router
                                                      │
                                                      ▼
                                                   Service
                                                      │
                                                      ▼
                                                   Model.create
                                                      │
                                                      ▼
                                                   SQLite
                                                      │
                                              ProjectResponse
                                                      │
User ◄── ProjectsGrid ◄── React Query cache ◄────────┘
```

### Task Status Update

```
User drag-drop ──► TaskBoard ──► PATCH /api/tasks/:id
                                        │
                                        ▼
                                     Service
                                        │
                                        ▼
                                     Model.update
                                        │
                                  TaskResponse
                                        │
User ◄── TaskCard ◄── optimistic update ┘
```
