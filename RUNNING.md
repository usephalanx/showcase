# Running the Application

## TEAM_BRIEF
stack: Python/FastAPI
test_runner: pytest tests/
lint_tool: ruff check .
coverage_tool: pytest-cov
coverage_threshold: 70
coverage_applies: true

---

## Prerequisites

- **Docker** and **Docker Compose** installed, **or**
- **Python 3.11+** available locally.

---

## Option 1 — Docker (recommended)

### Start the application

```bash
docker compose up --build
```

The API will be available at **http://localhost:8000**.

### Verify it works

Open a browser or run:

```bash
curl http://localhost:8000/health
```

Expected response:

```json
{"status": "ok"}
```

### Run the tests inside the container

```bash
docker compose exec api pytest tests/ -v
```

### Stop the application

```bash
docker compose down
```

---

## Option 2 — Local Python

### Install dependencies

```bash
pip install -r requirements.txt
```

### Start the server

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

### Run the tests

```bash
pytest tests/ -v
```

---

## Useful endpoints

| Method | Path           | Description             |
|--------|----------------|-------------------------|
| GET    | `/`            | Welcome message         |
| GET    | `/health`      | Health check            |
| GET    | `/todos`       | List all todos          |
| POST   | `/todos`       | Create a new todo       |
| GET    | `/todos/{id}`  | Retrieve a single todo  |
| PUT    | `/todos/{id}`  | Update a todo           |
| DELETE | `/todos/{id}`  | Delete a todo           |
