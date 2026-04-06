# Running the Todo Application

This guide explains how to set up and run both the backend and frontend of the Todo application locally.

---

## Prerequisites

- **Python 3.10+** with `pip`
- **Node.js 18+** with `npm`

---

## 1. Backend Setup

All commands below are run from the **repository root**.

### Install Python dependencies

```bash
pip install fastapi uvicorn sqlalchemy pydantic
```

### Seed the database with sample data (optional)

This inserts 5 demo tasks with varied statuses and due dates:

```bash
python seed.py
```

You can run the seed script multiple times — it will add new rows each time.
To start fresh, delete `todos.db` before seeding:

```bash
rm -f todos.db
python seed.py
```

### Start the backend server

```bash
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

The API will be available at **http://127.0.0.1:8000**.

- Interactive API docs (Swagger UI): **http://127.0.0.1:8000/docs**
- Alternative API docs (ReDoc): **http://127.0.0.1:8000/redoc**

---

## 2. Frontend Setup

Open a **new terminal** and navigate to the `frontend/` directory:

```bash
cd frontend
```

### Install Node.js dependencies

```bash
npm install
```

### Start the development server

```bash
npm run dev
```

The frontend will be available at **http://localhost:5173** (default Vite port).

---

## 3. Accessing the Application

| Component | URL                          |
| --------- | ---------------------------- |
| Frontend  | http://localhost:5173        |
| Backend   | http://127.0.0.1:8000       |
| API Docs  | http://127.0.0.1:8000/docs  |

The frontend communicates with the backend API at `http://127.0.0.1:8000`.
CORS is pre-configured to allow requests from `http://localhost:5173`.

---

## 4. API Endpoints Quick Reference

| Method | Endpoint              | Description                     |
| ------ | --------------------- | ------------------------------- |
| GET    | `/tasks`              | List all tasks (optional `?status=` filter) |
| POST   | `/tasks`              | Create a new task               |
| GET    | `/tasks/{task_id}`    | Retrieve a single task          |
| PUT    | `/tasks/{task_id}`    | Update a task                   |
| DELETE | `/tasks/{task_id}`    | Delete a task                   |

---

## 5. Troubleshooting

- **Port already in use**: Change the backend port with `--port 8001`, or the frontend port in `frontend/vite.config.ts`.
- **CORS errors**: Ensure the backend is running on port 8000 and the frontend on port 5173. If you change ports, update the `allow_origins` list in `app/main.py`.
- **Database issues**: Delete `todos.db` and restart the backend — tables are auto-created on startup.
