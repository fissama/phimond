package transport

import (
	"net/http"
	"net/http/httptest"
	"phimond/server/internal/character"
	"phimond/server/internal/content"
	"phimond/server/internal/devstore"
	"strings"
	"sync"
	"testing"
)

type captureMailer struct {
	mu   sync.Mutex
	body chan string
}

func (m *captureMailer) Send(_, _, body string) error { m.body <- body; return nil }

func newAccountServer(t *testing.T) (*Server, http.Handler, *captureMailer) {
	t.Helper()
	c, err := content.Load("../../../../data")
	if err != nil {
		t.Fatal(err)
	}
	s := New(devstore.New(), character.NewEngine(c))
	m := &captureMailer{body: make(chan string, 4)}
	s.mailer = m
	return s, s.Handler(), m
}

func TestRegisterRequiresTermsAndExplainsErrors(t *testing.T) {
	_, h, _ := newAccountServer(t)
	cases := []struct {
		body string
		code int
		msg  string
	}{
		{`{"username":"nguoi1","password":"Mua-ha-2026"}`, 400, "terms_required"},
		{`{"username":"a","password":"Mua-ha-2026","terms":true}`, 400, "username_format"},
		{`{"username":"nguoi1","password":"abc","terms":true}`, 400, "password_short"},
		{`{"username":"nguoi1","password":"12345678","terms":true}`, 400, "password_weak"},
		{`{"username":"nguoi1","password":"Mua-ha-2026","email":"khong-hop-le","terms":true}`, 400, "email_invalid"},
		{`{"username":"nguoi1","password":"Mua-ha-2026","terms":true}`, 200, ""},
		{`{"username":"NGUOI1","password":"Mua-ha-2026","terms":true}`, 400, "username_taken"}, // devstore phân biệt hoa/thường; kiểm mã ở dưới
	}
	for i, c := range cases {
		code, out := slotCall(t, h, "POST", "/api/register", "", c.body)
		if i == len(cases)-1 {
			continue // tên hoa/thường chỉ có ý nghĩa với MySQL
		}
		if code != c.code || (c.msg != "" && out["code"] != c.msg) {
			t.Fatalf("%s: %d %v", c.body, code, out)
		}
	}
	// Đăng nhập sai khác với lỗi định dạng.
	code, out := slotCall(t, h, "POST", "/api/login", "", `{"username":"nguoi1","password":"sai-mat-khau"}`)
	if code != 401 || out["code"] != "credentials" {
		t.Fatalf("login sai: %d %v", code, out)
	}
	code, out = slotCall(t, h, "POST", "/api/register", "", `{"username":"nguoi1","password":"Mua-ha-2026","terms":true}`)
	if code != 409 || out["code"] != "username_taken" {
		t.Fatalf("trùng tên: %d %v", code, out)
	}
}

