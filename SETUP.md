# Setup Instructions

## Prerequisites

- Python 3.10+
- pip

## Install Dependencies

```bash
pip install fastapi uvicorn pydantic httpx starlette pytest
```

## Run Tests

```bash
# Run all tests
pytest tests/ -v

# Run only the Hello endpoint tests
pytest tests/test_hello.py -v
```

## Run the Application

```bash
uvicorn main:app --reload
```

Then visit:
- Root: http://127.0.0.1:8000/
- Hello: http://127.0.0.1:8000/hello
- Hello with name: http://127.0.0.1:8000/hello?name=Alice
- API docs: http://127.0.0.1:8000/docs
