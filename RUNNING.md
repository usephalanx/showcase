# Running the Hello World API

## Prerequisites

- Python 3.10 or later
- pip (Python package manager)
- Docker and Docker Compose (optional, for containerised execution)

## Install dependencies

```bash
pip install -r requirements.txt
```

This installs FastAPI, Uvicorn, and all testing dependencies.

## Start the server

### Option 1 — Run directly with Uvicorn

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at <http://localhost:8000>.

Interactive docs are served at <http://localhost:8000/docs>.

### Option 2 — Run with Docker Compose

```bash
docker compose up --build
```

The API will be available at <http://localhost:8000>.

To stop the container:

```bash
docker compose down
```

### Option 3 — Run with plain Docker

```bash
docker build -t hello-world-api .
docker run -p 8000:8000 hello-world-api
```

## Verify the server is running

```bash
# Health check
curl http://localhost:8000/

# Hello endpoint
curl http://localhost:8000/hello
```

## Run the tests

```bash
pytest tests/ -v
```

## API Endpoints

| Method | Path     | Description                          | Response                        |
|--------|----------|--------------------------------------|---------------------------------|
| GET    | `/`      | Health check                         | `{"status": "ok"}`              |
| GET    | `/hello` | Returns a hello-world greeting       | `{"message": "hello-world"}`    |
