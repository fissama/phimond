package persistence

import (
	"context"
	"crypto/rand"
	"crypto/sha256"
	"database/sql"
	"encoding/hex"
	"errors"
	"net/mail"
	"strings"
	"time"

	"github.com/go-sql-driver/mysql"
	"golang.org/x/crypto/bcrypt"
)

// Lỗi tài khoản có mã ổn định để client hiển thị tiếng Việt đúng chỗ.
var (
	ErrUsernameFormat = errors.New("username must be 3-24 ASCII letters, digits or underscores")
	ErrPasswordShort  = errors.New("password must be at least 8 characters")
	ErrPasswordLong   = errors.New("password must be at most 72 bytes")
	ErrPasswordWeak   = errors.New("password is too common or too predictable")
	ErrUsernameTaken  = errors.New("username already taken")
	ErrEmailInvalid   = errors.New("invalid email address")
	ErrEmailTaken     = errors.New("email already used")
	ErrResetToken     = errors.New("reset link invalid or expired")
)

// ResetTTL là thời hạn của liên kết đặt lại mật khẩu.
const ResetTTL = 30 * time.Minute

// Mật khẩu phổ biến nhất (chữ thường); bị từ chối khi đăng ký/đặt lại.
var commonPasswords = map[string]bool{}

func init() {
	for _, p := range strings.Fields(`12345678 123456789 1234567890 12345678910 11111111 00000000 87654321 123123123 123456123456
password password1 password12 password123 passw0rd p@ssw0rd p@ssword password! qwertyui qwerty123 qwertyuiop qwerty12345
abc12345 abcd1234 abcdefgh abcdefg1 iloveyou iloveyou1 letmein1 welcome1 welcome123 admin123 administrator monkey123 dragon123
football1 baseball1 superman1 trustno1 sunshine1 princess1 master123 shadow123 michael1 charlie1 asdfghjk asdf1234 zxcvbnm1
zxcvbnm123 1q2w3e4r 1q2w3e4r5t 1qaz2wsx 123qweasd qazwsxedc q1w2e3r4 a1234567 a12345678 aa123456 aa12345678 abc123456
matkhau123 matkhau1234 matkhau12345 matkhaucuatoi vietnam123 vietnam2024 vietnam2025 hanoi123 saigon123 anhyeuem1 emyeuanh1
phimond123 phimond1234 phimond12 linhthu123 linhthu1234 pokezoo123`) {
		commonPasswords[p] = true
	}
}

func allSame(s string) bool {
	for i := 1; i < len(s); i++ {
		if s[i] != s[0] {
			return false
		}
	}
	return len(s) > 0
}

// ValidatePassword áp chính sách mật khẩu đăng ký: 8–72 byte, không nằm trong danh sách phổ biến, không trùng tên đăng nhập, không lặp một ký tự.
func ValidatePassword(username, password string) error {
	switch {
	case len(password) < 8:
		return ErrPasswordShort
	case len(password) > 72:
		return ErrPasswordLong
	}
	low := strings.ToLower(password)
	if commonPasswords[low] || allSame(low) || strings.EqualFold(password, username) {
		return ErrPasswordWeak
	}
	return nil
}

// ValidateRegistration kiểm tên đăng nhập + mật khẩu theo chính sách đăng ký.
func ValidateRegistration(username, password string) error {
	if !usernamePattern.MatchString(username) {
		return ErrUsernameFormat
	}
	return ValidatePassword(username, password)
}

// NormalizeEmail kiểm cú pháp và trả về địa chỉ chữ thường; chuỗi rỗng nghĩa là không dùng email.
func NormalizeEmail(raw string) (string, error) {
	raw = strings.TrimSpace(raw)
	if raw == "" {
		return "", nil
	}
	if len(raw) > 254 {
		return "", ErrEmailInvalid
	}
	a, e := mail.ParseAddress(raw)
	if e != nil || a.Address != raw || strings.ContainsAny(raw, " <>\"") {
		return "", ErrEmailInvalid
	}
	at := strings.LastIndexByte(raw, '@')
	if at < 1 || !strings.Contains(raw[at+1:], ".") {
		return "", ErrEmailInvalid
	}
	for _, r := range raw {
		if r > 126 {
			return "", ErrEmailInvalid
		}
	}
	return strings.ToLower(raw), nil
}

