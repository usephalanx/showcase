# Setup Instructions

## Install Dependencies

```bash
pip install -r requirements.txt
```

## Run Tests

```bash
pytest tests/ -v
```

## Run the Application

```bash
uvicorn app:app --host 0.0.0.0 --port 8000
```
