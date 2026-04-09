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
- npm (comes with Node.js)
- Python >= 3.9 (for Python-level tests)

## Setup

```bash
npm install
```

## Development

Start the development server:

```bash
npm run dev
```

The app runs on **http://localhost:5173** by default.

## Production Build

Create an optimized production build:

```bash
npm run build
```

## Preview Production Build

Preview the production build locally:

```bash
npm run preview
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
