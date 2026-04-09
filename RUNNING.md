# Running the Application

## TEAM_BRIEF
stack: Python/FastAPI
test_runner: pytest tests/
lint_tool: ruff check .
coverage_tool: pytest-cov
coverage_threshold: 70
coverage_applies: true

## Prerequisites

- Python 3.12+ installed
- (Optional) Docker and Docker Compose for containerised runs

## Quick Start with Docker

1. **Build and start** the application:

   ```bash
   docker compose up --build
   ```

2. **Verify** the service is running:

   ```bash
   curl http://localhost:8000/health
   ```

3. **Expected response**:

   ```json
   {"message": "hi"}
   ```

No authentication is required for the `/health` endpoint.

## Local Development (without Docker)

1. **Create a virtual environment** and install dependencies:

   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

2. **Run the server**:

   ```bash
   python main.py
   ```

   Or with uvicorn directly (with auto-reload for development):

   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8000 --reload
   ```

3. **Verify** the service is running:

   ```bash
   curl http://localhost:8000/health
   ```

   Expected response:

   ```json
   {"message": "hi"}
   ```

## Running Tests

1. **Install dependencies** (if not already done):

   ```bash
   pip install -r requirements.txt
   ```

2. **Run the test suite**:

   ```bash
   pytest tests/ -v
   ```

3. **Run with coverage**:

   ```bash
   pytest tests/ --cov=. --cov-report=term-missing
   ```
