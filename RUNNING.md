# Running Instructions

## TEAM_BRIEF
stack: Python/FastAPI
test_runner: pytest tests/ -v
lint_tool: ruff check .
coverage_tool: pytest-cov
coverage_threshold: 70
coverage_applies: true

## Local Development

```bash
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## Running Tests

```bash
pytest tests/ -v
```

## Running Tests with Coverage

```bash
pytest tests/ --cov=app --cov-report=term-missing --cov-fail-under=70
```

## Docker

### Build and run

```bash
docker compose up --build
```

### Run tests in container

```bash
docker compose run --rm api pytest tests/ --cov=app --cov-report=term-missing --cov-fail-under=70
```
