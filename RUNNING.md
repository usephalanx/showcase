# Running the Todo App

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

## Local Development

```bash
# Install dependencies
npm install

# Start dev server
npm run dev
```

Open http://localhost:5173 in your browser.

## Running Tests

```bash
# Python integration / static-file tests
pytest tests/
```

## Docker Setup (optional)

```bash
# Build and run
docker build -t todo-app .
docker run -p 5173:5173 todo-app
```

Open http://localhost:5173 in your browser.
