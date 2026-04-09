// Package main implements a minimal HTTP server with a health check endpoint.
package main

import (
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"os"
)

// healthResponse represents the JSON body returned by the /health endpoint.
type healthResponse struct {
	Status string `json:"status"`
}

// HealthHandler writes a JSON response with {"status":"ok"} and HTTP 200.
// It only accepts GET requests; all other methods receive 405 Method Not Allowed.
func HealthHandler(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodGet {
		w.Header().Set("Content-Type", "application/json")
		w.WriteHeader(http.StatusMethodNotAllowed)
		return
	}

	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(http.StatusOK)

	resp := healthResponse{Status: "ok"}
	_ = json.NewEncoder(w).Encode(resp)
}

// NewRouter creates and returns an *http.ServeMux with all application routes
// registered. Extracting this into its own function enables testing without
// starting a real server.
func NewRouter() *http.ServeMux {
	mux := http.NewServeMux()
	mux.HandleFunc("GET /health", HealthHandler)
	return mux
}

func main() {
	port := os.Getenv("PORT")
	if port == "" {
		port = "8080"
	}

	router := NewRouter()
	addr := fmt.Sprintf(":%s", port)
	log.Printf("listening on %s", addr)
	if err := http.ListenAndServe(addr, router); err != nil {
		log.Fatalf("server failed: %v", err)
	}
}
