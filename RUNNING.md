# Hello World React App

A minimal React + TypeScript application built with Vite, displaying a centered "Hello World" heading.

## TEAM_BRIEF

stack: TypeScript/React+Vite
test_runner: npx vitest run
lint_tool: none
coverage_tool: none
coverage_threshold: 0
coverage_applies: false

## Prerequisites

- Node.js 18+ and npm 9+

## Setup

```bash
npm install
```

## Development

Start the Vite dev server:

```bash
npm run dev
```

The app will be available at `http://localhost:5173` by default.

## Build

Create a production build:

```bash
npm run build
```

The output will be in the `dist/` directory.

## Preview Production Build

```bash
npm run preview
```

## Testing

Run the test suite:

```bash
npm test
```

Run tests in watch mode during development:

```bash
npm run test:watch
```

## Project Structure

```
.
├── index.html                        # Vite HTML entry point
├── package.json                      # Dependencies and scripts
├── tsconfig.json                     # TypeScript configuration
├── vite.config.ts                    # Vite configuration
├── vite-env.d.ts                     # Vite/CSS module type declarations
├── RUNNING.md                        # This file
└── src/
    ├── main.tsx                      # React bootstrap / DOM mount
    ├── App.tsx                       # Root application component
    ├── App.module.css                # App-level container styles
    ├── App.test.tsx                  # App integration tests
    ├── test-setup.ts                 # Test environment setup
    └── components/
        ├── HelloWorld.tsx            # HelloWorld component
        ├── HelloWorld.module.css     # HelloWorld scoped styles
        └── HelloWorld.test.tsx       # HelloWorld unit tests
```
