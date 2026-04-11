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
source .venv/bin/activate  # Linux/macOS
# .venv\Scripts\activate   # Windows

# Install dependencies
pip install -r requirements.txt

# Run the application
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

## Docker Setup

```bash
# Build and start
docker compose up --build

# The API will be available at http://localhost:8000
```

## Running Tests

```bash
# Local
pytest tests/

# With coverage
pytest tests/ --cov=app --cov-report=term-missing

# Inside Docker
docker compose run --rm web pytest tests/
```

## Available Endpoints

| Method | Path      | Description                          |
|--------|-----------|--------------------------------------|
| GET    | `/health` | Returns `{"status": "ok"}`           |
| GET    | `/hello`  | Returns `{"message": "Hello, world!"}` |
