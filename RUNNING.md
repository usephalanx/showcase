# Running the Todo Application

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/) (≥ 20.10)
- [Docker Compose](https://docs.docker.com/compose/install/) (≥ 2.0)

## Quick Start

```bash
docker compose up --build
```

Once the containers are running:

| Service | URL |
|---------|-----|
| **Frontend** | http://localhost:5173 |
| **Backend API** | http://localhost:8000 |
| **API Docs (Swagger)** | http://localhost:8000/docs |

## Stopping the Application

```bash
docker compose down
```

To also remove the database volume:

```bash
docker compose down -v
```
