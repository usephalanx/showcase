# Running the Project

## TEAM_BRIEF
stack: TypeScript/React+Vite
test_runner: pytest tests/
lint_tool: none
coverage_tool: none
coverage_threshold: 0
coverage_applies: false

## Prerequisites

- Python 3.9+ (for running file-structure tests)
- Node.js 18+ and npm (for the React application)

## Install Test Dependencies

```bash
pip install -r requirements-test.txt
```

## Run Tests

```bash
pytest tests/
```

## Install Application Dependencies

```bash
npm install
```

## Start Development Server

```bash
npm run dev
```

Open http://localhost:5173 in your browser.
