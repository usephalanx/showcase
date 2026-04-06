# Setup

## Prerequisites

- Python 3.11+
- pip

## Install Dependencies

```bash
pip install -r backend/requirements.txt
```

## Run the Application

```bash
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

## Run Tests

```bash
pip install pytest httpx
pytest tests/ -v
```
