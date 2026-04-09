# Architecture

## Overview

A minimal Todo REST API built with **Python 3.11+** and **FastAPI**.
Data is stored in-memory using a Python dictionary (no database).

## Runtime & Dependencies

| Dependency | Purpose |
|---|---|
| fastapi >=0.110 | Web framework |
| uvicorn[standard] >=0.29 | ASGI server |
| httpx >=0.27 | Test HTTP client (used by FastAPI TestClient) |
| pytest >=8 | Test runner |
| pytest-cov >=5 | Coverage reporting |

## Project Layout

```
.
├── main.py              # FastAPI app, /health & root endpoints
├── routes.py            # Todo CRUD router
├── models.py            # Pydantic request/response schemas
├── storage.py           # In-memory TodoStore
├── conftest.py          # Root pytest configuration
├── requirements.txt     # Python dependencies
├── Dockerfile           # Container image definition
├── docker-compose.yml   # One-command local startup
├── tests/
│   ├── __init__.py
│   └── test_health.py   # /health endpoint tests
└── RUNNING.md           # Setup & run instructions
```

## API Contract

### `GET /health`

**Response:** `200 OK`

```json
{"status": "ok"}
```

This endpoint carries no authentication and is intended for
liveness/readiness probes.

> **Note:** FastAPI will redirect `/health/` (trailing slash) to
> `/health` with a 307 by default.

## Design Decisions

- **No database** — storage is in-memory (`storage.py`), suitable for
  development and demos.
- **No authentication** — all endpoints are public.
- **Single-process** — designed to run as a single uvicorn worker.
