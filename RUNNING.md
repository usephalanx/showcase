# Running the Hello World API

## TEAM_BRIEF
stack: Python/FastAPI
test_runner: pytest tests/
lint_tool: ruff check .
coverage_tool: pytest-cov
coverage_threshold: 70
coverage_applies: true

## Prerequisites

- Python 3.12+ **or** Docker

## Option A — Local Python

```bash
pip install -r requirements.txt
uvicorn app:app --reload
```

Then visit: <http://localhost:8000/hello>

## Option B — Docker Compose

```bash
docker compose up --build
```

Then visit: <http://localhost:8000/hello>

## Running Tests

```bash
# Local
pip install -r requirements.txt
pytest tests/

# Docker
docker compose run --rm api pytest tests/
```

## Demo Credentials

No authentication is required. The API is open.
