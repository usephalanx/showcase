# Running the Phalanx Kanban Board

This guide explains how to get the entire application stack running with a single command using Docker Compose.

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/) (v20.10+)
- [Docker Compose](https://docs.docker.com/compose/install/) (v2.0+ — included with Docker Desktop)

## Quick Start

### 1. Clone the repository

```bash
git clone <repository-url>
cd <repository-name>
```

### 2. Set up environment variables (optional)

Copy the example environment file and adjust values if needed:

```bash
cp .env.example .env
```

The application works out of the box with default values for development. For production, update `JWT_SECRET` to a strong random value.

| Variable | Default | Description |
|---|---|---|
| `JWT_SECRET` | `dev-secret-key-change-in-production` | Secret key for signing JWT tokens |
| `DATABASE_URL` | `sqlite:///./kanban.db` | Database connection string |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | `60` | JWT token expiry in minutes |

### 3. Build and start the stack

```bash
docker compose up --build
```

This single command will:

1. Build the **backend** Docker image (Python 3.11 + FastAPI)
2. Build the **frontend** Docker image (Node 18 build + nginx serve)
3. Start both services with proper networking
4. Automatically run database migrations and **seed demo data**

> **Note:** The first build may take a few minutes to download base images and install dependencies. Subsequent builds will be faster thanks to Docker layer caching.

### 4. Access the application

| Service | URL |
|---|---|
| **Frontend** (Web UI) | [http://localhost:3000](http://localhost:3000) |
| **Backend** (API) | [http://localhost:8000](http://localhost:8000) |
| **API Docs** (Swagger) | [http://localhost:8000/docs](http://localhost:8000/docs) |
| **Health Check** | [http://localhost:8000/health](http://localhost:8000/health) |

### 5. Log in with demo credentials

A demo account is created automatically on first startup:

| Field | Value |
|---|---|
| **Email** | `demo@phalanx.dev` |
| **Password** | `demo1234` |

The demo account comes pre-loaded with:
- A sample board ("My First Board")
- Three columns: **To Do**, **In Progress**, **Done**
- Three sample cards distributed across the columns

## Running in Detached Mode

To run the stack in the background:

```bash
docker compose up --build -d
```

View logs:

```bash
# All services
docker compose logs -f

# Backend only
docker compose logs -f backend

# Frontend only
docker compose logs -f frontend
```

## Stopping the Stack

```bash
# Stop all services (preserves data)
docker compose down

# Stop and remove all data (volumes)
docker compose down -v
```

## Full Reset

To completely reset the application (removes all data, images, and volumes):

```bash
docker compose down -v --rmi all
docker compose up --build
```

This will:
- Stop all containers
- Remove all volumes (database data)
- Remove all built images
- Rebuild everything from scratch
- Re-seed the demo data

## Architecture Overview

```
┌─────────────────┐         ┌─────────────────┐
│                  │  :3000  │                  │
│    Browser       │────────▶│   Frontend       │
│                  │         │   (nginx:80)     │
└─────────────────┘         └────────┬─────────┘
                                     │
                              /auth/ │ /boards/
                              /cards/│ /health
                                     │
                                     ▼
                            ┌─────────────────┐
                            │                  │
                            │   Backend        │
                            │   (uvicorn:8000) │
                            │                  │
                            └────────┬─────────┘
                                     │
                                     ▼
                            ┌─────────────────┐
                            │   SQLite DB      │
                            │   (kanban.db)    │
                            └─────────────────┘
```

- **Frontend** serves the React SPA via nginx on port 80 (mapped to host port 3000)
- **nginx** proxies API requests (`/auth/`, `/boards/`, `/cards/`, `/health`) to the backend
- **Backend** runs FastAPI with uvicorn on port 8000
- **SQLite** database is stored in a Docker volume for persistence
- **Seed data** runs automatically on backend startup via the FastAPI lifespan handler

## Troubleshooting

### Port already in use

If port 3000 or 8000 is already in use, stop the conflicting service or modify the port mapping in `docker-compose.yml`:

```yaml
ports:
  - "3001:80"   # Change 3000 to 3001 for frontend
  - "8001:8000"  # Change 8000 to 8001 for backend
```

### Backend not ready

The frontend container waits for the backend health check to pass before starting. If you see connection errors, wait a few seconds for the backend to fully initialize.

### Fresh database

To reset the database without rebuilding images:

```bash
docker compose down -v
docker compose up
```
