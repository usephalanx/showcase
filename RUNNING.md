# Running the Todo API

## Quick Start (Docker)

```bash
git clone <repository-url>
cd <repository-directory>
docker compose up --build
```

The API will be available at **http://localhost:8000**.

Swagger documentation is at **http://localhost:8000/docs**.

## Local Development (without Docker)

### Prerequisites

- Python 3.11+
- pip

### Install Dependencies

```bash
pip install fastapi uvicorn pydantic
```

### Run the Server

```bash
uvicorn app.main:app --reload
```

### Run Tests

```bash
pip install pytest httpx
pytest tests/ -v
```

## Endpoints

| Method   | URL             | Description       |
| -------- | --------------- | ----------------- |
| `GET`    | `/todos`        | List all todos    |
| `GET`    | `/todos/{id}`   | Get one todo      |
| `POST`   | `/todos`        | Create a todo     |
| `PUT`    | `/todos/{id}`   | Update a todo     |
| `DELETE` | `/todos/{id}`   | Delete a todo     |
| `GET`    | `/health`       | Health check      |
