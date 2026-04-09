# Setup — Generated / Lock Files

The following files are **not** committed to the repository and must be
generated locally by running the commands below.

## Python Virtual Environment & Lock Files

```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate

# Install dependencies (generates .venv/, __pycache__/, *.egg-info/)
pip install -r requirements.txt
```

## Docker

```bash
# Build the image (generates build cache layers)
docker compose build
```

Do **not** commit `.venv/`, `__pycache__/`, `*.egg-info/`, or `build/`
directories.
