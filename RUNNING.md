# Running the SPA

## TEAM_BRIEF
stack: TypeScript/React+Vite
test_runner: cd spa && npx vitest run
lint_tool: none
coverage_tool: none
coverage_threshold: 0
coverage_applies: false

## Prerequisites

- Node.js >= 18
- npm >= 9

## Setup

```bash
cd spa
npm install
```

## Development

```bash
cd spa
npm run dev
```

Open http://localhost:5173 in your browser.

## Build

```bash
cd spa
npm run build
npm run preview
```

## Run Tests

```bash
cd spa
npm test
```

This runs the Vitest test suite which verifies that the App component
renders 'hello-world' as expected.

## Docker

```bash
docker build -t spa-hello-world -f Dockerfile.spa .
docker run --rm -p 5173:5173 spa-hello-world
```

Open http://localhost:5173 in your browser to see 'hello-world'.
