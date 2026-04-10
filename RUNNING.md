# Hello World React+Vite App

## TEAM_BRIEF
stack: TypeScript/React+Vite
test_runner: npx vitest run
lint_tool: none
coverage_tool: none
coverage_threshold: 0
coverage_applies: false

## Prerequisites

- Node.js 18+ (or Docker)

## Local Development (without Docker)

```bash
# Install dependencies
npm install

# Run development server
npm run dev

# Run tests
npm test

# Build for production
npm run build
```

The dev server will be available at http://localhost:5173.

## Docker-based Setup

### Run Tests in Docker

```bash
docker build --target test -t hello-world-test .
```

### Run Development Server with Docker Compose

```bash
docker compose up --build
```

The app will be available at http://localhost:5173.

### Stop the Server

```bash
docker compose down
```

## Project Structure

```
├── index.html              # HTML entry point
├── package.json            # Dependencies and scripts
├── vite.config.js          # Vite + Vitest configuration
├── Dockerfile              # Multi-stage Docker build
├── docker-compose.yml      # Docker Compose for dev server
└── src/
    ├── main.jsx            # React entry point
    ├── App.jsx             # Main App component
    ├── App.module.css      # Scoped CSS module styles
    └── App.test.jsx        # Test suite for App component
```
