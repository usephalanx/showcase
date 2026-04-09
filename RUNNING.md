# Hello API — Running Instructions

## TEAM_BRIEF
stack: Go/net-http
test_runner: go test ./...
lint_tool: go vet ./...
coverage_tool: go test -cover
coverage_threshold: 70
coverage_applies: true

## Prerequisites

- **Go 1.22+** installed ([https://go.dev/dl/](https://go.dev/dl/)), OR
- **Docker** and **Docker Compose** installed.

## Run Locally (without Docker)

```bash
# Build and start the server
go run main.go
```

The server listens on port `8080` by default. Override with the `PORT` environment variable:

```bash
PORT=3000 go run main.go
```

## Run with Docker Compose

```bash
docker compose up --build
```

The API will be available at `http://localhost:8080`.

## Run Tests

```bash
go test ./...
```

With coverage:

```bash
go test -cover ./...
```

Verbose output:

```bash
go test -v ./...
```

## Lint

```bash
go vet ./...
```

## Verify the Health Endpoint

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

### `GET /health`

| Field         | Value              |
|---------------|--------------------|
| Method        | `GET`              |
| Path          | `/health`          |
| Status Code   | `200 OK`           |
| Content-Type  | `application/json` |
| Response Body | `{"status":"ok"}` |

Non-GET methods return `405 Method Not Allowed`.
Unknown routes return `404 Not Found`.
