# Hello World API

## TEAM_BRIEF
stack: Python/FastAPI
test_runner: pytest tests/ -v
lint_tool: ruff check .
coverage_tool: pytest-cov
coverage_threshold: 70
coverage_applies: true

## Quick Start

```bash
pip install -r requirements.txt
uvicorn app:app --host 0.0.0.0 --port 8000
```

Then open http://localhost:8000/hello

## API Reference

### GET /hello

Returns a JSON object:

```json
{
  "message": "hello world",
  "timestamp": "2024-01-01T00:00:00+00:00"
}
```

| Field       | Type   | Description                          |
|-------------|--------|--------------------------------------|
| message     | string | Always `"hello world"`               |
| timestamp   | string | Current UTC time in ISO 8601 format  |

### GET /

Health-check endpoint returning `{"status": "ok"}`.

## Running Tests

```bash
pip install -r requirements.txt
pytest tests/ -v --tb=short --cov=app --cov-report=term-missing
```
