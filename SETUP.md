# Frontend Setup

## Prerequisites

- Node.js >= 18
- npm >= 9

## Install Dependencies

```bash
cd frontend
npm install
```

This will generate `package-lock.json` and `node_modules/` — both are gitignored
and must not be committed.

## Development Server

```bash
npm run dev
```

The dev server starts at http://localhost:5173 with API requests proxied to
http://localhost:8000.

## Production Build

```bash
npm run build
```

Output is written to `frontend/dist/`.
