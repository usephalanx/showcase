# Running the Application

## TEAM_BRIEF
stack: Python/FastAPI
test_runner: pytest tests/
lint_tool: ruff check .
coverage_tool: pytest-cov
coverage_threshold: 70
coverage_applies: true

## Prerequisites

- Docker and Docker Compose installed
- (Optional) Python 3.11+ for running locally without Docker

## Running with Docker

### Start the server

```bash
docker compose up --build
```

The API will be available at `http://localhost:8000`.

### Verify the endpoint

```bash
curl http://localhost:8000/hello
```

Expected response:

```json
{"message": "hello"}
```

### Stop the server

```bash
docker compose down
```

## Running Tests

### With Docker

```bash
docker compose run --rm api pytest tests/
```

### Locally (without Docker)

```bash
pip install -r requirements.txt
pytest tests/
```

## Running with Coverage

```bash
pip install pytest-cov
pytest tests/ --cov=app --cov-report=term-missing
```

## Local Development (without Docker)

```bash
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```
