# Hello API — Architecture

## 1. Overview

A minimal single-endpoint API that returns `{"message": "hello"}` on `GET /`.
The project is intentionally small to serve as a baseline for incremental
feature additions.

## 2. Framework Choice

**FastAPI** was chosen for the following reasons:

- Native async support via ASGI.
- Automatic OpenAPI / Swagger documentation at `/docs`.
- Built-in request/response validation through Pydantic.
- Minimal boilerplate for simple endpoints.

## 3. Project Structure

```
.
├── app/
│   ├── __init__.py          # Python package marker
│   └── main.py              # FastAPI application & GET / endpoint
├── tests/
│   ├── __init__.py          # Python package marker
│   └── test_main.py         # Automated tests for the endpoint
├── requirements.txt         # Pinned Python dependencies
├── Dockerfile               # Container image definition
├── docker-compose.yml       # One-command local startup
├── RUNNING.md               # How to run the project
└── ARCHITECTURE.md           # This file
```

## 4. Endpoint Specification

| Method | Path | Status | Content-Type       | Body                     |
|--------|------|--------|--------------------|--------------------------|
| GET    | `/`  | 200 OK | `application/json` | `{"message": "hello"}` |

Any other HTTP method on `/` returns **405 Method Not Allowed**.

## 5. Data Model

```python
class HelloResponse(BaseModel):
    message: str
```

A single Pydantic model is used as the `response_model` to guarantee the
response shape and enable OpenAPI schema generation.

## 6. Testing Strategy

- **Framework:** pytest + FastAPI `TestClient` (backed by httpx).
- **Tests:**
  1. `test_root_returns_200` — status code is 200.
  2. `test_root_returns_hello_message` — JSON body equals `{"message": "hello"}`.
  3. `test_root_content_type_is_json` — `Content-Type` header contains `application/json`.
  4. `test_post_root_returns_405` — `POST /` yields 405.

## 7. Deployment

- Docker image based on `python:3.12-slim`.
- Application served by **uvicorn** on `0.0.0.0:8000`.
- `docker compose up` for one-command local startup.
