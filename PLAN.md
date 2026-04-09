# Project Plan

## Architecture

A minimal FastAPI project with an in-memory Todo CRUD API and a `/health`
endpoint for operational monitoring.

## Project Layout

```
.
├── main.py              # FastAPI app instance, root & health endpoints
├── models.py            # Pydantic request/response schemas
├── routes.py            # Todo CRUD router
├── storage.py           # In-memory TodoStore
├── conftest.py          # Root pytest configuration
├── requirements.txt     # Python dependencies
├── Dockerfile           # Container image definition
├── docker-compose.yml   # One-command local startup
├── RUNNING.md           # Operational instructions
├── PLAN.md              # This file
└── tests/
    ├── __init__.py      # Package marker
    └── test_health.py   # /health endpoint tests
```

## Python Version

Python 3.11+

## Dependencies

| Package            | Purpose                          |
|--------------------|----------------------------------|
| fastapi            | Web framework                    |
| uvicorn[standard]  | ASGI server                      |
| httpx              | Test client transport (optional) |
| pytest             | Test runner                      |

## Key Decisions

1. **TestClient over httpx.AsyncClient** — The task specifies
   `from fastapi.testclient import TestClient`, which wraps httpx
   synchronously and requires no async test infrastructure.
2. **In-memory storage** — No database dependency; keeps the project
   self-contained for testing.
3. **Single `app` instance in `main.py`** — Importable by tests
   directly.
