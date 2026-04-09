# Running the Application

## Prerequisites

- Python 3.10 or later **or** Docker / Docker Compose

---

## Option 1 — Run locally with Python

### Install dependencies

```bash
pip install -r requirements.txt
```

### Start the server

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

The API will be available at <http://localhost:8000>.

Interactive docs are served at <http://localhost:8000/docs>.

### Run the tests

```bash
pytest tests/ -v
```

---

## Option 2 — Run with Docker Compose

### Build and start

```bash
docker compose up --build
```

### Verify

Open <http://localhost:8000> in a browser.  
Expected response:

```json
{"message": "hello"}
```

### Run the tests inside the container

```bash
docker compose exec api pytest tests/ -v
```

### Stop

```bash
docker compose down
```
