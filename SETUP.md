# Setup Instructions

This file documents commands to generate lock files and install dependencies.
Do **not** hand-write or commit generated lock files.

## Frontend

```bash
cd frontend
npm install
```

This generates:
- `node_modules/` — installed packages (git-ignored)
- `package-lock.json` — dependency lock file (git-ignored or auto-generated)

## Python Tests

```bash
pip install pytest
pytest tests/
```
