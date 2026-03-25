# Architecture

## Overview

This project is a single-page React application bootstrapped with Vite and written in TypeScript. It renders a "Hello World" greeting and is designed as the frontend scaffolding for future feature development.

The backend is a FastAPI application backed by SQLite that exposes a REST API for todo CRUD operations.

## Technology Stack

| Layer     | Technology       | Version |
|-----------|------------------|---------|
| UI        | React            | 18.x    |
| Bundler   | Vite             | 5.x     |
| Language  | TypeScript       | 5.x     |
| Backend   | FastAPI (Python) | latest  |
| Database  | SQLite           | 3.x     |

## File Structure

```
.
├── ARCHITECTURE.md          # This file
├── index.html               # HTML entry point for Vite
├── package.json             # Project metadata, dependencies, scripts
├── tsconfig.json            # TypeScript config for application source
├── tsconfig.node.json       # TypeScript config for Vite config (Node context)
├── vite.config.ts           # Vite configuration with React plugin
├── src/
│   ├── main.tsx             # React entry point – mounts <App /> into #root
│   ├── App.tsx              # Main application component
│   ├── App.css              # Styles for the App component
│   └── vite-env.d.ts        # Vite client type declarations
├── healthcheck/
│   └── e36e389f/
│       ├── main.py          # FastAPI application
│       └── database.py      # SQLite database layer
└── tests/
    └── test_frontend_setup.py  # Validation tests for frontend scaffolding
```

## Component Architecture

The frontend currently contains a single component:

- **`App`** – The root component rendered inside `React.StrictMode`. It displays an `<h1>` element with the text "Hello World", centred on the viewport.

All components live under `src/` and are bundled by Vite.

## Data Flow

```
index.html
  └─► /src/main.tsx  (Vite module entry)
        └─► <React.StrictMode>
              └─► <App />  (renders "Hello World")
```

## Build & Dev

| Command            | Description                                    |
|--------------------|------------------------------------------------|
| `npm install`      | Install all dependencies                       |
| `npm run dev`      | Start Vite dev server on http://localhost:5173 |
| `npm run build`    | Type-check with `tsc` then build for production|
| `npm run preview`  | Preview the production build locally           |
