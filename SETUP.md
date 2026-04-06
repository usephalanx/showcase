# Setup Instructions

## Prerequisites

- Python 3.11+
- pip

## Installation

```bash
cd backend
pip install fastapi uvicorn sqlalchemy python-slugify pydantic alembic
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
alembic upgrade head
```

## Environment Variables

| Variable       | Default              | Description          |
|---------------|----------------------|----------------------|
| DATABASE_URL  | sqlite:///kanban.db  | Database connection  |
