# Setup Instructions

## Prerequisites

- [Node.js](https://nodejs.org/) >= 18
- npm (bundled with Node.js)

## Install Dependencies

```bash
npm install
```

This generates `package-lock.json` and the `node_modules/` directory.
Both are **not** committed to version control.

## Development Server

```bash
npm run dev
```

Starts the Vite dev server on [http://localhost:3000](http://localhost:3000).

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
npm test
```

Runs the Vitest test suite.
