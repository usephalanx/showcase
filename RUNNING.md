# Hello API — Running Instructions

## TEAM_BRIEF
stack: Go/net-http
test_runner: go test ./...
lint_tool: go vet ./...
coverage_tool: go test -cover
coverage_threshold: 70
coverage_applies: true

## Prerequisites

- **Go 1.22+** installed, OR
- **Docker** and **Docker Compose** installed

## Run Tests

```bash
go test ./... -v
```

With coverage:

```bash
go test ./... -cover
```

## Run Locally (without Docker)

```bash
go run main.go
```

The server starts on port 8080 by default. Set the `PORT` environment
variable to override:

```bash
PORT=3000 go run main.go
```

## Run with Docker Compose

```bash
docker compose up --build
```

## Verify

```bash
curl -i http://localhost:8080/health
```

Expected response:

```
HTTP/1.1 200 OK
Content-Type: application/json

{"status":"ok"}
```

## API Contract

### GET /health

| Field        | Value              |
|-------------|--------------------|
| Method       | GET                |
| Path         | /health            |
| Status       | 200 OK             |
| Content-Type | application/json   |
| Body         | `{"status":"ok"}` |

Non-GET methods return **405 Method Not Allowed**.
Unknown paths return **404 Not Found**.
