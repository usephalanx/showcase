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

```bash
pip install -r requirements.txt
```

## Run the application

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

Then open http://localhost:8000/health to verify the service is running.

## Run tests

```bash
pytest tests/ -v --tb=short
```

## Run tests with coverage

```bash
pytest tests/ -v --tb=short --cov=. --cov-report=term-missing
```
