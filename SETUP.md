# Setup Instructions

## Prerequisites

- Node.js >= 18
- Python >= 3.11
- npm (comes with Node.js)

## Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

This will:
1. Install all dependencies listed in `package.json` (generates `package-lock.json` and `node_modules/`).
2. Start the Vite dev server on `http://localhost:5173`.

## Running Tests

From the repository root:

```bash
pip install pytest
pytest tests/ -v
```

## Build for Production

```bash
cd frontend
npm run build
```

Output will be in `frontend/dist/`.
