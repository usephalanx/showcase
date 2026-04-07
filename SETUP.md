# Setup Instructions

## Prerequisites

- Node.js >= 18.x
- npm >= 9.x (or pnpm / yarn)

## Installation

```bash
# Navigate to project root
cd .

# Install dependencies
npm install
```

## Development

```bash
# Start the Vite dev server on port 3000
npm run dev
```

## Build

```bash
# Create production build in dist/
npm run build

# Preview production build locally
npm run preview
```

## Testing

```bash
# Run config validation tests (requires Python 3.8+ with pytest)
pip install pytest
pytest tests/
```

## Notes

- Do NOT commit `node_modules/`, `dist/`, or lock files (`package-lock.json`, `yarn.lock`, `pnpm-lock.yaml`).
- Lock files are generated automatically by your package manager during `npm install`.
- The `tsconfig.json` and `tsconfig.node.json` files are hand-written and should be committed.
