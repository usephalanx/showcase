# Setup Instructions

The following lock and generated files are **not** committed to the
repository and must be produced locally via the project's own toolchain.

## Node.js dependencies

```bash
npm install
```

This generates:
- `package-lock.json`
- `node_modules/`

## TypeScript compilation check

```bash
npx tsc --noEmit
```

## Production build

```bash
npm run build
```

This generates the `dist/` directory.
