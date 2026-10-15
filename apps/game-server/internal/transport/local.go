package transport

import (
	"bytes"
	"context"
	"encoding/json"
	"errors"
	"io"
	"net/http/httptest"
	"sync"
)

// Truy cập trong tiến trình (không socket) cho bản wasm demo và kiểm thử: dùng đúng Handler, applyLive,
// stateEnvelope của server thật. Vòng lặp khung WS được tái hiện ở LocalConn.Handle; mọi luật vẫn do engine quyết định.

// LocalHTTP gọi REST của server (đăng ký/đăng nhập/content/đăng xuất…) mà không cần listener.
func (s *Server) LocalHTTP(method, path string, body []byte, token string) (int, []byte) {
	var rd io.Reader
	if body != nil {
		rd = bytes.NewReader(body)
	}
	r := httptest.NewRequest(method, path, rd)
	r.RemoteAddr = "127.0.0.1:1"
	if body != nil {
		r.Header.Set("Content-Type", "application/json")
	}
	if token != "" {
		r.Header.Set("Authorization", "Bearer "+token)
	}
	w := httptest.NewRecorder()
	s.Handler().ServeHTTP(w, r)
	return w.Code, w.Body.Bytes()
}

// LocalConn là một "kết nối WS" trong bộ nhớ.
type LocalConn struct {
	s      *Server
	mu     sync.Mutex
	id     string
	token  string
	authed bool
}

func (s *Server) NewLocalConn() *LocalConn { return &LocalConn{s: s} }

func errFrame(id, msg string) []byte {
	b, _ := json.Marshal(map[string]any{"op": "error", "request_id": id, "data": map[string]string{"message": msg}})
	return b
}

// Handle xử lý một khung client → trả khung server (rỗng nếu cần đóng kết nối, closed=true).
func (c *LocalConn) Handle(ctx context.Context, raw []byte) (out []byte, closed bool) {
	c.mu.Lock()
	defer c.mu.Unlock()
	m, err := parseEnvelope(raw)
	if err != nil {
		return errFrame("", "invalid message envelope"), false
	}
	if !c.authed {
		if m.Op != "auth.session" {
			return nil, true
		}
		var a struct {
			Token string `json:"token"`
		}
		if json.Unmarshal(m.Data, &a) != nil {
			return nil, true
		}
		id, err := c.s.authenticateSession(ctx, a.Token)
		if err != nil {
			return nil, true
		}
		initial, err := c.s.readLive(ctx, id)
		if err != nil {
			return nil, true
		}
		p, err := c.s.stateEnvelope(m, initial, false)
		if err != nil {
			return nil, true
		}
		c.id, c.token, c.authed = id, a.Token, true
		b, _ := json.Marshal(p)
		return b, false
	}
	if !c.s.allow("ws:"+c.id, 400) {
		return errFrame(m.RequestID, "slow down"), false
	}
	if _, err = c.s.authenticateSession(ctx, c.token); err != nil {
		return nil, true
	}
	fresh := false
	updated, err := c.s.applyLive(ctx, c.id, m, &fresh)
	if err != nil {
		msg := "could not apply action"
		var de *domainError
		if errors.As(err, &de) {
			msg = de.Error()
		}
		return errFrame(m.RequestID, msg), false
	}
	p, err := c.s.stateEnvelope(m, updated, fresh)
	if err != nil {
		return nil, true
	}
	b, _ := json.Marshal(p)
	return b, false
}
