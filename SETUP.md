# Setup Instructions

## Prerequisites

- Python 3.11+
- pip

## Backend Setup

```bash
# Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the development server
cd backend
uvicorn app.main:app --reload --port 8000
```

## Running Tests

```bash
cd backend
python -m pytest tests/ -v
```

## Notes

- The SQLite database file (`tasks.db`) is auto-created on first startup.
- Do **not** commit generated files: `__pycache__/`, `*.egg-info/`, `.venv/`, `tasks.db`.
