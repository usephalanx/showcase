# Hello World React App

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

## Run Tests

```bash
npm test
```

## Docker-based Setup

### Build the image

```bash
docker build -t hello-world-app .
```

### Run in development mode

```bash
docker run -it --rm -p 5173:5173 hello-world-app npm run dev -- --host 0.0.0.0
```

### Run tests inside Docker

```bash
docker run -it --rm hello-world-app npm test
```

### Dockerfile (if not present)

Create a `Dockerfile` at the project root:

```dockerfile
FROM node:18-alpine
WORKDIR /app
COPY package.json ./
RUN npm install
COPY . .
EXPOSE 5173
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]
```