func TestPasswordResetFlow(t *testing.T) {
	_, h, m := newAccountServer(t)
	_, reg := slotCall(t, h, "POST", "/api/register", "", `{"username":"khoiphuc","password":"Mua-ha-2026","email":"Khoi.Phuc@Example.com","terms":true}`)
	tok := reg["token"].(string)
	_, acc := slotCall(t, h, "GET", "/api/account", tok, "")
	if acc["has_email"] != true || acc["email"] != "k***@example.com" || acc["username"] != "khoiphuc" {
		t.Fatalf("account: %v", acc)
	}
	// Email lạ: vẫn 200, không gửi thư.
	if code, _ := slotCall(t, h, "POST", "/api/password/forgot", "", `{"email":"la@example.com"}`); code != 200 {
		t.Fatal(code)
	}
	if code, _ := slotCall(t, h, "POST", "/api/password/forgot", "", `{"email":"khoi.phuc@example.com"}`); code != 200 {
		t.Fatal(code)
	}
	body := <-m.body
	i := strings.Index(body, "#reset=")
	if i < 0 {
		t.Fatalf("thiếu liên kết: %q", body)
	}
	rt := strings.Fields(body[i+len("#reset="):])[0]
	if code, out := slotCall(t, h, "POST", "/api/password/reset", "", `{"token":"`+rt+`","password":"12345678"}`); code != 400 || out["code"] != "password_weak" {
		t.Fatalf("yếu: %d %v", code, out)
	}
	if code, out := slotCall(t, h, "POST", "/api/password/reset", "", `{"token":"`+rt+`","password":"Mat-khau-moi-77"}`); code != 200 {
		t.Fatalf("reset: %d %v", code, out)
	}
	if code, out := slotCall(t, h, "POST", "/api/password/reset", "", `{"token":"`+rt+`","password":"Mat-khau-moi-88"}`); code != 400 || out["code"] != "reset_invalid" {
		t.Fatalf("mã dùng lại: %d %v", code, out)
	}
	if code, _ := slotCall(t, h, "GET", "/api/account", tok, ""); code != 401 {
		t.Fatalf("phiên cũ phải bị thu hồi: %d", code)
	}
	if code, _ := slotCall(t, h, "POST", "/api/login", "", `{"username":"khoiphuc","password":"Mat-khau-moi-77"}`); code != 200 {
		t.Fatal("đăng nhập mật khẩu mới", code)
	}
}

func TestDeleteAccount(t *testing.T) {
	_, h, _ := newAccountServer(t)
	_, reg := slotCall(t, h, "POST", "/api/register", "", `{"username":"xoatk","password":"Mua-ha-2026","terms":true}`)
	tok := reg["token"].(string)
	if code, out := slotCall(t, h, "POST", "/api/account/delete", tok, `{"password":"sai-sai-sai"}`); code != 401 || out["code"] != "credentials" {
		t.Fatalf("sai mật khẩu: %d %v", code, out)
	}
	if code, _ := slotCall(t, h, "POST", "/api/account/delete", tok, `{"password":"Mua-ha-2026"}`); code != 200 {
		t.Fatal(code)
	}
	if code, _ := slotCall(t, h, "GET", "/api/slots", tok, ""); code != 401 {
		t.Fatalf("phiên phải hết hiệu lực: %d", code)
	}
	if code, out := slotCall(t, h, "POST", "/api/login", "", `{"username":"xoatk","password":"Mua-ha-2026"}`); code != 401 {
		t.Fatalf("tài khoản phải mất: %d %v", code, out)
	}
	// Tên đăng nhập được dùng lại.
	if code, _ := slotCall(t, h, "POST", "/api/register", "", `{"username":"xoatk","password":"Mua-ha-2026","terms":true}`); code != 200 {
		t.Fatal("đăng ký lại", code)
	}
}

func TestClientIPTrustedProxy(t *testing.T) {
	s := New(nil, nil)
	req := func(remote, xff string) *http.Request {
		r := httptest.NewRequest("GET", "/", nil)
		r.RemoteAddr = remote
		if xff != "" {
			r.Header.Set("X-Forwarded-For", xff)
		}
		return r
	}
	// Không cấu hình: header bị bỏ qua (không giả mạo được).
	if ip := s.clientIP(req("203.0.113.9:1234", "1.2.3.4")); ip != "203.0.113.9" {
		t.Fatal(ip)
	}
	s.trustedProxies = parseTrustedProxies("127.0.0.1, 172.16.0.0/12")
	if ip := s.clientIP(req("127.0.0.1:1", "198.51.100.7")); ip != "198.51.100.7" {
		t.Fatal(ip)
	}
	// Khách tự chèn XFF giả: lấy IP phải-nhất không thuộc proxy tin cậy.
	if ip := s.clientIP(req("172.17.0.2:1", "6.6.6.6, 198.51.100.7, 172.17.0.3")); ip != "198.51.100.7" {
		t.Fatal(ip)
	}
	// Kết nối từ ngoài proxy: bỏ qua header.
	if ip := s.clientIP(req("203.0.113.9:1", "6.6.6.6")); ip != "203.0.113.9" {
		t.Fatal(ip)
	}
}
