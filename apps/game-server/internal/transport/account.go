package transport

import (
	"context"
	"errors"
	"fmt"
	"log"
	"net"
	"net/http"
	"net/smtp"
	"net/url"
	"os"
	"strings"
	"time"

	"phimond/server/internal/persistence"
)

// AccountStorage là phần tài khoản nâng cao (email khôi phục, đặt lại mật khẩu, xoá tài khoản). Kho nào không hỗ trợ thì các đường này trả 501.
type AccountStorage interface {
	AccountInfo(ctx context.Context, token string) (persistence.AccountInfo, error)
	SetEmail(ctx context.Context, token, email string) error
	CreatePasswordReset(ctx context.Context, email string) (token, username string, found bool, err error)
	ResetPassword(ctx context.Context, token, newPassword string) error
	DeleteAccount(ctx context.Context, token, password string) ([]string, error)
}

// Mailer gửi thư giao dịch (chỉ thư đặt lại mật khẩu).
type Mailer interface {
	Send(to, subject, body string) error
}

type logMailer struct{}

// Send chỉ ghi log: dùng khi chưa cấu hình SMTP (dev). Nội dung thư có chứa mã đặt lại, KHÔNG dùng ở production.
func (logMailer) Send(to, subject, body string) error {
	log.Printf("MAIL (chưa cấu hình SMTP, chỉ ghi log) to=%s subject=%q\n%s", to, subject, body)
	return nil
}

type smtpMailer struct{ addr, user, pass, from string }

func (m smtpMailer) Send(to, subject, body string) error {
	host, _, _ := net.SplitHostPort(m.addr)
	var auth smtp.Auth
	if m.user != "" {
		auth = smtp.PlainAuth("", m.user, m.pass, host)
	}
	msg := "From: " + m.from + "\r\nTo: " + to + "\r\nSubject: " + subject + "\r\nMIME-Version: 1.0\r\nContent-Type: text/plain; charset=UTF-8\r\n\r\n" + body
	return smtp.SendMail(m.addr, auth, m.from, []string{to}, []byte(msg))
}

// mailerFromEnv: GAME_SMTP_ADDR (host:port), GAME_SMTP_USER, GAME_SMTP_PASS, GAME_MAIL_FROM.
func mailerFromEnv() Mailer {
	addr := os.Getenv("GAME_SMTP_ADDR")
	if addr == "" {
		return logMailer{}
	}
	from := os.Getenv("GAME_MAIL_FROM")
	if from == "" {
		from = os.Getenv("GAME_SMTP_USER")
	}
	return smtpMailer{addr: addr, user: os.Getenv("GAME_SMTP_USER"), pass: os.Getenv("GAME_SMTP_PASS"), from: from}
}

func parseTrustedProxies(v string) []*net.IPNet {
	var out []*net.IPNet
	for _, p := range strings.Split(v, ",") {
		p = strings.TrimSpace(p)
		if p == "" {
			continue
		}
		if !strings.Contains(p, "/") {
			if strings.Contains(p, ":") {
				p += "/128"
			} else {
				p += "/32"
			}
		}
		if _, n, e := net.ParseCIDR(p); e == nil {
			out = append(out, n)
		} else {
			log.Printf("GAME_TRUSTED_PROXIES: bỏ qua %q: %v", p, e)
		}
	}
	return out
}

func (s *Server) trusted(ip net.IP) bool {
	for _, n := range s.trustedProxies {
		if n.Contains(ip) {
			return true
		}
	}
	return false
}

// clientIP trả IP khách. Chỉ tin X-Forwarded-For/X-Real-IP khi kết nối đến từ proxy trong GAME_TRUSTED_PROXIES; ngược lại dùng RemoteAddr (không giả mạo được).
func (s *Server) clientIP(r *http.Request) string {
	host, _, _ := net.SplitHostPort(r.RemoteAddr)
	peer := net.ParseIP(host)
	if peer == nil || !s.trusted(peer) {
		return host
	}
	parts := strings.Split(r.Header.Get("X-Forwarded-For"), ",")
	for i := len(parts) - 1; i >= 0; i-- {
		ip := net.ParseIP(strings.TrimSpace(parts[i]))
		if ip == nil {
			continue
		}
		if !s.trusted(ip) {
			return ip.String()
		}
	}
	if ip := net.ParseIP(strings.TrimSpace(r.Header.Get("X-Real-IP"))); ip != nil {
		return ip.String()
	}
	return host
}

