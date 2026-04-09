# Setup

This project requires Node.js >= 18 and npm >= 9.

## Install dependencies

```bash
npm install
```

This generates `package-lock.json` and `node_modules/` — both are
git-ignored and must be produced by npm on each developer's machine.

## Run the development server

```bash
npm run dev
```

## Run structural tests (Python)

Requires Python 3.8+ and pytest:

```bash
pip install pytest
pytest tests/
```
