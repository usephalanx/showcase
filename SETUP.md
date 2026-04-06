# Backend Setup

## Prerequisites

- Python 3.10+
- pip

## Installation

```bash
# Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
# .venv\Scripts\activate   # Windows

# Install dependencies
pip install -r requirements.txt
```

## Running the application

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at http://localhost:8000.

## Running tests

```bash
python -m pytest tests/ -v
```

## Notes

- The SQLite database file (`todos.db`) is created automatically on first startup.
- CORS is configured to allow requests from `http://localhost:5173` (Vite dev server).
- Do **not** commit generated files: `todos.db`, `__pycache__/`, `.venv/`, `*.egg-info/`.
