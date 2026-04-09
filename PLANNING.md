# Project Planning

## Architecture

This project is a FastAPI application that serves a simple Hello API endpoint
alongside a Todo CRUD API with in-memory storage.

## Project Structure

```
.
├── main.py              # FastAPI app instance and root endpoint
├── routes.py            # Todo CRUD router
├── models.py            # Pydantic request/response schemas
├── storage.py           # In-memory todo store
├── conftest.py          # Root pytest configuration
├── requirements.txt     # Pinned Python dependencies
├── Dockerfile           # Container image definition
├── docker-compose.yml   # One-command local startup
├── RUNNING.md           # Instructions to run the application
├── PLANNING.md          # This file
└── tests/
    ├── __init__.py
    ├── test_main.py     # Tests for root endpoint
    └── test_todos.py    # Tests for todo CRUD endpoints
```

## Endpoints

| Method | Path            | Description                          | Response              |
|--------|-----------------|--------------------------------------|-----------------------|
| GET    | `/`             | Hello message                        | `{"message": "hello"}` |
| POST   | `/todos`        | Create a new todo                    | TodoResponse (201)    |
| GET    | `/todos`        | List all todos                       | List[TodoResponse]    |
| GET    | `/todos/{id}`   | Retrieve a single todo               | TodoResponse          |
| PUT    | `/todos/{id}`   | Update an existing todo              | TodoResponse          |
| DELETE | `/todos/{id}`   | Delete a todo                        | `{"detail": "..."}` |

## Technology Choices

- **FastAPI** — Modern, high-performance Python web framework with automatic
  OpenAPI documentation and request validation via Pydantic.
- **Uvicorn** — Lightning-fast ASGI server suitable for both development and
  production deployments.
- **Pydantic v2** — Data validation and serialisation for request/response models.
- **pytest** — Industry-standard Python test runner.
- **httpx** — Required by FastAPI's `TestClient` for synchronous test requests.

## Edge Cases

- `GET /` with and without trailing slash both resolve (FastAPI default).
- `POST /` returns 405 Method Not Allowed (FastAPI default behaviour).
- Response `Content-Type` is `application/json`.
