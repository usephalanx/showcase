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
- Python >= 3.9 (for pytest-based HTML validation tests)

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

## Build

```bash
npm run build
```

## Tests

### Python tests (HTML structure validation)

```bash
pytest tests/
```

### Vitest component tests

```bash
npm test
```
