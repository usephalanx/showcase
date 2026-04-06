# Running the Kanban Board Application

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/) and [Docker Compose](https://docs.docker.com/compose/install/) installed.
- Alternatively, for local development: Node.js 18+ and Python 3.11+.

---

## Quick Start (Docker Compose)

```bash
# 1. Clone the repository
git clone <repository-url>
cd <repository-name>

# 2. Start all services
docker compose up --build

# 3. Open in browser
# Frontend: http://localhost:5173
# Backend API: http://localhost:8000/api
```

## Local Development (Without Docker)

### Frontend

```bash
cd frontend
npm install
npm run dev
```

The frontend dev server starts at `http://localhost:5173` with API proxy to `http://localhost:8000`.

### Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -e ".[dev]"
uvicorn app.main:app --reload --port 8000
```

The backend API starts at `http://localhost:8000`.

---

## Project Status

> **Note:** This project is in the initial setup phase. The architecture is defined in [ARCHITECTURE.md](./ARCHITECTURE.md). Application features are being implemented incrementally.

---

## URLs

| Service   | URL                          |
|-----------|------------------------------|
| Frontend  | http://localhost:5173        |
| API       | http://localhost:8000/api    |
| API Docs  | http://localhost:8000/docs   |
