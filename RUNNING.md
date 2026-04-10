# React Counter App

A minimal Vite + React application featuring a Counter component with increment and decrement functionality.

## TEAM_BRIEF

stack: TypeScript/React+Vite
test_runner: npx vitest run
lint_tool: none
coverage_tool: none
coverage_threshold: 0
coverage_applies: false

## Prerequisites

- Node.js 18+ and npm
- Docker (optional, for containerised setup)

## Local Setup

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

## Docker Setup

### Development

```bash
# Build the Docker image
docker build -t react-counter-app .

# Run the container (development mode)
docker run -it --rm -p 5173:5173 react-counter-app npm run dev -- --host 0.0.0.0

# Run tests inside container
docker run -it --rm react-counter-app npm test
```

### Using Docker Compose (if available)

```bash
docker compose up
```

## Project Structure

```
.
├── index.html                  # HTML entry point
├── package.json                # Dependencies and scripts
├── vite.config.js              # Vite configuration with React plugin
├── src/
│   ├── main.jsx                # React entry point
│   ├── App.jsx                 # Root component
│   ├── App.css                 # Centering styles
│   ├── setupTests.js           # Test setup (jest-dom matchers)
│   └── components/
│       ├── Counter.jsx         # Counter component with state
│       └── Counter.test.jsx    # Counter component tests
└── RUNNING.md                  # This file
```

## Testing

Tests use **Vitest** with **@testing-library/react** and **@testing-library/jest-dom**.

```bash
# Run tests once
npm test

# Run tests in watch mode
npm run test:watch
```

## Scripts

| Script         | Description                          |
| -------------- | ------------------------------------ |
| `npm run dev`  | Start Vite dev server with HMR       |
| `npm run build`| Build for production                 |
| `npm run preview` | Preview production build locally  |
| `npm test`     | Run tests with Vitest                |
| `npm run test:watch` | Run tests in watch mode        |
