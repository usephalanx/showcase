package main

import (
	"encoding/json"
	"io"
	"net/http"
	"net/http/httptest"
	"testing"
)

// TestHealthHandler_ReturnsOKStatus verifies that GET /health returns HTTP 200,
// Content-Type application/json, and the body {"status":"ok"}.
func TestHealthHandler_ReturnsOKStatus(t *testing.T) {
	req := httptest.NewRequest(http.MethodGet, "/health", nil)
	rec := httptest.NewRecorder()

	HealthHandler(rec, req)

	res := rec.Result()
	defer res.Body.Close()

	if res.StatusCode != http.StatusOK {
		t.Fatalf("expected status 200, got %d", res.StatusCode)
	}

	ct := res.Header.Get("Content-Type")
	if ct != "application/json" {
		t.Fatalf("expected Content-Type application/json, got %q", ct)
	}

	body, err := io.ReadAll(res.Body)
	if err != nil {
		t.Fatalf("failed to read body: %v", err)
	}

	expected := `{"status":"ok"}`
	var got map[string]string
	if err := json.Unmarshal(body, &got); err != nil {
		t.Fatalf("body is not valid JSON: %v (raw: %s)", err, string(body))
	}
	if got["status"] != "ok" {
		t.Fatalf("expected body %s, got %s", expected, string(body))
	}
}

// TestHealthHandler_MethodNotAllowed verifies that non-GET methods to /health
// return HTTP 405.
func TestHealthHandler_MethodNotAllowed(t *testing.T) {
	methods := []string{http.MethodPost, http.MethodPut, http.MethodDelete, http.MethodPatch}

	for _, method := range methods {
		t.Run(method, func(t *testing.T) {
			req := httptest.NewRequest(method, "/health", nil)
			rec := httptest.NewRecorder()

			HealthHandler(rec, req)

			res := rec.Result()
			defer res.Body.Close()

			if res.StatusCode != http.StatusMethodNotAllowed {
				t.Fatalf("expected status 405 for %s, got %d", method, res.StatusCode)
			}
		})
	}
}

// TestHealthHandler_ResponseBodyIsValidJSON unmarshals the response body into a
// map and asserts the "status" key equals "ok".
func TestHealthHandler_ResponseBodyIsValidJSON(t *testing.T) {
	req := httptest.NewRequest(http.MethodGet, "/health", nil)
	rec := httptest.NewRecorder()

	HealthHandler(rec, req)

	res := rec.Result()
	defer res.Body.Close()

	body, err := io.ReadAll(res.Body)
	if err != nil {
		t.Fatalf("failed to read body: %v", err)
	}

	var parsed map[string]string
	if err := json.Unmarshal(body, &parsed); err != nil {
		t.Fatalf("body is not valid JSON: %v (raw: %s)", err, string(body))
	}

	if val, ok := parsed["status"]; !ok || val != "ok" {
		t.Fatalf("expected {\"status\":\"ok\"}, got %v", parsed)
	}
}

// TestNewRouter_HealthRouteRegistered creates an httptest server with NewRouter
// and verifies that GET /health returns HTTP 200.
func TestNewRouter_HealthRouteRegistered(t *testing.T) {
	server := httptest.NewServer(NewRouter())
	defer server.Close()

	resp, err := http.Get(server.URL + "/health")
	if err != nil {
		t.Fatalf("request failed: %v", err)
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusOK {
		t.Fatalf("expected status 200, got %d", resp.StatusCode)
	}

	body, err := io.ReadAll(resp.Body)
	if err != nil {
		t.Fatalf("failed to read body: %v", err)
	}

	var parsed map[string]string
	if err := json.Unmarshal(body, &parsed); err != nil {
		t.Fatalf("body is not valid JSON: %v", err)
	}

	if parsed["status"] != "ok" {
		t.Fatalf("expected status ok, got %q", parsed["status"])
	}
}

// TestUnknownRoute_Returns404 verifies that a request to an unregistered path
// returns HTTP 404.
func TestUnknownRoute_Returns404(t *testing.T) {
	server := httptest.NewServer(NewRouter())
	defer server.Close()

	resp, err := http.Get(server.URL + "/nonexistent")
	if err != nil {
		t.Fatalf("request failed: %v", err)
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusNotFound {
		t.Fatalf("expected status 404, got %d", resp.StatusCode)
	}
}
