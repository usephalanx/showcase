# Hi App

A minimal React + TypeScript + Vite application that displays "Hi".

## Stack

- **React 18** — UI library
- **TypeScript** — type safety
- **Vite** — build tool and dev server
- **Vitest** — test runner
- **React Testing Library** — component testing

## Project Structure

```
index.html          HTML entry point
src/
  App.tsx           Main component (renders "Hi")
  App.test.tsx      Test for App component
  main.tsx          React DOM entry point
  vite-env.d.ts     Vite type declarations
```

## Getting Started

```bash
npm install
npm run dev
```

Open http://localhost:5173 in your browser.

## Testing

```bash
npm test
```

## Building

```bash
npm run build
npm run preview
```

## Docker

```bash
docker compose up --build
```

Open http://localhost:5173 in your browser.
