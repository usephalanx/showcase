# Setup Instructions

## Prerequisites

- Python 3.10 or later

## Install Dependencies

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Run the Server

```bash
uvicorn main:app --reload
```

The API will be available at http://127.0.0.1:8000.
Interactive docs at http://127.0.0.1:8000/docs.

## Run Tests

```bash
pytest tests/ -v
```
