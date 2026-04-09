# Architecture

## Overview

A lightweight Todo REST API built with **Python 3.11+** and **FastAPI**.
Data is stored in-memory (development) or in SQLite (healthcheck variant).

## Tech Stack

| Layer       | Choice                |
|-------------|-----------------------|
| Runtime     | Python 3.11+          |
| Framework   | FastAPI               |
| Server      | Uvicorn (ASGI)        |
| Validation  | Pydantic v2           |
| Testing     | pytest, httpx         |
| Container   | Docker + Compose      |

## Dependencies

- `fastapi>=0.110.0,<1`
- `uvicorn[standard]>=0.29.0,<1`
- `httpx>=0.27.0,<1`
- `pytest>=8.0.0,<9`
- `pytest-cov>=5.0.0,<6`
- `pydantic>=2.0.0`

## Project Layout

```
.
├── main.py              # FastAPI app with /health and root
├── routes.py            # Todo CRUD router
├── models.py            # Pydantic request/response models
├── storage.py           # In-memory todo store
├── requirements.txt     # Pinned dependencies
├── Dockerfile           # Container image definition
├── docker-compose.yml   # One-command local startup
├── tests/
│   ├── __init__.py
│   └── test_health.py   # /health endpoint tests
└── RUNNING.md           # How to run locally
```

## API Contract

### GET /health

**Purpose:** Liveness / readiness probe.

- **Response:** `200 OK`
- **Body:** `{"status": "ok"}`

### GET /

- **Response:** `200 OK`
- **Body:** `{"message": "Welcome to the Todo API"}`

### Todo CRUD — /todos

See `routes.py` for full endpoint documentation.

## Notes

- No database required for the default in-memory mode.
- No authentication/authorisation.
- FastAPI automatically returns `405 Method Not Allowed` for unsupported methods.
- Trailing-slash requests (e.g. `/health/`) are redirected by FastAPI by default.
