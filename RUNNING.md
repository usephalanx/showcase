# Hello World React + Vite Application

## TEAM_BRIEF
stack: TypeScript/React+Vite
test_runner: npx vitest run
lint_tool: npx eslint src/ --ext .ts,.tsx
coverage_tool: none
coverage_threshold: 0
coverage_applies: false

## Prerequisites

- **Docker** and **Docker Compose** installed, OR
- **Node.js 18+** and **npm** installed locally

## Quick Start (Docker)

```bash
# Build and start the development server
docker compose up --build

# The app will be available at http://localhost:5173
```

## Quick Start (Local)

```bash
# Install dependencies
npm install

# Start the development server
npm run dev

# The app will be available at http://localhost:5173
```

## Running Tests

```bash
# Run the test suite once
npm test

# Run tests in watch mode
npm run test:watch
```

## Linting

```bash
npm run lint
```

## Building for Production

```bash
npm run build
npm run preview
```

## Project Structure

```
├── index.html              # HTML entry point (Vite convention)
├── src/
│   ├── main.tsx            # React DOM mount point
│   ├── App.tsx             # Main App component (Hello World)
│   ├── App.module.css      # CSS Module for App component
│   ├── App.test.tsx        # Tests for App component
│   ├── index.css           # Global styles
│   ├── setupTests.ts       # Test setup (jest-dom matchers)
│   └── vite-env.d.ts       # Vite/CSS module type declarations
├── vite.config.ts          # Vite + vitest configuration
├── tsconfig.json           # TypeScript configuration
├── package.json            # Dependencies and scripts
├── .eslintrc.json          # ESLint configuration
├── Dockerfile              # Container image definition
└── docker-compose.yml      # Docker Compose for local dev
```
