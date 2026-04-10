# React Counter App

A minimal React counter application built with Vite, featuring increment and decrement buttons with a comprehensive test suite.

## TEAM_BRIEF
stack: TypeScript/React+Vite
test_runner: npx vitest run
lint_tool: none
coverage_tool: none
coverage_threshold: 0
coverage_applies: false

## Prerequisites

- Node.js 18+ and npm
- Docker (optional, for containerized setup)

## Local Setup

```bash
# Install dependencies
npm install

# Start development server
npm run dev

# Run tests
npm test

# Build for production
npm run build
```

## Docker Setup

### Build and Run

```bash
# Build the Docker image
docker build -t react-counter-app .

# Run the container (development server on port 5173)
docker run -p 5173:5173 react-counter-app
```

### Run Tests in Docker

```bash
# Run the test suite inside a container
docker run --rm react-counter-app npm test
```

## Project Structure

```
├── index.html                    # HTML entry point
├── package.json                  # Dependencies and scripts
├── vite.config.js                # Vite + Vitest configuration
├── src/
│   ├── main.jsx                  # React entry point
│   ├── App.jsx                   # Root App component
│   ├── App.css                   # Global and centering styles
│   ├── setupTests.js             # Test setup (jest-dom matchers)
│   └── components/
│       ├── Counter.jsx           # Counter component
│       └── Counter.test.jsx      # Test suite for Counter and App
```

## Testing

Tests are written using [Vitest](https://vitest.dev/) and [@testing-library/react](https://testing-library.com/docs/react-testing-library/intro/).

```bash
# Run all tests
npm test

# Run tests in watch mode
npm run test:watch
```

### Test Coverage

- Initial count renders as 0
- Increment button increases count by 1
- Decrement button decreases count by 1
- Mixed increment/decrement sequences
- Count can go negative
- Rapid clicking updates correctly
- Accessibility labels and aria-live region
- Centering classes are applied
- App renders Counter within centered container
