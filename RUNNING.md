# Hello World React+Vite App

## TEAM_BRIEF
stack: TypeScript/React+Vite
test_runner: npx vitest run
lint_tool: npx eslint src/ --ext .ts,.tsx
coverage_tool: vitest --coverage
coverage_threshold: 80
coverage_applies: true

## Prerequisites

- **Node.js** >= 18
- **npm** >= 9
- **Docker** and **Docker Compose** (optional, for containerised workflow)

## Local Setup (without Docker)

```bash
# Install dependencies
npm install

# Start the development server
npm run dev
# App available at http://localhost:5173

# Run tests
npm test

# Run tests in watch mode
npm run test:watch

# Run tests with coverage
npm run test:coverage

# Run linter
npm run lint

# Build for production
npm run build
```

## Docker Setup

```bash
# Build and start the container
docker compose up --build

# App available at http://localhost:5173

# Run tests inside the container
docker compose exec app npm test

# Run linter inside the container
docker compose exec app npm run lint

# Stop and clean up
docker compose down
```

## Project Structure

```
├── index.html            # HTML entry point for Vite
├── src/
│   ├── main.tsx          # React DOM render entry
│   ├── App.tsx           # Main App component (renders Hello World)
│   ├── App.test.tsx      # Test suite for App component
│   ├── index.css         # Global styles (centred layout)
│   └── setupTests.ts     # Vitest setup (jest-dom matchers)
├── package.json          # Dependencies and scripts
├── tsconfig.json         # TypeScript configuration
├── vite.config.ts        # Vite + Vitest configuration
├── .eslintrc.json        # ESLint configuration
├── Dockerfile            # Container image definition
└── docker-compose.yml    # Docker Compose service definition
```

## Acceptance Criteria

1. `npm test` passes — confirms "Hello World" renders correctly
2. The app displays "Hello World" in a centred `<h1>` element
3. `npm run lint` completes with no errors
4. Styles from `src/index.css` are applied (flexbox centering)
