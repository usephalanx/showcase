# Setup Instructions

## Prerequisites

- Node.js >= 18
- npm >= 9

## Install Dependencies

```bash
npm install
```

This generates `node_modules/` and `package-lock.json` (both are git-ignored
and must not be hand-written).

## Development

```bash
npm run dev
```

Starts the Vite dev server with hot module replacement.

## Build

```bash
npm run build
```

Runs TypeScript type-checking (`tsc`) then produces a production build in `dist/`.

## Preview

```bash
npm run preview
```

Serves the production build locally for verification.

## Run Tests

```bash
npm run test
```

Runs Vitest in single-run mode with jsdom environment.
