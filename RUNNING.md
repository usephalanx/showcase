# Running the Todo API

## TEAM_BRIEF
stack: Python/FastAPI
test_runner: pytest tests/
lint_tool: ruff check .
coverage_tool: pytest-cov
coverage_threshold: 70
coverage_applies: true

## Prerequisites

- Python 3.11+
- Docker and Docker Compose (for containerised usage)

## Local Development

### Install dependencies

```bash
pip install -r requirements.txt
```

### Run the application

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

Open: <http://localhost:8000/health>

### Run tests

```bash
pytest tests/
```

## Docker

### Build and run

```bash
docker compose up --build
```

The API will be available at: <http://localhost:8000/health>

### Stop

```bash
docker compose down
```

## Endpoints

| Method | Path      | Description              |
|--------|-----------|--------------------------|
| GET    | `/health` | Returns `{"status": "ok"}` |
