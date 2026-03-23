# Architecture

## Backend Structure

The backend is a **FastAPI** application backed by **SQLite** via
**SQLAlchemy 2.0** ORM.  Authentication uses **JWT** tokens signed with
**HS256** (via python-jose) and passwords are hashed with **bcrypt**
(via passlib).

```
backend/
├── app/
│   ├── __init__.py          # Package marker
│   ├── main.py              # FastAPI app factory, lifespan, router mounts
│   ├── config.py            # Settings from environment variables
│   ├── database.py          # Engine, SessionLocal, Base, get_db, init_db
│   ├── models.py            # SQLAlchemy ORM models (User, Project, Task)
│   ├── schemas.py           # Pydantic v2 request/response schemas
│   ├── security.py          # Password hashing + JWT utilities
│   ├── auth.py              # get_current_user FastAPI dependency
│   └── routers/
│       ├── __init__.py
│       └── auth.py          # POST /auth/register, POST /auth/login
├── tests/
│   ├── __init__.py
│   ├── conftest.py          # Fixtures (in-memory DB, TestClient, auth_headers)
│   ├── test_auth.py         # Auth endpoint & dependency tests
│   └── test_security.py     # Unit tests for hashing & JWT
├── init_db.py               # CLI script to create tables
├── requirements.txt         # Python dependencies
└── SETUP.md                 # Setup instructions
```

## Authentication Flow

```
Client                          Server
  │                               │
  │  POST /auth/register          │
  │  {username, password}  ──────>│──> hash password
  │                               │──> INSERT into users
  │  <────── 201 {user}           │
  │                               │
  │  POST /auth/login             │
  │  {username, password}  ──────>│──> lookup user
  │                               │──> verify_password()
  │                               │──> create_access_token(sub=username)
  │  <────── 200 {access_token}   │
  │                               │
  │  GET /projects                │
  │  Authorization: Bearer <JWT>  │
  │  ────────────────────────────>│──> decode JWT
  │                               │──> load User from DB
  │                               │──> execute endpoint logic
  │  <────── 200 [projects]       │
```

## Data Models

### Users
- id, username (unique), hashed_password, is_active, created_at

### Projects
- id, name, description, owner_id (FK → users.id), created_at

### Tasks
- id, project_id (FK → projects.id), title, description, status, priority, due_date, created_at

## Protecting Endpoints

Any endpoint can be protected by adding the `get_current_user` dependency:

```python
from app.auth import get_current_user
from app.models import User

@router.get("/projects")
def list_projects(current_user: User = Depends(get_current_user)):
    ...
```

## Frontend Structure (Planned)

```
frontend/
├── src/
│   ├── main.tsx
│   ├── App.tsx
│   ├── api/           # Axios/fetch wrappers
│   ├── context/       # AuthContext (React Context + useReducer)
│   ├── pages/         # ProjectsPage, ProjectDetailPage, LoginPage
│   ├── components/    # ProjectsGrid, TaskBoard, TaskCard, AddTaskForm
│   └── hooks/         # useAuth, useProjects, useTasks
├── index.html
├── tailwind.config.js
└── vite.config.ts
```

## State Management

- **Auth state**: React Context + useReducer (token, user, isAuthenticated)
- **Server state**: TanStack Query (React Query) for projects/tasks

## Theming

- Tailwind CSS with a custom colour palette
- Dark-mode via `class` strategy
