# Architecture

## Overview

This project is a single-page **Hello World** web application built with
React, Vite, and TypeScript. It serves as a minimal starting point that
demonstrates the frontend tooling setup and component composition pattern
without any backend dependency.

## Tech Stack

| Technology | Version | Purpose |
|---|---|---|
| React | 18.x | UI component library |
| ReactDOM | 18.x | DOM rendering |
| TypeScript | 5.x | Static type checking with strict mode |
| Vite | 5.x | Dev server and production bundler |
| @vitejs/plugin-react | 4.x | React Fast Refresh & JSX transform |

## File Structure

```
frontend/
├── index.html                 # Vite HTML entry point
├── package.json               # Dependencies and npm scripts
├── tsconfig.json              # TypeScript compiler configuration
├── vite.config.ts             # Vite build configuration
└── src/
    ├── main.tsx               # Application entry – mounts React root
    ├── App.tsx                # Root component
    ├── App.css                # Global styles
    ├── vite-env.d.ts          # Vite client type declarations
    └── pages/
        └── HelloPage.tsx      # Hello World page component
```

## Component Tree

```
<React.StrictMode>
  └── <App>              # Root wrapper (src/App.tsx)
      └── <HelloPage>    # Page component (src/pages/HelloPage.tsx)
          └── <h1>       # "Hello World" heading
```

- **App** – Top-level component that composes page-level children. Future
  pages or layout elements (header, footer, router) would be added here.
- **HelloPage** – The single page of the application. Renders the greeting
  heading with a `data-testid` attribute for automated testing.

## Build & Dev

| Command | Description |
|---|---|
| `npm run dev` | Start the Vite dev server with Hot Module Replacement |
| `npm run build` | Type-check with `tsc` then create a production bundle |
| `npm run preview` | Serve the production build locally for inspection |

## Design Decisions

1. **No backend** – The app is purely static; no API calls are needed for
   a Hello World greeting.
2. **No routing** – With a single page there is no need for `react-router`
   or similar libraries.
3. **No state management** – No application state beyond what React's
   built-in component model provides.
4. **Strict TypeScript** – `strict: true` catches common errors early and
   enforces consistent type safety across the codebase.
5. **Vite over CRA** – Vite provides faster cold starts and HMR thanks to
   native ES module support.
