# Mini React Counter App

## TEAM_BRIEF
stack: TypeScript/React+Vite
test_runner: npx vitest run
lint_tool: none
coverage_tool: none
coverage_threshold: 0
coverage_applies: false

## Overview

A minimal React application built with Vite that displays a counter with
increment and decrement buttons, centered on the page.

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
# Start the Vite dev server (default: http://localhost:5173)
npm run dev
```

## Build

```bash
# Create a production build in dist/
npm run build

# Preview the production build
npm run preview
```

## Running Tests

```bash
# Run all tests
npx vitest run
```

## Docker Setup (Optional)

```bash
# Build the Docker image
docker build -t mini-react-counter .

# Run the container
docker run -p 5173:5173 mini-react-counter
```

Then open http://localhost:5173 in your browser.

## Project Structure

```
├── index.html                 # Root HTML file with #root div
├── package.json               # Dependencies and scripts
├── vite.config.js             # Vite configuration with React plugin
├── src/
│   ├── main.jsx               # Application entry point
│   ├── index.css              # Global styles for page layout
│   ├── App.jsx                # Main App component
│   ├── App.test.jsx           # App smoke tests
│   ├── setupTests.js          # Test setup (jest-dom)
│   └── components/
│       ├── Counter.jsx        # Counter component with state logic
│       └── Counter.test.jsx   # Counter unit tests
```
