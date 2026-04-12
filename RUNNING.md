# Hello World API

## TEAM_BRIEF
stack: Python/FastAPI
test_runner: pytest tests/
lint_tool: ruff check .
coverage_tool: pytest-cov
coverage_threshold: 70
coverage_applies: true

## Quick Start

### Using Docker

```bash
docker compose up --build
```

Open <http://localhost:8000/hello> in your browser.

### Without Docker

```bash
pip install -r requirements.txt
python app.py
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

Returns a JSON object with a greeting and the current UTC timestamp.

**Response (200)**

```json
{
  "message": "hello world",
  "timestamp": "2025-01-01T00:00:00.000000Z"
}
```

| Field       | Type   | Description                          |
|-------------|--------|--------------------------------------|
| message     | string | Always `"hello world"`               |
| timestamp   | string | ISO-8601 UTC timestamp ending in `Z` |
