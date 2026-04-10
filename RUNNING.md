# Running the Mini React Todo App

## TEAM_BRIEF
stack: TypeScript/React+Vite
test_runner: pytest tests/
lint_tool: none
coverage_tool: none
coverage_threshold: 0
coverage_applies: false

## Prerequisites

- Node.js 18+ and npm (or Docker)

## Local Development (npm)

```bash
npm install
npm run dev
```

Open **http://localhost:5173** in your browser.

## Docker

```bash
docker build -t todo-react-app .
docker run -p 5173:5173 todo-react-app
```

Open **http://localhost:5173** in your browser.

## Authentication

No authentication is required. The app is fully client-side with no backend.

## Available Scripts

| Command           | Description                        |
|-------------------|------------------------------------|
| `npm run dev`     | Start the Vite dev server          |
| `npm run build`   | Create a production build          |
| `npm run preview` | Preview the production build       |
