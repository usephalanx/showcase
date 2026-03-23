# Frontend Setup

## Prerequisites

- Node.js >= 18
- npm >= 9

## Install Dependencies

```bash
cd frontend
npm install
```

This will generate `package-lock.json` and `node_modules/`.

## Development Server

```bash
npm run dev
```

The app runs at http://localhost:5173 and proxies `/api` requests to the backend at http://localhost:8000.

## Run Tests

```bash
npm test
```

## Build for Production

```bash
npm run build
```

Output will be in `dist/`.
