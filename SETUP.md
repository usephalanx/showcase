# Setup Notes

## Generated / Lock Files

The following files are **not** checked in and must be generated locally:

```bash
# Install project and dev dependencies (generates .venv, egg-info, etc.)
pip install -e ".[dev]"

# If using a lock-file workflow:
pip freeze > requirements-lock.txt   # optional
```

Do **not** commit `__pycache__/`, `*.egg-info/`, `.venv/`, or `dist/`.
