# Architecture Plan

## File Tree

```
.
├── index.html              # HTML entry point
├── package.json            # Dependencies and scripts
├── tsconfig.json           # TypeScript configuration
├── vite.config.ts          # Vite + Vitest configuration
├── RUNNING.md              # Run instructions
├── PLAN.md                 # This file
├── src/
│   ├── App.tsx             # Main application component
│   ├── App.css             # Component styles
│   ├── main.tsx            # React DOM mount point
│   ├── setupTests.ts       # Test setup (jest-dom)
│   └── App.test.tsx        # Component tests
└── tests/
    └── test_app_component.py  # Python structural tests
```

## Component Responsibilities

### App (src/App.tsx)
- Renders an `<h1>Hello World</h1>` heading
- Manages a `count` state variable via `useState<number>(0)`
- Renders a `<button>` displaying "Count: {count}" that increments on click
- Imports App.css for styling

### Styling (src/App.css)
- Uses flexbox on `#root` for vertical and horizontal centering
- Styles the heading with sans-serif font
- Styles the button with padding, border-radius, and hover state

## Design Decisions

1. **Vite + React**: Chosen for fast development builds and native TypeScript support
2. **useState hook**: Simple state management appropriate for a single counter
3. **Functional component**: Modern React pattern with hooks
4. **Vitest**: Native Vite test runner with jsdom environment for component testing
5. **Python structural tests**: Validate file existence and content without Node.js dependency
