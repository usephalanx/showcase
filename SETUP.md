# Setup Instructions

## Prerequisites

- Python 3.10+
- pip

## Install Dependencies

```bash
pip install fastapi uvicorn sqlalchemy pydantic pytest httpx
```

## Run Tests

```bash
python -m pytest tests/ -v
```

## Run the Development Server

```bash
uvicorn app.main:app --reload
```
