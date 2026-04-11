# Madhuri Real Estate — Running Guide

## TEAM_BRIEF
stack: TypeScript/React+Vite
test_runner: cd . && npx react-scripts test --watchAll=false
lint_tool: none
coverage_tool: none
coverage_threshold: 0
coverage_applies: false

## Prerequisites

- Node.js >= 16
- npm >= 8

## Setup

```bash
npm install
```

## Development

```bash
npm start
```

Open [http://localhost:3000](http://localhost:3000) in your browser.

## Testing

```bash
npm test
```

## Build

```bash
npm run build
```

## Project Structure

```
src/
  components/
    Logo.tsx          — Company logo component
    CompanyName.tsx   — Company name heading component
  styles/
    global.css        — Global styles, colors, typography
  __tests__/
    App.test.tsx      — Component tests
  App.tsx             — Main application layout
  index.tsx           — React DOM entry point
public/
  index.html          — HTML template
  logo.svg            — SVG logo asset
```
