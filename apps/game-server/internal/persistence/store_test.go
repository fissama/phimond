package persistence

import (
	"bytes"
	"context"
	"crypto/ed25519"
	"crypto/rand"
	"crypto/tls"
	"crypto/x509"
	"database/sql"
	"encoding/json"
	"encoding/pem"
	"errors"
	"fmt"
	"math/big"
	"os"
	"path/filepath"
	"sync/atomic"
	"testing"
	"time"
)

func TestDatabaseIdentifiers(t *testing.T) {
	for _, name := range []string{"", "mysql", "information_schema", "performance_schema", "sys", "foo`bar", "foo-bar", "x;DROP DATABASE x"} {
		if validDatabase(name) {
			t.Errorf("accepted unsafe database %q", name)
		}
	}
	if !validDatabase("phimond_reconstruction_2") {
		t.Fatal("rejected dedicated identifier")
	}
}

func TestCredentials(t *testing.T) {
	for _, name := range []string{"ab", "has space", "你好abc", "aaaaaaaaaaaaaaaaaaaaaaaaa"} {
		if validateCredentials(name, "0123456789") == nil {
			t.Errorf("accepted %q", name)
		}
	}
	if validateCredentials("alice_1", "0123456789") != nil {
		t.Fatal("valid credentials rejected")
	}
	if validateCredentials("alice", "short") == nil {
		t.Fatal("short password accepted")
	}
}

// Opt in only against an already bootstrapped, dedicated schema. This test
// never creates/adopts databases and leaves its random fixture for inspection.
func TestMySQLAtomicMutation(t *testing.T) {
	if os.Getenv("MYSQL_TEST") != "1" {
		t.Skip("MYSQL_TEST=1 required")
	}
	ctx := context.Background()
	cfg, err := ConfigFromEnv()
	if err != nil {
		t.Fatal(err)
	}
	s, err := Open(ctx, cfg)
	if err != nil {
		t.Fatal(err)
	}
	defer s.Close()
	username, _ := randomID()
	username = "t" + username[:20]
	token, id, err := s.Register(ctx, username, "integration-password", func(id string) (json.RawMessage, error) {
		return json.Marshal(map[string]any{"id": id, "revision": 0, "pets": []any{}})
	})
	if err != nil {
		t.Fatal(err)
	}
	if got, err := s.Authenticate(ctx, token); err != nil || got != id {
		t.Fatalf("authenticate %s %v", got, err)
	}
	calls := 0
	fn := func(raw json.RawMessage) (json.RawMessage, []AuditEvent, error) {
		calls++
		var v map[string]any
		_ = json.Unmarshal(raw, &v)
		v["revision"] = 1
		b, e := json.Marshal(v)
		return b, nil, e
	}
	if _, err = s.Mutate(ctx, id, "request-1", fn); err != nil {
		t.Fatal(err)
	}
	if _, err = s.Mutate(ctx, id, "request-1", fn); err != nil {
		t.Fatal(err)
	}
	if calls != 1 {
		t.Fatalf("duplicate applied %d times", calls)
	}
	before, err := s.Read(ctx, id)
	if err != nil {
		t.Fatal(err)
	}
	if _, err = s.Mutate(ctx, id, "rollback", func(raw json.RawMessage) (json.RawMessage, []AuditEvent, error) {
		return json.RawMessage(`{}`), nil, errors.New("reject")
	}); err == nil {
		t.Fatal("callback failure committed")
	}
	after, err := s.Read(ctx, id)
	if err != nil || !bytes.Equal(before, after) {
		t.Fatal("rollback changed state")
	}
	if _, err = s.Mutate(ctx, id, "rollback", fn); err != nil {
		t.Fatal("failed request consumed dedup key", err)
	}
	if err = s.Logout(ctx, token); err != nil {
		t.Fatal(err)
	}
	if _, err = s.Authenticate(ctx, token); err == nil {
		t.Fatal("logged out token accepted")
	}
}

