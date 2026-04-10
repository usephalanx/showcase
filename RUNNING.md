# React Counter App

## TEAM_BRIEF
stack: TypeScript/React+Vite
test_runner: npx vitest run
lint_tool: none
coverage_tool: none
coverage_threshold: 0
coverage_applies: false

## Prerequisites

- Docker installed and running

## Running with Docker

### 1. Build the Docker image

```bash
docker build -t react-counter-app .
```

### 2. Run the container

```bash
docker run -p 5173:5173 react-counter-app
```

### 3. Open the app

Navigate to [http://localhost:5173](http://localhost:5173) in your browser.

## Running Tests

### Inside Docker

```bash
docker run --rm react-counter-app npm test
```

### Locally (requires Node.js 18+)

```bash
npm install
npm test
```

## Development (local)

```bash
npm install
npm run dev
```

The dev server starts at http://localhost:5173 with hot module replacement enabled.

## Building for Production

```bash
npm run build
```

Output is written to the `dist/` directory.
