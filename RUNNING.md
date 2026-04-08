# Running the Todo API

## Quick Start (Docker)

```bash
git clone <repository-url>
cd <repository-directory>
docker compose up --build
```

The API will be available at **http://localhost:8000**.

Swagger documentation is at **http://localhost:8000/docs**.

## Local Development (without Docker)

### Prerequisites

- Python 3.11+
- pip

### Install Dependencies

```bash
pip install -r requirements.txt
```

Or install packages directly:

```bash
pip install fastapi uvicorn pydantic httpx pytest
```

### Run the Server

```bash
uvicorn app.main:app --reload
```

The server starts on **http://localhost:8000** by default.

On startup the application automatically seeds a few sample todo items
for demo purposes (see `app/seed.py`).  The seed data is only inserted
when the in-memory store is empty, so it will not duplicate items if
the server is restarted (the store resets on restart anyway since it is
in-memory).

### Run Tests

```bash
pytest
```

Or with verbose output:

```bash
pytest tests/ -v
```

To run a specific test file:

```bash
pytest tests/test_seed.py -v
```

## Seed Data

The application ships with a small set of sample todos that are loaded
automatically at startup via the FastAPI lifespan handler in
`app/main.py`.  You can also call the seed function programmatically:

```python
from app.seed import seed_todos
from app.storage import storage

seed_todos(storage)
```

To reset the store and re-seed:

```python
storage.clear()
seed_todos(storage)
```

The seed function is **idempotent** — it only inserts data when the
store is empty.

## Endpoints

| Method   | URL             | Description       |
| -------- | --------------- | ----------------- |
| `GET`    | `/todos`        | List all todos    |
| `GET`    | `/todos/{id}`   | Get one todo      |
| `POST`   | `/todos`        | Create a todo     |
| `PUT`    | `/todos/{id}`   | Update a todo     |
| `DELETE` | `/todos/{id}`   | Delete a todo     |
| `GET`    | `/health`       | Health check      |

## Architecture

See [ARCHITECTURE.md](ARCHITECTURE.md) for detailed information about
the data model, storage layer, and API design decisions.
