# Hello World React+Vite App

## Prerequisites

- Node.js 18+ and npm
- Docker and Docker Compose (optional)

## Local Development

```bash
npm install
npm run dev
```

Open [http://localhost:5173](http://localhost:5173) in your browser.

## Build for Production

```bash
npm run build
npm run preview
```

## Run Tests

```bash
npm install
npm test
```

## Docker Setup

```bash
docker build -t hello-world-app .
docker run -p 5173:5173 hello-world-app
```

Open [http://localhost:5173](http://localhost:5173) in your browser.

## TEAM_BRIEF
stack: TypeScript/React+Vite
test_runner: npx vitest run
lint_tool: none
coverage_tool: none
coverage_threshold: 0
coverage_applies: false
