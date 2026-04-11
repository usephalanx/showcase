# Running the Application

## TEAM_BRIEF
stack: Python/FastAPI
test_runner: pytest tests/
lint_tool: ruff check .
coverage_tool: pytest-cov
coverage_threshold: 70
coverage_applies: true

## Prerequisites

- Python 3.11+ (or Docker)
- pip

## Local Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

# Run the tests
pytest tests/
```

## Docker Setup

```bash
# Build and start
docker compose up --build

# Run tests inside the container
docker compose run --rm web pytest tests/
```

## Endpoints

| Method | Path      | Description             | Response                        |
|--------|-----------|-------------------------|---------------------------------|
| GET    | `/health` | Service health check    | `{"status": "ok"}`              |
| GET    | `/hello`  | Greeting message        | `{"message": "Hello, world!"}` |
