# Mini React Counter App

## TEAM_BRIEF
stack: TypeScript/React+Vite
test_runner: npx vitest run
lint_tool: none
coverage_tool: none
coverage_threshold: 0
coverage_applies: false

## Overview

A minimal React counter application built with Vite. Features a Counter
component with increment and decrement buttons, fully tested with Vitest
and React Testing Library.

## Prerequisites

- Node.js >= 18
- npm >= 9

## Setup

```bash
# Install dependencies
npm install
```

## Development

```bash
# Start the dev server
npm run dev
```

The app will be available at http://localhost:5173 by default.

## Build

```bash
npm run build
npm run preview
```

## Testing

```bash
# Run all tests once
npm test

# Run tests in watch mode
npm run test:watch
```

## Docker Setup

```bash
# Build the image
docker build -t mini-react-counter .

# Run the container
docker run -p 5173:5173 mini-react-counter
```

## Project Structure

```
├── index.html                  # Root HTML with #root div
├── package.json                # Dependencies and scripts
├── vite.config.js              # Vite + Vitest configuration
├── src/
│   ├── main.jsx                # React entry point
│   ├── App.jsx                 # Main App component
│   ├── App.test.jsx            # App smoke tests
│   ├── setupTests.js           # Test setup (jest-dom)
│   └── components/
│       ├── Counter.jsx          # Counter component
│       └── Counter.test.jsx     # Counter unit tests
└── RUNNING.md                  # This file
```
