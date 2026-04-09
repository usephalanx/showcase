# Running the Todo App

## TEAM_BRIEF
stack: TypeScript/React+Vite
test_runner: pytest tests/
lint_tool: none
coverage_tool: none
coverage_threshold: 0
coverage_applies: false

## Prerequisites

- Python 3.9+ (for structural tests)
- Node.js 18+ and npm (for running the frontend)

## Quick Start (Development)

```bash
# Install Node dependencies
npm install

# Start the Vite dev server
npm run dev
```

Open http://localhost:5173 in your browser.

## Running Tests

```bash
# Install Python test dependencies
pip install pytest

# Run structural tests
pytest tests/
```

## Docker (Optional)

```bash
# Build and run
docker build -t todo-app .
docker run -p 5173:5173 todo-app
```

Open http://localhost:5173 in your browser.
