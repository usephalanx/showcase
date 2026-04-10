# Running Yellow World

## TEAM_BRIEF
stack: HTML/CSS/JS + Python http.server
test_runner: pytest tests/
lint_tool: ruff check .
coverage_tool: pytest-cov
coverage_threshold: 70
coverage_applies: true

## Prerequisites

- Python 3.10+ (standard library only — no pip packages required for the server)
- Docker & Docker Compose (optional, for containerised run)

## Run Locally

```bash
python server.py
```

Then open <http://localhost:8000> in your browser.

To use a custom port:

```bash
PORT=3000 python server.py
```

## Run with Docker Compose

```bash
docker compose up --build
```

The app will be available at <http://localhost:8000>.

## Run Tests

```bash
pip install pytest pytest-cov
pytest tests/ -v --tb=short
```

With coverage:

```bash
pytest tests/ --cov=. --cov-report=term-missing
```

## Lint

```bash
pip install ruff
ruff check .
```
