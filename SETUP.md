# Setup Instructions

## Install dependencies

```bash
pip install -r requirements.txt
```

## Run the application

```bash
uvicorn app.main:app --reload
```

## Run tests

```bash
pytest tests/ -v
```

## Default Development User

On first startup the application seeds a default user:

- **Username:** `admin`
- **Password:** `admin123`

This is for development/testing only. Change `SECRET_KEY` in production
via the `SECRET_KEY` environment variable.
