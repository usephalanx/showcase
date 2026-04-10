# Hello World React + Vite App

## TEAM_BRIEF
stack: TypeScript/React+Vite
test_runner: npx vitest run
lint_tool: npx eslint src/ --ext .ts,.tsx
coverage_tool: vitest --coverage
coverage_threshold: 80
coverage_applies: true

## Prerequisites

- **Docker** and **Docker Compose** installed, OR
- **Node.js 18+** and **npm** installed locally

## Quick Start with Docker

```bash
# Build and start the development server
docker compose up --build

# The app will be available at http://localhost:5173
```

## Local Development (without Docker)

```bash
# Install dependencies
npm install

# Start the Vite dev server
npm run dev

# The app will be available at http://localhost:5173
```

## Running Tests

```bash
# Run tests once
npm test

# Run tests in watch mode
npm run test:watch

# Run tests with coverage
npx vitest run --coverage
```

## Linting

```bash
npm run lint
```

## Building for Production

```bash
npm run build

# Preview the production build
npm run preview
```

## Project Structure

```
.
├── index.html            # HTML template with #root mount point
├── src/
│   ├── main.tsx          # Application entry point
│   ├── App.tsx           # Main App component
│   ├── App.test.tsx      # Tests for App component
│   ├── index.css         # Global styles
│   └── setupTests.ts     # Test setup (jest-dom matchers)
├── vite.config.ts        # Vite configuration
├── vitest.config.ts      # Vitest test configuration
├── tsconfig.json         # TypeScript configuration
├── .eslintrc.json        # ESLint configuration
├── package.json          # Dependencies and scripts
├── Dockerfile            # Container definition
└── docker-compose.yml    # Docker Compose services
```
