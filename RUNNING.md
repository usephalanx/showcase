# Running the Project

## TEAM_BRIEF
stack: TypeScript/React+Vite
test_runner: pytest tests/
lint_tool: none
coverage_tool: none
coverage_threshold: 0
coverage_applies: false

## Quick Start

### Using Docker (recommended)

```bash
docker compose up
```

The application will be available at http://localhost:5173.

### Using npm directly

```bash
npm install
npm run dev
```

## Running Tests

```bash
pip install pytest
pytest tests/
```

## Project Structure

- `index.html` — Vite entry HTML file with root div and module script
- `tsconfig.json` — TypeScript compiler configuration
- `package.json` — Project metadata and dependencies
- `vite.config.ts` — Vite build tool configuration with React plugin
- `src/main.tsx` — React entry point
- `src/App.tsx` — Main App component rendering "Hello World"
- `Dockerfile` — Container definition for development
- `docker-compose.yml` — Docker Compose configuration for one-command startup
