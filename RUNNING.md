# Running the Todo App

## TEAM_BRIEF
stack: TypeScript/React+Vite
test_runner: pytest tests/
lint_tool: none
coverage_tool: none
coverage_threshold: 0
coverage_applies: false

## Prerequisites

- Python 3.10+ (for running tests)
- Node.js 18+ and npm (for running the React dev server)

## Quick Start

### 1. Install Python test dependencies

```bash
pip install pytest
```

### 2. Run tests

```bash
pytest tests/
```

### 3. Install frontend dependencies (when package.json is set up)

```bash
npm install
```

### 4. Start development server

```bash
npm run dev
```

Open http://localhost:5173 in your browser.

## Docker Setup

```bash
# Build and run
docker compose up --build

# Open in browser
open http://localhost:5173
```

## Running Tests Only

```bash
pytest tests/ -v
```
