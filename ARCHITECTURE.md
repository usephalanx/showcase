# Architecture

## Tech Stack

- **UI Library:** React 18
- **Build Tool:** Vite 5
- **Language:** TypeScript 5 (strict mode)
- **Test Runner:** Vitest 2 with jsdom environment
- **Test Utilities:** React Testing Library, jest-dom matchers

## File Structure

```
├── ARCHITECTURE.md          # This file – architecture overview
├── package.json             # Project metadata, dependencies, npm scripts
├── tsconfig.json            # TypeScript compiler configuration
├── vite.config.ts           # Vite + Vitest configuration
├── index.html               # HTML entry point (served by Vite)
├── src/
│   ├── main.tsx             # Application entry – mounts React tree into DOM
│   ├── App.tsx              # Root component – renders Hello World heading
│   └── App.test.tsx         # Unit tests for the App component
├── SETUP.md                 # Instructions for installing and running
└── (backend files)          # Existing FastAPI backend (main.py, routes.py, etc.)
```

## Component Hierarchy

```
<React.StrictMode>
  └── <App />
        └── <h1>Hello World</h1>
```

### App Component Contract

- **Props:** none
- **State:** none
- **Side effects:** none
- **Renders:** a single `<h1>` element with the text content `Hello World`

## Entry Point

`src/main.tsx` imports the `App` component and mounts it into the `<div id="root">`
element in `index.html` using `ReactDOM.createRoot` wrapped in `<React.StrictMode>`.

## Build & Test Commands

| Command         | Description                              |
| --------------- | ---------------------------------------- |
| `npm run dev`   | Start Vite dev server with HMR           |
| `npm run build` | Type-check with `tsc` then build for prod|
| `npm run preview`| Preview the production build locally    |
| `npm run test`  | Run Vitest in single-run mode            |
