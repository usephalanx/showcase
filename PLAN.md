# Architecture & Design Plan

## Overview

A minimal Todo REST API built with **FastAPI** and backed by in-memory
storage. The project is designed for simplicity, fast iteration, and
easy containerised deployment.

## Python Version

- Python **3.11+** is required.

## Project Layout

| File / Directory       | Responsibility                                      |
|------------------------|-----------------------------------------------------|
| `main.py`              | FastAPI app instance (`app`), root and `/health` endpoints, `uvicorn` bootstrap |
| `routes.py`            | `APIRouter` with full Todo CRUD (`/todos`)          |
| `models.py`            | Pydantic schemas (`TodoCreate`, `TodoUpdate`, `TodoResponse`) |
| `storage.py`           | In-memory `TodoStore` with auto-incrementing IDs    |
| `requirements.txt`     | Pinned dependency ranges                            |
| `Dockerfile`           | Production-ready container image                    |
| `docker-compose.yml`   | One-command local startup                           |
| `tests/`               | Pytest test suite                                   |
| `tests/test_health.py` | Verifies `GET /health` returns `{"status": "ok"}`   |
| `tests/test_todos.py`  | Verifies Todo CRUD endpoints                        |

## Dependencies

| Package          | Purpose                         |
|------------------|----------------------------------|
| fastapi          | Web framework                    |
| uvicorn[standard]| ASGI server                      |
| httpx            | Async HTTP client for testing    |
| pytest           | Test runner                      |
| pytest-asyncio   | Async test support               |

## Key Decisions

1. **In-memory storage** — no external database needed; the `TodoStore`
   class provides a simple dict-based store with thread-safe access.
2. **Health endpoint** — `GET /health` returns `{"status": "ok"}` for
   liveness probes and manual verification.
3. **Separate router** — Todo routes live in `routes.py` to keep
   `main.py` focused on app configuration.
