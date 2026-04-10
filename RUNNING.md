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

## Prerequisites

- [Node.js](https://nodejs.org/) (v18 or later recommended)
- npm (comes bundled with Node.js)

## Running Locally

1. **Install dependencies:**

   ```bash
   npm install
   ```

2. **Start the development server:**

   ```bash
   npm run dev
   ```

3. **Open the app in your browser:**

   Navigate to [http://localhost:5173](http://localhost:5173).

### What to Expect

When the dev server starts and you open http://localhost:5173 you will see a
yellow-themed page displaying **"Yellow World"** as a large, centered heading.
The page features:

- A bright yellow (#FFD700) background
- The text "Yellow World" prominently displayed in the center
- A welcoming subheading beneath the main title

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
