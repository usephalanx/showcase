# Architecture Plan

## File Tree

```
.
├── index.html              # HTML entry point served by Vite
├── package.json            # Project metadata and dependencies
├── tsconfig.json           # TypeScript compiler configuration
├── vite.config.ts          # Vite build + vitest test configuration
├── PLAN.md                 # This file – architecture documentation
├── RUNNING.md              # Instructions for running the project
├── conftest.py             # Root pytest configuration
├── src/
│   ├── main.tsx            # React mount point
│   ├── App.tsx             # Main App component (heading + counter)
│   ├── App.css             # Styles for the App component
│   ├── App.test.tsx        # Vitest unit tests for App component
│   └── setupTests.ts       # Test setup (jest-dom matchers)
└── tests/
    └── test_index_html.py  # Pytest tests validating index.html structure
```

## Component Responsibilities

| Component      | Responsibility                                                      |
| -------------- | ------------------------------------------------------------------- |
| `index.html`   | Minimal HTML5 shell; contains `<div id="root">` and module script   |
| `src/main.tsx` | Imports React, mounts `<App />` into the root DOM element           |
| `src/App.tsx`  | Renders "Hello World" heading and an interactive counter button     |
| `src/App.css`  | Provides layout (centred flexbox) and basic styling                 |

## Design Decisions

1. **Vite as bundler** – Fast HMR, native ESM support, first-class React/TS plugin.
2. **Vitest for component tests** – Zero-config integration with Vite; uses jsdom.
3. **Pytest for static HTML validation** – Ensures the HTML entry point meets spec
   without requiring a Node.js environment for CI validation.
4. **No external CDN links** – All dependencies are bundled by Vite at build time.
5. **Strict TypeScript** – `strict: true` catches type errors early.
