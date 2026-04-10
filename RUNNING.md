# Mini React Counter App

## TEAM_BRIEF
stack: TypeScript/React+Vite
test_runner: npx vitest run
lint_tool: none
coverage_tool: none
coverage_threshold: 0
coverage_applies: false

## Overview

A minimal React application built with Vite featuring a Counter component
with increment and decrement functionality.

## Prerequisites

- Node.js 18+ and npm
- Or Docker

## Setup & Run (Local)

```bash
# Install dependencies
npm install

# Start development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

The app will be available at http://localhost:5173 in development mode.

## Setup & Run (Docker)

```bash
# Build the Docker image
docker build -t mini-react-counter .

# Run the container
docker run -p 5173:5173 mini-react-counter
```

## Running Tests

```bash
# Install dependencies (if not done already)
npm install

# Run all tests
npx vitest run
```

## Project Structure

```
├── index.html                  # Root HTML file with #root div
├── package.json                # Dependencies and scripts
├── vite.config.js              # Vite + React plugin configuration
├── src/
│   ├── main.jsx                # Entry point – renders App to DOM
│   ├── App.jsx                 # Main App component
│   ├── App.test.jsx            # Smoke tests for App
│   ├── setupTests.js           # Test setup (jest-dom matchers)
│   └── components/
│       ├── Counter.jsx          # Counter component with state
│       └── Counter.test.jsx     # Unit tests for Counter
```
