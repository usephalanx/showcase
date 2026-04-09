# Setup Instructions

## Install Node.js dependencies

Run the following command from the repository root to generate the
lock file and install all packages into `node_modules/`:

```bash
npm install
```

This produces `package-lock.json` and `node_modules/` — both are
generated artifacts and are **not** checked into version control.

## Install Python test dependencies

```bash
pip install pytest
```

## Verify setup

```bash
pytest tests/
```
