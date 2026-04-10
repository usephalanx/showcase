# Yellow World Web App

A minimal React/Vite/TypeScript application that displays "yellow world" with yellow-themed styling.

## TEAM_BRIEF
stack: TypeScript/React+Vite
test_runner: npx vitest run
lint_tool: none
coverage_tool: none
coverage_threshold: 0
coverage_applies: false

## Prerequisites

- Node.js 18+ and npm
- Docker and Docker Compose (for containerised run)

## Local Development

```bash
# Install dependencies
npm install

# Start dev server
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

# Open in browser
# http://localhost:5173
```

## Project Structure

```
├── index.html              # HTML entry point
├── src/
│   ├── main.tsx            # React entry point
│   ├── main.css            # Global styles
│   ├── App.tsx             # Main App component
│   ├── App.module.css      # Yellow-themed CSS module
│   ├── setupTests.ts       # Test setup (jest-dom matchers)
│   └── __tests__/
│       └── App.test.tsx    # App component test suite
├── vite.config.ts          # Vite + Vitest configuration
├── tsconfig.json           # TypeScript configuration
├── package.json            # Dependencies and scripts
├── Dockerfile              # Multi-stage Docker build
└── docker-compose.yml      # Docker Compose config
```

## Testing

Tests use Vitest with React Testing Library and jest-dom matchers.
The test suite verifies:

1. The "yellow world" text is rendered in the DOM
2. The text appears inside an `<h1>` element
3. CSS module classes (`container`, `heading`) are correctly applied
4. The DOM structure is correct (div wrapping h1)

Run tests:

```bash
npm test
```
