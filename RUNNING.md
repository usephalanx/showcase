# Running the Project

## TEAM_BRIEF
stack: Python/FastAPI
test_runner: pytest tests/
lint_tool: ruff check .
coverage_tool: pytest-cov
coverage_threshold: 70
coverage_applies: true

## Prerequisites

- Python 3.11+ **or** Docker + Docker Compose

---

## Option A: Run with Docker (recommended)

```bash
docker compose up --build
```

The API will be available at **http://localhost:8000**.

Health check: **http://localhost:8000/health**

### Run tests inside the container

```bash
docker compose exec api pytest tests/ -v
```

---

## Option B: Run locally without Docker

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the server

Either:

```bash
python main.py
```

Or:

```bash
uvicorn main:app --reload
```

The API will be available at **http://localhost:8000**.

### 3. Run tests

```bash
pytest tests/
```

### 4. Verify manually

```bash
curl http://localhost:8000/health
```

Expected response:

```json
{"status": "ok"}
```

---

## Endpoints

| Method | Path              | Description                          |
|--------|-------------------|--------------------------------------|
| GET    | `/`               | Welcome message                      |
| GET    | `/health`         | Health check (`{"status": "ok"}`)    |
| POST   | `/todos`          | Create a todo                        |
| GET    | `/todos`          | List all todos                       |
| GET    | `/todos/{todo_id}`| Get a single todo                    |
| PUT    | `/todos/{todo_id}`| Update a todo                        |
| DELETE | `/todos/{todo_id}`| Delete a todo                        |

---

## Project Structure

```
.
├── main.py              # FastAPI app entry point with /health endpoint
├── routes.py            # Todo CRUD API router
├── models.py            # Pydantic request/response schemas
├── storage.py           # In-memory todo storage
├── requirements.txt     # Python dependencies
├── Dockerfile           # Container image definition
├── docker-compose.yml   # One-command local startup
├── conftest.py          # Root pytest configuration
├── PLAN.md              # Architectural decisions
├── RUNNING.md           # This file
└── tests/
    ├── __init__.py
    ├── test_health.py   # Health endpoint tests
    └── test_todos.py    # Todo CRUD endpoint tests
```
