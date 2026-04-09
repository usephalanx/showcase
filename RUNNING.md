# Running the Application

## Quick Start (Docker)

1. Build and start the application:
   ```bash
   docker compose up --build
   ```

2. Open your browser or curl the health endpoint:
   ```
   http://localhost:8000/health
   ```

3. Expected response:
   ```json
   {"message": "hi"}
   ```

No authentication is required for any endpoint.

## Local Development (without Docker)

1. Create a virtual environment and install dependencies:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

2. Run the server:
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8000 --reload
   ```

3. Run the tests:
   ```bash
   pytest tests/
   ```

## TEAM_BRIEF
stack: Python/FastAPI
test_runner: pytest tests/
lint_tool: ruff check .
coverage_tool: pytest-cov
coverage_threshold: 70
coverage_applies: true
