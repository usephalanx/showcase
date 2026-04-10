# Yellow World App

A bright, cheerful "Yellow World" single-page web application served by a
minimal Python HTTP server.

## Quick Start

```bash
# Serve locally
python server.py

# Run tests
pytest tests/
```

## TEAM_BRIEF
stack: Python/static-HTML
test_runner: pytest tests/
lint_tool: ruff check .
coverage_tool: pytest-cov
coverage_threshold: 70
coverage_applies: true

## Project Structure

```
├── public/
│   ├── index.html      # Main HTML page
│   ├── styles.css       # Yellow-themed stylesheet
│   └── app.js           # Minimal JavaScript
├── server.py            # Python HTTP server
├── tests/
│   └── test_yellow_world.py   # Comprehensive test suite
├── Dockerfile
├── docker-compose.yml
└── RUNNING.md
```

## Running Tests

```bash
pip install pytest
pytest tests/ -v
```

## Docker

```bash
docker compose up --build
# Visit http://localhost:8000
```
