# Running the Application

## TEAM_BRIEF
stack: Python/FastAPI
test_runner: pytest tests/
lint_tool: ruff check .
coverage_tool: pytest-cov
coverage_threshold: 70
coverage_applies: true

## Prerequisites

- Docker and Docker Compose installed on your machine.

## Running with Docker Compose

```bash
docker compose up --build
```

The application will be available at:

- **Hello endpoint:** [http://localhost:8000/hello](http://localhost:8000/hello)
- **Health endpoint:** [http://localhost:8000/health](http://localhost:8000/health)

To stop the application:

```bash
docker compose down
```

## Running Locally (without Docker)

1. Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Start the server:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## Running Tests

```bash
pip install -r requirements.txt
pytest tests/
```

To run tests with coverage:

```bash
pip install pytest-cov
pytest tests/ --cov=app --cov-report=term-missing
```

## Running Tests in Docker

```bash
docker compose run --rm app pytest tests/
```
