# Running the Application

## TEAM_BRIEF
stack: Python/FastAPI
test_runner: pytest tests/
lint_tool: ruff check .
coverage_tool: pytest-cov
coverage_threshold: 70
coverage_applies: true

## Prerequisites

- Python 3.11+
- Docker (optional)

## Local Setup

```bash
pip install -r requirements.txt
```

## Run the Application

### Using uvicorn directly

```bash
# Run the app/main.py entry point
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### Using Docker

```bash
docker compose up --build
```

The application will be available at http://localhost:8000

## Key Endpoints

| Method | Path      | Description             |
|--------|-----------|-------------------------|
| GET    | /         | Root - Hello World      |
| GET    | /health   | Health check            |
| GET    | /hello    | Hello, World! greeting  |

## Run Tests

```bash
pytest tests/ -v
```

## Run Tests with Coverage

```bash
pytest tests/ --cov=app --cov-report=term-missing
```
