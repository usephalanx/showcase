# Running the Todo API

## Prerequisites

- Python 3.10 or later
- `pip` package manager

## Install dependencies

Install all required packages from the pinned `requirements.txt`:

```bash
pip install -r requirements.txt
```

This installs FastAPI, Uvicorn, Pydantic, httpx, pytest, and pytest-timeout.

## Start the server

Launch the application with Uvicorn's auto-reload mode for development:

```bash
uvicorn main:app --reload
```

By default the server binds to `http://127.0.0.1:8000`.

To listen on all interfaces and/or a custom port:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at <http://localhost:8000>.

Interactive Swagger docs are served at <http://localhost:8000/docs>.

## Verify the server is running

```bash
curl http://localhost:8000/
```

Expected response:

```json
{"message": "Welcome to the Todo API"}
```

## Run the tests

```bash
pytest tests/
```

For verbose output:

```bash
pytest tests/ -v
```
