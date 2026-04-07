# Setup — Installing Dependencies

This project has both Python (backend) and Node.js (frontend) dependencies.
Do **not** commit lock files — generate them locally.

## Frontend (Node.js)

```bash
# Install Node.js dependencies (generates node_modules/ and lock file)
npm install
```

## Python (Backend)

```bash
# Create a virtual environment and install dependencies
python -m venv .venv
source .venv/bin/activate   # On Windows: .venv\Scripts\activate
pip install fastapi uvicorn pydantic
pip install pytest pytest-timeout httpx   # dev dependencies
```

## Running Tests

```bash
# Frontend tests
npm test

# Backend tests
pytest
```
