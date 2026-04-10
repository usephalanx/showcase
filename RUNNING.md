# Running the Hello API

## TEAM_BRIEF
stack: Python/FastAPI
test_runner: pytest tests/
lint_tool: ruff check .
coverage_tool: pytest-cov
coverage_threshold: 70
coverage_applies: true

## Prerequisites

- Docker and Docker Compose installed on your machine.

## Start the Server

Build and start the application container:

```bash
docker compose up --build
```

The API will be available at **http://localhost:8000**.

Verify it is running:

```bash
curl http://localhost:8000/hello
```

Expected response:

```json
{"message": "hello"}
```

## Stop the Server

```bash
docker compose down
```

## Run Tests

Run the test suite inside the container:

```bash
docker compose run --rm app pytest tests/
```

Or, if you have Python 3.11+ and the dependencies installed locally:

```bash
pip install -r requirements.txt
pytest tests/
```

## Run Without Docker

```bash
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000
```
