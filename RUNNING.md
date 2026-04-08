# Running the Todo API

## Quick Start (Docker)

```bash
docker compose up --build
```

The API is available at **http://localhost:8000**.

Interactive API documentation (Swagger UI) is at **http://localhost:8000/docs**.

## Running Tests

```bash
docker compose exec app pytest -v
```

Or locally (with a virtual environment):

```bash
pip install -r requirements.txt
pytest -v
```

## Notes

- **No authentication** is required — this is a public Todo API.
- The database is **SQLite in-memory** — all data is lost when the
  process restarts.
- CORS is configured to allow all origins (`*`) for development
  convenience.
