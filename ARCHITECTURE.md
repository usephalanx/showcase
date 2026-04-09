# Architecture Overview

## Tech Stack

- **Language**: Python 3.12
- **Framework**: FastAPI
- **ASGI Server**: Uvicorn
- **Storage**: In-memory (dict-based via `storage.py`)
- **Containerisation**: Docker + Docker Compose

## Project Structure

```
.
├── main.py                 # FastAPI application entry point
├── routes.py               # Todo CRUD API router
├── models.py               # Pydantic request/response schemas
├── storage.py              # In-memory todo store
├── requirements.txt        # Python dependencies
├── Dockerfile              # Container image definition
├── docker-compose.yml      # Single-command local startup
├── conftest.py             # Root pytest configuration
├── tests/
│   ├── __init__.py
│   └── test_health.py      # Tests for GET /health
├── ARCHITECTURE.md          # This file
└── RUNNING.md               # Setup and run instructions
```

## API Endpoints

| Method | Path              | Status | Response                  |
|--------|-------------------|--------|---------------------------|
| GET    | `/`               | 200    | `{"message": "Welcome to the Todo API"}` |
| GET    | `/health`         | 200    | `{"message": "hi"}`       |
| POST   | `/todos`          | 201    | Created todo object       |
| GET    | `/todos`          | 200    | List of todo objects      |
| GET    | `/todos/{id}`     | 200    | Single todo object        |
| PUT    | `/todos/{id}`     | 200    | Updated todo object       |
| DELETE | `/todos/{id}`     | 200    | `{"detail": "Todo deleted successfully"}` |

## Running

See [RUNNING.md](RUNNING.md) for setup and run instructions.

## Testing

```bash
pip install -r requirements.txt
pytest tests/ -v --tb=short
```

Coverage report:

```bash
pytest tests/ --cov=. --cov-report=term-missing
```

## Design Decisions

- **Single `main.py` entry point** keeps the application simple while delegating route logic to `routes.py`.
- **In-memory storage** (`storage.py`) avoids external database dependencies for development and testing.
- **No authentication** — this is a minimal API scaffold ready to be extended.
- **Docker Compose** enables one-command local startup (`docker compose up --build`).
