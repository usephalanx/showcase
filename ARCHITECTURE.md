# Architecture — Hello World API

## 1. Overview

A single-endpoint Hello World REST API built with FastAPI.
The sole purpose of the service is to respond to `GET /hello` with a
JSON body `{"message": "hello world"}`.

## 2. Project Structure

```
.
├── app.py                 # FastAPI application & /hello endpoint
├── requirements.txt       # Python dependencies
├── conftest.py            # Root pytest configuration
├── Dockerfile             # Container image definition
├── docker-compose.yml     # Single-command startup
├── RUNNING.md             # How to run & test the project
├── ARCHITECTURE.md        # This file
└── tests/
    ├── __init__.py        # Package marker
    └── test_hello.py      # Endpoint tests
```

## 3. Endpoint Contract

| Method | Path     | Status | Content-Type       | Body                              |
|--------|----------|--------|--------------------|-----------------------------------|
| GET    | `/hello` | 200    | `application/json` | `{"message": "hello world"}`   |

Any other HTTP method against `/hello` returns **405 Method Not Allowed**.
Unknown routes return **404 Not Found**.

## 4. Tech Stack

| Component   | Version Constraint | Purpose                     |
|-------------|--------------------|-----------------------------||
| FastAPI     | >=0.115, <1        | Web framework               |
| Uvicorn     | >=0.34, <1         | ASGI server                 |
| httpx       | >=0.28, <1         | Test-time HTTP client        |
| pytest      | >=8, <9            | Test runner                 |
| Python      | >=3.10             | Runtime                     |

## 5. Running Locally

```bash
pip install -r requirements.txt
uvicorn app:app --reload
curl http://localhost:8000/hello
```

See [RUNNING.md](RUNNING.md) for Docker instructions.

## 6. Testing

```bash
pytest tests/
```

Tests cover:
- `GET /hello` returns status 200 with `{"message": "hello world"}`
- Response `Content-Type` is `application/json`
- Non-GET methods to `/hello` return 405
- Unknown routes return 404
