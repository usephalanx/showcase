# Running the Kanban Application

## Prerequisites

- Python 3.11+
- pip

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## Access

- **API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

## Running Tests

```bash
python -m pytest tests/ -v
```

## Database

The application uses SQLite. The database file (`kanban.db`) is created
automatically on first startup. For testing, an in-memory SQLite database
is used.
