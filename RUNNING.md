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
- pip

## Setup

Install dependencies:

```bash
pip install -r requirements.txt
```

## Run the application

Option 1 — run directly:

```bash
python main.py
```

Option 2 — run with auto-reload:

```bash
uvicorn main:app --reload
```

The server starts on port **8000** by default.

## Verify the service

```bash
curl http://localhost:8000/health
```

Expected response:

```json
{"status": "ok"}
```

## Run tests

```bash
pytest tests/ -v --tb=short
```

## Run tests with coverage

```bash
pytest tests/ -v --tb=short --cov=. --cov-report=term-missing
```
