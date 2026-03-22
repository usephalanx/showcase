# Setup

## Install Dependencies

```bash
pip install -r requirements.txt
```

For running tests you also need `pytest` and `httpx` (required by FastAPI's `TestClient`):

```bash
pip install pytest httpx
```

## Run the Application

```bash
uvicorn main:app --reload
```

## Run the Tests

```bash
pytest tests/ -v
```
