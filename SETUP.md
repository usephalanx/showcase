# Setup Instructions

This document describes how to generate tooling-managed files that are
not committed to the repository.

## Node.js Dependencies

Run the following command from the project root to install JavaScript
dependencies and generate `package-lock.json` and `node_modules/`:

```bash
npm install
```

## Python Test Dependencies

Install pytest to run the structural tests:

```bash
pip install pytest
```

Then run:

```bash
pytest tests/test_structure.py -v
```
