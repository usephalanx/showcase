# Running the Hello World App

## Prerequisites

### With Docker

* [Docker](https://docs.docker.com/get-docker/) (v20+ recommended)
* [Docker Compose](https://docs.docker.com/compose/install/) (v2+)

### Without Docker

* [Python 3](https://www.python.org/downloads/) (3.8 or later)

## Quick Start (Docker)

```bash
# 1. Clone the repository and enter the directory
git clone <repo-url> && cd <repo-directory>

# 2. Build and start the container
docker compose up --build -d

# 3. Open in your browser
open http://localhost:8000   # macOS
# or visit http://localhost:8000 manually
```

## Quick Start (Without Docker)

```bash
# 1. Clone the repository and enter the directory
git clone <repo-url> && cd <repo-directory>

# 2. Start the server
python server.py

# 3. Open http://localhost:8000 in your browser
```

## Stop the App

### Docker

```bash
docker compose down
```

### Without Docker

Press `Ctrl+C` in the terminal where `server.py` is running.

## Running Tests

```bash
python -m pytest tests/ -v
```

## What You Should See

A white page with the text **Hello World** centred on the screen.

> **Note:** No authentication or demo credentials are required.
