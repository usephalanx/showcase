# Running the Application

## TEAM_BRIEF
stack: TypeScript/React+Vite
test_runner: npx vitest run
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

# Start dev server (default: http://localhost:5173)
npm run dev

# Run tests
npm test

# Build for production
npm run build

# Preview production build
npm run preview
```

## Docker

```bash
# Build the image
docker build -t hello-world-spa .

# Run the container
docker run -p 5173:5173 hello-world-spa

# Open in browser
# http://localhost:5173
```

## What You Should See

Opening the app in a browser displays only the text **hello-world** in the viewport.

## Running Tests

```bash
npm install
npx vitest run
```

The test suite verifies that the `<App />` component renders the text "hello-world".
