# Running the Mini React Todo App

## Prerequisites

- Node.js >= 18
- npm >= 9
- Python >= 3.9 (for running the test suite)

## Quick Start

```bash
# Install dependencies
npm install

# Start the Vite dev server
npm run dev
```

The application will be available at **http://localhost:5173**.

## Running Tests

```bash
# Install Python test dependencies
pip install pytest

# Run the test suite
pytest tests/
```

## Docker (optional)

```bash
docker compose up --build
```

Open **http://localhost:5173** in your browser.

## Notes

- No authentication is required.
- No demo credentials needed.
- All state is in-memory (browser only); refreshing the page clears todos.

## TEAM_BRIEF
stack: TypeScript/React+Vite
test_runner: pytest tests/
lint_tool: none
coverage_tool: none
coverage_threshold: 0
coverage_applies: false
