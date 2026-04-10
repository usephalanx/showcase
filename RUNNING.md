# Hello World React+Vite App

## TEAM_BRIEF
stack: TypeScript/React+Vite
test_runner: npx vitest run
lint_tool: none
coverage_tool: none
coverage_threshold: 0
coverage_applies: false

## Prerequisites

- Docker and Docker Compose installed
- OR Node.js 18+ and npm

## Running with Docker Compose

```bash
docker-compose up --build
```

The app will be available at [http://localhost:5173](http://localhost:5173).

## Running Locally (without Docker)

```bash
npm install
npm run dev
```

The app will be available at [http://localhost:5173](http://localhost:5173).

## Building for Production

```bash
npm run build
npm run preview
```

## Running Tests

```bash
npm install
npm test
```

This runs Vitest with jsdom and React Testing Library to verify the App component renders correctly.
