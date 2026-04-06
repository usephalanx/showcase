# Setup Instructions

## Install Dependencies

```bash
pip install fastapi uvicorn sqlalchemy pydantic pytest
```

Or using the requirements file:

```bash
pip install -r requirements.txt
```

## Generated Files

Do NOT commit the following — they are generated automatically:

- `__pycache__/`
- `*.egg-info/`
- `.venv/`
- `kanban.db` (SQLite database file)
- `poetry.lock`, `Pipfile.lock`
