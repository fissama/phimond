package transport

import (
	"bytes"
	"context"
	"crypto/rand"
	"encoding/binary"
	"encoding/json"
	"errors"
	"github.com/coder/websocket"
	"io"
	"log"
	"net"
	"net/http"
	"os"
	"phimond/server/internal/character"
	"phimond/server/internal/persistence"
	"strings"
	"sync"
	"sync/atomic"
	"time"
)

type Storage interface {
	Receipts(context.Context, string, func(string)) error
	HasReceipt(context.Context, string, string) (bool, error)
	Checkpoint(context.Context, string, int, json.RawMessage, []string) error
	Register(context.Context, string, string, func(string) (json.RawMessage, error)) (string, string, error)
	Login(context.Context, string, string) (string, string, error)
	Authenticate(context.Context, string) (string, error)
	Logout(context.Context, string) error
	Read(context.Context, string) (json.RawMessage, error)
	Mutate(context.Context, string, string, func(json.RawMessage) (json.RawMessage, []persistence.AuditEvent, error)) (json.RawMessage, error)
}
type window struct {
	Start time.Time
	Count int
}
type Server struct {
	metrics     *runtimeMetrics
	liveMu      sync.Mutex
	live        map[string]*liveCharacter
	sessionMu   sync.Mutex
	sessions    map[string]sessionEntry
	stopping    atomic.Bool
	Store       Storage
	Game        *character.Engine
	mu          sync.Mutex
	limits      map[string]window
	connections map[string]int
}

func New(s Storage, e *character.Engine) *Server {
	return &Server{metrics: newRuntimeMetrics(os.Getenv("GAME_METRICS") == "1"), Store: s, Game: e, limits: map[string]window{}, connections: map[string]int{}, live: map[string]*liveCharacter{}, sessions: map[string]sessionEntry{}}
}
func jsonResponse(w http.ResponseWriter, status int, data any) {
	w.Header().Set("Content-Type", "application/json")
	w.Header().Set("Cache-Control", "no-store")
	w.WriteHeader(status)
	_ = json.NewEncoder(w).Encode(data)
}
func fail(w http.ResponseWriter, status int, msg string) {
	jsonResponse(w, status, map[string]string{"message": msg})
}
func decode(r *http.Request, w http.ResponseWriter, out any) error {
	r.Body = http.MaxBytesReader(w, r.Body, 16384)
	d := json.NewDecoder(r.Body)
	d.DisallowUnknownFields()
	if e := d.Decode(out); e != nil {
		return e
	}
	if d.Decode(&struct{}{}) != io.EOF {
		return errors.New("trailing JSON")
	}
	return nil
}
func (s *Server) allow(key string, limit int) bool {
	s.mu.Lock()
	defer s.mu.Unlock()
	now := time.Now()
	if len(s.limits) > 10000 {
		for k, v := range s.limits {
			if now.Sub(v.Start) > time.Minute {
				delete(s.limits, k)
			}
		}
	}
	v := s.limits[key]
	if now.Sub(v.Start) > time.Minute {
		v = window{Start: now}
	}
	v.Count++
	s.limits[key] = v
	return v.Count <= limit
}
func token(r *http.Request) string {
	return strings.TrimPrefix(r.Header.Get("Authorization"), "Bearer ")
}
func (s *Server) authenticate(w http.ResponseWriter, r *http.Request) (string, bool) {
	t := token(r)
	if len(t) != 64 || s.Store == nil {
		fail(w, 401, "login required")
		return "", false
	}
	id, e := s.authenticateSession(r.Context(), t)
	if e != nil {
		if errors.Is(e, persistence.ErrSession) {
			fail(w, 401, "session expired; log in again")
		} else {
			fail(w, 503, "session service unavailable; try again")
		}
		return "", false
	}
	return id, true
}
func (s *Server) Handler() http.Handler {
	mux := http.NewServeMux()
	mux.HandleFunc("GET /healthz", func(w http.ResponseWriter, r *http.Request) {
		jsonResponse(w, 200, map[string]string{"service": "Phimond", "status": "ok"})
	})
	mux.HandleFunc("GET /api/content", func(w http.ResponseWriter, r *http.Request) { jsonResponse(w, 200, s.Game.Data) })
	for _, path := range []string{"/api/register", "/api/login"} {
		mux.HandleFunc("POST "+path, s.credentials)
	}
	mux.HandleFunc("POST /api/logout", func(w http.ResponseWriter, r *http.Request) {
		id, ok := s.authenticate(w, r)
		if !ok {
			return
		}
		if e := s.logoutSession(r.Context(), token(r), id); e != nil {
			fail(w, 500, "logout failed")
			return
		}
		jsonResponse(w, 200, map[string]bool{"ok": true})
	})
	mux.HandleFunc("GET /api/character", func(w http.ResponseWriter, r *http.Request) {
		c, ok := s.character(w, r)
		if !ok {
			return
		}
		jsonResponse(w, 200, s.Game.Snapshot(c))
	})
	mux.HandleFunc("GET /api/lineage/{id}", func(w http.ResponseWriter, r *http.Request) {
		c, ok := s.character(w, r)
		if !ok {
			return
		}
		n := s.Game.Lineage(c, r.PathValue("id"))
		if n == nil {
			fail(w, 404, "pet not found")
			return
		}
		jsonResponse(w, 200, n)
	})
	mux.HandleFunc("GET /api/battles", func(w http.ResponseWriter, r *http.Request) {
		c, ok := s.character(w, r)
		if !ok {
			return
		}
		jsonResponse(w, 200, map[string]any{"battles": s.Game.PublicHistory(c)})
	})
	mux.HandleFunc("GET /ws", s.ws)
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("X-Content-Type-Options", "nosniff")
		ip, _, _ := net.SplitHostPort(r.RemoteAddr)
		if !s.allow("http:"+ip, 600) {
			fail(w, 429, "too many requests")
			return
		}
		mux.ServeHTTP(w, r)
	})
}
func (s *Server) credentials(w http.ResponseWriter, r *http.Request) {
	var d struct {
		Username string `json:"username"`
		Password string `json:"password"`
	}
	if e := decode(r, w, &d); e != nil {
		fail(w, 400, "invalid credentials request")
		return
	}
	ip, _, _ := net.SplitHostPort(r.RemoteAddr)
	if !s.allow("auth:"+ip, 20) {
		fail(w, 429, "too many login attempts; retry in a minute")
		return
	}
	if s.Store == nil {
		fail(w, 503, "database unavailable")
		return
	}
	var tok, id string
	var err error
	if r.URL.Path == "/api/register" {
		tok, id, err = s.Store.Register(r.Context(), d.Username, d.Password, func(id string) (json.RawMessage, error) {
			var seed [8]byte
			if _, e := rand.Read(seed[:]); e != nil {
				return nil, e
			}
			return json.Marshal(s.Game.NewCharacter(id, d.Username, binary.LittleEndian.Uint64(seed[:])))
		})
	} else {
		tok, id, err = s.Store.Login(r.Context(), d.Username, d.Password)
	}
	if err != nil {
		fail(w, 400, "Unable to sign in/register. Use a unique 3–24 character username and a 10–72 byte password.")
		return
	}
	jsonResponse(w, 200, map[string]string{"token": tok, "character_id": id})
}
func (s *Server) character(w http.ResponseWriter, r *http.Request) (*character.Character, bool) {
	id, ok := s.authenticate(w, r)
	if !ok {
		return nil, false
	}
	raw, e := s.readLive(r.Context(), id)
	if e != nil {
		fail(w, 500, "could not load character")
		return nil, false
	}
	var c character.Character
	if json.Unmarshal(raw, &c) != nil {
		fail(w, 500, "invalid saved character")
		return nil, false
	}
	return &c, true
}

