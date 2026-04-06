# Setup Guide

## Prerequisites

- Python 3.11+
- pip

## Installation

```bash
cd backend
pip install -r requirements.txt
```

## Running the Application

```bash
cd backend
uvicorn main:app --reload
```

## Running Tests

```bash
cd backend
python -m pytest tests/ -v
```

## Running Migrations

```bash
cd backend
alembic revision --autogenerate -m "description"
alembic upgrade head
```

## Environment Variables

| Variable | Default | Description |
|---|---|---|
| `DATABASE_URL` | `sqlite:///kanban.db` | SQLAlchemy database URL |
| `SITE_BASE_URL` | `https://example.com` | Base URL for canonical links |
| `SITE_NAME` | `Kanban Board` | Site name appended to page titles |
