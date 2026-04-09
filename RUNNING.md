# Running the Application

## TEAM_BRIEF
stack: TypeScript/React+Vite
test_runner: npx vitest run
lint_tool: none
coverage_tool: none
coverage_threshold: 0
coverage_applies: false

## Prerequisites

- Node.js >= 18
- npm >= 9

## Setup

```bash
npm install
```

## Development

```bash
npm run dev
```

The dev server starts at http://localhost:5173 by default.

## Build

```bash
npm run build
```

## Tests

```bash
npm test
```

This runs `vitest run` which executes all `*.test.tsx` files under `src/`.

## Preview Production Build

```bash
npm run preview
```
