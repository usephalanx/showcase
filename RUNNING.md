# Running the Project

## TEAM_BRIEF
stack: TypeScript/React+Vite
test_runner: pytest tests/
lint_tool: none
coverage_tool: none
coverage_threshold: 0
coverage_applies: false

## Prerequisites

- Node.js >= 18
- npm >= 9
- Python >= 3.9 (for running structural tests)
- pytest (`pip install pytest`)

## Setup

```bash
npm install
```

## Development

```bash
npm run dev
```

The Vite dev server starts on http://localhost:5173 by default.

## Build

```bash
npm run build
```

## Preview production build

```bash
npm run preview
```

## Running tests

Structural validation tests are written in Python using pytest:

```bash
pytest tests/
```

These tests verify that all configuration files exist and contain the
required content markers. They do **not** require `npm install` to run.
