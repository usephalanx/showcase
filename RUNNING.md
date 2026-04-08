# Running the Todo API

## Quick Start (Docker)

```bash
git clone <repository-url>
cd <repository-directory>
docker compose up --build
```

The API will be available at:

- **API base URL:** http://localhost:8000
- **Swagger docs:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

## Local Development (without Docker)

### Prerequisites

- Python 3.10+

### Install Dependencies

```bash
pip install -e ".[dev]"
```

### Run the Server

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Run Tests

```bash
pytest
```

## Environment Variables

No environment variables are required. The application uses in-memory
storage by default.
