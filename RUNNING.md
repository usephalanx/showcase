# Yellow World — Running Instructions

## TEAM_BRIEF
stack: TypeScript/React+Vite
test_runner: npx vitest run
lint_tool: none
coverage_tool: none
coverage_threshold: 0
coverage_applies: false

## Prerequisites

- Node.js 18+ (or Docker)
- npm

## Local Development

```bash
# Install dependencies
npm install

# Start development server
npm run dev

# Run tests
npm test

# Build for production
npm run build

# Preview production build
npm run preview
```

## Docker

```bash
# Build and run with Docker Compose
docker compose up --build

# Or build manually
docker build -t yellow-world .
docker run -p 5173:5173 yellow-world
```

Open http://localhost:5173 in your browser.
