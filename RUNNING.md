# Running the Hello World FastAPI Application

## TEAM_BRIEF
stack: Python/FastAPI
test_runner: pytest tests/ -v
lint_tool: ruff check .
coverage_tool: pytest-cov
coverage_threshold: 70
coverage_applies: true

## Prerequisites

- Python 3.11+ **or** Docker
- pip (if running locally)

## Local Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

The API is available at: http://localhost:8000/hello

## Docker Setup

```bash
# Build and run with docker-compose
docker compose up --build
```

The API is available at: http://localhost:8000/hello

## Running Tests

```bash
# Run all tests with verbose output
pytest tests/ -v

# Run tests with coverage
pytest tests/ -v --cov=app --cov-report=term-missing
```

## Endpoints

| Method | Path    | Description                  |
|--------|---------|------------------------------|
| GET    | /hello  | Returns a greeting message   |
