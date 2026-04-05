# Setup

This file documents the commands needed to install dependencies and
generate lock files / build artifacts that are **not** checked into
version control.

## Prerequisites

- Node.js >= 18
- npm >= 9

## Install Dependencies

```bash
npm install
```

This generates `package-lock.json` and populates `node_modules/`.

## Development Server

```bash
npm run dev
```

Opens the Vite dev server (default: http://localhost:5173).

## Production Build

```bash
npm run build
```

Outputs optimised assets to `dist/`.

## Preview Production Build

```bash
npm run preview
```

## Run Tests

```bash
npm run test
```

Runs Vitest in watch mode. For CI (single run):

```bash
npm run test -- --run
```
