# Architecture

## Overview

The Echo API is a single-service FastAPI application with no database or
external dependencies.  It accepts arbitrary JSON objects and returns them
unchanged, making it useful for testing, debugging, and as a starter
template.

## Project Structure

| File / Directory        | Purpose                                              |
|-------------------------|------------------------------------------------------|
| `main.py`               | FastAPI application with `/` and `/echo` endpoints   |
| `requirements.txt`      | Pinned Python dependencies                           |
| `Dockerfile`            | Container image definition                           |
| `docker-compose.yml`    | One-command local startup                            |
| `tests/`                | Automated test suite                                 |
| `tests/test_echo.py`    | Tests for the echo and health endpoints              |
| `ARCHITECTURE.md`       | This file — high-level architecture documentation    |
| `RUNNING.md`            | Step-by-step instructions for running the service    |

## Endpoint Reference

### `GET /`

Health check endpoint.

**Response (200)**
```json
{"status": "ok"}
```

### `POST /echo`

Accepts any JSON **object** and returns it verbatim.

**Request**
```json
{"any": "json", "object": true}
```

**Response (200)**
```json
{"any": "json", "object": true}
```

**Error (422)** — returned when the body is not a valid JSON object
(e.g. array, plain text, or missing body).

## Running

See [RUNNING.md](RUNNING.md) for detailed instructions.
