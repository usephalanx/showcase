# Hello World FastAPI

A minimal FastAPI application with a `/hello` endpoint and full test coverage.

## Setup

```bash
pip install -r requirements.txt
```

## Run the app

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## Run tests

```bash
pytest tests/ -v
```

## Run tests with coverage

```bash
pytest tests/ --cov=app --cov-report=term-missing --cov-fail-under=70
```

## Docker

```bash
docker compose up --build
```
