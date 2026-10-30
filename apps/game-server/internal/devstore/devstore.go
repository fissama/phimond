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
	tokens   map[string]string   // token -> character id đang chọn
	owner    map[string]string   // token -> id tài khoản (= id nhân vật ô 0)
	slots    map[string][]string // id tài khoản -> id nhân vật theo ô
	chars    map[string]json.RawMessage
	receipts map[string]map[string]bool
	resets   map[string]string // mã đặt lại -> username
}

type account struct{ id, username, password, email string }

// New tạo kho rỗng.
func New() *Store {
	return &Store{accounts: map[string]*account{}, tokens: map[string]string{}, owner: map[string]string{}, slots: map[string][]string{}, chars: map[string]json.RawMessage{}, receipts: map[string]map[string]bool{}, resets: map[string]string{}}
}

func randHex(n int) string {
	b := make([]byte, n)
	_, _ = rand.Read(b)
	return hex.EncodeToString(b)
}

func (m *Store) session(id string) string {
	t := randHex(32) // 64 ký tự hex, giống độ dài token thật
	m.tokens[t] = id
	m.owner[t] = id
	return t
}

func (m *Store) Register(_ context.Context, username, password string, initial func(string) (json.RawMessage, error)) (string, string, error) {
	m.mu.Lock()
	defer m.mu.Unlock()
	if err := persistence.ValidateRegistration(username, password); err != nil {
		return "", "", err
	}
	if _, ok := m.accounts[username]; ok {
		return "", "", persistence.ErrUsernameTaken
	}
	id := randHex(8)
	raw, err := initial(id)
	if err != nil {
		return "", "", err
	}
	m.accounts[username] = &account{id: id, username: username, password: password}
	m.slots[id] = []string{id}
	m.chars[id] = append(json.RawMessage{}, raw...)
	m.receipts[id] = map[string]bool{}
	return m.session(id), id, nil
}

func (m *Store) Login(_ context.Context, username, password string) (string, string, error) {
	m.mu.Lock()
	defer m.mu.Unlock()
	a, ok := m.accounts[username]
	if !usernamePattern.MatchString(username) || !ok || a.password != password || password == "" {
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

// Slots liệt kê các ô nhân vật của tài khoản (ô trống không có mục).
func (m *Store) Slots(_ context.Context, token string) ([]persistence.Slot, error) {
	m.mu.Lock()
	defer m.mu.Unlock()
	acc, ok := m.owner[token]
	if !ok {
		return nil, persistence.ErrSession
	}
	var out []persistence.Slot
	for i, id := range m.slots[acc] {
		if id != "" {
			out = append(out, persistence.Slot{Slot: i, ID: id, State: append(json.RawMessage{}, m.chars[id]...)})
		}
	}
	return out, nil
}

// OpenSlot chọn (và tạo nếu trống) một ô nhân vật cho phiên.
func (m *Store) OpenSlot(_ context.Context, token string, slot int, initial func(string) (json.RawMessage, error)) (string, error) {
	m.mu.Lock()
	defer m.mu.Unlock()
	acc, ok := m.owner[token]
	if !ok || slot < 0 || slot >= persistence.MaxSlots {
		return "", persistence.ErrSession
	}
	for len(m.slots[acc]) <= slot {
		m.slots[acc] = append(m.slots[acc], "")
	}
	id := m.slots[acc][slot]
	if id == "" {
		id = randHex(8)
		raw, err := initial(id)
		if err != nil {
			return "", err
		}
		m.slots[acc][slot] = id
		m.chars[id] = append(json.RawMessage{}, raw...)
		m.receipts[id] = map[string]bool{}
	}
	m.tokens[token] = id
	return id, nil
}

func (m *Store) byToken(token string) (*account, bool) {
	id, ok := m.owner[token]
	if !ok {
		return nil, false
	}
	for _, a := range m.accounts {
		if a.id == id {
			return a, true
		}
	}
	return nil, false
}

// AccountInfo trả tên đăng nhập và email của phiên.
func (m *Store) AccountInfo(_ context.Context, token string) (persistence.AccountInfo, error) {
	m.mu.Lock()
	defer m.mu.Unlock()
	a, ok := m.byToken(token)
	if !ok {
		return persistence.AccountInfo{}, persistence.ErrSession
	}
	return persistence.AccountInfo{Username: a.username, Email: a.email}, nil
}

// SetEmail đặt/xoá email (rỗng = xoá).
func (m *Store) SetEmail(_ context.Context, token, email string) error {
	email, err := persistence.NormalizeEmail(email)
	if err != nil {
		return err
	}
	m.mu.Lock()
	defer m.mu.Unlock()
	a, ok := m.byToken(token)
	if !ok {
		return persistence.ErrSession
	}
	if email != "" {
		for _, o := range m.accounts {
			if o != a && o.email == email {
				return persistence.ErrEmailTaken
			}
		}
	}
	a.email = email
	return nil
}

// CreatePasswordReset tạo mã đặt lại cho email.
func (m *Store) CreatePasswordReset(_ context.Context, email string) (string, string, bool, error) {
	email, err := persistence.NormalizeEmail(email)
	if err != nil || email == "" {
		return "", "", false, nil
	}
	m.mu.Lock()
	defer m.mu.Unlock()
	for _, a := range m.accounts {
		if a.email == email {
			t := randHex(32)
			m.resets[t] = a.username
			return t, a.username, true, nil
		}
	}
	return "", "", false, nil
}

// ResetPassword đổi mật khẩu bằng mã một lần và thu hồi mọi phiên.
func (m *Store) ResetPassword(_ context.Context, token, newPassword string) error {
	m.mu.Lock()
	defer m.mu.Unlock()
	u, ok := m.resets[token]
	if !ok {
		return persistence.ErrResetToken
	}
	if err := persistence.ValidatePassword(u, newPassword); err != nil {
		return err
	}
	a := m.accounts[u]
	a.password = newPassword
	delete(m.resets, token)
	for t, id := range m.owner {
		if id == a.id {
			delete(m.owner, t)
			delete(m.tokens, t)
		}
	}
	return nil
}

// DeleteAccount xoá tài khoản của phiên (cần mật khẩu); trả id các nhân vật đã xoá.
func (m *Store) DeleteAccount(_ context.Context, token, password string) ([]string, error) {
	m.mu.Lock()
	defer m.mu.Unlock()
	a, ok := m.byToken(token)
	if !ok {
		return nil, persistence.ErrSession
	}
	if a.password != password {
		return nil, persistence.ErrCredentials
	}
	var ids []string
	for _, id := range m.slots[a.id] {
		if id != "" {
			ids = append(ids, id)
			delete(m.chars, id)
			delete(m.receipts, id)
		}
	}
	delete(m.slots, a.id)
	for t, id := range m.owner {
		if id == a.id {
			delete(m.owner, t)
			delete(m.tokens, t)
		}
	}
	delete(m.accounts, a.username)
	return ids, nil
}
