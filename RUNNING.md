# Madhuri Real Estate — Frontend

## TEAM_BRIEF
stack: TypeScript/React+Vite
test_runner: cd frontend && npx vitest run
lint_tool: none
coverage_tool: none
coverage_threshold: 0
coverage_applies: false

## Overview
Single-page real estate website for Madhuri Real Estate built with Vite, React, and TypeScript.

## Prerequisites
- Node.js >= 18
- npm >= 9

## Setup
```bash
cd frontend
npm install
```

## Development
```bash
cd frontend
npm run dev
```
The app will start at http://localhost:3000.

## Build
```bash
cd frontend
npm run build
```
Output goes to `frontend/dist/`.

## Testing
```bash
cd frontend
npm test
```
Runs all tests under `src/__tests__/` via Vitest + jsdom.

## Project Structure
```
frontend/
├── public/
│   └── logo.svg
├── src/
│   ├── __tests__/
│   │   ├── App.test.tsx
│   │   ├── ContactInfo.test.tsx
│   │   └── RecentSales.test.tsx
│   ├── components/
│   │   ├── CompanyName.tsx
│   │   ├── ContactInfo.tsx
│   │   ├── Logo.tsx
│   │   ├── Profile.tsx
│   │   └── RecentSales.tsx
│   ├── styles/
│   │   └── global.css
│   ├── App.tsx
│   ├── main.tsx
│   ├── test-setup.ts
│   └── vite-env.d.ts
├── index.html
├── package.json
├── tsconfig.json
├── tsconfig.node.json
└── vite.config.ts
```
