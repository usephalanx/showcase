# Setup

After cloning the repository, install the Python dependencies:

```bash
pip install -r requirements.txt
```

No lock files are committed to the repository.  The `requirements.txt`
file pins compatible version ranges.  To generate a fully pinned lock
file for reproducible installs:

```bash
pip freeze > requirements-lock.txt
```
