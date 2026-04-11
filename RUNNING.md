# Running the Application

## TEAM_BRIEF
stack: Python/FastAPI
test_runner: pytest tests/
lint_tool: ruff check .
coverage_tool: pytest-cov
coverage_threshold: 70
coverage_applies: true

## Docker-Based Instructions

### Build and Run

```bash
docker compose up --build
```

The API will be available at `http://localhost:8000`.

### Run Tests

```bash
pip install -r requirements.txt
pytest tests/ -v
```

### Run Tests with Coverage

```bash
pytest tests/ --cov=app --cov-report=term-missing
```

### Verify the Endpoint

```bash
curl http://localhost:8000/hello
```

Expected response:

```json
{"message": "Hello, World!"}
```
