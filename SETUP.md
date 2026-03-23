# TaskBoard API — Setup

## Prerequisites

- Python 3.11+

## Installation

```bash
python -m venv .venv
source .venv/bin/activate   # Linux/macOS
# .venv\Scripts\activate    # Windows

pip install -r requirements.txt
```

## Running the Application

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API docs are available at http://localhost:8000/docs

## Running Tests

```bash
pytest tests/ -v
```

## Database

SQLite database file `taskboard.db` is created automatically on first startup.
For tests, a separate `test_taskboard.db` file is used and is rebuilt for each test.
