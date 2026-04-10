# Running the Application

## TEAM_BRIEF
stack: TypeScript/React+Vite
test_runner: npx vitest run
lint_tool: none
coverage_tool: none
coverage_threshold: 0
coverage_applies: false

## Prerequisites

- **Node.js** >= 18
- **npm** >= 9 (or any compatible package manager)
- **Docker** (optional, for containerised setup)

## Local Development

```bash
# Install dependencies
npm install

# Start the development server
npm run dev

# Open http://localhost:5173 in your browser
```

## Running Tests

```bash
npm install
npx vitest run
```

## Production Build

```bash
npm run build
npm run preview
```

## Docker Setup

```bash
# Build the Docker image
docker build -t react-vite-spa .

# Run the container (maps port 5173 to the host)
docker run -p 5173:5173 react-vite-spa

# Open http://localhost:5173 in your browser
```

You should see **hello-world** rendered in the viewport.
