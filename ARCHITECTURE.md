# Architecture Overview

## Tech Stack

- **Language**: Python 3.12
- **Framework**: FastAPI
- **ASGI Server**: Uvicorn
- **Storage**: In-memory dictionary (development/testing)
- **Testing**: pytest + pytest-cov

## Project Structure

```
.
├── main.py                 # Application entry point, /health endpoint
├── routes.py               # Todo CRUD API router
├── models.py               # Pydantic request/response schemas
├── storage.py              # In-memory TodoStore
├── requirements.txt        # Python dependencies
├── Dockerfile              # Container image definition
├── docker-compose.yml      # Single-command local startup
├── conftest.py             # Root pytest configuration
├── tests/
│   ├── __init__.py
│   └── test_health.py      # Health endpoint tests
├── ARCHITECTURE.md          # This file
└── RUNNING.md              # Startup and verification instructions
```

## API Endpoints

| Method | Path              | Status | Response                          |
|--------|-------------------|--------|-----------------------------------|
| GET    | `/`               | 200    | `{"message": "Welcome to the Todo API"}` |
| GET    | `/health`         | 200    | `{"message": "hi"}`               |
| POST   | `/todos`          | 201    | Created todo object               |
| GET    | `/todos`          | 200    | List of all todos                 |
| GET    | `/todos/{id}`     | 200    | Single todo object                |
| PUT    | `/todos/{id}`     | 200    | Updated todo object               |
| DELETE | `/todos/{id}`     | 200    | `{"detail": "Todo deleted successfully"}` |

## Running

See [RUNNING.md](RUNNING.md) for detailed setup and startup instructions.

## Testing

```bash
pytest tests/ -v
pytest tests/ --cov=. --cov-report=term-missing
```

## Design Decisions

- **Single-file entry point**: `main.py` keeps the startup surface minimal.
- **In-memory storage**: No database dependency for the initial scope; easy to swap for SQLite or PostgreSQL later.
- **No authentication**: The current scope does not require auth; ready to extend with FastAPI dependency injection.
- **Health endpoint**: Simple `/health` returning `{"message": "hi"}` for liveness probes.
