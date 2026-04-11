# Running the Application

## TEAM_BRIEF
stack: TypeScript/React+Vite
test_runner: npx vitest run
lint_tool: none
coverage_tool: none
coverage_threshold: 0
coverage_applies: false

## Prerequisites

- Node.js 20+ and npm, OR Docker + Docker Compose

## Local Development

```bash
npm install
npm run dev
```

Open http://localhost:5173.

## Running Tests

```bash
npm install
npx vitest run
```

## Docker Setup

```bash
docker compose up --build
```

Open http://localhost:5173.

## Build for Production

```bash
npm install
npm run build
npm run preview
```
