# Hello World React App

A minimal React application that renders a centered "Hello World" heading.

## TEAM_BRIEF
stack: TypeScript/React+Vite
test_runner: pytest tests/
lint_tool: none
coverage_tool: none
coverage_threshold: 0
coverage_applies: false

## Prerequisites

- Node.js >= 18
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

The dev server starts on http://localhost:5173 by default.

## Build

```bash
npm run build
```

## Running Tests

```bash
pytest tests/
```

The test suite validates project structure and file contents using Python/pytest.
No Node.js runtime is required for running the tests.
