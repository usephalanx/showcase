# Architecture — Hello World API

## 1. Overview

A minimal FastAPI application exposing a single `GET /hello` endpoint that
returns `{"message": "hello world"}`.  The project serves as a lightweight
health-check target and as a starting point for further API development.

## 2. Project Structure

```
.
├── app.py                  # FastAPI application & /hello route
├── requirements.txt        # Python dependencies
├── Dockerfile              # Container image definition
├── docker-compose.yml      # Single-command startup
├── RUNNING.md              # How to run & test locally
├── ARCHITECTURE.md         # This file
├── conftest.py             # Root pytest configuration
└── tests/
    ├── __init__.py
    └── test_hello.py       # Endpoint tests
```

## 3. Endpoint Contract

| Method | Path     | Status | Response Body                  | Content-Type       |
|--------|----------|--------|--------------------------------|--------------------|
| GET    | `/hello` | 200    | `{"message": "hello world"}`   | application/json   |

All other methods on `/hello` return **405 Method Not Allowed**.  
Unknown paths return **404 Not Found**.

## 4. Tech Stack

| Component  | Version      |
|------------|--------------|
| Python     | 3.12+        |
| FastAPI    | ≥ 0.115, < 1 |
| Uvicorn    | ≥ 0.34, < 1  |
| httpx      | ≥ 0.28, < 1  |
| pytest     | ≥ 8, < 9     |

## 5. Running Locally

```bash
pip install -r requirements.txt
uvicorn app:app --reload
curl http://localhost:8000/hello
```

Or via Docker:

```bash
docker compose up --build
curl http://localhost:8000/hello
```

## 6. Testing

```bash
pytest tests/
```

The test suite covers:
- 200 response with correct JSON body
- `Content-Type: application/json` header
- 405 for non-GET methods
- 404 for unknown routes
- Response body shape validation
