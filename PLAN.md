# Architecture Plan

## File Tree

```
.
├── RUNNING.md              # Setup and run instructions
├── PLAN.md                 # This file — architecture documentation
├── package.json            # Node.js project manifest and scripts
├── tsconfig.json           # TypeScript compiler configuration
├── vite.config.ts          # Vite build and test configuration
├── index.html              # HTML entry point served by Vite
├── conftest.py             # Root pytest configuration
├── src/
│   ├── main.tsx            # React app entry point
│   ├── App.tsx             # Main component (Hello World + counter)
│   ├── App.css             # Styles for the App component
│   ├── App.test.tsx        # Vitest component tests
│   └── setupTests.ts       # Test setup (jest-dom matchers)
└── tests/
    ├── __init__.py
    └── test_app_component.py  # Python tests for file structure
```

## Component Responsibilities

### `src/App.tsx`
- Renders an `<h1>Hello World</h1>` heading
- Manages a counter via `useState<number>(0)`
- Renders a `<button>` that increments the counter on click
- Imports `App.css` for styling

### `src/main.tsx`
- Mounts the `<App />` component into the DOM `#root` element
- Wraps the app in `React.StrictMode`

### `index.html`
- Provides the `<div id="root">` mount point
- Loads `src/main.tsx` as an ES module

## Design Decisions

1. **Vite** — chosen as the build tool for fast HMR and optimised production builds
2. **TypeScript** — strict mode enabled for type safety
3. **React 18** — uses `createRoot` API for concurrent features
4. **Vitest + Testing Library** — component tests run in jsdom environment
5. **Python tests** — verify file structure without requiring Node.js, enabling CI validation of project scaffolding
