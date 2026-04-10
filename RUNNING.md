# Running the Application

## TEAM_BRIEF
stack: TypeScript/React+Vite
test_runner: pytest tests/
lint_tool: none
coverage_tool: none
coverage_threshold: 0
coverage_applies: false

## Prerequisites

- Node.js 18+ and npm
- Docker and Docker Compose (optional, for containerised development)

## Local Development

```bash
npm install
npm run dev
```

Open [http://localhost:5173](http://localhost:5173) in your browser.

## Docker

```bash
docker compose up --build
```

Open [http://localhost:5173](http://localhost:5173) in your browser.

## Authentication

No authentication is required. The application is a client-side-only todo app.

## Build for Production

```bash
npm run build
npm run preview
```
