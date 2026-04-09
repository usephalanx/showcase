# Running the Application

## TEAM_BRIEF
stack: TypeScript/React+Vite
test_runner: pytest tests/
lint_tool: none
coverage_tool: none
coverage_threshold: 0
coverage_applies: false

## Prerequisites

- Node.js >= 18
- Python >= 3.9 (for Python-level tests)

## Setup

```bash
npm install
```

## Development

```bash
npm run dev
```

## Build

```bash
npm run build
```

## Testing

### Python structure tests

```bash
pytest tests/
```

### Vitest component tests (requires npm install)

```bash
npm test
```

## Project Structure

- `src/App.tsx` — Main React component with Hello World heading and counter
- `src/App.css` — Centered layout styling with flexbox, button hover states
- `src/main.tsx` — Application entry point, mounts App to DOM
- `src/setupTests.ts` — Test setup importing jest-dom matchers
- `src/App.test.tsx` — Vitest component tests for App
- `index.html` — HTML entry point served by Vite
- `tests/test_app_component.py` — Python tests verifying file structure and content
