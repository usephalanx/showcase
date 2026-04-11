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

### 3. Access the API

Open your browser or use curl:

```bash
curl http://localhost:8000/hello
```

Expected response:

```json
{"message": "Hello, World!"}
```

### 4. Run tests

```bash
pytest tests/
```

## Docker

### Build and run with Docker Compose

```bash
docker compose up --build
```

The application will be accessible at `http://localhost:8000/hello`.

### Stop the service

```bash
docker compose down
```
