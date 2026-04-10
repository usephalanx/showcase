# Mini React Counter App

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

## Local Development

```bash
# Install dependencies
npm install

# Start development server
npm run dev

# Build for production
npm run build

# Run tests
npm test

# Run tests in watch mode
npm run test:watch
```

## Docker Setup

### Build and run

```bash
# Build the Docker image
docker build -t counter-app .

# Run the container (development server on port 5173)
docker run -p 5173:5173 counter-app

# Run tests inside Docker
docker run --rm counter-app npm test
```

### Using docker-compose (if available)

```bash
docker-compose up
```

## Project Structure

```
src/
├── main.jsx                    # React entry point
├── App.jsx                     # Root component
├── App.css                     # Global centering styles
├── setupTests.js               # Test setup (jest-dom)
└── components/
    ├── Counter.jsx             # Counter component
    ├── Counter.module.css      # Counter scoped styles
    └── Counter.test.jsx        # Counter unit tests
```

## Testing

Tests are written using Vitest and @testing-library/react.

```bash
npm test
```

This runs all `*.test.jsx` files via `vitest run`.
