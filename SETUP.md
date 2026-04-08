# Setup Instructions

## Prerequisites

- Python 3.10+

## Install dependencies

```bash
python -m pip install -r requirements.txt
```

## Run the application

```bash
python main.py
```

Or with uvicorn directly:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

## Run tests

```bash
python -m pytest tests/ -v
```

## API documentation

Once running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
