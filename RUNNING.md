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

## Option A — Docker (recommended)

```bash
# Build and start
docker compose up --build -d

# Verify
curl http://localhost:8000/health
# {"status": "ok"}

# Run tests inside the container
docker compose exec app pytest tests/ -v --tb=short

# Stop
docker compose down
```

## Option B — Local virtualenv

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Start the server
uvicorn main:app --host 0.0.0.0 --port 8000

# In another terminal
curl http://localhost:8000/health
```

## Running Tests

```bash
pytest tests/ -v --tb=short
```

## Demo Credentials

No authentication is required — the API is open.
