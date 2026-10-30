package persistence

import (
	"errors"
	"testing"
)

func TestPasswordPolicy(t *testing.T) {
	cases := []struct {
		user, pw string
		want     error
	}{
		{"nguoichoi", "abcd123", ErrPasswordShort},
		{"nguoichoi", "Mua-ha-2026", nil},
		{"nguoichoi", "matkhau-12345", nil},
		{"nguoichoi", "12345678", ErrPasswordWeak},
		{"nguoichoi", "Password123", ErrPasswordWeak},
		{"nguoichoi", "aaaaaaaaaa", ErrPasswordWeak},
		{"nguoichoi", "NguoiChoi", ErrPasswordWeak},
		{"nguoichoi", string(make([]byte, 73)), ErrPasswordLong},
	}
	for _, c := range cases {
		if got := ValidatePassword(c.user, c.pw); !errors.Is(got, c.want) {
			t.Errorf("%q: got %v want %v", c.pw, got, c.want)
		}
	}
	if !errors.Is(ValidateRegistration("a", "Mua-ha-2026"), ErrUsernameFormat) {
		t.Error("username format")
	}
}

func TestNormalizeEmail(t *testing.T) {
	ok := map[string]string{"": "", " A@B.vn ": "a@b.vn", "Nguoi.Choi@Gmail.com": "nguoi.choi@gmail.com"}
	for in, want := range ok {
		got, err := NormalizeEmail(in)
		if err != nil || got != want {
			t.Errorf("%q: %q %v", in, got, err)
		}
	}
	for _, in := range []string{"abc", "a@b", "a b@c.vn", "<a@b.vn>", "Tên <a@b.vn>", "á@b.vn"} {
		if _, err := NormalizeEmail(in); err == nil {
			t.Errorf("%q should fail", in)
		}
	}
}
