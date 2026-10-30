package transport

import (
	"encoding/json"
	"net/http"
	"net/http/httptest"
	"phimond/server/internal/character"
	"phimond/server/internal/content"
	"phimond/server/internal/devstore"
	"strings"
	"testing"
)

func slotCall(t *testing.T, h http.Handler, method, path, tok, body string) (int, map[string]any) {
	t.Helper()
	r := httptest.NewRequest(method, path, strings.NewReader(body))
	if tok != "" {
		r.Header.Set("Authorization", "Bearer "+tok)
	}
	w := httptest.NewRecorder()
	h.ServeHTTP(w, r)
	var out map[string]any
	_ = json.Unmarshal(w.Body.Bytes(), &out)
	return w.Code, out
}

// Ba ô nhân vật độc lập: đăng ký chỉ tạo bản nháp, mỗi ô có id riêng, chọn ô đổi nhân vật của phiên.
func TestCharacterSlotsAreIndependent(t *testing.T) {
	c, err := content.Load("../../../../data")
	if err != nil {
		t.Fatal(err)
	}
	s := New(devstore.New(), character.NewEngine(c))
	h := s.Handler()
	code, reg := slotCall(t, h, "POST", "/api/register", "", `{"username":"slotuser","password":"matkhau-12345","terms":true}`)
	if code != 200 {
		t.Fatalf("register %d", code)
	}
	tok := reg["token"].(string)
	_, list := slotCall(t, h, "GET", "/api/slots", tok, "")
	for _, sl := range list["slots"].([]any) {
		if !sl.(map[string]any)["empty"].(bool) {
			t.Fatalf("ô phải trống sau đăng ký: %v", sl)
		}
	}
	ids := map[string]bool{}
	for _, slot := range []string{"0", "1", "2"} {
		code, sel := slotCall(t, h, "POST", "/api/slots/select", tok, `{"slot":`+slot+`}`)
		if code != 200 {
			t.Fatalf("select %s: %d", slot, code)
		}
		id := sel["character_id"].(string)
		if ids[id] {
			t.Fatalf("ô %s trùng id nhân vật", slot)
		}
		ids[id] = true
		_, ch := slotCall(t, h, "GET", "/api/character", tok, "")
		if ch["id"] != id || ch["draft"] != true {
			t.Fatalf("ô %s: nhân vật của phiên không đổi theo ô: %v", slot, ch["id"])
		}
	}
	if code, _ := slotCall(t, h, "POST", "/api/slots/select", tok, `{"slot":3}`); code != 400 {
		t.Fatalf("ô 3 phải bị từ chối, got %d", code)
	}
	if code, _ := slotCall(t, h, "GET", "/api/slots", "", ""); code != 401 {
		t.Fatalf("thiếu token: %d", code)
	}
}
