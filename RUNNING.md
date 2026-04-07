# Running the Todo Application

A client-side React + TypeScript Todo application built with Vite. Manage your
tasks with add, complete, delete, and filter functionality. All data is persisted
in the browser via localStorage — no backend required.

---

## Prerequisites

- [Node.js](https://nodejs.org/) (v18 or later recommended)
- npm (bundled with Node.js)
- Optionally: [Docker](https://docs.docker.com/get-docker/) and
  [Docker Compose](https://docs.docker.com/compose/install/)

---

## Quick Start (npm)

### 1. Install dependencies

```bash
npm install
```

### 2. Start the development server

```bash
npm run dev
```

The app will be available at **<http://localhost:5173>**.

### 3. Run the tests

```bash
npm test
```

This runs the full test suite via Vitest, including component and hook tests.

---

## Quick Start (Docker)

If you prefer a containerised environment:

```bash
# Build and start the application
docker compose up --build

# Open in your browser
#   http://localhost:5173
```

To stop:

```bash
docker compose down
```

---

## Available npm Scripts

| Command         | Description                                  |
| --------------- | -------------------------------------------- |
| `npm run dev`   | Start the Vite development server            |
| `npm run build` | Create a production build in `dist/`         |
| `npm test`      | Run the test suite with Vitest               |

---

## Application Overview

This is a single-page Todo application that lets you:

- **Add** new todo items (with whitespace trimming and empty-input rejection)
- **Toggle** completion status of individual todos
- **Delete** todos you no longer need
- **Filter** the list by All, Active, or Completed

State is managed with React `useState` hooks inside the `TodoPage` component.
Todos are persisted to `localStorage` so they survive page refreshes. If
`localStorage` is unavailable (e.g. private browsing quota exceeded), the app
gracefully falls back to in-memory state.

---

## Notes

- No authentication is required — there is no backend dependency for the frontend.
- No demo credentials are needed.
- The frontend dev server runs on port **5173** by default.
