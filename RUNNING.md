# Running the Hello World React Application

## Prerequisites

- [Node.js](https://nodejs.org/) (v18 or later recommended)
- npm (included with Node.js)

## Install Dependencies

```bash
npm install
```

## Development Server

Start the Vite development server on port 3000:

```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser.

## Production Build

Compile TypeScript and bundle the application:

```bash
npm run build
```

The output is written to the `dist/` directory.

## Preview Production Build

Serve the production build locally:

```bash
npm run preview
```

## Running Tests

The structural tests use Python and pytest:

```bash
pip install pytest
pytest tests/test_structure.py -v
```
