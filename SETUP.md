# Setup Instructions

## Prerequisites

- Node.js >= 18
- npm >= 9 (or pnpm / yarn)

## Install Dependencies

```bash
npm install
```

## Run Tests

```bash
npx vitest run
```

## Run Tests in Watch Mode

```bash
npx vitest
```

## Project Configuration

The following lock files and generated directories are **not** checked into version control
and must be produced by the toolchain:

- `node_modules/`
- `package-lock.json` / `yarn.lock` / `pnpm-lock.yaml`
- `dist/`
- `.vite/`

Run `npm install` to generate them locally.