type envelope struct {
	Op        string          `json:"op"`
	RequestID string          `json:"request_id"`
	Data      json.RawMessage `json:"data"`
}

func parseEnvelope(raw []byte) (envelope, error) {
	var m envelope
	d := json.NewDecoder(bytes.NewReader(raw))
	d.DisallowUnknownFields()
	if e := d.Decode(&m); e != nil {
		return m, e
	}
	if d.Decode(&struct{}{}) != io.EOF {
		return m, errors.New("trailing JSON")
	}
	if m.RequestID == "" || len(m.RequestID) > 128 || len(m.Op) > 64 {
		return m, errors.New("valid request_id and op required")
	}
	return m, nil
}
func (s *Server) ws(w http.ResponseWriter, r *http.Request) {
	origins := []string{"localhost:3100", "127.0.0.1:3100"}
	if v := os.Getenv("GAME_ALLOWED_ORIGINS"); v != "" {
		origins = strings.Split(v, ",")
	}
	conn, err := websocket.Accept(w, r, &websocket.AcceptOptions{OriginPatterns: origins})
	if err != nil {
		return
	}
	defer conn.CloseNow()
	conn.SetReadLimit(16384)
	ctx := r.Context()
	authCtx, cancel := context.WithTimeout(ctx, 10*time.Second)
	_, raw, err := conn.Read(authCtx)
	cancel()
	if err != nil {
		return
	}
	m, err := parseEnvelope(raw)
	if err != nil || m.Op != "auth.session" {
		_ = conn.Close(websocket.StatusPolicyViolation, "authenticate first")
		return
	}
	var auth struct {
		Token string `json:"token"`
	}
	if json.Unmarshal(m.Data, &auth) != nil {
		return
	}
	id, err := s.authenticateSession(ctx, auth.Token)
	if err != nil {
		if errors.Is(err, persistence.ErrSession) {
			_ = conn.Close(websocket.StatusPolicyViolation, "invalid session")
		} else {
			_ = conn.Close(websocket.StatusInternalError, "session service unavailable")
		}
		return
	}
	s.mu.Lock()
	active := s.connections[id]
	if active < 3 {
		s.connections[id]++
	}
	s.mu.Unlock()
	if active >= 3 {
		_ = conn.Close(websocket.StatusPolicyViolation, "connection limit")
		return
	}
	defer func() {
		flushCtx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
		defer cancel()
		_ = s.flushLive(flushCtx, id)
		s.mu.Lock()
		s.connections[id]--
		if s.connections[id] == 0 {
			delete(s.connections, id)
		}
		s.mu.Unlock()
	}()
	requestStarted := time.Now()
	send := func(payload any) bool {
		b, e := json.Marshal(payload)
		if e != nil {
			return false
		}
		response, _ := payload.(map[string]any)
		s.metrics.observe("response_ready", m.Op, time.Since(requestStarted), response["op"] == "error")
		writeCtx, c := context.WithTimeout(ctx, 10*time.Second)
		defer c()
		started := time.Now()
		err := conn.Write(writeCtx, websocket.MessageText, b)
		s.metrics.observe("socket_write", m.Op, time.Since(started), err != nil)
		if err == nil {
			s.metrics.recordBytes(m.Op, len(b))
		}
		return err == nil
	}
	state := func(request envelope, raw json.RawMessage, fresh bool) bool {
		payload, err := s.stateEnvelope(request, raw, fresh)
		if err != nil {
			return false
		}
		return send(payload)
	}
	initial, err := s.readLive(ctx, id)
	if err != nil || !state(m, initial, false) {
		return
	}
	for {
		readCtx, cancel := context.WithTimeout(ctx, 10*time.Minute)
		_, raw, err = conn.Read(readCtx)
		cancel()
		requestStarted = time.Now()
		if err != nil {
			return
		}
		m, err = parseEnvelope(raw)
		if err != nil {
			if !send(map[string]any{"op": "error", "data": map[string]string{"message": "invalid message envelope"}}) {
				return
			}
			continue
		}
		if !s.allow("ws:"+id, 400) {
			if !send(map[string]any{"op": "error", "request_id": m.RequestID, "data": map[string]string{"message": "slow down"}}) {
				return
			}
			continue
		}
		if _, err = s.authenticateSession(ctx, auth.Token); err != nil {
			if errors.Is(err, persistence.ErrSession) {
				_ = conn.Close(websocket.StatusPolicyViolation, "session expired")
			} else {
				_ = conn.Close(websocket.StatusInternalError, "session service unavailable")
			}
			return
		}
		fresh := false
		updated, err := s.applyLive(ctx, id, m, &fresh)
		if err != nil {
			msg := "could not apply action" // Domain failures are safe; DB errors are kept out of the wire.
			var de *domainError
			if errors.As(err, &de) {
				msg = de.Error()
			}
			if !send(map[string]any{"op": "error", "request_id": m.RequestID, "data": map[string]string{"message": msg}}) {
				return
			}
			continue
		}
		if !state(m, updated, fresh) {
			return
		}
	}
}

type domainError struct{ error }

func Run(ctx context.Context, s *Server, addr string) error {
	checkpoints, stopCheckpoints := context.WithCancel(context.Background())
	done := make(chan struct{})
	go func() { s.checkpointLoop(checkpoints, checkpointInterval); close(done) }()
	go s.metricsLoop(checkpoints)
	defer func() {
		s.stopping.Store(true)
		stopCheckpoints()
		<-done
		flushCtx, cancel := context.WithTimeout(context.Background(), 15*time.Second)
		defer cancel()
		s.checkpointAll(flushCtx)
	}()
	srv := &http.Server{Addr: addr, Handler: s.Handler(), ReadHeaderTimeout: 5 * time.Second, ReadTimeout: 15 * time.Second, IdleTimeout: time.Minute}
	go func() {
		<-ctx.Done()
		s.stopping.Store(true)
		shutdown, cancel := context.WithTimeout(context.Background(), 5*time.Second)
		defer cancel()
		_ = srv.Shutdown(shutdown)
	}()
	log.Printf("Phimond listening on http://%s", addr)
	e := srv.ListenAndServe()
	if errors.Is(e, http.ErrServerClosed) {
		return nil
	}
	return e
}