func TestStateIdentity(t *testing.T) {
	if validateState(json.RawMessage(`{"id":"someone-else"}`), "owner") == nil {
		t.Fatal("identity mutation accepted")
	}
	if validateState(json.RawMessage(`{"id":"owner"}`), "owner") != nil {
		t.Fatal("valid identity rejected")
	}
}
func TestConfigNeverUsesDatabaseURLPath(t *testing.T) {
	t.Setenv("MYSQL_USER", "test")
	t.Setenv("MYSQL_DATABASE", "")
	t.Setenv("GAME_DB_NAME", "")
	t.Setenv("MYSQL_PORT", "3306")
	t.Setenv("DATABASE_URL", "mysql://x:y@localhost/valuable_existing_database")
	cfg, err := ConfigFromEnv()
	if err != nil {
		t.Fatal(err)
	}
	if cfg.Database != "phimond_reconstruction" {
		t.Fatal("adopted URL database")
	}
}

func TestCustomCARejectsMissingAndInvalid(t *testing.T) {
	cfg := Config{Host: "db.example.com", Port: "3306", User: "test", Database: "phimond_test", TLS: true, CAFile: filepath.Join(t.TempDir(), "missing.pem")}
	if _, err := connect(cfg, false); err == nil {
		t.Fatal("missing CA accepted")
	}
	cfg.CAFile = filepath.Join(t.TempDir(), "invalid.pem")
	if err := os.WriteFile(cfg.CAFile, []byte("not a certificate"), 0600); err != nil {
		t.Fatal(err)
	}
	if _, err := connect(cfg, false); err == nil {
		t.Fatal("invalid CA accepted")
	}
}
func TestTLSVerifiedDefaults(t *testing.T) {
	cfg, _, err := tlsConfiguration(Config{TLS: true, Host: "db.example.com"})
	if err != nil {
		t.Fatal(err)
	}
	if cfg.InsecureSkipVerify || cfg.ServerName != "db.example.com" || cfg.MinVersion < tls.VersionTLS12 {
		t.Fatal("unsafe TLS config")
	}
}
func TestMySQLConcurrentMutations(t *testing.T) {
	if os.Getenv("MYSQL_TEST") != "1" {
		t.Skip("MYSQL_TEST=1 required")
	}
	ctx := context.Background()
	cfg, err := ConfigFromEnv()
	if err != nil {
		t.Fatal(err)
	}
	s, err := Open(ctx, cfg)
	if err != nil {
		t.Fatal(err)
	}
	defer s.Close()
	username, err := randomID()
	if err != nil {
		t.Fatal(err)
	}
	_, id, err := s.Register(ctx, "t"+username[:20], "integration-password", func(id string) (json.RawMessage, error) {
		return json.Marshal(map[string]any{"id": id, "revision": 0, "pets": []any{}})
	})
	if err != nil {
		t.Fatal(err)
	}
	var calls atomic.Int32
	fn := func(raw json.RawMessage) (json.RawMessage, []AuditEvent, error) {
		calls.Add(1)
		var v map[string]any
		if err := json.Unmarshal(raw, &v); err != nil {
			return nil, nil, err
		}
		v["revision"] = v["revision"].(float64) + 1
		b, e := json.Marshal(v)
		return b, []AuditEvent{{Type: "increment", Data: json.RawMessage(`{}`)}}, e
	}
	run := func(distinct bool) {
		start := make(chan struct{})
		errs := make(chan error, 8)
		for i := 0; i < 8; i++ {
			go func(i int) {
				<-start
				requestID := "duplicate"
				if distinct {
					requestID = fmt.Sprintf("unique-%d", i)
				}
				_, err := s.Mutate(ctx, id, requestID, fn)
				errs <- err
			}(i)
		}
		close(start)
		for i := 0; i < 8; i++ {
			if err := <-errs; err != nil {
				t.Error(err)
			}
		}
	}
	run(false)
	if calls.Load() != 1 {
		t.Fatalf("concurrent duplicate applied %d times", calls.Load())
	}
	run(true)
	if calls.Load() != 9 {
		t.Fatalf("distinct requests applied %d times", calls.Load())
	}
	raw, err := s.Read(ctx, id)
	if err != nil {
		t.Fatal(err)
	}
	var state struct {
		Revision int `json:"revision"`
	}
	if err = json.Unmarshal(raw, &state); err != nil {
		t.Fatal(err)
	}
	if state.Revision != 9 {
		t.Fatalf("lost updates: revision %d", state.Revision)
	}
	for _, table := range []string{"audit_events", "command_receipts"} {
		var count int
		if err = s.DB.QueryRowContext(ctx, "SELECT COUNT(*) FROM "+table+" WHERE character_id=?", id).Scan(&count); err != nil {
			t.Fatal(err)
		}
		if count != 9 {
			t.Fatalf("%s count %d", table, count)
		}
	}
}

