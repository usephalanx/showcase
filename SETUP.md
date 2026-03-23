# Setup Instructions

## Prerequisites

- Python 3.11+

## Backend Setup

```bash
cd backend

# Create a virtual environment
python -m venv .venv
source .venv/bin/activate   # Linux/macOS
# .venv\Scripts\activate    # Windows

# Install dependencies
pip install -r requirements.txt

# Initialise the database (creates app.db with all tables)
python init_db.py

# Run the development server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## Running Tests

```bash
cd backend
pip install pytest httpx
pytest tests/ -v
```

## Auto-generated files (do NOT commit)

- `backend/.venv/`
- `backend/__pycache__/`
- `backend/*.egg-info/`
- `backend/app.db`
