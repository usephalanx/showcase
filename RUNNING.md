# Yellow World App

A single-page React application that displays "Yellow World" as a large heading
centered on a bright yellow (#FFD700) background with a welcoming subheading.

## TEAM_BRIEF
stack: TypeScript/React+Vite
test_runner: pytest tests/
lint_tool: none
coverage_tool: none
coverage_threshold: 0
coverage_applies: false

## Running Locally

```bash
npm install
npm run dev
```

The app will be available at http://localhost:5173 (default Vite port).

## Building for Production

```bash
npm run build
```

The static assets are output to the `dist/` directory.

## Serving with Python (static fallback)

```bash
python server.py
```

Serves the `public/` directory on port 8000 (override via `PORT` env var).
