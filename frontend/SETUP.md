# Frontend Setup

## Prerequisites

- Node.js >= 18
- npm >= 9

## Install Dependencies

```bash
cd frontend
npm install
```

This will generate `package-lock.json` and populate `node_modules/`.

## Environment Variables

Create a `.env` file (optional) in the `frontend/` directory:

```env
# Base URL for the backend API.
# Leave empty or omit to use the Vite dev-server proxy (recommended for local dev).
VITE_API_BASE_URL=
```

## Development Server

```bash
npm run dev
```

The Vite dev server proxies `/api` requests to `http://localhost:8000`.

## Run Tests

```bash
npm test
```

## Build for Production

```bash
npm run build
```

Output will be in `frontend/dist/`.
