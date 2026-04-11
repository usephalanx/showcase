# Hello World App — Running Instructions

## TEAM_BRIEF
stack: TypeScript/React+Vite
test_runner: pytest tests/
lint_tool: none
coverage_tool: none
coverage_threshold: 0
coverage_applies: false

## Overview

A minimal React + TypeScript + Vite application that displays a centered "Hello World" heading with modern, clean styling using CSS modules.

## Prerequisites

- Node.js >= 18
- npm >= 9
- Python >= 3.9 (for running tests)
- pytest (for running tests)

## Setup

```bash
# Install Node.js dependencies
npm install

# Install Python test dependencies
pip install pytest
```

## Development

```bash
# Start the Vite dev server
npm run dev
```

The app will be available at `http://localhost:5173`.

## Build

```bash
npm run build
```

## Testing

Python-based tests validate that all CSS files, components, and styling rules are correctly in place:

```bash
pytest tests/
```

## Project Structure

```
├── index.html                          # HTML entry point
├── src/
│   ├── main.tsx                        # React bootstrap
│   ├── index.css                       # Global reset & base styles
│   ├── App.tsx                         # Root component
│   ├── App.module.css                  # App container centering styles
│   ├── App.css                         # Legacy/fallback app styles
│   ├── vite-env.d.ts                   # TypeScript declarations
│   ├── test-setup.ts                   # Vitest setup
│   └── components/
│       ├── HelloWorld.tsx              # HelloWorld component
│       └── HelloWorld.module.css       # Scoped heading styles
├── tests/
│   └── test_frontend_styling.py        # Python tests for styling
├── package.json
├── tsconfig.json
├── vite.config.ts
└── vitest.config.ts
```