func failCode(w http.ResponseWriter, status int, code, msg string) {
	jsonResponse(w, status, map[string]string{"message": msg, "code": code})
}

// credentialError ánh xạ lỗi kho sang mã ổn định cho client.
func credentialError(w http.ResponseWriter, err error) {
	switch {
	case errors.Is(err, persistence.ErrUsernameFormat):
		failCode(w, 400, "username_format", "Tên đăng nhập gồm 3–24 ký tự chữ, số hoặc gạch dưới.")
	case errors.Is(err, persistence.ErrPasswordShort):
		failCode(w, 400, "password_short", "Mật khẩu cần ít nhất 8 ký tự.")
	case errors.Is(err, persistence.ErrPasswordLong):
		failCode(w, 400, "password_long", "Mật khẩu tối đa 72 ký tự.")
	case errors.Is(err, persistence.ErrPasswordWeak):
		failCode(w, 400, "password_weak", "Mật khẩu quá dễ đoán (phổ biến, lặp một ký tự hoặc trùng tên đăng nhập). Hãy chọn mật khẩu khác.")
	case errors.Is(err, persistence.ErrUsernameTaken):
		failCode(w, 409, "username_taken", "Tên đăng nhập này đã có người dùng.")
	case errors.Is(err, persistence.ErrSession):
		failCode(w, 401, "session", "Phiên đăng nhập đã hết hạn, hãy đăng nhập lại.")
	case errors.Is(err, persistence.ErrCredentials):
		failCode(w, 401, "credentials", "Sai tên đăng nhập hoặc mật khẩu.")
	case errors.Is(err, persistence.ErrEmailInvalid):
		failCode(w, 400, "email_invalid", "Địa chỉ email chưa hợp lệ.")
	case errors.Is(err, persistence.ErrEmailTaken):
		failCode(w, 409, "email_taken", "Email này đã gắn với tài khoản khác.")
	case errors.Is(err, persistence.ErrResetToken):
		failCode(w, 400, "reset_invalid", "Liên kết đặt lại mật khẩu không hợp lệ hoặc đã hết hạn.")
	default:
		failCode(w, 500, "server", "Máy chủ gặp lỗi, thử lại sau.")
	}
}

func (s *Server) accounts(w http.ResponseWriter) (AccountStorage, bool) {
	a, ok := s.Store.(AccountStorage)
	if !ok || s.Store == nil {
		failCode(w, 501, "unsupported", "Tính năng này chưa bật trên máy chủ.")
		return nil, false
	}
	return a, true
}

func maskEmail(e string) string {
	at := strings.LastIndexByte(e, '@')
	if at < 1 {
		return ""
	}
	return e[:1] + "***" + e[at:]
}

