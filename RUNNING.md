# Running the Todo API

## Prerequisites

- Python 3.10 or later

## Install dependencies

```bash
pip install -r requirements.txt
```

For running the test suite you will also need:

```bash
pip install httpx pytest
```

## Start the server

```bash
uvicorn main:app --reload
```

By default the server binds to `127.0.0.1:8000`. You can customise the
host and port:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Alternatively, run the application directly with Python:

```bash
python main.py
```

The API will be available at <http://localhost:8000>.

Interactive docs are served at <http://localhost:8000/docs>.

## API Endpoints

| Method | Path              | Description           |
|--------|-------------------|-----------------------|
| GET    | `/`               | Health / welcome page |
| POST   | `/todos`          | Create a new todo     |
| GET    | `/todos`          | List all todos        |
| GET    | `/todos/{todo_id}`| Get a single todo     |
| PUT    | `/todos/{todo_id}`| Update a todo         |
| DELETE | `/todos/{todo_id}`| Delete a todo         |

## Run the tests

```bash
pytest tests/
```
