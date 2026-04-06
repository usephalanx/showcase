# Running the Todo Application

This guide explains how to run the full-stack Todo application locally
using **Docker** and **Docker Compose**.

---

## Prerequisites

| Tool             | Minimum Version |
| ---------------- | --------------- |
| Docker           | 20.10+          |
| Docker Compose   | 2.0+ (V2)       |

Both are included in [Docker Desktop](https://www.docker.com/products/docker-desktop/).

---

## Quick Start

```bash
# 1. Clone the repository
git clone <repo-url>
cd <repo-directory>

# 2. Build and start all services
docker compose up --build

# 3. Open the frontend
#    http://localhost:5173
```

That's it! The application is now running:

| Service  | URL                                   |
| -------- | ------------------------------------- |
| Frontend | http://localhost:5173                 |
| Backend  | http://localhost:8000                 |
| API Docs | http://localhost:8000/docs            |

The backend runs on `http://localhost:8000` and exposes interactive
Swagger documentation at `http://localhost:8000/docs`.

---

## Stopping the Application

```bash
docker compose down
```

This stops and removes all containers created by `docker compose up`.

To also remove the persisted database volume:

```bash
docker compose down -v
```

---

## Running Without Docker

If you prefer to run services directly on your host machine, see the
**Development Workflow** section in [ARCHITECTURE.md](./ARCHITECTURE.md).
