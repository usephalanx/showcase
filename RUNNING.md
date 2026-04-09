# Hello World React + Vite

A minimal React application scaffolded with Vite and TypeScript.

## TEAM_BRIEF

stack: TypeScript/React+Vite
test_runner: pytest tests/
lint_tool: none
coverage_tool: none
coverage_threshold: 0
coverage_applies: false

## Prerequisites

- **Node.js** >= 20 (for local development)
- **Docker** & **Docker Compose** (for containerised development)
- **Python** >= 3.9 and **pytest** (for running structural tests)

## Local Development

```bash
npm install
npm run dev
```

The app will be available at [http://localhost:5173](http://localhost:5173).

## Docker

```bash
docker compose up --build
```

The app will be available at [http://localhost:5173](http://localhost:5173).

## Build for Production

```bash
npm run build
npm run preview
```

## Running Tests

```bash
pip install pytest
pytest tests/
```

The test suite validates that all required project files exist and are
correctly structured. No Node.js runtime or `npm install` is needed to
run the tests.
