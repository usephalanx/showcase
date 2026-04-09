# Running the Todo API

## Prerequisites

- Python 3.10 or later
- `pip` (Python package installer)

## Install Dependencies

Install all project dependencies from the `requirements.txt` file:

```bash
pip install -r requirements.txt
```

This will install:

- **FastAPI** — the async web framework powering the API
- **Uvicorn** — the ASGI server used to run the application
- **Pydantic** — data validation and serialization
- **httpx** — HTTP client used by the test suite
- **pytest** — test runner
- **pytest-timeout** — timeout support for tests

## Start the Server

Run the application with Uvicorn:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at <http://localhost:8000>.

Interactive API docs (Swagger UI) are served at <http://localhost:8000/docs>.

Alternative ReDoc documentation is available at <http://localhost:8000/redoc>.

## Run the Tests

Execute the full test suite with pytest:

```bash
pytest tests/
```

To run tests with verbose output:

```bash
pytest tests/ -v
```

## Docker (Optional)

If you prefer to run the application in a container:

```bash
docker compose up --build
```

This will build the image and start the server on port 8000.
