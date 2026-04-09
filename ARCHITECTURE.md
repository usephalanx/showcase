# Architecture

## 1. Overview

This project is a lightweight **Todo API** built with FastAPI. It also
exposes a minimal Hello World endpoint (`GET /hello`) that serves as a
health-check / smoke-test target.

## 2. Project Structure

```
.
├── app.py                 # Hello World FastAPI app (GET /hello)
├── main.py                # Todo API entry-point (includes router)
├── routes.py              # Todo CRUD route handlers
├── models.py              # Pydantic request/response schemas
├── storage.py             # In-memory dict-backed todo store
├── requirements.txt       # Pinned Python dependencies
├── Dockerfile             # Container image for the API
├── docker-compose.yml     # Single-command startup
├── conftest.py            # Root pytest configuration
├── tests/
│   ├── __init__.py
│   └── test_hello.py      # Tests for GET /hello
├── healthcheck/           # SQLite-backed variant (legacy)
├── ARCHITECTURE.md         # This file
└── RUNNING.md             # How to run & test locally
```

## 3. Endpoint Contract — Hello World

| Method | Path     | Status | Body                            | Content-Type     |
|--------|----------|--------|---------------------------------|------------------|
| GET    | `/hello` | 200    | `{"message": "hello world"}` | application/json |

Any non-GET method returns **405 Method Not Allowed**.  
Unknown paths return **404 Not Found**.

## 4. Tech Stack

| Component   | Version constraint |
|-------------|--------------------|
| Python      | 3.12+              |
| FastAPI     | >=0.115, <1        |
| Uvicorn     | >=0.34, <1         |
| httpx       | >=0.28, <1         |
| pytest      | >=8, <9            |
| Pydantic    | >=2.0              |

## 5. Running Locally

```bash
pip install -r requirements.txt
uvicorn app:app --host 0.0.0.0 --port 8000
curl http://localhost:8000/hello
```

## 6. Testing

```bash
pytest tests/
```

Tests use `starlette.testclient.TestClient` (bundled with FastAPI/httpx)
to exercise:

* `GET /hello` returns 200 with `{"message": "hello world"}`
* Response Content-Type is `application/json`
* Non-GET methods return 405
* Unknown routes return 404
