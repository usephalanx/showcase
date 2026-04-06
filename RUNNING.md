# Running the Todo Application

This document provides **two** ways to run the application: with Docker
(recommended) or manually with local Python and Node.js installations.

---

## Option 1 — Docker (Recommended)

### Prerequisites

- [Docker](https://docs.docker.com/get-docker/) (≥ 20.10)
- [Docker Compose](https://docs.docker.com/compose/install/) (≥ 2.0)

### Quick Start

```bash
docker compose up --build
```

Once the containers are running:

| Service              | URL                          |
| -------------------- | ---------------------------- |
| **Frontend**         | http://localhost:5173         |
| **Backend API**      | http://localhost:8000         |
| **API Docs (Swagger)** | http://localhost:8000/docs |

### Stopping the Application

```bash
docker compose down
```

To also remove the database volume:

```bash
docker compose down -v
```

---

## Option 2 — Manual Local Setup

### Prerequisites

- [Python](https://www.python.org/downloads/) ≥ 3.11
- [Node.js](https://nodejs.org/) ≥ 18 (with npm)

### 1. Backend

Open a terminal in the project root directory.

#### Install dependencies

```bash
pip install -r requirements.txt
```

> If a `requirements.txt` does not yet exist, install the packages
> directly:
>
> ```bash
> pip install fastapi uvicorn sqlalchemy pydantic
> ```

#### Run the API server

```bash
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

The backend will be available at:

| Endpoint             | URL                          |
| -------------------- | ---------------------------- |
| **REST API**         | http://localhost:8000/api     |
| **Swagger UI**       | http://localhost:8000/docs    |
| **ReDoc**            | http://localhost:8000/redoc   |

#### Seed the database (optional)

Populate the database with 5 sample tasks covering every status
(`todo`, `in-progress`, `done`) and a variety of due dates:

```bash
python -m backend.seed
```

You can run this command at any time — it will create the tables if they
don't already exist and then insert the sample rows.

### 2. Frontend

Open a **second** terminal in the `frontend/` directory.

#### Install dependencies

```bash
cd frontend
npm install
```

#### Start the development server

```bash
npm run dev
```

The frontend dev server (Vite) will be available at:

| Service      | URL                  |
| ------------ | -------------------- |
| **Frontend** | http://localhost:5173 |

Vite is configured to proxy API requests to the backend at
`http://localhost:8000`.

---

## Summary of URLs

| Service              | URL                          |
| -------------------- | ---------------------------- |
| **Frontend**         | http://localhost:5173         |
| **Backend API**      | http://localhost:8000/api     |
| **Swagger UI**       | http://localhost:8000/docs    |
| **ReDoc**            | http://localhost:8000/redoc   |