// AccountInfo là thông tin tài khoản hiển thị cho chính chủ.
type AccountInfo struct {
	Username string
	Email    string
}

func isDup(e error) bool {
	var me *mysql.MySQLError
	return errors.As(e, &me) && me.Number == 1062
}

func (s *Store) accountOfToken(ctx context.Context, token string) (string, error) {
	if len(token) != 64 {
		return "", ErrSession
	}
	h := sha256.Sum256([]byte(token))
	var acc string
	if e := s.DB.QueryRowContext(ctx, "SELECT account_id FROM sessions WHERE token_hash=? AND expires_at>UTC_TIMESTAMP(6)", h[:]).Scan(&acc); e != nil {
		if errors.Is(e, sql.ErrNoRows) {
			return "", ErrSession
		}
		return "", e
	}
	return acc, nil
}

// AccountInfo trả tên đăng nhập và email (nếu có) của phiên.
func (s *Store) AccountInfo(ctx context.Context, token string) (AccountInfo, error) {
	acc, e := s.accountOfToken(ctx, token)
	if e != nil {
		return AccountInfo{}, e
	}
	var info AccountInfo
	var email sql.NullString
	if e = s.DB.QueryRowContext(ctx, "SELECT username,email FROM accounts WHERE id=?", acc).Scan(&info.Username, &email); e != nil {
		return AccountInfo{}, e
	}
	info.Email = email.String
	return info, nil
}

// SetEmail đặt hoặc xoá (email rỗng) email của tài khoản; email đã dùng cho tài khoản khác trả ErrEmailTaken.
func (s *Store) SetEmail(ctx context.Context, token, email string) error {
	email, e := NormalizeEmail(email)
	if e != nil {
		return e
	}
	acc, e := s.accountOfToken(ctx, token)
	if e != nil {
		return e
	}
	var v any
	if email != "" {
		v = email
	}
	if _, e = s.DB.ExecContext(ctx, "UPDATE accounts SET email=? WHERE id=?", v, acc); e != nil {
		if isDup(e) {
			return ErrEmailTaken
		}
		return e
	}
	return nil
}

// CreatePasswordReset tạo mã đặt lại cho tài khoản có email này. found=false khi không có tài khoản (caller vẫn trả lời giống nhau).
func (s *Store) CreatePasswordReset(ctx context.Context, email string) (token, username string, found bool, err error) {
	email, err = NormalizeEmail(email)
	if err != nil || email == "" {
		return "", "", false, nil
	}
	var acc string
	if e := s.DB.QueryRowContext(ctx, "SELECT id,username FROM accounts WHERE email=?", email).Scan(&acc, &username); e != nil {
		if errors.Is(e, sql.ErrNoRows) {
			return "", "", false, nil
		}
		return "", "", false, e
	}
	b := make([]byte, 32)
	if _, err = rand.Read(b); err != nil {
		return "", "", false, err
	}
	token = hex.EncodeToString(b)
	h := sha256.Sum256([]byte(token))
	tx, err := s.DB.BeginTx(ctx, nil)
	if err != nil {
		return "", "", false, err
	}
	defer tx.Rollback()
	// Chỉ giữ mã mới nhất cho mỗi tài khoản.
	if _, err = tx.ExecContext(ctx, "DELETE FROM password_resets WHERE account_id=? OR expires_at<UTC_TIMESTAMP(6)", acc); err != nil {
		return "", "", false, err
	}
	if _, err = tx.ExecContext(ctx, "INSERT INTO password_resets(token_hash,account_id,expires_at) VALUES (?,?,?)", h[:], acc, time.Now().UTC().Add(ResetTTL)); err != nil {
		return "", "", false, err
	}
	return token, username, true, tx.Commit()
}

