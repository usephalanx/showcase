# Running the Application

This project is a **Todo App** built with a [FastAPI](https://fastapi.tiangolo.com/) backend (Python / SQLite) and a lightweight frontend served as static HTML. It lets you create, complete, and delete todo items through a clean REST API and web interface.

---

## Prerequisites

| Tool | Minimum version |
|--------|-----------------|
| Node.js | 18+ |
| npm | 9+ |

> **Note:** The backend also requires Python 3.10+ and the dependencies listed in the Python project files, but the steps below cover the front-end development workflow.

---

## 1. Install dependencies

From the project root, run:

```bash
npm install
```

This installs all packages declared in `package.json` (React, Vite, TypeScript, testing libraries, etc.).

---

## 2. Start the development server

```bash
npm run dev
```

Vite will start a local development server with hot-module replacement (HMR) enabled.

---

## 3. Open the app

Once the dev server is running, open your browser and navigate to:

```
http://localhost:5173
```

You should see the application's landing page. Any changes you make to source files under `src/` will be reflected in the browser immediately thanks to Vite's HMR.

---

## 4. Other useful commands

| Command | Description |
|---------------------|------------------------------------------|
| `npm run build` | Create an optimised production build |
| `npm run preview` | Serve the production build locally |
| `npm test` | Run the test suite with Vitest |

---

## What does this app do?

The Todo App provides a simple task-management interface:

- **Create** todo items with a title.
- **Toggle** the completed status of any item.
- **Delete** items you no longer need.
- All data is persisted in a local SQLite database (`todos.db`).

The backend exposes a RESTful API under `/api/todos` (see `main.py`), and the frontend consumes it to render an interactive UI.
