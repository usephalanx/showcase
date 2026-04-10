# Yellow World — Architecture

## Technology Stack

- **Frontend:** Static HTML, CSS, and vanilla JavaScript
- **Server:** Python `http.server` (standard library) serving static files
- **Containerisation:** Docker with `python:3.12-slim` base image
- **Orchestration:** Docker Compose for one-command startup

## File Structure

```
.
├── ARCHITECTURE.md          # This file
├── RUNNING.md               # How to run the application
├── Dockerfile               # Container definition
├── docker-compose.yml       # Compose configuration
├── server.py                # Python HTTP server entry point
├── public/                  # Static assets served by the server
│   ├── index.html           # Main HTML page
│   ├── styles.css           # Yellow-themed stylesheet
│   └── app.js               # Minimal client-side JavaScript
└── tests/                   # Test suite
    └── test_app.py          # Tests for server and static assets
```

## Color Palette

| Token           | Variable            | Hex       | Usage                  |
|-----------------|---------------------|-----------|------------------------|
| Primary Yellow  | `--yellow-primary`  | `#FFD700` | Header background      |
| Background      | `--yellow-bg`       | `#FFF8DC` | Page background        |
| Accent          | `--yellow-accent`   | `#FFC107` | Footer background      |
| Text Dark       | `--text-dark`       | `#333333` | Body / paragraph text  |
| Heading Text    | `--text-heading`    | `#1A1A00` | h1 heading color       |

## Layout Design

Single-page layout with vertically centred content:

1. **Header** — Full-width bar with primary yellow background and app title.
2. **Main** — Flex-centred area containing the large "Yellow World" greeting
   (`h1.greeting`) and a subtitle paragraph.
3. **Footer** — Accent-coloured bar with copyright text.

The page uses `min-height: 100vh` with flexbox column layout so the footer
sticks to the bottom even when content is short.

## Python Server

`server.py` uses `http.server.SimpleHTTPRequestHandler` with its `directory`
parameter pointed at `public/`.  The port defaults to **8000** and can be
overridden via the `PORT` environment variable.  The server binds to
`0.0.0.0` so it is accessible inside Docker containers.

## Docker Strategy

- **Base image:** `python:3.12-slim` (no extra dependencies needed).
- Only `public/` and `server.py` are copied into the image.
- Port 8000 is exposed and mapped by Docker Compose.
