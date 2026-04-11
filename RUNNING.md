# Hello World React App

A minimal React + Vite TypeScript application that displays a centered "Hello World" heading.

## TEAM_BRIEF
stack: TypeScript/React+Vite
test_runner: npx vitest run
lint_tool: none
coverage_tool: none
coverage_threshold: 0
coverage_applies: false

## Prerequisites

- Node.js >= 18
- npm >= 9

## Setup

```bash
npm install
```

## Development

```bash
npm run dev
```

Open http://localhost:5173 in your browser.

## Build

```bash
npm run build
```

## Testing

```bash
npm test
```

This runs `vitest run` which executes all `*.test.tsx` files in the `src/` directory.

## Project Structure

```
index.html                          # HTML entry point with #root div
src/
  main.tsx                          # React 18 bootstrap (createRoot)
  App.tsx                           # Root component with centered container
  App.module.css                    # App-level flexbox centering styles
  App.test.tsx                      # Integration test for App component
  components/
    HelloWorld.tsx                  # Reusable heading component
    HelloWorld.module.css           # Scoped heading styles
    HelloWorld.test.tsx             # Unit test for HelloWorld component
vite.config.ts                      # Vite + Vitest configuration
tsconfig.json                       # TypeScript compiler options
package.json                        # Dependencies and scripts
```
