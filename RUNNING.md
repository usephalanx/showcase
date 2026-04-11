# Hello World FastAPI Application

## TEAM_BRIEF
stack: Python/FastAPI
test_runner: pytest tests/
lint_tool: ruff check .
coverage_tool: pytest-cov
coverage_threshold: 70
coverage_applies: true

## Prerequisites

- Python 3.11+ (for local development)
- Docker and Docker Compose (for containerised execution)

## Local Development

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the application

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

The API will be available at: **http://localhost:8000/hello**

### 3. Run the test suite

```bash
pytest tests/
```

To run with verbose output:

```bash
pytest tests/ -v
```

## Docker

### Build and run with Docker Compose

```bash
docker compose up --build
```

The application will be accessible at: **http://localhost:8000/hello**

To stop the application:

```bash
docker compose down
```

### Build and run with Docker only

```bash
docker build -t hello-api .
docker run -p 8000:8000 hello-api
```

## API Endpoints

| Method | Path     | Description                          | Response                          |
|--------|----------|--------------------------------------|-----------------------------------|
| GET    | `/hello` | Returns a JSON greeting message      | `{"message": "Hello, World!"}` |

## Project Structure

```
.
├── app/
│   ├── __init__.py
│   └── main.py          # FastAPI application with /hello endpoint
├── tests/
│   ├── __init__.py
│   └── test_hello.py    # Comprehensive test suite
├── conftest.py           # Root pytest configuration
├── requirements.txt      # Python dependencies
├── Dockerfile            # Container image definition
├── docker-compose.yml    # Docker Compose orchestration
└── RUNNING.md            # This file
```
