# Architecture Plan

## Project Layout

```
.
├── main.py               # FastAPI app instance with /health and / endpoints
├── models.py             # Pydantic request/response schemas
├── routes.py             # Todo CRUD APIRouter
├── storage.py            # In-memory TodoStore
├── conftest.py           # Root pytest configuration
├── requirements.txt      # Python dependencies
├── Dockerfile            # Container image definition
├── docker-compose.yml    # Local orchestration
├── tests/
│   ├── __init__.py
│   └── test_health.py    # /health endpoint tests
├── PLAN.md               # This file
└── RUNNING.md            # Instructions for running the project
```

## Python Version

Python 3.11+

## Dependencies

| Package         | Purpose                           |
|-----------------|-----------------------------------|
| fastapi         | Web framework                     |
| uvicorn         | ASGI server                       |
| httpx           | Async HTTP client for testing     |
| pytest          | Test runner                       |
| pytest-asyncio  | Async test support                |

## Key Decisions

- **main.py** holds the FastAPI `app` instance with a single GET `/health`
  endpoint returning `{"status": "ok"}`.
- **routes.py** contains the full Todo CRUD router, mounted via
  `app.include_router(router)`.
- **storage.py** provides an in-memory dict-based store (no database required
  for development).
- **tests/test_health.py** uses `httpx.AsyncClient` with `ASGITransport` to
  verify the `/health` endpoint returns the expected response.
- The `if __name__ == "__main__"` block in main.py runs uvicorn on
  `0.0.0.0:8000` for convenience.
