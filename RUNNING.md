# Running the Application

## TEAM_BRIEF
stack: TypeScript/React+Vite
test_runner: npm test
lint_tool: none
coverage_tool: none
coverage_threshold: 0
coverage_applies: false

## Prerequisites

- Node.js 20+ **or** Docker

## Local Setup

```bash
npm install
npm run dev
```

Visit http://localhost:5173.

## Docker Setup

```bash
docker compose up --build
```

Visit http://localhost:5173.

## Running Tests

```bash
npm install   # if not already done
npm test
```

## Building for Production

```bash
npm run build
npm run preview
```

## Available Scripts

| Command          | Description                        |
|------------------|------------------------------------|
| `npm run dev`    | Start Vite dev server              |
| `npm run build`  | Type-check and build for production|
| `npm run preview`| Preview production build locally   |
| `npm test`       | Run tests with Vitest              |
| `npm run test:watch` | Run tests in watch mode        |
