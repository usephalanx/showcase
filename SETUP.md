# Setup Instructions

After cloning the repository, run the following commands to install
dependencies and generate lock files:

```bash
# Install Node.js dependencies (generates package-lock.json and node_modules/)
npm install

# Install Python test dependencies
pip install pytest
```

Do **not** commit `node_modules/`, `package-lock.json`, or `dist/` to
version control — they are generated artefacts.
