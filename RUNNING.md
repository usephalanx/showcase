# Running the Application

This document describes how to install dependencies and start the development server for the Hello World application.

## Prerequisites

- **Node.js** ≥ 18 (LTS recommended)
- **npm** ≥ 9 (ships with Node.js)

Verify your installation:

```bash
node --version
npm --version
```

## Install Dependencies

From the project root directory run:

```bash
npm install
```

This reads `package.json` and installs all required runtime and development
dependencies into the local `node_modules/` directory.

## Start the Development Server

Launch the Vite development server with:

```bash
npm run dev
```

The server starts on **http://localhost:5173** by default.  
Open that URL in your browser to see the application.

The dev server supports **hot module replacement** — any changes you save
will be reflected in the browser immediately without a full page reload.

## Run Tests

Execute the test suite with:

```bash
npm test
```

This runs all `test_*.tsx` files under the `tests/` directory using Vitest.

## Build for Production

Create an optimised production bundle:

```bash
npm run build
```

The output is written to the `dist/` directory. You can preview it locally:

```bash
npm run preview
```
