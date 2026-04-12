# Running the Application

## TEAM_BRIEF
stack: Python/FastAPI
test_runner: pytest tests/
lint_tool: ruff check .
coverage_tool: pytest-cov
coverage_threshold: 70
coverage_applies: true

## Quick Start

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Run the application:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

3. Open http://localhost:8000 in your browser.

## Run Tests

```bash
pytest tests/ -v
```

## API Reference

- `GET /` — Welcome message
- `POST /todos` — Create a new todo
- `GET /todos` — List all todos
- `GET /todos/{id}` — Retrieve a single todo
- `PUT /todos/{id}` — Update a todo
- `DELETE /todos/{id}` — Delete a todo
