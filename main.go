// Package main provides a minimal HTTP server with a health-check endpoint.
package main

import (
	"encoding/json"
	"fmt"
	"net/http"
	"os"
)

// HealthHandler handles requests to the /health endpoint.
// It returns HTTP 200 with a JSON body {"status":"ok"} for GET requests
// and HTTP 405 Method Not Allowed for any other HTTP method.
func HealthHandler(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodGet {
		w.Header().Set("Content-Type", "application/json")
		w.WriteHeader(http.StatusMethodNotAllowed)
		_ = json.NewEncoder(w).Encode(map[string]string{"error": "method not allowed"})
		return
	}

	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(http.StatusOK)
	_, _ = w.Write([]byte(`{"status":"ok"}`))
}

// NewRouter creates and returns a new http.ServeMux with all application
// routes registered. Extracting the mux into its own function allows
// tests to exercise the full routing layer without starting a real server.
func NewRouter() *http.ServeMux {
	mux := http.NewServeMux()
	mux.HandleFunc("/health", HealthHandler)
	return mux
}

func main() {
	port := os.Getenv("PORT")
	if port == "" {
		port = "8080"
	}

	router := NewRouter()

	addr := fmt.Sprintf(":%s", port)
	fmt.Printf("Server listening on %s\n", addr)
	if err := http.ListenAndServe(addr, router); err != nil {
		fmt.Fprintf(os.Stderr, "server error: %v\n", err)
		os.Exit(1)
	}
}
