# Running the Application

This document describes how to install dependencies and run the real estate website locally.

## Prerequisites

- **Node.js** >= 18.x
- **npm** >= 9.x (ships with Node.js 18+)

## Installation

```bash
npm install
```

## Development Server

Start the Vite development server with hot module replacement:

```bash
npm run dev
```

The app will be available at [http://localhost:5173](http://localhost:5173) by default.

## Production Build

Create an optimised production build:

```bash
npm run build
```

The output will be placed in the `dist/` directory.

## Preview Production Build

Serve the production build locally for testing:

```bash
npm run preview
```

## Linting

Run ESLint to check for code quality issues:

```bash
npm run lint
```

## Routes

| Path               | Page                | Description                  |
| ------------------ | ------------------- | ---------------------------- |
| `/`                | HomePage            | Property listings & hero     |
| `/property/:id`    | PropertyDetailPage  | Individual property details  |
| `/contact`         | ContactPage         | Contact form                 |
| `*` (catch-all)    | NotFoundPage        | Styled 404 page              |
