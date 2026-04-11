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
- Docker and Docker Compose (for containerised usage)

## Local Development

### Install dependencies

```bash
pip install -r requirements.txt
pip install anyio pytest-anyio
```

### Run the application

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

The API will be available at: http://localhost:8000

### Run tests

```bash
pytest tests/
```

### Run tests with coverage

```bash
pytest tests/ --cov=app --cov-report=term-missing
```

## Docker

### Build and run

```bash
docker compose up --build
```

The API will be available at: http://localhost:8000

### Stop

```bash
docker compose down
```

## Endpoints

| Method | Path     | Description              |
|--------|----------|--------------------------|
| GET    | `/hello` | Returns a greeting JSON  |

### Example

```bash
curl http://localhost:8000/hello
# {"message": "Hello, World!"}
```
