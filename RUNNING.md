# Running the Todo API

## Quick Start (Docker)

```bash
git clone <repository-url>
cd <repository-directory>
docker compose up --build
```

The API will be available at **http://localhost:8000**.

## API Documentation

FastAPI auto-generates interactive API docs:

- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

## Running Without Docker

### Prerequisites

- Python 3.11+
- pip

### Install Dependencies

```bash
pip install fastapi uvicorn pydantic
```

### Start the Server

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## Running Tests

```bash
pip install pytest httpx
pytest tests/ -v
```

## Health Check

```bash
curl http://localhost:8000/health
# {"status": "ok"}
```
