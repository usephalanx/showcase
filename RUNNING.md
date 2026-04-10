# Yellow World — Running Instructions

## TEAM_BRIEF
stack: TypeScript/React+Vite
test_runner: npx vitest run
lint_tool: none
coverage_tool: none
coverage_threshold: 0
coverage_applies: false

## Prerequisites

- **Node.js** ≥ 18
- **npm** ≥ 9
- **Docker** and **Docker Compose** (for containerised usage)

## Local Development

```bash
# Install dependencies
npm install

# Start the dev server (http://localhost:5173)
npm run dev

# Run tests
npm test

# Build for production
npm run build

# Preview the production build
npm run preview
```

## Docker

```bash
# Build and start the container
docker compose up --build

# The app is available at http://localhost:5173
```

## Project Structure

```
├── index.html            # HTML entry point
├── src/
│   ├── main.tsx          # React bootstrap
│   ├── main.css          # Global styles
│   ├── App.tsx           # Main App component
│   ├── App.module.css    # Scoped styles for App
│   └── __tests__/
│       ├── setup.ts      # Test setup (jest-dom)
│       └── App.test.tsx  # App component tests
├── vite.config.ts        # Vite configuration
├── tsconfig.json         # TypeScript configuration
├── package.json          # Dependencies and scripts
├── Dockerfile            # Multi-stage Docker build
└── docker-compose.yml    # Compose orchestration
```
