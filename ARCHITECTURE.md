# Architecture

## Framework Choice

**FastAPI** was chosen as the web framework for the following reasons:

- Native async support via ASGI
- Automatic OpenAPI/Swagger documentation generation
- Built-in Pydantic request/response validation
- Minimal boilerplate for simple endpoints
- Excellent performance characteristics

## Project Structure

```
.
├── app/
│   ├── __init__.py          # Package marker
│   └── main.py              # FastAPI application & route definitions
├── tests/
│   ├── __init__.py          # Package marker
│   └── test_hello.py        # Endpoint test suite
├── requirements.txt         # Pinned Python dependencies
├── Dockerfile               # Container image definition
├── docker-compose.yml       # Local development orchestration
├── conftest.py              # Root pytest configuration
└── ARCHITECTURE.md          # This file
```

## Endpoints

### GET /

Health-check endpoint.

- **Response Model:** `HealthResponse`
- **Response Body:** `{"status": "ok"}`
- **Status Code:** 200

### GET /hello

Greeting endpoint.

- **Response Model:** `HelloResponse`
- **Response Body:** `{"message": "hello-world"}`
- **Status Code:** 200

## Response Models

| Model           | Field     | Type | Description            |
|-----------------|-----------|------|------------------------|
| `HelloResponse` | `message` | str  | Greeting message       |
| `HealthResponse`| `status`  | str  | Service health status  |

Both models are defined using Pydantic's `BaseModel` with `Field` descriptors.

## Deployment Strategy

The application is containerised with Docker:

1. **Base image:** `python:3.12-slim` for a small footprint.
2. **Dependencies** are installed via `requirements.txt` in a separate layer for caching.
3. **Runtime:** `uvicorn` serves the ASGI app on `0.0.0.0:8000`.
4. **Local development:** `docker-compose up` starts the service with port 8000 mapped.
5. **Direct execution:** `uvicorn app.main:app --reload` for development without Docker.

## Testing Strategy

- **Framework:** pytest with FastAPI's synchronous `TestClient` (backed by httpx).
- **Coverage:** Every endpoint is tested for status code, response body, and content type.
- **Negative cases:** POST to GET-only routes (405), non-existent routes (404).
- **Execution:** `pytest tests/` from the project root.
