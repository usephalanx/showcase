# Architecture

## Framework Choice

This project uses **FastAPI** as the web framework for the following reasons:

- **Async support**: Built on Starlette, FastAPI natively supports async request handlers.
- **Automatic OpenAPI documentation**: Interactive Swagger UI and ReDoc are generated from route definitions and Pydantic models.
- **Pydantic validation**: Request and response data is validated and serialized through Pydantic models, providing type safety at runtime.
- **Minimal boilerplate**: Endpoints are concise Python functions with type annotations.

## Project Structure

```
.
├── app/
│   ├── __init__.py          # Python package marker
│   └── main.py              # FastAPI application and endpoint definitions
├── tests/
│   ├── __init__.py          # Python package marker
│   └── test_hello.py        # Test suite for all endpoints
├── requirements.txt         # Pinned Python dependencies
├── Dockerfile               # Container image definition
├── docker-compose.yml       # Single-command local development
├── conftest.py              # Root pytest configuration
├── RUNNING.md               # How to install and run
└── ARCHITECTURE.md          # This file
```

## Endpoint Design

### GET `/`

Health-check endpoint. Returns HTTP 200 with body:

```json
{"status": "ok"}
```

Response model: `HealthResponse` with field `status: str`.

### GET `/hello`

Greeting endpoint. Returns HTTP 200 with body:

```json
{"message": "hello-world"}
```

Response model: `HelloResponse` with field `message: str`.

## Response Schema

All responses use Pydantic `BaseModel` subclasses to guarantee a consistent JSON structure. The models are defined in `app/main.py`:

- **HelloResponse**: `{"message": str}`
- **HealthResponse**: `{"status": str}`

## Deployment Strategy

The application is containerised using Docker:

1. A multi-stage-friendly `Dockerfile` based on `python:3.12-slim` installs dependencies and copies the application code.
2. `docker-compose.yml` provides a single-command (`docker compose up`) development experience with port mapping and restart policy.
3. Uvicorn serves the ASGI application on `0.0.0.0:8000`.

## Testing Strategy

Tests use **pytest** with FastAPI's synchronous `TestClient` (backed by `httpx`):

- Every endpoint is tested for correct status code, response body, and content-type header.
- Negative cases (wrong HTTP method, non-existent routes) are covered.
- Tests are located in `tests/test_hello.py` and can be run with `pytest tests/ -v`.
