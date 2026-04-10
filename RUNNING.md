# Counter App

A minimal React counter application built with Vite.

## TEAM_BRIEF
stack: TypeScript/React+Vite
test_runner: npx vitest run
lint_tool: none
coverage_tool: none
coverage_threshold: 0
coverage_applies: false

## Prerequisites

- Node.js >= 18
- npm >= 9

## Setup

```bash
npm install
```

## Development

```bash
npm run dev
```

The app will be available at `http://localhost:5173`.

## Build

```bash
npm run build
```

## Run Tests

```bash
npm test
```

This runs all Vitest test suites (`src/**/*.test.jsx`).

## Docker

```bash
docker build -t counter-app .
docker run -p 5173:5173 counter-app
```

## Project Structure

```
├── index.html                  # Root HTML with #root div
├── package.json                # Dependencies and scripts
├── vite.config.js              # Vite + React plugin config
├── src/
│   ├── main.jsx                # React entry point
│   ├── App.jsx                 # Root App component
│   ├── App.test.jsx            # App smoke tests
│   ├── setupTests.js           # Test setup (jest-dom)
│   └── components/
│       ├── Counter.jsx         # Counter component (logic + UI)
│       ├── Counter.module.css  # Counter styles (CSS Modules)
│       └── Counter.test.jsx    # Counter unit tests
└── RUNNING.md                  # This file
```
