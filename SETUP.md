# Setup

## Prerequisites

- Python 3.10+
- pip

## Installation

```bash
# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install fastapi uvicorn sqlalchemy pydantic pytest
```

## Running Tests

```bash
pytest tests/ -v
```

## Running the Application

```bash
uvicorn backend.app.main:app --reload
```

## Generated Files (do not commit)

- `.venv/`
- `__pycache__/`
- `*.egg-info/`
- `poetry.lock` / `Pipfile.lock`
- `app.db` (SQLite database file)
