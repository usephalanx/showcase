# Running the Echo API

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/) (v20 or later)
- [Docker Compose](https://docs.docker.com/compose/install/) (v2 or later — included with Docker Desktop)

## Quick Start

```bash
# 1. Clone the repository and enter the directory
git clone <repo-url>
cd <repo-directory>

# 2. Build and start the service
docker compose up --build
```

The API is now available at **http://localhost:8000**.

## Interactive Documentation

Open **http://localhost:8000/docs** in your browser to access the
auto-generated Swagger UI where you can try every endpoint.

## Example Usage

### Health check

```bash
curl http://localhost:8000/
```

Expected response:
```json
{"status": "ok"}
```

### Echo

```bash
curl -X POST http://localhost:8000/echo \
  -H 'Content-Type: application/json' \
  -d '{"hello": "world"}'
```

Expected response:
```json
{"hello": "world"}
```

## Running Tests

```bash
# Via Docker
docker compose run --rm echo-api pytest -v

# Or locally (requires Python 3.12+)
pip install -r requirements.txt
pytest -v
```

## Stopping the Service

```bash
docker compose down
```
