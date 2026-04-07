# Running the Todo Application

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/) and [Docker Compose](https://docs.docker.com/compose/install/) installed.

## Quick Start

```bash
# 1. Build and start the application
docker compose up --build

# 2. Open in your browser
#    http://localhost:5173
```

## Stopping

```bash
docker compose down
```

## Notes

- No authentication is required — there is no backend dependency for the frontend.
- No demo credentials are needed.
- The frontend dev server runs on port **5173** by default.
