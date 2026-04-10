# Mini React Counter App

## TEAM_BRIEF
stack: TypeScript/React+Vite
test_runner: npx vitest run
lint_tool: none
coverage_tool: none
coverage_threshold: 0
coverage_applies: false

## Overview

A minimal React counter application built with Vite. Displays a counter with
Increment and Decrement buttons.

## Prerequisites

- Node.js 18+ or Docker

## Running Locally (without Docker)

```bash
npm install
npm run dev
```

The app will be available at http://localhost:5173.

## Running with Docker

```bash
docker build -t counter-app .
docker run -p 5173:5173 counter-app
```

The app will be available at http://localhost:5173.

## Running Tests

```bash
npm install
npm test
```

Or equivalently:

```bash
npx vitest run
```

## Building for Production

```bash
npm run build
npm run preview
```

## Project Structure

```
src/
  main.jsx           - Entry point, mounts App into the DOM
  App.jsx            - Root component, renders Counter
  App.test.jsx       - Tests for App component
  index.css          - Global styles
  setupTests.js      - Test setup (jest-dom matchers)
  components/
    Counter.jsx      - Counter component with state management
    Counter.test.jsx - Tests for Counter component
public/
  index.html         - HTML template (fallback)
index.html           - Vite HTML entry point
package.json         - Dependencies and scripts
vite.config.js       - Vite + vitest configuration
Dockerfile           - Docker container setup
```
