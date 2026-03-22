# Setup Instructions

## Install Dependencies

```bash
pip install -r requirements.txt
```

## Run the Application

```bash
uvicorn backend.main:app --reload
```

The server starts at `http://127.0.0.1:8000`.
API documentation is available at `http://127.0.0.1:8000/docs`.

## Run Tests

```bash
pytest tests/ -v
```

## Notes

- The SQLite database file `tasks.db` is created automatically on first
  startup in the current working directory.
- A separate `test_tasks.db` is used during test runs and is torn down
  after each test.
