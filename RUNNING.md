# Running the Todo Application

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/) (v20+ recommended)
- [Docker Compose](https://docs.docker.com/compose/install/) (v2+ recommended)

## Quick Start

```bash
docker compose up --build
```

This single command builds and starts both the backend and frontend services.

- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API Docs (Swagger)**: http://localhost:8000/docs
- **API Docs (ReDoc)**: http://localhost:8000/redoc

## Stopping the Application

```bash
docker compose down
```

This stops and removes all containers. The SQLite database file (`todo.db`)
persists in the backend volume between restarts.

## Manual Setup (without Docker)

### Backend

```bash
cd backend
pip install fastapi uvicorn sqlalchemy pydantic
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```
