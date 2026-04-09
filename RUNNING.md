# Running the Project

## TEAM_BRIEF
stack: TypeScript/React+Vite
test_runner: pytest tests/
lint_tool: none
coverage_tool: none
coverage_threshold: 0
coverage_applies: false

## Prerequisites

- Node.js >= 18
- npm >= 9
- Python >= 3.9 (for scaffold validation tests)

## Setup

```bash
npm install
```

## Development Server

```bash
npm run dev
```

Opens on http://localhost:5173 by default.

## Build for Production

```bash
npm run build
```

Outputs to `dist/`.

## Preview Production Build

```bash
npm run preview
```

## Run Component Tests (Vitest)

```bash
npm test
```

## Run Scaffold Validation Tests (pytest)

```bash
pytest tests/
```

These Python tests validate that configuration files (package.json, tsconfig.json, vite.config.ts, etc.) are present and correctly structured. They do not require `npm install`.
