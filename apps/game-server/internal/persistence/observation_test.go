package persistence

import (
	"context"
	"database/sql"
	"encoding/json"
	"errors"
	"os"
	"testing"
	"time"
)

func TestMySQLPoolRetainsConcurrentConnections(t *testing.T) {
	if os.Getenv("MYSQL_TEST") != "1" {
		t.Skip("MYSQL_TEST=1 required")
	}
	cfg, err := ConfigFromEnv()
	if err != nil {
		t.Fatal(err)
	}
	s, err := Open(context.Background(), cfg)
	if err != nil {
		t.Fatal(err)
	}
	defer s.Close()
	conns := []*sql.Conn{}
	defer func() {
		for _, c := range conns {
			c.Close()
		}
	}()
	for i := 0; i < 8; i++ {
		c, err := s.DB.Conn(context.Background())
		if err != nil {
			t.Fatal(err)
		}
		conns = append(conns, c)
	}
	for _, c := range conns {
		c.Close()
	}
	stat := s.DB.Stats()
	if stat.Idle != 8 || stat.MaxIdleClosed != 0 {
		t.Fatalf("steady concurrency discards reusable connections: idle=%d closed=%d", stat.Idle, stat.MaxIdleClosed)
	}
}

// Missing/incorrect stage reporting must not hide rollback or duplicate work.
func TestMySQLMutationObservations(t *testing.T) {
	if os.Getenv("MYSQL_TEST") != "1" {
		t.Skip("MYSQL_TEST=1 required")
	}
	cfg, err := ConfigFromEnv()
	if err != nil {
		t.Fatal(err)
	}
	s, err := Open(context.Background(), cfg)
	if err != nil {
		t.Fatal(err)
	}
	defer s.Close()
	name, _ := randomID()
	_, id, err := s.Register(context.Background(), "t"+name[:20], "integration-password", func(id string) (json.RawMessage, error) {
		return json.Marshal(map[string]any{"id": id, "revision": 0, "pets": []any{}})
	})
	if err != nil {
		t.Fatal(err)
	}
	seen := map[string]int{}
	failures := map[string]int{}
	ctx := WithObservation(context.Background(), func(stage string, d time.Duration, failed bool) {
		if d < 0 {
			t.Error("negative duration")
		}
		seen[stage]++
		if failed {
			failures[stage]++
		}
	})
	fn := func(raw json.RawMessage) (json.RawMessage, []AuditEvent, error) {
		var v map[string]any
		_ = json.Unmarshal(raw, &v)
		v["revision"] = 1
		b, e := json.Marshal(v)
		return b, []AuditEvent{{Type: "test", Data: json.RawMessage(`{}`)}}, e
	}
	if _, err = s.Mutate(ctx, id, "observed", fn); err != nil {
		t.Fatal(err)
	}
	for _, stage := range []string{"db_begin", "db_lock_read", "db_receipt_read", "db_state_write", "db_audit_write", "db_receipt_write", "db_commit"} {
		if seen[stage] != 1 {
			t.Errorf("missing stage %s: %v", stage, seen)
		}
	}
	if _, err = s.Mutate(ctx, id, "observed", func(json.RawMessage) (json.RawMessage, []AuditEvent, error) {
		t.Error("duplicate applied")
		return nil, nil, nil
	}); err != nil {
		t.Fatal(err)
	}
	if seen["db_commit"] != 1 || seen["db_state_write"] != 1 {
		t.Fatal("duplicate reported committed mutation")
	}
	rejected := errors.New("domain rejection")
	if _, err = s.Mutate(ctx, id, "rejected", func(json.RawMessage) (json.RawMessage, []AuditEvent, error) { return nil, nil, rejected }); !errors.Is(err, rejected) {
		t.Fatal(err)
	}
	if seen["db_commit"] != 1 {
		t.Fatal("rejection committed")
	}
	if len(failures) != 0 {
		t.Fatalf("domain rejection misclassified as DB failure: %v", failures)
	}
	canceled, cancel := context.WithCancel(ctx)
	cancel()
	if _, err = s.Mutate(canceled, id, "canceled", fn); err == nil {
		t.Fatal("cancellation ignored")
	}
	if failures["db_begin"] != 1 {
		t.Fatalf("failed begin not measured: %v", failures)
	}
}
