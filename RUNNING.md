# Running the Hello World API

## TEAM_BRIEF

| Key                | Value              |
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
# Inside the running container
docker compose exec api pytest tests/ -v

# Or locally (with a virtualenv)
pip install -r requirements.txt
pytest tests/ -v
```
