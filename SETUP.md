# Setup Instructions

## Prerequisites

- Python 3.10+
- pip

## Installation

```bash
cd backend
pip install fastapi uvicorn sqlalchemy python-slugify pydantic
pip install pytest httpx  # for testing
```

## Running the Application

```bash
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## Running Tests

```bash
# From the project root
python -m pytest tests/ -v
```

## Database Migrations

```bash
cd backend
alembic revision --autogenerate -m "description"
alembic upgrade head
```

## Auto-generated Files (Do Not Commit)

- `__pycache__/`
- `*.egg-info/`
- `.venv/`
- `poetry.lock`
- `Pipfile.lock`
- `kanban.db` (SQLite database file)
