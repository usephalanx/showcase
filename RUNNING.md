# Running Instructions

## TEAM_BRIEF
stack: Python/FastAPI
test_runner: pytest tests/
lint_tool: ruff check .
coverage_tool: pytest-cov
coverage_threshold: 70
coverage_applies: true

## Local Development

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run the Application

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### Run Tests

```bash
pytest tests/ -v
```

### Run Tests with Coverage

```bash
pytest tests/ --cov=app --cov-report=term-missing
```

## Docker

### Build and Run

```bash
docker compose up --build
```

### Run Tests in Docker

```bash
docker compose run --rm web pytest tests/ --cov=app --cov-report=term-missing
```
