# Running the Mini React Todo App

## TEAM_BRIEF
stack: TypeScript/React+Vite
test_runner: pytest tests/
lint_tool: none
coverage_tool: none
coverage_threshold: 0
coverage_applies: false

## Prerequisites

- Node.js 18+ and npm
- Python 3.9+ and pip (for running tests)

## Installing Dependencies

```bash
npm install
```

This installs all Node.js dependencies listed in `package.json`, including React, TypeScript, and Vite.

## Running the Dev Server

```bash
npm run dev
```

Open **http://localhost:5173** in your browser.  
The Vite dev server supports hot module replacement (HMR) — changes to source files are reflected instantly.

## Building for Production

```bash
npm run build
```

This creates an optimised production bundle in the `dist/` directory.  
To preview the production build locally:

```bash
npm run preview
```

## Running Tests

```bash
pip install pytest
pytest
```

Or, if you prefer to be explicit about the test directory:

```bash
pip install pytest
pytest tests/
```

## Docker

```bash
docker build -t todo-react-app .
docker run -p 5173:5173 todo-react-app
```

Open **http://localhost:5173** in your browser.

## Authentication

No authentication is required. The app is fully client-side with no backend.

## Available Scripts

| Command           | Description                        |
|-------------------|------------------------------------|
| `npm install`     | Install all dependencies           |
| `npm run dev`     | Start the Vite dev server          |
| `npm run build`   | Create a production build          |
| `npm run preview` | Preview the production build       |

## Expected File Structure

```
.
├── RUNNING.md
├── ARCHITECTURE.md
├── package.json
├── tsconfig.json
├── vite.config.ts
├── index.html
├── public/
├── src/
│   ├── main.tsx
│   ├── App.tsx
│   ├── App.css
│   ├── index.css
│   ├── types/
│   │   └── Todo.ts
│   └── components/
│       ├── TodoInput.tsx
│       ├── TodoList.tsx
│       └── TodoItem.tsx
├── tests/
│   └── test_*.py
├── conftest.py
├── main.py
├── models.py
├── routes.py
└── storage.py
```
