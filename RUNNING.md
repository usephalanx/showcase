# Running the FastAPI Application

## TEAM_BRIEF
stack: Python/FastAPI
test_runner: pytest tests/
lint_tool: ruff check .
coverage_tool: pytest-cov
coverage_threshold: 70
coverage_applies: true

## Prerequisites

- Python 3.11+ **or** Docker / Docker Compose

## Local Setup (without Docker)

```bash
# Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate   # Linux / macOS
# .venv\Scripts\activate    # Windows

# Install dependencies
pip install -r requirements.txt

# Run the application
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

# Run the test suite
pytest tests/
```

## Docker Setup

```bash
# Build and start
docker compose up --build

# Run tests inside the container
docker compose run --rm app pytest tests/
```

## Endpoints

| Method | Path      | Response                          |
|--------|-----------|-----------------------------------|
| GET    | `/health` | `{"status": "ok"}`               |
| GET    | `/hello`  | `{"message": "Hello, world!"}` |
