# Project Plan

## Overview

A Todo REST API built with FastAPI and backed by in-memory storage,
with an additional health-check endpoint for operational monitoring.

## Architecture

### Python Version

- Python 3.11+

### Dependencies

| Package          | Version Constraint | Purpose                          |
|------------------|--------------------|----------------------------------|
| fastapi          | >=0.110.0,<1       | Web framework                    |
| uvicorn[standard]| >=0.29.0,<1        | ASGI server                      |
| pydantic         | >=2.0.0            | Data validation / serialisation  |
| httpx            | >=0.27.0,<1        | Async HTTP client (testing)      |
| pytest           | >=8.0.0,<9         | Test runner                      |
| pytest-asyncio   | >=0.23,<1          | Async test support               |
| pytest-timeout   | >=2.1.0            | Test timeout guard               |

### Project Layout

```
.
├── main.py                 # FastAPI app with root route + health endpoint
├── routes.py               # Todo CRUD router
├── models.py               # Pydantic request/response schemas
├── storage.py              # In-memory TodoStore
├── conftest.py             # Root pytest configuration
├── requirements.txt        # Pinned dependencies
├── Dockerfile              # Container image definition
├── docker-compose.yml      # Local orchestration
├── RUNNING.md              # How to run & test
├── PLAN.md                 # This file
├── tests/
│   ├── __init__.py
│   └── test_health.py      # Health endpoint tests
└── healthcheck/
    └── e36e389f/           # SQLite-backed variant (legacy)
```

### Key Design Decisions

1. **`main.py`** owns the FastAPI `app` instance.
   - Mounts the Todo CRUD router from `routes.py`.
   - Exposes `GET /health` returning `{"status": "ok"}`.
   - Exposes `GET /` as a welcome/root endpoint.

2. **`tests/test_health.py`** uses `httpx.AsyncClient` with
   `ASGITransport` to exercise `/health` without starting a real
   server.

3. **Docker** setup provides one-command local startup via
   `docker compose up --build`.
