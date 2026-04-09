# Running the Application

## TEAM_BRIEF
stack: Python/FastAPI
test_runner: pytest tests/
lint_tool: ruff check .
coverage_tool: pytest-cov
coverage_threshold: 70
coverage_applies: true

## Prerequisites

- Python 3.12+ **or** Docker / Docker Compose

## Option A — Docker (recommended)

```bash
# Build and start the API
docker compose up --build

# In another terminal, verify it works
curl http://localhost:8000/hello
# => {"message":"hello world"}

# Run the test suite inside the container
docker compose exec api pytest tests/
```

## Option B — Local virtualenv

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# Start the server
uvicorn app:app --host 0.0.0.0 --port 8000

# Run the tests (separate terminal)
pytest tests/
```

## Endpoints

| Method | Path     | Description             |
|--------|----------|-------------------------|
| GET    | `/hello` | Returns hello world JSON |
| GET    | `/`      | Todo API welcome message |
| *      | `/todos` | Todo CRUD endpoints      |

## Authentication

No authentication is required — this is a development/demo application.
