# Hello World React App

## TEAM_BRIEF
stack: TypeScript/React+Vite
test_runner: pytest tests/
lint_tool: none
coverage_tool: none
coverage_threshold: 0
coverage_applies: false

## Overview

A minimal React + TypeScript application bootstrapped with Vite that
renders a centered "Hello World" heading.

## Prerequisites

- **Node.js** >= 20
- **npm** (bundled with Node.js)
- **Python** >= 3.9 (for running the structural test suite)
- **Docker** & **Docker Compose** (optional, for containerised development)

## Quick Start (Local)

```bash
npm install
npm run dev
```

Open http://localhost:5173 in your browser.

## Quick Start (Docker)

```bash
docker compose up --build
```

## Build for Production

```bash
npm run build
npm run preview
```

## Running Tests

The test suite uses **pytest** and validates the project file structure
and content — no Node.js runtime is required for tests.

```bash
pip install pytest
pytest tests/
```
