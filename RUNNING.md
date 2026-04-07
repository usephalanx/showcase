# Running the Todo API

This document explains how to install dependencies and run the
Todo API application locally.

## Prerequisites

- Python 3.10 or later
- `pip` (bundled with Python)

## 1. Install dependencies

```bash
pip install -r requirements.txt
```

## 2. Run the application

You can start the server in either of two ways:

### Option A — Using the convenience entry point

```bash
python main.py
```

This starts Uvicorn on **http://127.0.0.1:8000** with auto-reload
enabled.

### Option B — Using Uvicorn directly

```bash
uvicorn app.main:app --reload
```

## 3. Explore the API

Once the server is running you can:

- Open the interactive docs at **http://127.0.0.1:8000/docs**
- Open the alternative docs at **http://127.0.0.1:8000/redoc**
- List all todos: `GET /todos`
- Get a single todo: `GET /todos/{id}`
- Create a todo: `POST /todos`
- Update a todo: `PUT /todos/{id}`
- Delete a todo: `DELETE /todos/{id}`

## 4. Seed data

The application ships with a few example todos so the demo is not
empty on first launch.  These are loaded into in-memory storage when
the module is imported and will reset every time the server restarts.

## 5. Running the tests

```bash
python -m pytest tests/ -v
```
