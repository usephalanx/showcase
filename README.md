# Hi App

A minimal React + TypeScript application built with Vite that displays "Hi".

## Stack

- **React 18** — UI library
- **TypeScript** — type safety
- **Vite** — dev server and build tool
- **Vitest** — unit testing
- **Docker** — containerised development

## Project Structure

```
.
├── index.html          # HTML entry point (Vite convention)
├── src/
│   ├── main.tsx        # React entry point
│   ├── App.tsx         # Main App component
│   ├── App.test.tsx    # Tests for App component
│   ├── setupTests.ts   # Test setup (jest-dom matchers)
│   └── vite-env.d.ts   # Vite type declarations
├── vite.config.ts      # Vite configuration
├── tsconfig.json       # TypeScript configuration
├── package.json        # Dependencies and scripts
├── Dockerfile          # Docker image definition
└── docker-compose.yml  # Docker Compose orchestration
```

## Getting Started

### Local Development

```bash
npm install
npm run dev
```

Open http://localhost:5173 in your browser.

### Docker

```bash
docker compose up --build
```

Open http://localhost:5173 in your browser.

### Running Tests

```bash
npm test
```

### Building for Production

```bash
npm run build
npm run preview
```
