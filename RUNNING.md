# Running the Hello World API

## TEAM_BRIEF
stack: Python/FastAPI
test_runner: pytest tests/
lint_tool: ruff check .
coverage_tool: pytest-cov
coverage_threshold: 70
coverage_applies: true

## Prerequisites

- Python 3.11+ **or** Docker / Docker Compose

---

## Run Locally (without Docker)

```bash
# 1. Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate   # Linux/macOS
# .venv\Scripts\activate    # Windows

# 2. Install dependencies
pip install -r requirements.txt

# 3. Start the server
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

The API is now available at **http://localhost:8000/hello**.

---

## Run with Docker Compose

```bash
docker compose up --build
```

The API is now available at **http://localhost:8000/hello**.

Stop with `Ctrl+C` or:

```bash
docker compose down
```

---

## Run Tests

```bash
# Install dependencies (if not already installed)
pip install -r requirements.txt

# Run the test suite with coverage
pytest tests/ -v --tb=short --cov=app --cov-report=term-missing
```

All tests should pass with 100% coverage on `app/main.py`.

---

## Endpoints

| Method | Path     | Description                      | Status |
|--------|----------|----------------------------------|--------|
| GET    | `/hello` | Returns `{"message": "Hello, World!"}` | 200    |
