# Madhuri Real Estate - Single Page Application

## TEAM_BRIEF
stack: TypeScript/React+Vite
test_runner: npx vitest run
lint_tool: none
coverage_tool: none
coverage_threshold: 0
coverage_applies: false

## Setup

```bash
npm install
```

## Development

```bash
npm run dev
```

## Run Tests

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
├── main.tsx                    # Entry point
├── App.tsx                     # Main layout composition
├── setupTests.ts               # Test setup (jest-dom)
├── components/
│   ├── Logo.tsx                # Company logo display
│   ├── CompanyName.tsx         # Company name heading
│   ├── Profile.tsx             # Agent profile with photo and bio
│   ├── RecentSales.tsx         # Recent property sales grid
│   └── ContactInfo.tsx         # Contact details and form
├── styles/
│   └── global.css              # Global styles, colors, responsive
└── __tests__/
    ├── App.test.tsx             # Integration tests for all sections
    ├── RecentSales.test.tsx     # RecentSales component tests
    └── ContactInfo.test.tsx     # ContactInfo form & display tests
```

## Section Order (in App.tsx)

1. Logo
2. CompanyName
3. Profile
4. RecentSales
5. ContactInfo
