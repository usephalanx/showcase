# Setup Instructions

## Python Environment

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install fastapi uvicorn sqlalchemy pydantic pytest
```

## Running Tests

```bash
pytest tests/ -v
```

## Lock Files

Do not manually create or edit lock files. Generate them with:

```bash
# If using pip-tools:
pip-compile requirements.in -o requirements.txt

# If using poetry:
poetry lock

# If using npm (frontend):
cd frontend && npm install
```

The following files are auto-generated and should NOT be hand-written:
- `poetry.lock`, `Pipfile.lock`
- `package-lock.json`, `yarn.lock`, `pnpm-lock.yaml`
- `*.egg-info/`, `__pycache__/`, `.venv/`, `node_modules/`
- `build/`, `dist/`
