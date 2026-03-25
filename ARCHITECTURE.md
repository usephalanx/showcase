# Architecture

## Overview

A single-page React application bootstrapped with **Vite** and written in
**TypeScript**.  The app renders a "Hello World" heading — serving as a
minimal starting point for further development.

## Technology Stack

| Layer       | Technology         | Version  |
| ----------- | ------------------ | -------- |
| UI Library  | React              | ^18.3.1  |
| Language    | TypeScript         | ^5.5.0   |
| Bundler     | Vite               | ^5.4.0   |
| Test Runner | Vitest             | ^2.1.0   |
| Test Utils  | Testing Library    | ^16.1.0  |

## File Structure

```
.
├── index.html              # HTML entry point (Vite serves this)
├── package.json            # Dependencies and npm scripts
├── tsconfig.json           # TypeScript config (app source)
├── tsconfig.node.json      # TypeScript config (Vite/Node context)
├── vite.config.ts          # Vite configuration
├── RUNNING.md              # How to install and run
├── ARCHITECTURE.md         # This file
├── src/
│   ├── main.tsx            # ReactDOM.createRoot – mounts <App />
│   ├── App.tsx             # Root component – imports & renders HomePage
│   ├── index.css           # Global styles (centered text, clean font)
│   ├── vite-env.d.ts       # Vite client type declarations
│   └── pages/
│       └── HomePage.tsx    # HomePage component – renders "Hello World"
└── tests/
    ├── setup.ts            # Test setup (jest-dom matchers)
    ├── test_App.tsx         # App component tests
    └── test_HomePage.tsx    # HomePage component tests
```

## Component Architecture

```
main.tsx
  └── <App />              (src/App.tsx)
        └── <HomePage />   (src/pages/HomePage.tsx)
              └── <h1>Hello World</h1>
```

- **main.tsx** — Application entry point.  Mounts the root `<App />`
  component into the `#root` DOM node inside `React.StrictMode`.
- **App** — Top-level component.  Imports global styles (`index.css`)
  and renders `<HomePage />`.
- **HomePage** — Page-level component.  Returns a `<main>` element
  containing the `<h1>Hello World</h1>` heading.

## Build & Dev

| Command            | Description                                |
| ------------------ | ------------------------------------------ |
| `npm run dev`      | Start Vite dev server on port 5173         |
| `npm run build`    | Type-check with `tsc` then bundle for prod |
| `npm run preview`  | Preview the production build locally       |
| `npm test`         | Run Vitest test suite                      |

## Data Flow

This is a purely static application with no data fetching, state
management, or side effects.  The component tree is rendered once and
displays static content.