// ResetPassword đổi mật khẩu bằng mã một lần và thu hồi mọi phiên đang đăng nhập.
func (s *Store) ResetPassword(ctx context.Context, token, newPassword string) error {
	if len(token) != 64 {
		return ErrResetToken
	}
	h := sha256.Sum256([]byte(token))
	tx, e := s.DB.BeginTx(ctx, nil)
	if e != nil {
		return e
	}
	defer tx.Rollback()
	var acc, username string
	if e = tx.QueryRowContext(ctx, "SELECT r.account_id,a.username FROM password_resets r JOIN accounts a ON a.id=r.account_id WHERE r.token_hash=? AND r.expires_at>UTC_TIMESTAMP(6) FOR UPDATE", h[:]).Scan(&acc, &username); e != nil {
		if errors.Is(e, sql.ErrNoRows) {
			return ErrResetToken
		}
		return e
	}
	if e = ValidatePassword(username, newPassword); e != nil {
		return e
	}
	hash, e := bcrypt.GenerateFromPassword([]byte(newPassword), bcrypt.DefaultCost)
	if e != nil {
		return e
	}
	if _, e = tx.ExecContext(ctx, "UPDATE accounts SET password_hash=? WHERE id=?", hash, acc); e != nil {
		return e
	}
	if _, e = tx.ExecContext(ctx, "DELETE FROM sessions WHERE account_id=?", acc); e != nil {
		return e
	}
	if _, e = tx.ExecContext(ctx, "DELETE FROM password_resets WHERE account_id=?", acc); e != nil {
		return e
	}
	return tx.Commit()
}

// DeleteAccount xoá vĩnh viễn tài khoản của phiên (cần mật khẩu) cùng mọi nhân vật, linh thú, nhật ký và phiên. Trả danh sách id nhân vật đã xoá.
func (s *Store) DeleteAccount(ctx context.Context, token, password string) ([]string, error) {
	acc, e := s.accountOfToken(ctx, token)
	if e != nil {
		return nil, e
	}
	tx, e := s.DB.BeginTx(ctx, nil)
	if e != nil {
		return nil, e
	}
	defer tx.Rollback()
	var hash []byte
	if e = tx.QueryRowContext(ctx, "SELECT password_hash FROM accounts WHERE id=? FOR UPDATE", acc).Scan(&hash); e != nil {
		return nil, e
	}
	if bcrypt.CompareHashAndPassword(hash, []byte(password)) != nil {
		return nil, ErrCredentials
	}
	rows, e := tx.QueryContext(ctx, "SELECT id FROM characters WHERE account_id=?", acc)
	if e != nil {
		return nil, e
	}
	var ids []string
	for rows.Next() {
		var id string
		if e = rows.Scan(&id); e != nil {
			rows.Close()
			return nil, e
		}
		ids = append(ids, id)
	}
	rows.Close()
	for _, id := range ids {
		for _, q := range []string{
			"DELETE FROM pet_ancestry WHERE child_id IN (SELECT id FROM pets WHERE character_id=?) OR parent_id IN (SELECT id FROM pets WHERE character_id=?)",
		} {
			if _, e = tx.ExecContext(ctx, q, id, id); e != nil {
				return nil, e
			}
		}
		for _, q := range []string{"DELETE FROM pets WHERE character_id=?", "DELETE FROM audit_events WHERE character_id=?", "DELETE FROM command_receipts WHERE character_id=?"} {
			if _, e = tx.ExecContext(ctx, q, id); e != nil {
				return nil, e
			}
		}
	}
	for _, q := range []string{"DELETE FROM sessions WHERE account_id=?", "DELETE FROM password_resets WHERE account_id=?", "DELETE FROM characters WHERE account_id=?", "DELETE FROM accounts WHERE id=?"} {
		if _, e = tx.ExecContext(ctx, q, acc); e != nil {
			return nil, e
		}
	}
	return ids, tx.Commit()
}
