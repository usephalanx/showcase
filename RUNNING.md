# Running the Application

## TEAM_BRIEF
stack: Python/FastAPI
test_runner: pytest tests/
lint_tool: ruff check .
coverage_tool: pytest-cov
coverage_threshold: 70
coverage_applies: true

## Prerequisites

- Python 3.11+
- pip

## Local Setup

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run the application
python main.py

# 3. Verify health endpoint
curl http://localhost:8000/health
# Expected: {"status": "ok"}
```

## Running Tests

```bash
pytest tests/ -v
```

## Running Tests with Coverage

```bash
pytest tests/ -v --cov=. --cov-report=term-missing
```
