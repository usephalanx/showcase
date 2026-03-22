# Project Architecture

## Technology Stack

- **Backend**: FastAPI with SQLAlchemy ORM and SQLite database
- **Frontend**: Vanilla HTML/CSS/JavaScript with fetch API
- **Backend serves frontend static files**

## Directory Structure

### Backend

```
backend/
  app/
    __init__.py
    main.py          # FastAPI app entry point
    database.py      # SQLAlchemy engine, session, Base
    models.py        # ORM models (Project, Task)
    schemas.py       # Pydantic request/response models
    seed.py          # Sample data seeder
    routes/
      __init__.py
      projects.py    # /api/projects endpoints
      tasks.py       # /api/tasks endpoints
      dashboard.py   # /api/dashboard endpoint
```

### Frontend

```
frontend/
  index.html             # Dashboard page
  projects.html          # Projects list + create form
  project_detail.html    # Project detail + task list + add task form
  css/
    style.css
  js/
    api.js               # Shared API client helper
    dashboard.js
    projects.js
    project_detail.js
```

### Tests

```
tests/
  __init__.py
  conftest.py            # Shared fixtures
  test_database.py
  test_models.py
  test_schemas.py
  test_seed.py
```

## Frontend Pages

1. **Dashboard** (`/`): Summary stats (total projects, total tasks, tasks by status, overdue tasks) and recent tasks.
2. **Projects** (`/projects.html`): Table of all projects (name, status, created_at) plus a create-project form.
3. **Project Detail** (`/project_detail.html?id=:id`): Project info header, task table, add-task form.

## Input Validation Rules

| Field               | Type     | Constraints                                          |
|---------------------|----------|------------------------------------------------------|
| Project.name        | string   | Required, 1–100 chars                                |
| Project.description | string   | Optional, max 500 chars                              |
| Project.status      | enum     | `active`, `completed`, `archived` (default `active`) |
| Task.title          | string   | Required, 1–200 chars                                |
| Task.status         | enum     | `todo`, `in_progress`, `done` (default `todo`)       |
| Task.priority       | enum     | `low`, `medium`, `high` (default `medium`)           |
| Task.due_date       | date     | Optional, ISO 8601 (YYYY-MM-DD)                      |
| Task.project_id     | integer  | Required, must reference existing project             |

## Error Handling Strategy

| HTTP Status | Usage                                |
|-------------|--------------------------------------|
| 400         | Validation errors                    |
| 404         | Resource not found                   |
| 422         | Malformed request body               |
| 500         | Unexpected server errors             |

All error responses follow this JSON format:

```json
{
  "detail": "Human-readable message",
  "errors": [
    {"field": "field_name", "message": "specific error"}
  ]
}
```

The `errors` array is optional and included only for validation errors.

## Seed Data

**Projects:**

1. Website Redesign – "Redesign the company website with modern UI/UX" (active)
2. Mobile App Launch – "Develop and launch the mobile application" (active)

**Tasks:**

1. Create wireframes – Project 1, done, high, 2025-01-15
2. Design homepage mockup – Project 1, in_progress, high, 2025-02-01
3. Implement responsive CSS – Project 1, todo, medium, 2025-02-15
4. Set up React Native project – Project 2, done, high, 2025-01-20
5. Build authentication flow – Project 2, in_progress, high, 2025-02-10
