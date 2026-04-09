# Running the Hello World API

## TEAM_BRIEF
stack: Python/FastAPI
test_runner: pytest tests/
lint_tool: ruff check .
coverage_tool: pytest-cov
coverage_threshold: 70
coverage_applies: true

## Project Overview

A minimal Hello World API built with **FastAPI**. It exposes a single
endpoint that returns a JSON greeting:

| Method | Path     | Response                        | Status |
|--------|----------|---------------------------------|--------|
| GET    | `/hello` | `{"message": "hello world"}` | 200    |

## Prerequisites

- **Python 3.10+** (3.12 recommended) **or** Docker

## Install Dependencies

```bash
pip install -r requirements.txt
```

## Running the Server

### Without Docker

```bash
uvicorn app:app --reload
```

Then visit: <http://localhost:8000/hello>

### With Docker

```bash
docker compose up --build
```

Then visit: <http://localhost:8000/hello>

## Running Tests

### Without Docker

```bash
pip install -r requirements.txt
pytest tests/
```

### With Docker

```bash
docker compose exec api pytest tests/
```

## Verifying the Endpoint

```bash
curl http://localhost:8000/hello
# Expected: {"message":"hello world"}
```

## Endpoint Documentation

### GET /hello

Returns a JSON greeting.

**Request:**

```
GET /hello HTTP/1.1
Host: localhost:8000
```

**Response (200 OK):**

```json
{
  "message": "hello world"
}
```

**Content-Type:** `application/json`

**Error responses:**

| Method       | Status | Detail                |
|--------------|--------|-----------------------|
| POST /hello  | 405    | Method Not Allowed    |
| GET /notfound| 404    | Not Found             |

## No Authentication

This API has no authentication. No demo credentials are required.