func TestCustomCATrustAndHostnameVerification(t *testing.T) {
	pub, key, err := ed25519.GenerateKey(rand.Reader)
	if err != nil {
		t.Fatal(err)
	}
	template := &x509.Certificate{SerialNumber: big.NewInt(1), DNSNames: []string{"db.example.com"}, NotBefore: time.Now().Add(-time.Hour), NotAfter: time.Now().Add(time.Hour), IsCA: true, BasicConstraintsValid: true, KeyUsage: x509.KeyUsageCertSign | x509.KeyUsageDigitalSignature, ExtKeyUsage: []x509.ExtKeyUsage{x509.ExtKeyUsageServerAuth}}
	der, err := x509.CreateCertificate(rand.Reader, template, template, pub, key)
	if err != nil {
		t.Fatal(err)
	}
	path := filepath.Join(t.TempDir(), "ca.pem")
	if err = os.WriteFile(path, pem.EncodeToMemory(&pem.Block{Type: "CERTIFICATE", Bytes: der}), 0600); err != nil {
		t.Fatal(err)
	}
	cfg, _, err := tlsConfiguration(Config{Host: "db.example.com", CAFile: path})
	if err != nil {
		t.Fatal(err)
	}
	cert, err := x509.ParseCertificate(der)
	if err != nil {
		t.Fatal(err)
	}
	if _, err = cert.Verify(x509.VerifyOptions{Roots: cfg.RootCAs, DNSName: cfg.ServerName}); err != nil {
		t.Fatal(err)
	}
	if _, err = cert.Verify(x509.VerifyOptions{Roots: cfg.RootCAs, DNSName: "attacker.example.com"}); err == nil {
		t.Fatal("hostname mismatch accepted")
	}
	if cfg.InsecureSkipVerify {
		t.Fatal("certificate verification disabled")
	}
}

func TestTLSInsecureRequiresExplicitOptIn(t *testing.T) {
	t.Setenv("MYSQL_USER", "test")
	t.Setenv("MYSQL_PORT", "3306")
	t.Setenv("MYSQL_DATABASE", "phimond_reconstruction")
	t.Setenv("MYSQL_TLS_INSECURE", "")
	secure, err := ConfigFromEnv()
	if err != nil {
		t.Fatal(err)
	}
	if secure.TLSInsecure {
		t.Fatal("insecure TLS enabled by default")
	}
	t.Setenv("MYSQL_TLS_INSECURE", "true")
	insecure, err := ConfigFromEnv()
	if err != nil {
		t.Fatal(err)
	}
	if !insecure.TLSInsecure {
		t.Fatal("explicit insecure option ignored")
	}
	insecure.Host = "db.example.com"
	insecure.CAFile = ""
	cfg, insecureName, err := tlsConfiguration(insecure)
	if err != nil {
		t.Fatal(err)
	}
	if !cfg.InsecureSkipVerify {
		t.Fatal("explicit insecure option not applied")
	}
	insecure.TLSInsecure = false
	cfg, secureName, err := tlsConfiguration(insecure)
	if err != nil {
		t.Fatal(err)
	}
	if cfg.InsecureSkipVerify {
		t.Fatal("secure verification disabled")
	}
	if secureName == insecureName {
		t.Fatal("secure and insecure TLS configurations share registry key")
	}
}

