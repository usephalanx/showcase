# Running the React Todo App

## TEAM_BRIEF
stack: TypeScript/React+Vite
test_runner: pytest tests/
lint_tool: none
coverage_tool: none
coverage_threshold: 0
coverage_applies: false

---

## Prerequisites

- **Node.js** >= 18
- **npm** >= 9
- **Docker** and **Docker Compose** (optional, for containerised setup)

---

## Quick Start (Local)

```bash
# 1. Install dependencies
npm install

# 2. Start the development server
npm run dev

# 3. Open in browser
#    http://localhost:5173
```

## Quick Start (Docker)

```bash
# 1. Build and start
docker compose up --build

# 2. Open in browser
#    http://localhost:5173
```

## Build for Production

```bash
npm run build
npm run preview
```

The production build is output to the `dist/` directory.

---

## Project Structure

See [PLAN.md](./PLAN.md) for the full architecture, component hierarchy, data model, and testing strategy.
