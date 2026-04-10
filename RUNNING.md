# Running the Hello API

## TEAM_BRIEF
stack: Python/FastAPI
test_runner: pytest tests/
lint_tool: ruff check .
coverage_tool: pytest-cov
coverage_threshold: 70
coverage_applies: true

## Prerequisites

- Docker and Docker Compose installed, **or**
- Python 3.11+ installed locally

---

## Docker-based Setup (Recommended)

### Build and Start the Server

```bash
docker-compose up --build
```

The API will be available at `http://localhost:8000`.

### Verify the /hello Endpoint

```bash
curl http://localhost:8000/hello
```

Expected response:

```json
{"message": "hello"}
```

### Run Tests inside Docker

```bash
docker-compose run --rm api pytest tests/ -v
```

### Stop the Server

```bash
docker-compose down
```

---

## Local Setup (without Docker)

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Start the Server

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### Run Tests

```bash
pytest tests/ -v
```

---

## Project Structure

```
.
├── app/
│   ├── __init__.py
│   └── main.py          # FastAPI application with GET /hello
├── tests/
│   ├── __init__.py
│   └── test_hello.py    # Pytest tests for the /hello endpoint
├── conftest.py           # Root pytest configuration
├── requirements.txt      # Python dependencies
├── Dockerfile            # Container image definition
├── docker-compose.yml    # Docker Compose orchestration
└── RUNNING.md            # This file
```

## API Endpoints

| Method | Path     | Description                       | Response              |
|--------|----------|-----------------------------------|-----------------------|
| GET    | `/hello` | Returns a JSON greeting message   | `{"message": "hello"}` |