func TestAuthenticationDatabaseFailureIsNotInvalidSession(t *testing.T) {
	db, err := sql.Open("mysql", "test:test@tcp(localhost:1)/unused")
	if err != nil {
		t.Fatal(err)
	}
	db.Close()
	store := &Store{DB: db}
	_, err = store.Authenticate(context.Background(), "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
	if err == nil || errors.Is(err, ErrSession) {
		t.Fatal("database outage reported as expired session", err)
	}
}
func TestUnchangedPetProjectionIgnoresJSONFormatting(t *testing.T) {
	a := json.RawMessage(`{"pets":[{"id":"a","hp":10}],"x":1}`)
	b := json.RawMessage(`{"x":2,"pets": [ {"hp":10, "id":"a"} ]}`)
	if petsChanged(a, b) {
		t.Fatal("walking rewrites unchanged pets")
	}
	if !petsChanged(a, json.RawMessage(`{"pets":[{"id":"a","hp":9}]}`)) {
		t.Fatal("health change skipped projection")
	}
}
func TestMySQLMovementCheckpoint(t *testing.T) {
	if os.Getenv("MYSQL_TEST") != "1" {
		t.Skip("MYSQL_TEST=1 required")
	}
	ctx := context.Background()
	cfg, err := ConfigFromEnv()
	if err != nil {
		t.Fatal(err)
	}
	s, err := Open(ctx, cfg)
	if err != nil {
		t.Fatal(err)
	}
	defer s.Close()
	name, _ := randomID()
	_, id, err := s.Register(ctx, "t"+name[:20], "integration-password", func(id string) (json.RawMessage, error) {
		return json.Marshal(map[string]any{"id": id, "revision": 0, "x": 6, "gold": 100, "pets": []any{}})
	})
	if err != nil {
		t.Fatal(err)
	}
	next, _ := json.Marshal(map[string]any{"id": id, "revision": 2, "x": 8, "gold": 100, "pets": []any{}})
	if err = s.Checkpoint(ctx, id, 0, next, []string{"move1", "move2"}); err != nil {
		t.Fatal(err)
	}
	if err = s.Checkpoint(ctx, id, 0, next, []string{"move1", "move2"}); err != nil {
		t.Fatal("uncertain checkpoint retry failed", err)
	}
	for _, receipt := range []string{"move1", "move2"} {
		ok, err := s.HasReceipt(ctx, id, receipt)
		if err != nil || !ok {
			t.Fatal("missing receipt", receipt, err)
		}
	}
	invalid, _ := json.Marshal(map[string]any{"id": id, "revision": 3, "x": 9, "gold": 999, "pets": []any{}})
	if err = s.Checkpoint(ctx, id, 2, invalid, []string{"forged"}); err == nil {
		t.Fatal("checkpoint changed economy")
	}
	stale, _ := json.Marshal(map[string]any{"id": id, "revision": 1, "x": 7, "gold": 100, "pets": []any{}})
	if err = s.Checkpoint(ctx, id, 0, stale, []string{"stale"}); !errors.Is(err, ErrRevisionConflict) {
		t.Fatal("stale checkpoint overwrote state", err)
	}
	got, err := s.Read(ctx, id)
	if err != nil || !sameJSON(got, next) {
		t.Fatal("failed checkpoint changed state", err)
	}
	if ok, err := s.HasReceipt(ctx, id, "forged"); err != nil || ok {
		t.Fatal("failed checkpoint consumed receipt", err)
	}
}

func TestMySQLAuditBatchPreservesEscapedJSON(t *testing.T) {
	if os.Getenv("MYSQL_TEST") != "1" {
		t.Skip("MYSQL_TEST=1 required")
	}
	ctx := context.Background()
	cfg, err := ConfigFromEnv()
	if err != nil {
		t.Fatal(err)
	}
	s, err := Open(ctx, cfg)
	if err != nil {
		t.Fatal(err)
	}
	defer s.Close()
	name, _ := randomID()
	_, id, err := s.Register(ctx, "t"+name[:20], "integration-password", func(id string) (json.RawMessage, error) {
		return json.Marshal(map[string]any{"id": id, "pets": []any{}})
	})
	if err != nil {
		t.Fatal(err)
	}
	data, _ := json.Marshal(map[string]string{"message": "quote ' slash \\ unicode 蛇 and ; --"})
	_, err = s.Mutate(ctx, id, "audit", func(raw json.RawMessage) (json.RawMessage, []AuditEvent, error) {
		return raw, []AuditEvent{{Type: "one", Data: data}, {Type: "two"}, {Type: "three", Data: data}}, nil
	})
	if err != nil {
		t.Fatal(err)
	}
	var count int
	if err = s.DB.QueryRowContext(ctx, "SELECT COUNT(*) FROM audit_events WHERE character_id=? AND request_id=?", id, "audit").Scan(&count); err != nil || count != 3 {
		t.Fatal("missing audit events", count, err)
	}
	var got []byte
	if err = s.DB.QueryRowContext(ctx, "SELECT data FROM audit_events WHERE character_id=? AND event_type=?", id, "one").Scan(&got); err != nil || !sameJSON(got, data) {
		t.Fatal("escaped audit data changed", err)
	}
}
