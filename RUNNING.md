# Mini React Counter App

## TEAM_BRIEF
stack: JavaScript/React+Vite
test_runner: npm test
lint_tool: none
coverage_tool: none
coverage_threshold: 0
coverage_applies: false

## Prerequisites

- Docker installed and running
- OR Node.js 20+ and npm installed locally

## Running with Docker

```bash
# 1. Build the Docker image
docker build -t mini-react-counter .

# 2. Run the container
docker run -p 3000:3000 mini-react-counter
```

Open http://localhost:3000 in your browser.

## Running Locally (without Docker)

```bash
# 1. Install dependencies
npm install

# 2. Start the development server
npm run dev
```

Open the URL printed in the terminal (usually http://localhost:5173).

## Running Tests

```bash
# Install dependencies (if not already done)
npm install

# Run the test suite
npm test
```

## Building for Production

```bash
npm run build
```

The production-ready files will be in the `dist/` directory.
