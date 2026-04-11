# Running the Application

## TEAM_BRIEF
stack: Python/FastAPI
test_runner: pytest tests/
lint_tool: ruff check .
coverage_tool: pytest-cov
coverage_threshold: 70
coverage_applies: true

## Prerequisites

- Python 3.11+ (or Docker)
- pip

## Local Setup

```bash
pip install -r requirements.txt
```

## Running the App

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

The API will be available at http://localhost:8000.

### Endpoints

| Method | Path      | Response                         |
|--------|-----------|----------------------------------|
| GET    | `/health` | `{"status": "ok"}`               |
| GET    | `/hello`  | `{"message": "Hello, world!"}` |

## Running Tests

```bash
pytest tests/
```

## Docker

### Build and Run

```bash
docker compose up --build
```

### Run Tests in Docker

```bash
docker compose run --rm web pytest tests/
```
