# Hello World React+Vite Application

## TEAM_BRIEF
stack: TypeScript/React+Vite
test_runner: cd frontend && npx vitest run
lint_tool: cd frontend && npx eslint src/ --ext .ts,.tsx
coverage_tool: none
coverage_threshold: 0
coverage_applies: false

## Overview

A minimal React application built with Vite and TypeScript that displays "Hello World".

## Prerequisites

- **Docker** and **Docker Compose** installed, OR
- **Node.js 18+** and **npm** installed locally

---

## Docker Setup (Recommended)

### 1. Build and start the container

```bash
cd frontend
docker compose up --build
```

### 2. Access the app

Open your browser and navigate to:

```
http://localhost:5173
```

You should see **"Hello World"** displayed on the page.

### 3. Run tests inside Docker

```bash
cd frontend
docker compose run --rm app npm test
```

### 4. Run linting inside Docker

```bash
cd frontend
docker compose run --rm app npm run lint
```

### 5. Stop the container

```bash
cd frontend
docker compose down
```

---

## Local Setup (Without Docker)

### 1. Install dependencies

```bash
cd frontend
npm install
```

### 2. Start the development server

```bash
npm run dev
```

Open your browser at `http://localhost:5173`.

### 3. Run tests

```bash
npm test
```

### 4. Run linting

```bash
npm run lint
```

### 5. Build for production

```bash
npm run build
```

The production-ready files will be in the `dist/` directory.

### 6. Preview production build

```bash
npm run preview
```

---

## Project Structure

```
frontend/
├── public/
│   └── index.html          # HTML template with <div id="root">
├── src/
│   ├── App.tsx             # Main App component (Hello World)
│   ├── App.test.tsx        # Tests for App component
│   ├── index.css           # Global styles
│   ├── main.tsx            # Application entry point
│   ├── setupTests.ts       # Test setup (jest-dom matchers)
│   └── vite-env.d.ts       # Vite type declarations
├── .eslintrc.json          # ESLint configuration
├── docker-compose.yml      # Docker Compose service definition
├── Dockerfile              # Container image definition
├── package.json            # Dependencies and scripts
├── tsconfig.json           # TypeScript configuration
├── tsconfig.node.json      # TypeScript config for Vite
└── vite.config.ts          # Vite configuration
```

## Available Scripts

| Script          | Command             | Description                        |
| --------------- | ------------------- | ---------------------------------- |
| `npm run dev`   | `vite`              | Start development server           |
| `npm run build` | `tsc && vite build` | Type-check and build for production|
| `npm run preview`| `vite preview`     | Preview production build           |
| `npm test`      | `vitest run`        | Run test suite                     |
| `npm run lint`  | `eslint src/`       | Lint source files                  |
