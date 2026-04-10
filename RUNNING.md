# Running the Mini React Todo App

## TEAM_BRIEF
stack: TypeScript/React+Vite
test_runner: pytest tests/
lint_tool: none
coverage_tool: none
coverage_threshold: 0
coverage_applies: false

## Prerequisites

- Node.js 18+ and npm
- (Optional) Docker and Docker Compose

## Local Development (npm)

```bash
# Install dependencies
npm install

# Start the Vite dev server
npm run dev
```

Open [http://localhost:5173](http://localhost:5173) in your browser.

## Docker

```bash
# Build and start
docker compose up --build

# Or run in background
docker compose up --build -d
```

Open [http://localhost:5173](http://localhost:5173) in your browser.

## Authentication

No authentication is required. The app runs entirely client-side with no backend.

## Build for Production

```bash
npm run build
```

Output is placed in the `dist/` directory and can be served by any static file server.
