# Architecture

## Overview

This project is a full-stack Todo application. The **backend** is a FastAPI
service backed by SQLite (see `healthcheck/`). The **frontend** is a
single-page React application bootstrapped with Vite and written in
TypeScript.

This document focuses on the frontend.

## Technology Stack

| Layer         | Technology                          | Version  |
| ------------- | ----------------------------------- | -------- |
| UI Library    | React                               | 18.x     |
| Build Tool    | Vite                                | 5.x      |
| Language      | TypeScript                          | 5.x      |
| Test Runner   | Vitest                              | 2.x      |
| Test Utils    | @testing-library/react, jest-dom    | 16.x/6.x |

## Project Structure

```
.
├── ARCHITECTURE.md          # This file
├── SETUP.md                 # Commands to install and run
├── index.html               # Vite HTML entry point
├── package.json             # NPM metadata, deps, scripts
├── tsconfig.json            # TypeScript compiler options
├── vite.config.ts           # Vite + Vitest configuration
└── src/
    ├── main.tsx             # React DOM entry – renders <App />
    ├── App.tsx              # Root component – renders <HomePage />
    ├── App.css              # Global reset & centered layout
    ├── components/
    │   └── Greeting.tsx     # Reusable <Greeting name? /> component
    ├── pages/
    │   └── HomePage.tsx     # Page shell – composes <Greeting />
    └── test/
        └── setup.ts         # Vitest setup – imports jest-dom matchers
```

## Component Catalog

### `<App />`

Root component. Imports global CSS and renders `<HomePage />`.

### `<HomePage />`

Page-level component. Renders the `<Greeting />` component inside a
semantic `<main>` element.

### `<Greeting />`

| Prop   | Type     | Default   | Description               |
| ------ | -------- | --------- | ------------------------- |
| `name` | `string` | `"World"` | Name to display in the h1 |

Renders `<h1 data-testid="greeting">Hello {name}</h1>`.

## Data Flow

The data flow is intentionally trivial for the initial scaffold:

```
App  →  HomePage  →  Greeting(name)
```

Props flow downward; there is no global state yet.

## Build & Run

```bash
npm install
npm run dev      # Start Vite dev server
npm run build    # Production build to dist/
npm run preview  # Preview production build locally
npm run test     # Run Vitest in watch mode
```

## Testing Strategy

- **Unit / Component tests** live alongside source in `tests/` (project
  root) or co-located `*.test.tsx` files.
- Tests use **Vitest** as the runner with a **jsdom** environment.
- **@testing-library/react** provides DOM-based component queries.
- **@testing-library/jest-dom** extends assertions with matchers like
  `toBeInTheDocument()`.
- A global setup file (`src/test/setup.ts`) is loaded by Vitest to
  register jest-dom matchers automatically.
