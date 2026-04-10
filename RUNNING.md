# Running the Mini React Todo App

## TEAM_BRIEF
stack: TypeScript/React+Vite
test_runner: pytest tests/
lint_tool: none
coverage_tool: none
coverage_threshold: 0
coverage_applies: false

## Prerequisites

- **Docker** and **Docker Compose** installed, OR
- **Node.js >= 18** with npm

## Running with Docker

```bash
docker compose up --build
```

Open [http://localhost:5173](http://localhost:5173) in your browser.

## Running Locally (without Docker)

```bash
npm install
npm run dev
```

Open [http://localhost:5173](http://localhost:5173) in your browser.

## Authentication

No authentication is required. The app runs entirely in the browser with no backend.

## Build for Production

```bash
npm run build
```

Output is written to `dist/`.
