# Hello World React App

## TEAM_BRIEF
stack: TypeScript/React+Vite
test_runner: npx vitest run
lint_tool: none
coverage_tool: none
coverage_threshold: 0
coverage_applies: false

## Prerequisites

- Node.js 18+ and npm
- Docker (optional, for containerised execution)

## Local Setup

```bash
# Install dependencies
npm install

# Start the development server
npm run dev

# Run the test suite
npm test

# Build for production
npm run build

# Preview the production build
npm run preview
```

## Docker-based Setup

```bash
# Build the Docker image
docker build -t hello-world-react .

# Run the tests inside a container
docker run --rm hello-world-react npm test

# Run the dev server (accessible on http://localhost:5173)
docker run --rm -p 5173:5173 hello-world-react npm run dev -- --host 0.0.0.0
```

## Project Structure

```
.
├── index.html            # Vite HTML entry point
├── package.json          # Dependencies and scripts
├── vite.config.js        # Vite + Vitest configuration
├── RUNNING.md            # This file
└── src/
    ├── main.jsx          # React entry point
    ├── App.jsx           # Main App component (renders Hello World)
    ├── App.test.jsx      # Vitest test suite for App component
    └── setupTests.js     # Test setup (jest-dom matchers)
```

## Testing

The test suite uses **Vitest** with **React Testing Library** and verifies that the
`App` component renders an `<h1>` heading containing the text "Hello World".

Run the tests:

```bash
npm test
```

Run tests in watch mode:

```bash
npm run test:watch
```
