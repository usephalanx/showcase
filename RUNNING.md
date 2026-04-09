# Hello API — Running Instructions

## TEAM_BRIEF
stack: Go/net-http
test_runner: go test ./...
lint_tool: go vet ./...
coverage_tool: go test -cover
coverage_threshold: 70
coverage_applies: true

## Prerequisites

- **Go 1.22+** (for local development)
- **Docker & Docker Compose** (for containerised startup)

## Local Development

```bash
# Run tests
go test ./... -v

# Run tests with coverage
go test ./... -cover

# Lint
go vet ./...

# Start the server
go run main.go
```

The server listens on port 8080 by default. Override with the `PORT`
environment variable:

```bash
PORT=3000 go run main.go
```

## Docker

```bash
# Build and start
docker compose up --build

# Or build and run manually
docker build -t hello-api .
docker run -p 8080:8080 hello-api
```

## Verify

```bash
curl -s http://localhost:8080/health | jq .
```

Expected response:

```json
{
  "status": "ok"
}
```

## API Contract

### GET /health

| Field        | Value                |
|------------- |----------------------|
| Method       | GET                  |
| Path         | /health              |
| Status       | 200 OK               |
| Content-Type | application/json     |
| Body         | `{"status": "ok"}`   |

Non-GET methods return **405 Method Not Allowed**.  
Unknown routes return **404 Not Found**.
