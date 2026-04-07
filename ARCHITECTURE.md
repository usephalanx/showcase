# Architecture

## Overview

This project is a single static HTML page served by Python's built-in
HTTP server.  There are no frameworks, no databases, and no build steps.

## File Structure

| File                  | Purpose                                                        |
|-----------------------|----------------------------------------------------------------|
| `index.html`          | Static HTML page displaying "Hello World" on a white background|
| `server.py`           | Python HTTP server using `http.server` from the standard lib   |
| `Dockerfile`          | Container image definition (Python 3.12-slim base)             |
| `docker-compose.yml`  | One-command orchestration via Docker Compose                   |
| `RUNNING.md`          | Instructions to build and run the application                  |
| `ARCHITECTURE.md`     | This file – documents architecture and design decisions        |
| `tests/test_server.py`| Automated tests verifying the server and HTML content          |

## Technology Choices

* **Python 3 standard library** – `http.server.SimpleHTTPRequestHandler`
  provides a zero-dependency static file server.
* **No framework** – the app serves a single static page; adding Flask,
  FastAPI, or similar would be unnecessary overhead.
* **No database** – there is no dynamic data to persist.

## How It Works

1. `server.py` starts an HTTP server on port **8000**, bound to
   `0.0.0.0`, serving files from the working directory.
2. When a browser requests `/`, the server returns `index.html`.
3. `index.html` uses minimal inline CSS to centre the text "Hello World"
   both vertically and horizontally on a white (`#ffffff`) background.

## Design Decisions

* **Inline CSS** – a single `<style>` block keeps the project to one
  HTML file, which is the simplest possible deployment unit.
* **Flexbox centring** – `display: flex` with `justify-content` and
  `align-items` is the most widely supported modern centring technique.
* **`0.0.0.0` binding** – required so the server is reachable from the
  host when running inside Docker.
