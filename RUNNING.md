# Running the Application

## TEAM_BRIEF
stack: TypeScript/React+Vite
test_runner: pytest tests/
lint_tool: none
coverage_tool: none
coverage_threshold: 0
coverage_applies: false

## Prerequisites

- Node.js >= 18
- npm >= 9 (or Docker + Docker Compose)

## Local Development (npm)

```bash
npm install
npm run dev
```

Open <http://localhost:5173> in your browser.

## Docker

```bash
docker compose up --build
```

Open <http://localhost:5173> in your browser.

## Authentication

No authentication is required. The app runs entirely in the browser with no
backend dependencies.

## Running Tests

```bash
pytest tests/
```

Tests validate component structure and file presence. No browser or Node.js
runtime is required for the test suite.