func (s *Server) registerAccountRoutes(mux *http.ServeMux) {
	mux.HandleFunc("GET /api/account", func(w http.ResponseWriter, r *http.Request) {
		if _, ok := s.authenticate(w, r); !ok {
			return
		}
		a, ok := s.accounts(w)
		if !ok {
			return
		}
		info, e := a.AccountInfo(r.Context(), token(r))
		if e != nil {
			credentialError(w, e)
			return
		}
		jsonResponse(w, 200, map[string]any{"username": info.Username, "has_email": info.Email != "", "email": maskEmail(info.Email)})
	})
	mux.HandleFunc("POST /api/account/email", func(w http.ResponseWriter, r *http.Request) {
		if _, ok := s.authenticate(w, r); !ok {
			return
		}
		a, ok := s.accounts(w)
		if !ok {
			return
		}
		var d struct {
			Email string `json:"email"`
		}
		if e := decode(r, w, &d); e != nil {
			fail(w, 400, "invalid request")
			return
		}
		if e := a.SetEmail(r.Context(), token(r), d.Email); e != nil {
			credentialError(w, e)
			return
		}
		jsonResponse(w, 200, map[string]bool{"ok": true})
	})
	mux.HandleFunc("POST /api/password/forgot", func(w http.ResponseWriter, r *http.Request) {
		a, ok := s.accounts(w)
		if !ok {
			return
		}
		var d struct {
			Email string `json:"email"`
		}
		if e := decode(r, w, &d); e != nil {
			fail(w, 400, "invalid request")
			return
		}
		ip := s.clientIP(r)
		em, _ := persistence.NormalizeEmail(d.Email)
		if !s.allow("forgot:"+ip, 5) || (em != "" && !s.allow("forgot-mail:"+em, 3)) {
			failCode(w, 429, "rate_limited", "Bạn thử quá nhanh, vui lòng đợi một phút.")
			return
		}
		// Luôn trả lời giống nhau để không lộ email nào đã đăng ký.
		resp := map[string]bool{"ok": true}
		tok, user, found, e := a.CreatePasswordReset(r.Context(), d.Email)
		if e != nil {
			log.Printf("password reset: %v", e)
		} else if found {
			base := strings.TrimRight(os.Getenv("GAME_PUBLIC_URL"), "/")
			if base == "" {
				base = "http://localhost:5173"
			}
			link := base + "/#reset=" + url.QueryEscape(tok)
			body := fmt.Sprintf("Chào %s,\n\nBạn (hoặc ai đó) vừa yêu cầu đặt lại mật khẩu Phimond. Mở liên kết sau trong 30 phút để đặt mật khẩu mới:\n\n%s\n\nNếu không phải bạn, hãy bỏ qua thư này; mật khẩu hiện tại vẫn an toàn.\n", user, link)
			go func(to string) {
				if err := s.mailer.Send(to, "Đặt lại mật khẩu Phimond", body); err != nil {
					log.Printf("password reset mail: %v", err)
				}
			}(em)
		}
		jsonResponse(w, 200, resp)
	})
	mux.HandleFunc("POST /api/password/reset", func(w http.ResponseWriter, r *http.Request) {
		a, ok := s.accounts(w)
		if !ok {
			return
		}
		var d struct {
			Token    string `json:"token"`
			Password string `json:"password"`
		}
		if e := decode(r, w, &d); e != nil {
			fail(w, 400, "invalid request")
			return
		}
		if !s.allow("reset:"+s.clientIP(r), 10) {
			failCode(w, 429, "rate_limited", "Bạn thử quá nhanh, vui lòng đợi một phút.")
			return
		}
		if e := a.ResetPassword(r.Context(), d.Token, d.Password); e != nil {
			credentialError(w, e)
			return
		}
		// Mọi phiên của tài khoản đã bị thu hồi trong kho; bỏ bộ nhớ đệm để chúng được kiểm lại ngay.
		s.sessionMu.Lock()
		for t, e := range s.sessions {
			if !e.revoked {
				delete(s.sessions, t)
			}
		}
		s.sessionMu.Unlock()
		jsonResponse(w, 200, map[string]bool{"ok": true})
	})
	mux.HandleFunc("POST /api/account/delete", func(w http.ResponseWriter, r *http.Request) {
		if _, ok := s.authenticate(w, r); !ok {
			return
		}
		a, ok := s.accounts(w)
		if !ok {
			return
		}
		var d struct {
			Password string `json:"password"`
		}
		if e := decode(r, w, &d); e != nil {
			fail(w, 400, "invalid request")
			return
		}
		if !s.allow("delete:"+s.clientIP(r), 5) {
			failCode(w, 429, "rate_limited", "Bạn thử quá nhanh, vui lòng đợi một phút.")
			return
		}
		tok := token(r)
		ids, e := a.DeleteAccount(r.Context(), tok, d.Password)
		if e != nil {
			credentialError(w, e)
			return
		}
		s.forgetAccount(tok, ids)
		jsonResponse(w, 200, map[string]bool{"ok": true})
	})
}

// forgetAccount bỏ khỏi bộ nhớ mọi nhân vật đang chạy của tài khoản vừa xoá và thu hồi các phiên còn trong bộ nhớ đệm.
func (s *Server) forgetAccount(token string, ids []string) {
	gone := map[string]bool{}
	for _, id := range ids {
		gone[id] = true
	}
	s.sessionMu.Lock()
	for t, e := range s.sessions {
		if gone[e.id] {
			s.sessions[t] = sessionEntry{revoked: true, until: time.Now().Add(7 * 24 * time.Hour)}
		}
	}
	s.sessions[token] = sessionEntry{revoked: true, until: time.Now().Add(7 * 24 * time.Hour)}
	s.sessionMu.Unlock()
	s.liveMu.Lock()
	for id := range gone {
		delete(s.live, id)
	}
	s.liveMu.Unlock()
}
