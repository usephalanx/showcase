# Hello World API

A minimal FastAPI application exposing a single `GET /hello` endpoint.

## TEAM_BRIEF
stack: Python/FastAPI
test_runner: pytest tests/ -v
lint_tool: ruff check .
coverage_tool: pytest-cov
coverage_threshold: 70
coverage_applies: true

## Quick Start

### Local

```bash
pip install -r requirements.txt
uvicorn app:app --host 0.0.0.0 --port 8000
```

Open <http://localhost:8000/hello>

### Docker

```bash
docker compose up --build
```

## Run Tests

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

**Response** `200 OK`

```json
{
  "message": "hello world",
  "timestamp": "2025-01-01T00:00:00+00:00"
}
```

| Field       | Type   | Description                              |
|-------------|--------|------------------------------------------|
| message     | string | Always `"hello world"`                   |
| timestamp   | string | Current UTC time in ISO 8601 format      |
