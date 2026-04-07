# Setup Instructions

## Prerequisites

- Node.js >= 18
- npm >= 9

## Install Dependencies

```bash
npm install
```

This will generate `package-lock.json` and `node_modules/` — both are
git-ignored and must not be hand-written.

## Development Server

```bash
npm run dev
```

Opens the dev server at `http://localhost:3000`.

## Run Tests

```bash
npm test
```

## Production Build

```bash
npm run build
```

Output is written to `dist/`.

## Preview Production Build

```bash
npm run preview
```
