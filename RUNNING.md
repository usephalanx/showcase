# Running the Application

## TEAM_BRIEF
stack: Python/FastAPI
test_runner: pytest tests/
lint_tool: ruff check .
coverage_tool: pytest-cov
coverage_threshold: 70
coverage_applies: true

## Prerequisites

- Python 3.12+ (or Docker)
- pip

## Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

# Run the test suite
pytest tests/ -v

# Run tests with coverage
pytest tests/ -v --cov=app --cov-report=term-missing
```

## Docker

```bash
# Build and start
docker compose up --build

# The API is available at:
#   http://localhost:8000/hello
#   http://localhost:8000/health
```

## Endpoints

| Method | Path      | Response                        |
|--------|-----------|---------------------------------|
| GET    | `/hello`  | `{"message": "hello world"}`    |
| GET    | `/health` | `{"status": "ok"}`              |
