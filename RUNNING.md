# Running the Todo / Hello World API

## TEAM_BRIEF

| Key                | Value                  |
|--------------------|------------------------|
| stack              | Python, FastAPI        |
| test_runner        | pytest                 |
| lint_tool          | N/A                    |
| coverage_tool      | pytest-cov             |
| coverage_threshold | 80%                    |
| coverage_applies   | app.py, routes.py, storage.py |

## Architecture

| File                  | Purpose                                           |
|-----------------------|---------------------------------------------------|
| `app.py`              | FastAPI application entry point (GET `/` and `/hello`) |
| `routes.py`           | Todo CRUD API router (`/todos`)                   |
| `models.py`           | Pydantic request/response schemas                 |
| `storage.py`          | In-memory dictionary-backed todo store            |
| `requirements.txt`    | Pinned Python dependencies                        |
| `Dockerfile`          | Container image definition                        |
| `docker-compose.yml`  | One-command local startup                         |
| `tests/test_hello.py` | Automated tests for GET `/hello`                  |
| `conftest.py`         | Root pytest configuration                         |

## Endpoint Contract

### `GET /hello`

**Response** `200 OK`

```json
{"message": "hello world"}
```

### `GET /`

**Response** `200 OK`

```json
{"message": "Welcome to the Todo API"}
```

See `routes.py` for the full Todo CRUD contract.

## Local Setup

```bash
# 1. Build the image
docker compose build

# 2. Start the service
docker compose up -d

# 3. Verify it works
curl http://localhost:8000/hello
```

## Running Tests

```bash
# Inside the running container
docker compose exec api pytest tests/ -v

# Or locally (with a virtualenv)
pip install -r requirements.txt
pytest tests/ -v
```
