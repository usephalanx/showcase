# Running the Todo App

## TEAM_BRIEF
stack: Python/FastAPI
test_runner: pytest tests/
lint_tool: ruff check .
coverage_tool: pytest-cov
coverage_threshold: 70
coverage_applies: true

## Prerequisites

- Python 3.10+
- pip

## Setup

```bash
pip install fastapi uvicorn pydantic pytest httpx pytest-cov ruff
```

## Run the App

```bash
uvicorn main:app --reload
```

The API will be available at http://localhost:8000

## Run Tests

```bash
pytest tests/ -v
```

## Run Tests with Coverage

```bash
pytest tests/ -v --cov=. --cov-report=term-missing
```

## Lint

```bash
ruff check .
```
