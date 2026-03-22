# Task Manager

A lightweight task management application with a **FastAPI** backend and a
**vanilla JavaScript** single-page frontend.

---

## Architecture

```
├── backend/
│   ├── __init__.py          # Package marker
│   ├── database.py          # SQLAlchemy engine, session, schema init
│   ├── models.py            # ORM model (Task)
│   ├── schemas.py           # Pydantic request/response schemas
│   └── main.py              # FastAPI app, CORS config, route handlers
├── frontend/
│   ├── index.html           # SPA entry point
│   ├── style.css            # Application styles
│   └── app.js               # Client-side JS (fetch API)
├── tests/
│   ├── __init__.py          # Test package marker
│   ├── test_api.py          # Backend API integration tests
│   └── test_frontend.py     # Frontend file structure tests
├── requirements.txt         # Python dependencies
└── README.md                # This file
```

---

## Database Schema

SQLite via SQLAlchemy ORM.

| Column       | Type     | Constraints                                |
|-------------|----------|--------------------------------------------|
| id          | INTEGER  | PRIMARY KEY AUTOINCREMENT                  |
| title       | TEXT     | NOT NULL                                   |
| description | TEXT     | NOT NULL, DEFAULT ''                       |
| status      | TEXT     | NOT NULL, DEFAULT 'pending'                |
| created_at  | DATETIME | NOT NULL, DEFAULT now (UTC)                |

Valid `status` values: `pending`, `done`.

---

## API Endpoints

### `GET /tasks`

Returns all tasks ordered by `created_at` descending.

**Response** `200 OK`:
```json
[
  {
    "id": 1,
    "title": "Buy groceries",
    "description": "Milk, eggs, bread",
    "status": "pending",
    "created_at": "2024-01-15T10:30:00"
  }
]
```

### `POST /tasks`

Create a new task.

**Request body**:
```json
{
  "title": "Buy groceries",
  "description": "Milk, eggs, bread"
}
```

**Response** `201 Created`:
```json
{
  "id": 1,
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "status": "pending",
  "created_at": "2024-01-15T10:30:00"
}
```

### `PATCH /tasks/{id}`

Update the status of an existing task.

**Request body**:
```json
{
  "status": "done"
}
```

**Response** `200 OK`:
```json
{
  "id": 1,
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "status": "done",
  "created_at": "2024-01-15T10:30:00"
}
```

**Response** `404 Not Found`:
```json
{
  "detail": "Task not found"
}
```

---

## CORS Configuration

The backend allows all origins (`*`) for local development convenience.

---

## Developer Setup

### Backend

```bash
# Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the API server
uvicorn backend.main:app --reload
```

The API will be available at `http://localhost:8000`.

### Frontend

Serve the `frontend/` directory with any static file server:

```bash
# Using Python's built-in server
cd frontend
python -m http.server 5500
```

Then open `http://localhost:5500` in your browser.

The frontend defaults to `http://localhost:8000` as the API base URL.
Override it by setting `window.TASK_API_BASE_URL` before `app.js` loads.

### Tests

```bash
pytest -v
```

Backend tests use `httpx` with FastAPI's `TestClient`. Frontend tests
validate file structure and content.
