# Hello World React App

## TEAM_BRIEF
stack: TypeScript/React+Vite
test_runner: npx vitest run
lint_tool: none
coverage_tool: none
coverage_threshold: 0
coverage_applies: false

## Prerequisites

- Node.js >= 18
- npm

## Setup

```bash
npm install
```

## Development

```bash
npm run dev
```

Open http://localhost:5173 in your browser.

## Build

```bash
npm run build
```

## Run Tests

```bash
npm test
```

## Docker

```bash
docker build -t hello-world-app .
docker run -p 8080:80 hello-world-app
```

Open http://localhost:8080 in your browser.
