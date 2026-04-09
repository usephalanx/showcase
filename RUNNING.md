# Running the Application

## TEAM_BRIEF
stack: Python/FastAPI
test_runner: pytest tests/
lint_tool: ruff check .
coverage_tool: pytest-cov
coverage_threshold: 70
coverage_applies: true

## Prerequisites

- Python 3.11+ **or** Docker + Docker Compose

## Quick Start (Docker)

```bash
docker compose up --build -d
```

Open <http://localhost:8000/health> — you should see:

```json
{"status": "ok"}
```

## Quick Start (local venv)

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000
```

## Running Tests

### Docker

```bash
docker compose exec app pytest tests/ -v --tb=short
```

### Local

```bash
pytest tests/ -v --tb=short
```

### With Coverage

```bash
pytest tests/ --cov=. --cov-report=term-missing
```

## Demo Credentials

No authentication is required — all endpoints are public.
