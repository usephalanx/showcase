# Running the Hello World API

## TEAM_BRIEF

| Key                | Value                 |
|--------------------|-----------------------|
| stack              | Python 3.12, FastAPI  |
| test_runner        | pytest                |
| lint_tool          | N/A                   |
| coverage_tool      | N/A                   |
| coverage_threshold | N/A                   |
| coverage_applies   | N/A                   |

## Architecture

| File                    | Purpose                                                |
|-------------------------|--------------------------------------------------------|
| `app.py`                | FastAPI application entry point with GET /hello route  |
| `routes.py`             | Todo CRUD API router (mounted by app.py)               |
| `models.py`             | Pydantic request/response models for Todo resources    |
| `storage.py`            | In-memory dictionary-based Todo storage                |
| `requirements.txt`      | Pinned Python dependencies                             |
| `Dockerfile`            | Container image definition                             |
| `docker-compose.yml`    | One-command local startup                              |
| `tests/test_hello.py`   | Automated tests for the GET /hello endpoint            |
| `tests/__init__.py`     | Makes tests/ a discoverable Python package             |

## Endpoint Contract

```
GET /hello

Response 200 OK
Content-Type: application/json

{"message": "hello world"}
```

## Local Setup

Install the dependencies and start the server:

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Start the server
uvicorn app:app
```

> **Note:** The endpoint is available at http://127.0.0.1:8000/hello

You can verify the server is running with:

```bash
curl http://127.0.0.1:8000/hello
```

Expected response:

```json
{"message": "hello world"}
```

## Docker Setup (alternative)

```bash
# 1. Build the image
docker compose build

# 2. Start the service
docker compose up -d

# 3. Verify
curl http://localhost:8000/hello
```

## Running Tests

```bash
# Locally (with a virtualenv)
pip install -r requirements.txt
pytest tests/ -v

# Or inside the running container
docker compose exec api pytest tests/ -v
```
