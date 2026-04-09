# Running the Project

## TEAM_BRIEF
stack: TypeScript/React+Vite
test_runner: pytest tests/
lint_tool: none
coverage_tool: none
coverage_threshold: 0
coverage_applies: false

## Feature Summary

A **React Todo Application** built with TypeScript and Vite that allows users to:

- **Add** new todo items via a text input and submit button (or Enter key)
- **Toggle** the completed state of each todo (checkbox with line-through styling)
- **Delete** individual todo items
- View all todos in a clean, responsive list
- See an empty-state message when no todos exist

The frontend is backed by a **FastAPI REST API** with in-memory storage, providing full CRUD endpoints for todo items.

## Prerequisites

- **Node.js 18+** and **npm** (for the React application)
- **Python 3.9+** and **pip** (for running file-structure tests)

## Install Application Dependencies

```bash
npm install
```

## Start Development Server

```bash
npm run dev
```

Open [http://localhost:5173](http://localhost:5173) in your browser.

## Run Tests

Install the Python test dependencies and run the file-structure tests:

```bash
pip install -r requirements-test.txt && pytest
```

Or step by step:

```bash
pip install -r requirements-test.txt
pytest tests/
```
