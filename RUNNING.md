# Hello World React App

A minimal React + Vite + TypeScript application that renders a centered "Hello World" heading using CSS modules.

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

## Development Server

```bash
npm run dev
```

Opens on http://localhost:5173 by default.

## Build

```bash
npm run build
```

## Running Tests

```bash
npm test
```

This runs `vitest run` which executes all `*.test.tsx` files in the `src/` directory.

Test files:
- `src/components/HelloWorld.test.tsx` — Unit tests for the HelloWorld component
- `src/App.test.tsx` — Integration tests for the App component

## Project Structure

```
├── index.html                          # Vite HTML entry point
├── package.json                        # Dependencies and scripts
├── tsconfig.json                       # TypeScript configuration
├── vite.config.ts                      # Vite + Vitest configuration
├── vite-env.d.ts                       # TypeScript declarations for Vite
├── src/
│   ├── main.tsx                        # React DOM entry point
│   ├── App.tsx                         # Root App component
│   ├── App.module.css                  # App-level centering styles
│   ├── App.test.tsx                    # Integration tests for App
│   └── components/
│       ├── HelloWorld.tsx              # HelloWorld component
│       ├── HelloWorld.module.css       # HelloWorld scoped styles
│       └── HelloWorld.test.tsx         # Unit tests for HelloWorld
└── RUNNING.md                          # This file
```
