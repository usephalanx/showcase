# Hello World React Application

## TEAM_BRIEF
stack: TypeScript/React+Vite
test_runner: pytest tests/
lint_tool: none
coverage_tool: none
coverage_threshold: 0
coverage_applies: false

## Overview
A minimal React application that renders "Hello World" centered on the page
using inline CSS styles.

## Prerequisites
- Node.js 20+ (or Docker)
- Python 3.9+ with pytest (for running tests)

## Setup

### Local Development
```bash
npm install
npm run dev
```
The app will be available at http://localhost:5173

### Docker
```bash
docker compose up --build
```
The app will be available at http://localhost:5173

## Running Tests
```bash
pip install pytest
pytest tests/
```

## Build for Production
```bash
npm run build
npm run preview
```
