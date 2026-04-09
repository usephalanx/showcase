# Architecture

## 1. Overview

A minimal single-endpoint Hello World API built with FastAPI.
The sole purpose is to serve `GET /hello` and return a JSON greeting.

## 2. Project Structure

```
.
├── app.py                 # FastAPI application with GET /hello
├── conftest.py            # Root pytest configuration
├── requirements.txt       # Python dependencies
├── Dockerfile             # Container image definition
├── docker-compose.yml     # Docker Compose orchestration
├── RUNNING.md             # Run & test instructions
├── ARCHITECTURE.md        # This file
└── tests/
    ├── __init__.py        # Package marker
    └── test_hello.py      # Endpoint tests
```

## 3. Endpoint Contract

| Method | Path     | Status | Response Body                  | Content-Type     |
|--------|----------|--------|--------------------------------|------------------|
| GET    | `/hello` | 200    | `{"message": "hello world"}` | application/json |

Any other method on `/hello` returns **405 Method Not Allowed**.
Unknown paths return **404 Not Found**.

## 4. Tech Stack

| Component  | Version      |
|------------|--------------|
| FastAPI    | >= 0.115, <1 |
| Uvicorn    | >= 0.34, <1  |
| httpx      | >= 0.28, <1  |
| pytest     | >= 8, <9     |
| Python     | 3.12+        |

## 5. Running Locally

```bash
pip install -r requirements.txt
uvicorn app:app --reload
curl http://localhost:8000/hello
```

## 6. Testing

```bash
pytest tests/
```

Tests cover:
- `GET /hello` returns 200 with correct JSON body
- Response Content-Type is `application/json`
- Response body has exactly one key (`message`)
- `POST`, `PUT`, `DELETE` on `/hello` return 405
- Unknown route returns 404
