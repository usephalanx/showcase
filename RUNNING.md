# Hello World API

## TEAM_BRIEF
stack: Python/FastAPI
test_runner: pytest tests/ -v
lint_tool: ruff check .
coverage_tool: pytest-cov
coverage_threshold: 70
coverage_applies: true

## Quick Start

### With Docker

```bash
docker compose up --build
```

Then open <http://localhost:8000/hello>.

### Without Docker

```bash
pip install -r requirements.txt
uvicorn app:app --host 0.0.0.0 --port 8000
```

## API Reference

### `GET /`

Health-check endpoint.

**Response** `200 OK`

```json
{"status": "ok"}
```

### `GET /hello`

Returns a greeting with the current UTC timestamp.

**Response** `200 OK`

```json
{
  "message": "hello world",
  "timestamp": "2024-01-15T12:00:00.000000+00:00"
}
```

| Field       | Type   | Description                          |
|-------------|--------|--------------------------------------|
| `message`   | string | Always `"hello world"`               |
| `timestamp` | string | Current UTC time in ISO 8601 format  |

## Running Tests

```bash
pip install -r requirements.txt
pytest tests/ -v --tb=short --cov=app --cov-report=term-missing
```

Or with Docker:

```bash
docker compose exec api pytest tests/ -v --tb=short --cov=app --cov-report=term-missing
```
