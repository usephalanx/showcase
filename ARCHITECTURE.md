# Architecture Overview

## Tech Stack

- **Language**: Python 3.12
- **Framework**: FastAPI
- **ASGI Server**: Uvicorn
- **Data Storage**: In-memory dictionary (development/testing)
- **Validation**: Pydantic v2
- **Testing**: pytest + httpx (via FastAPI TestClient)

## Project Structure

```
.
├── main.py               # FastAPI application entry point & /health endpoint
├── routes.py             # Todo CRUD API router
├── models.py             # Pydantic request/response schemas
├── storage.py            # In-memory todo storage
├── requirements.txt      # Python dependencies
├── Dockerfile            # Container image definition
├── docker-compose.yml    # Single-command local startup
├── conftest.py           # Root pytest configuration
├── tests/
│   ├── __init__.py
│   └── test_health.py    # Health endpoint tests
├── ARCHITECTURE.md       # This file
└── RUNNING.md            # Setup & run instructions
```

## API Endpoints

| Method | Path              | Status | Response                              |
|--------|-------------------|--------|---------------------------------------|
| GET    | `/`               | 200    | `{"message": "Welcome to the Todo API"}` |
| GET    | `/health`         | 200    | `{"message": "hi"}`                   |
| POST   | `/todos`          | 201    | Created todo object                   |
| GET    | `/todos`          | 200    | List of all todos                     |
| GET    | `/todos/{id}`     | 200    | Single todo object                    |
| PUT    | `/todos/{id}`     | 200    | Updated todo object                   |
| DELETE | `/todos/{id}`     | 200    | `{"detail": "Todo deleted successfully"}` |

## Running

See [RUNNING.md](RUNNING.md) for setup and startup instructions.

## Testing

```bash
pip install -r requirements.txt
pytest tests/ --cov=. --cov-report=term-missing
```

## Design Decisions

- **Single-file entry point**: `main.py` keeps the application bootstrap minimal and easy to locate.
- **In-memory storage**: No database dependency for fast iteration; ready to swap for SQLite or PostgreSQL.
- **No authentication**: Not required for current scope; can be layered in via FastAPI dependencies.
- **Health endpoint**: Provides a lightweight liveness probe suitable for container orchestrators.
