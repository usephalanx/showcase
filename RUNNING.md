# Running the Application

## Prerequisites

- Python 3.11+
- `pip install -r requirements.txt`

## Start the server

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

Then open http://localhost:8000/health — expected response: `{"status": "ok"}`

## Run tests

```bash
pytest tests/ -v
```

## TEAM_BRIEF
stack: Python/FastAPI
test_runner: pytest tests/
lint_tool: ruff check .
coverage_tool: pytest-cov
coverage_threshold: 70
coverage_applies: true
