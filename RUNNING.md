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
- npm

## Setup

```bash
npm install
```

## Development

```bash
npm run dev
```

The development server will start and serve the application at `http://localhost:5173`.

## Build

```bash
npm run build
```

## Project Structure

- `index.html` — HTML entry point with `#root` div and script tag pointing to `/src/main.tsx`
- `src/main.tsx` — React entry point, renders `<App />` into `#root`
- `src/App.tsx` — Root App component
