# Architecture

## Tech Stack

- **React 18** — UI library
- **Vite 5** — Build tool and dev server
- **TypeScript 5** — Type-safe JavaScript
- **Vitest + React Testing Library** — Unit testing

## File Structure

```
├── index.html              # HTML entry point with div#root
├── package.json            # Dependencies, scripts, metadata
├── tsconfig.json           # TypeScript compiler configuration
├── vite.config.ts          # Vite + Vitest configuration
├── SETUP.md                # Instructions to install and run
├── src/
│   ├── main.tsx            # Application entry point (mounts React tree)
│   ├── App.tsx             # Root component rendering <h1>Hello World</h1>
│   └── App.test.tsx        # Unit tests for the App component
```

## Entry Point

`src/main.tsx` is the application entry point. It:

1. Imports `React` and `ReactDOM` (client).
2. Imports the root `<App />` component.
3. Calls `ReactDOM.createRoot()` targeting `document.getElementById('root')`.
4. Renders `<App />` wrapped in `<React.StrictMode>`.

## App Component

- Default-exported function component named `App`.
- Renders a single `<h1>` element with the text "Hello World".
- No props, no state, no side effects.

## Build Commands

| Command         | Description                        |
| --------------- | ---------------------------------- |
| `npm run dev`   | Start Vite dev server              |
| `npm run build` | Type-check then build for prod     |
| `npm run preview` | Preview production build locally |
| `npm run test`  | Run Vitest unit tests              |
