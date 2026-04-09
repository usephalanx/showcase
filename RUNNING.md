# Running the Project

## TEAM_BRIEF
stack: Python/FastAPI
test_runner: pytest tests/
lint_tool: ruff check .
coverage_tool: pytest-cov
coverage_threshold: 70
coverage_applies: true

## Prerequisites

- Docker and Docker Compose installed, **or**
- Python 3.11+ installed locally

## Quick Start with Docker

```bash
# Build and start the API server
docker compose up --build
```

The API will be available at **http://localhost:8000**.

### Verify

```bash
curl http://localhost:8000/health
# Expected: {"status":"ok"}
```

### Run Tests inside Docker

```bash
docker compose exec api pytest tests/ -v
```

## Local Development (without Docker)

```bash
# Install dependencies
pip install -r requirements.txt

# Start the server
python main.py

# In another terminal, run tests
pytest tests/ -v
```

## Endpoints

| Method | Path              | Description                |
|--------|-------------------|----------------------------|
| GET    | `/`               | Welcome message            |
| GET    | `/health`         | Health check               |
| POST   | `/todos`          | Create a todo              |
| GET    | `/todos`          | List all todos             |
| GET    | `/todos/{id}`     | Get a single todo          |
| PUT    | `/todos/{id}`     | Update a todo              |
| DELETE | `/todos/{id}`     | Delete a todo              |
