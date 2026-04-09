# Project Plan — Hello World React

## File Tree

```
hello-world-react/
├── index.html              # HTML entry point served by Vite
├── package.json            # Dependencies and npm scripts
├── tsconfig.json           # TypeScript compiler configuration
├── vite.config.ts          # Vite build + Vitest test configuration
├── PLAN.md                 # This file — architecture documentation
├── RUNNING.md              # How to run, build, and test the project
├── src/
│   ├── main.tsx            # React DOM entry — mounts <App /> into #root
│   ├── App.tsx             # Main component: Hello World heading + counter
│   ├── App.css             # Styles for the App component
│   ├── App.test.tsx        # Unit tests for App component (vitest)
│   └── setupTests.ts       # Test setup — imports jest-dom matchers
└── tests/
    └── test_scaffold.py    # Python tests validating scaffold config files
```

## Component Responsibilities

| File             | Responsibility                                                       |
|------------------|----------------------------------------------------------------------|
| `index.html`     | Minimal HTML shell with `<div id="root">` and module script tag      |
| `main.tsx`       | Bootstraps React — calls `createRoot` and renders `<App />`          |
| `App.tsx`        | Renders a heading ("Hello World") and a stateful counter button      |
| `App.css`        | Flexbox centering, typography, and button styling                    |
| `setupTests.ts`  | Extends Vitest with `@testing-library/jest-dom` matchers             |
| `App.test.tsx`   | Three tests: heading render, counter initial state, counter click    |

## Design Decisions

1. **Vite as bundler**: Chosen for fast HMR, native ESM support, and first-class TypeScript handling.
2. **React 18**: Uses `createRoot` API for concurrent features readiness.
3. **TypeScript strict mode**: Catches type errors early; `react-jsx` transform avoids manual React imports.
4. **Vitest + jsdom**: Co-located with Vite config; uses the same transform pipeline as the build.
5. **Testing Library**: Encourages testing by user-visible behavior rather than implementation details.
6. **Bundler module resolution**: Matches Vite's resolution strategy without Node.js-specific assumptions.
