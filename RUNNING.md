# React Counter App

A minimal React application featuring a Counter component centered on the page.

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

## Running the App

```bash
npm run dev
```

The app will be available at `http://localhost:5173` by default.

## Building for Production

```bash
npm run build
npm run preview
```

## Running Tests

```bash
npm test
```

Or in watch mode:

```bash
npm run test:watch
```

## Docker Setup

### Dockerfile

Create a `Dockerfile` at the project root:

```dockerfile
FROM node:18-alpine AS base
WORKDIR /app
COPY package.json ./
RUN npm install
COPY . .

# Run tests
FROM base AS test
RUN npm test

# Build for production
FROM base AS build
RUN npm run build

# Serve with a lightweight server
FROM nginx:alpine AS production
COPY --from=build /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

### Running with Docker

```bash
# Build and run tests
docker build --target test -t counter-app-test .

# Build production image
docker build --target production -t counter-app .

# Run production container
docker run -p 8080:80 counter-app
```

The production app will be available at `http://localhost:8080`.
