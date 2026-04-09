# Running the Hello API

## Prerequisites

- **Python 3.12+** (for local execution), or
- **Docker** and **Docker Compose** (for containerised execution).

---

## Option 1 — Run Locally

```bash
# 1. Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate   # Linux / macOS
# .venv\Scripts\activate    # Windows

# 2. Install dependencies
pip install -r requirements.txt

# 3. Start the server
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

Open <http://localhost:8000> in your browser — you should see:

```json
{"message": "hello"}
```

Interactive API docs are available at <http://localhost:8000/docs>.

---

## Option 2 — Run with Docker Compose

```bash
docker compose up --build
```

The API will be available at <http://localhost:8000>.

---

## Running Tests

```bash
# Make sure dependencies are installed (see step 2 above)
pytest tests/ -v
```
