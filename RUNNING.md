# Running the Hello World App

## Prerequisites

* [Docker](https://docs.docker.com/get-docker/) (v20+ recommended)
* [Docker Compose](https://docs.docker.com/compose/install/) (v2+)

## Quick Start

```bash
# 1. Clone the repository and enter the directory
git clone <repo-url> && cd <repo-directory>

# 2. Build and start the container
docker compose up --build -d

# 3. Open in your browser
open http://localhost:8000   # macOS
# or visit http://localhost:8000 manually
```

## Stop the App

```bash
docker compose down
```

## Running Without Docker

```bash
python server.py
# Then open http://localhost:8000
```

## Running Tests

```bash
python -m pytest tests/ -v
```

## What You Should See

A white page with the text **Hello World** centred on the screen.

> **Note:** No authentication or demo credentials are required.
