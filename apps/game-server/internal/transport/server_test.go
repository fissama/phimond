package transport

import (
	"net/http"
	"net/http/httptest"
	"phimond/server/internal/character"
	"phimond/server/internal/content"
	"strings"
	"testing"
)

func TestPublicContentAndStrictAuthBoundary(t *testing.T) {
	c, err := content.Load("../../../../data")
	if err != nil {
		t.Fatal(err)
	}
	s := New(nil, character.NewEngine(c))
	h := s.Handler()
	for _, tt := range []struct {
		path string
		code int
	}{{"/api/content", 200}, {"/api/character", 401}, {"/api/lineage/other", 401}, {"/api/battles", 401}} {
		w := httptest.NewRecorder()
		h.ServeHTTP(w, httptest.NewRequest("GET", tt.path, nil))
		if w.Code != tt.code {
			t.Fatalf("%s: %d", tt.path, w.Code)
		}
	}
}
func TestRejectMalformedCredentialsBeforeStore(t *testing.T) {
	s := New(nil, nil)
	for _, body := range []string{`{`, strings.Repeat("x", 17000), `{"username":"a","password":"b","gold":1000}`} {
		w := httptest.NewRecorder()
		s.Handler().ServeHTTP(w, httptest.NewRequest(http.MethodPost, "/api/register", strings.NewReader(body)))
		if w.Code != 400 && w.Code != 413 {
			t.Fatalf("got %d", w.Code)
		}
	}
}
