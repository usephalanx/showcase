# Stage 1: Build the Go binary
FROM golang:1.22-alpine AS builder

WORKDIR /app

COPY go.mod ./
COPY main.go ./

RUN go build -o /hello-api .

# Stage 2: Minimal runtime image
FROM alpine:3.19

RUN apk --no-cache add ca-certificates

COPY --from=builder /hello-api /hello-api

EXPOSE 8080

ENTRYPOINT ["/hello-api"]
