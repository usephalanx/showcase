# Hello World FastAPI Application

A minimal FastAPI application with a single `/hello` endpoint.

## Setup

### Local Development

```bash
pip install -r requirements.txt
```

### Running the Application

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### Running with Docker

```bash
docker compose up --build
```

The API will be available at `http://localhost:8000`.

## Endpoints

| Method | Path     | Description                          |
|--------|----------|--------------------------------------|
| GET    | `/hello` | Returns `{"message": "Hello, World!"}` |

## Running Tests

```bash
pytest tests/ -v
```

### With Coverage

```bash
pytest tests/ --cov=app --cov-report=term-missing
```

Coverage threshold: **70%**
