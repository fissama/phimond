package transport

import (
	"net/http"
	"net/http/httptest"
	"testing"
)

func corsServer(origins string) *Server {
	return &Server{cors: parseCORSOrigins(origins)}
}

func TestParseCORSOriginsRejectsWildcardAndMalformed(t *testing.T) {
	got := parseCORSOrigins(" http://localhost:5173 ,*, http://x/ ,localhost:1,https://game.example")
	if len(got) != 2 || !got["http://localhost:5173"] || !got["https://game.example"] {
		t.Fatalf("unexpected allowlist: %v", got)
	}
}

func TestCORSDisabledByDefault(t *testing.T) {
	s := corsServer("")
	r := httptest.NewRequest("OPTIONS", "/api/login", nil)
	r.Header.Set("Origin", "http://localhost:5173")
	r.Header.Set("Access-Control-Request-Method", "POST")
	w := httptest.NewRecorder()
	if s.applyCORS(w, r) || w.Header().Get("Access-Control-Allow-Origin") != "" {
		t.Fatal("CORS must be off without GAME_CORS_ORIGINS")
	}
}

func TestCORSPreflightAllowedOrigin(t *testing.T) {
	s := corsServer("http://localhost:5173")
	r := httptest.NewRequest("OPTIONS", "/api/character", nil)
	r.Header.Set("Origin", "http://localhost:5173")
	r.Header.Set("Access-Control-Request-Method", "GET")
	r.Header.Set("Access-Control-Request-Headers", "authorization")
	w := httptest.NewRecorder()
	if !s.applyCORS(w, r) || w.Code != http.StatusNoContent {
		t.Fatalf("preflight not handled: %d", w.Code)
	}
	h := w.Header()
	if h.Get("Access-Control-Allow-Origin") != "http://localhost:5173" || h.Get("Access-Control-Allow-Headers") != "Authorization, Content-Type" {
		t.Fatalf("bad headers: %v", h)
	}
	if h.Get("Access-Control-Allow-Credentials") != "" {
		t.Fatal("credentials must not be allowed")
	}
}

func TestCORSPreflightDeniedOrigin(t *testing.T) {
	s := corsServer("http://localhost:5173")
	r := httptest.NewRequest("OPTIONS", "/api/login", nil)
	r.Header.Set("Origin", "https://evil.example")
	r.Header.Set("Access-Control-Request-Method", "POST")
	w := httptest.NewRecorder()
	if !s.applyCORS(w, r) || w.Code != http.StatusForbidden || w.Header().Get("Access-Control-Allow-Origin") != "" {
		t.Fatalf("denied origin got %d %v", w.Code, w.Header())
	}
}

func TestCORSSimpleRequestHeadersOnlyForAllowedOrigin(t *testing.T) {
	s := corsServer("http://localhost:5173")
	for origin, want := range map[string]string{"http://localhost:5173": "http://localhost:5173", "https://evil.example": ""} {
		r := httptest.NewRequest("GET", "/api/content", nil)
		r.Header.Set("Origin", origin)
		w := httptest.NewRecorder()
		if s.applyCORS(w, r) {
			t.Fatal("simple request must continue to the handler")
		}
		if got := w.Header().Get("Access-Control-Allow-Origin"); got != want {
			t.Fatalf("origin %s got %q want %q", origin, got, want)
		}
		if w.Header().Get("Vary") == "" {
			t.Fatal("Vary: Origin missing")
		}
	}
}
