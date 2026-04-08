# Running the Todo App

## Quick Start (Docker)

```bash
# 1. Build and start the application
docker compose up --build

# 2. The API is now available at:
#    http://localhost:8000

# 3. Interactive API documentation (Swagger UI):
#    http://localhost:8000/docs
```

## Running Tests

```bash
# Run the full test suite inside the running container
docker compose exec app pytest -v
```

## Running Locally (without Docker)

```bash
# 1. Create a virtual environment
python -m venv .venv
source .venv/bin/activate   # Linux / macOS
# .venv\Scripts\activate    # Windows

# 2. Install dependencies
pip install -r requirements.txt

# 3. Start the development server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# 4. Run tests
pytest -v
```

## Notes

- **No authentication** is required — this is a public Todo API.
- The database is **SQLite in-memory** so all data is lost on restart.
- API docs are auto-generated at `/docs` (Swagger) and `/redoc` (ReDoc).
