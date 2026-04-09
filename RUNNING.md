# Hello World React + Vite

A minimal React + TypeScript application bootstrapped with Vite.

## TEAM_BRIEF
stack: TypeScript/React+Vite
test_runner: pytest tests/
lint_tool: none
coverage_tool: none
coverage_threshold: 0
coverage_applies: false

## Prerequisites

- Node.js 20+ and npm
- Python 3.9+ (for running tests)
- Docker and Docker Compose (optional, for containerised development)

## Setup

```bash
npm install
```

## Development

```bash
npm run dev
```

The development server starts at http://localhost:5173.

## Build

```bash
npm run build
```

## Preview Production Build

```bash
npm run preview
```

## Docker

```bash
docker compose up --build
```

Access at http://localhost:5173.

## Tests

Python-based structural tests that verify file existence and content:

```bash
pytest tests/
```
