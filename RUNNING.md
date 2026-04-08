# Running the Todo API

## Prerequisites

- Python 3.10 or later

## Install dependencies

```bash
pip install fastapi uvicorn pydantic
```

For running the test suite you will also need:

```bash
pip install httpx pytest
```

## Start the server

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at <http://localhost:8000>.

Interactive docs are served at <http://localhost:8000/docs>.

## Run the tests

```bash
pytest tests/
```
