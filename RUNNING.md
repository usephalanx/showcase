# Running the React + Vite Hello World Application

## TEAM_BRIEF
stack: TypeScript/React+Vite
test_runner: cd frontend && npx vitest run
lint_tool: none
coverage_tool: none
coverage_threshold: 0
coverage_applies: false

---

## Prerequisites

- **Docker** ≥ 20.10
- **Docker Compose** ≥ 1.29 (or the `docker compose` v2 plugin)

## Quick Start (Docker)

```bash
cd frontend
docker compose up --build
```

The development server will be available at **http://localhost:5173**.

## Running Tests (Docker)

```bash
cd frontend
docker compose run --rm app npm test
```

## Running Locally (without Docker)

```bash
cd frontend
npm install
npm run dev      # start dev server on http://localhost:5173
npm test         # run Vitest test suite
npm run build    # production build to dist/
```

## Project Structure

```
frontend/
├── index.html            # Vite HTML entry point
├── package.json          # Dependencies & scripts
├── vite.config.js        # Vite + React plugin config
├── Dockerfile            # Container image definition
├── docker-compose.yml    # Compose service definition
├── .dockerignore         # Files excluded from Docker context
└── src/
    ├── main.jsx          # React DOM mount point
    ├── App.jsx           # Main App component (Hello World)
    ├── App.module.css    # Scoped CSS module for App
    ├── App.test.jsx      # Vitest + React Testing Library tests
    └── setupTests.js     # jest-dom matcher setup
```
