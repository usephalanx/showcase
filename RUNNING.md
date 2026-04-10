# Mini React Counter App

## TEAM_BRIEF
stack: TypeScript/React+Vite
test_runner: npx vitest run
lint_tool: none
coverage_tool: none
coverage_threshold: 0
coverage_applies: false

## Overview

A minimal React counter application with increment/decrement buttons and a comprehensive test suite using Vitest and React Testing Library.

## Prerequisites

- Docker (for containerized setup), OR
- Node.js 18+ and npm

## Running with Docker (3 commands)

```bash
docker build -t counter-app .
docker run -p 5173:5173 counter-app
# Open http://localhost:5173 in your browser
```

## Running Tests with Docker

```bash
docker build -t counter-app .
docker run --rm counter-app npm test
```

## Running Locally (without Docker)

```bash
npm install
npm run dev
# Open http://localhost:5173 in your browser
```

## Running Tests Locally

```bash
npm install
npm test
```

## Project Structure

```
├── public/
│   └── index.html          # HTML entry point
├── src/
│   ├── components/
│   │   ├── Counter.jsx      # Counter component
│   │   └── Counter.test.jsx # Counter unit tests
│   ├── App.jsx              # Root App component
│   ├── App.test.jsx         # App integration tests
│   ├── main.jsx             # React DOM entry point
│   ├── index.css            # Global styles
│   └── setupTests.js        # Vitest setup (jest-dom)
├── vite.config.js           # Vite + Vitest config
├── package.json             # Dependencies and scripts
├── Dockerfile               # Docker configuration
└── RUNNING.md               # This file
```

## Test Coverage

The test suite covers:
- Counter renders with initial count of 0
- Counter heading and buttons render correctly
- Increment button increases count by 1
- Decrement button decreases count by 1
- Mixed increment/decrement sequences
- Rapid clicking updates correctly
- Negative numbers display correctly (no lower bound)
- Return to zero after equal operations
- App renders Counter component
- Counter is functional within App
