# Architecture

## Overview

This is a minimal "Hello World" web application consisting of a single
static HTML page served by Python's built-in HTTP server.  No external
frameworks, databases, or build tools are required.

## File Structure

```
.
├── index.html           # Static HTML page displaying "Hello World"
├── server.py            # Python HTTP server (stdlib only)
├── Dockerfile           # Container image definition
├── docker-compose.yml   # One-command container orchestration
├── RUNNING.md           # Instructions for running the application
├── ARCHITECTURE.md      # This file – architecture documentation
└── tests/
    └── test_server.py   # Automated tests for the server
```

## Technology Choices

| Component      | Choice                                  | Rationale                                         |
| -------------- | --------------------------------------- | ------------------------------------------------- |
| Web server     | `http.server` (Python standard library) | Zero dependencies; ships with every Python 3 install |
| Containerisation | Docker + Docker Compose               | Reproducible environment; single-command startup   |
| Frontend       | Plain HTML + inline CSS                 | No build step needed for a single static page      |
| Testing        | `unittest` (Python standard library)    | No extra test runner required                      |

## How It Works

1. `server.py` starts a `TCPServer` on `0.0.0.0:8000` using
   `SimpleHTTPRequestHandler` pointed at the current working directory.
2. When a browser requests `/`, the handler automatically serves
   `index.html` as the directory index.
3. `index.html` renders a centred "Hello World" heading on a white
   background.

## Design Decisions

* **No framework** – A full web framework (Flask, FastAPI, etc.) would
  be overkill for serving a single static file.  The standard library
  provides everything needed.
* **Bind to `0.0.0.0`** – Ensures the server is reachable from outside
  a Docker container (where `127.0.0.1` would not be accessible from
  the host).
* **`allow_reuse_address = True`** – Prevents "Address already in use"
  errors during quick restart cycles in development.
* **`functools.partial`** – Used to pass the `directory` argument to
  `SimpleHTTPRequestHandler` cleanly, avoiding a custom subclass.
