# Running the Hello World API

## TEAM_BRIEF
stack: Python/FastAPI
test_runner: pytest tests/
lint_tool: ruff check .
coverage_tool: pytest-cov
coverage_threshold: 70
coverage_applies: true

## Prerequisites

- Python 3.12+ **or** Docker

## Running Locally (without Docker)

```bash
pip install -r requirements.txt
uvicorn app:app --reload
```

Then visit: <http://localhost:8000/hello>

## Running with Docker

```bash
docker compose up --build
```

Then visit: <http://localhost:8000/hello>

## Running Tests

```bash
pip install -r requirements.txt
pytest tests/
```

Or inside Docker:

```bash
docker compose exec api pytest tests/
```

## Verifying the Endpoint

```bash
curl http://localhost:8000/hello
# Expected: {"message":"hello world"}
```

## No Authentication

This API has no authentication. No demo credentials are required.
