# Backend Setup

## Prerequisites

- Python 3.11+
- pip

## Installation

```bash
cd backend
python -m venv .venv
source .venv/bin/activate   # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Environment Variables

| Variable | Default | Description |
|---|---|---|
| `AUTH_SECRET_KEY` | `change-me-in-production-use-a-long-random-string` | JWT signing secret |
| `AUTH_ALGORITHM` | `HS256` | JWT algorithm |
| `AUTH_ACCESS_TOKEN_EXPIRE_MINUTES` | `30` | Token expiry in minutes |
| `DATABASE_URL` | `sqlite:///./app.db` | SQLAlchemy database URL |

## Initialize Database

```bash
python init_db.py
```

## Run Server

```bash
uvicorn app.main:app --reload
```

## Run Tests

```bash
pytest tests/ -v
```
