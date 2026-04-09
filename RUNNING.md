# Running the Application

## Prerequisites

- Node.js >= 18
- npm >= 9

## Install Dependencies

```bash
npm install
```

## Development Server

Start the Vite development server on port 3000:

```bash
npm run dev
```

Open <http://localhost:3000> in your browser.

## Build for Production

```bash
npm run build
```

The output will be in the `dist/` directory.

## Preview Production Build

```bash
npm run preview
```

## Run Frontend Tests (Vitest)

```bash
npm test
```

## Run Structure Tests (pytest)

```bash
pip install pytest
pytest tests/test_structure.py -v
```
