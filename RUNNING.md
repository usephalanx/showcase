# Hello World API

## TEAM_BRIEF
stack: Python/FastAPI
test_runner: pytest tests/ -v
lint_tool: ruff check .
coverage_tool: pytest-cov
coverage_threshold: 70
coverage_applies: true

## Prerequisites

- Python 3.11+
- pip

## Install Dependencies

```bash
pip install -r requirements.txt
```

## Start the Server

```bash
uvicorn app:app --host 0.0.0.0 --port 8000
```

The server will be available at <http://localhost:8000>.

## Sample Request

```bash
curl http://localhost:8000/hello
```

**Expected JSON response:**

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

## Quick Start with Docker

```bash
docker compose up --build
```

Then open <http://localhost:8000/hello>.

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

## Running Tests

```bash
pip install -r requirements.txt
pytest tests/ -v --tb=short --cov=app --cov-report=term-missing
```

Or with Docker:

```bash
docker compose exec api pytest tests/ -v --tb=short --cov=app --cov-report=term-missing
```
