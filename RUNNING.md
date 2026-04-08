# Running the Todo API

## Prerequisites

- Python 3.10 or later
- pip (Python package manager)
- (Optional) Docker & Docker Compose

---

## Option 1 — Local Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the Server

```bash
uvicorn app.main:app --reload
```

The API is available at **http://localhost:8000**.

Interactive API documentation (Swagger UI) is at **http://localhost:8000/docs**.

Alternative ReDoc documentation is at **http://localhost:8000/redoc**.

### 3. Seed Sample Data

To populate the database with sample todo items for quick testing:

```bash
python seed_data.py
```

This inserts several example todos so you can immediately exercise the
API without manually creating items first.  Run it **after** the server
has started at least once (so the database tables exist), or the script
will create the tables itself.

### 4. Run Tests

```bash
pytest -v
```

---

## Option 2 — Docker

### 1. Build & Start

```bash
docker compose up --build
```

The API is available at **http://localhost:8000**.

Interactive API documentation (Swagger UI) is at **http://localhost:8000/docs**.

### 2. Run Tests (inside the container)

```bash
docker compose exec app pytest -v
```

---

## Notes

- **No authentication** is required — this is a public Todo API.
- The database is **SQLite in-memory** — all data is lost when the
  process restarts.
- CORS is configured to allow all origins (`*`) for development
  convenience.
- The seed script connects to the same in-memory database **only when
  run inside the same process** (e.g., during tests).  When running
  against a live server, use the API endpoints or switch to a
  file-based SQLite URL.
