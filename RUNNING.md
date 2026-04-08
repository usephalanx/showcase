# Running the Todo API

## Prerequisites

- Python 3.10 or later

## Install dependencies

```bash
pip install fastapi uvicorn pydantic
```

For running the test suite you will also need:

```bash
pip install httpx pytest
```

## Start the server

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at <http://localhost:8000>.

Interactive docs are served at <http://localhost:8000/docs>.

## Run the tests

```bash
pytest tests/
```

---

# Running the Hello World React App

## Prerequisites

- Node.js 18 or later
- npm 9 or later

## Install dependencies

```bash
npm install
```

This installs all production and development dependencies defined in
`package.json`, including React, Vite, TypeScript, Vitest, and React
Testing Library.

## Start the development server

```bash
npm run dev
```

This starts the Vite development server with hot module replacement.

Once started, open your browser and navigate to:

> <http://localhost:5173>

You should see a page displaying **Hello World** as a heading.

## Run the tests

```bash
npm test
```

This runs the Vitest test suite which verifies that:

- The `App` component renders an `<h1>` heading with the text "Hello World".
- The heading element is visible on the page.

All tests run in a jsdom environment and use React Testing Library for
DOM assertions.

## Create a production build

```bash
npm run build
```

This first runs the TypeScript compiler (`tsc`) to type-check the project
and then invokes Vite to produce an optimised production bundle in the
`dist/` directory.

To preview the production build locally:

```bash
npm run preview
```

The preview server will also be available at <http://localhost:4173> by
default.
