# Hello World FastAPI Application

A minimal FastAPI application with a `/hello` endpoint.

## Setup

```bash
pip install -r requirements.txt
```

## Running the Application

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

Or with Docker:

```bash
docker compose up --build
```

## Running Tests

```bash
pytest tests/ -v
```

### With Coverage

```bash
pytest tests/ --cov=app --cov-report=term-missing
```

Coverage threshold target: **70%**
