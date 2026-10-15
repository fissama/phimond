// Package devstore là kho dữ liệu trong bộ nhớ CHỈ DÙNG CHO DEV/E2E/DEMO (không mã hóa mật khẩu, không lưu đĩa).
package devstore

import (
	"context"
	"crypto/rand"
	"encoding/hex"
	"encoding/json"
	"errors"
	"phimond/server/internal/persistence"
	"regexp"
	"sync"
)

var usernamePattern = regexp.MustCompile(`^[A-Za-z0-9_]{3,24}$`)

// Store là kho dữ liệu trong bộ nhớ CHỈ DÙNG CHO DEV/E2E: không mã hóa mật khẩu,
// không lưu xuống đĩa, mất hết khi tắt tiến trình. Triển khai transport.Storage.
type Store struct {
	mu       sync.Mutex
	accounts map[string]*account // theo username
	tokens   map[string]string   // token -> character id
	chars    map[string]json.RawMessage
	receipts map[string]map[string]bool
}

type account struct{ id, password string }

// New tạo kho rỗng.
func New() *Store {
	return &Store{accounts: map[string]*account{}, tokens: map[string]string{}, chars: map[string]json.RawMessage{}, receipts: map[string]map[string]bool{}}
}

func randHex(n int) string {
	b := make([]byte, n)
	_, _ = rand.Read(b)
	return hex.EncodeToString(b)
}

func (m *Store) session(id string) string {
	t := randHex(32) // 64 ký tự hex, giống độ dài token thật
	m.tokens[t] = id
	return t
}

func (m *Store) Register(_ context.Context, username, password string, initial func(string) (json.RawMessage, error)) (string, string, error) {
	m.mu.Lock()
	defer m.mu.Unlock()
	if !usernamePattern.MatchString(username) || len(password) < 10 || len(password) > 72 {
		return "", "", errors.New("username 3-24 ký tự [A-Za-z0-9_], mật khẩu 10-72 byte")
	}
	if _, ok := m.accounts[username]; ok {
		return "", "", errors.New("username đã tồn tại")
	}
	id := randHex(8)
	raw, err := initial(id)
	if err != nil {
		return "", "", err
	}
	m.accounts[username] = &account{id: id, password: password}
	m.chars[id] = append(json.RawMessage{}, raw...)
	m.receipts[id] = map[string]bool{}
	return m.session(id), id, nil
}

func (m *Store) Login(_ context.Context, username, password string) (string, string, error) {
	m.mu.Lock()
	defer m.mu.Unlock()
	a, ok := m.accounts[username]
	if !usernamePattern.MatchString(username) || !ok || a.password != password {
		return "", "", persistence.ErrCredentials
	}
	return m.session(a.id), a.id, nil
}

func (m *Store) Authenticate(_ context.Context, token string) (string, error) {
	m.mu.Lock()
	defer m.mu.Unlock()
	id, ok := m.tokens[token]
	if !ok {
		return "", persistence.ErrSession
	}
	return id, nil
}

func (m *Store) Logout(_ context.Context, token string) error {
	m.mu.Lock()
	defer m.mu.Unlock()
	delete(m.tokens, token)
	return nil
}

func (m *Store) Read(_ context.Context, id string) (json.RawMessage, error) {
	m.mu.Lock()
	defer m.mu.Unlock()
	raw, ok := m.chars[id]
	if !ok {
		return nil, errors.New("không có nhân vật")
	}
	return append(json.RawMessage{}, raw...), nil
}

func (m *Store) Receipts(_ context.Context, id string, visit func(string)) error {
	m.mu.Lock()
	defer m.mu.Unlock()
	for r := range m.receipts[id] {
		visit(r)
	}
	return nil
}

func (m *Store) HasReceipt(_ context.Context, id, requestID string) (bool, error) {
	m.mu.Lock()
	defer m.mu.Unlock()
	return m.receipts[id][requestID], nil
}

func (m *Store) Checkpoint(_ context.Context, id string, _ int, next json.RawMessage, ids []string) error {
	m.mu.Lock()
	defer m.mu.Unlock()
	m.chars[id] = append(json.RawMessage{}, next...)
	for _, r := range ids {
		m.receipts[id][r] = true
	}
	return nil
}

func (m *Store) Mutate(_ context.Context, id, requestID string, fn func(json.RawMessage) (json.RawMessage, []persistence.AuditEvent, error)) (json.RawMessage, error) {
	m.mu.Lock()
	defer m.mu.Unlock()
	if m.receipts[id][requestID] {
		return append(json.RawMessage{}, m.chars[id]...), nil
	}
	next, _, err := fn(m.chars[id])
	if err != nil {
		return nil, err
	}
	m.chars[id] = append(json.RawMessage{}, next...)
	m.receipts[id][requestID] = true
	return append(json.RawMessage{}, next...), nil
}
