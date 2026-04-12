# Hello World API

## TEAM_BRIEF
stack: Python/FastAPI
test_runner: pytest tests/
lint_tool: ruff check .
coverage_tool: pytest-cov
coverage_threshold: 70
coverage_applies: true

## Prerequisites

- Python 3.10+
- pip (Python package manager)
- Docker and Docker Compose (optional, for containerised usage)

## Install

```bash
pip install -r requirements.txt
```

## Run

### Option 1 — Direct Python

```bash
python app.py
```

### Option 2 — Uvicorn CLI

```bash
uvicorn app:app --host 0.0.0.0 --port 8000
```

### Option 3 — Docker Compose

```bash
docker compose up --build
```

## Test

### Manual smoke test

```bash
curl http://localhost:8000/hello
```

Expected response:

```json
{
  "message": "hello world",
  "timestamp": "2025-01-01T00:00:00.000000+00:00"
}
```

### Automated tests

```bash
pip install -r requirements.txt
pytest tests/ -v
```

Or via Docker:

```bash
docker compose run --rm api pytest tests/ -v
```

## API Reference

### GET /hello

Returns a JSON object with a greeting and the current UTC timestamp.

**Response (200)**

```json
{
  "message": "hello world",
  "timestamp": "2025-01-01T00:00:00.000000+00:00"
}
```

| Field     | Type   | Description                              |
|-----------|--------|------------------------------------------|
| message   | string | Always `"hello world"`                   |
| timestamp | string | ISO-8601 UTC timestamp with timezone info |

### Swagger UI

Interactive API documentation is available at the `/docs` endpoint:

```
http://localhost:8000/docs
```
