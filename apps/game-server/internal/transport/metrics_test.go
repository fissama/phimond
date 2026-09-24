package transport

import (
	"context"
	"encoding/json"
	"github.com/coder/websocket"
	"net/http/httptest"
	"strings"
	"testing"
	"time"
)

func TestRejectedResponseMetrics(t *testing.T) {
	s, _ := liveFixture(t)
	s.metrics = newRuntimeMetrics(true)
	server := httptest.NewServer(s.Handler())
	defer server.Close()
	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	defer cancel()
	conn, _, err := websocket.Dial(ctx, "ws"+strings.TrimPrefix(server.URL, "http")+"/ws", nil)
	if err != nil {
		t.Fatal(err)
	}
	defer conn.CloseNow()
	for _, req := range []map[string]any{
		{"op": "auth.session", "request_id": "auth", "data": map[string]string{"token": strings.Repeat("a", 64)}},
		{"op": "battle.action", "request_id": "bad", "data": map[string]any{}},
	} {
		raw, _ := json.Marshal(req)
		if err = conn.Write(ctx, websocket.MessageText, raw); err != nil {
			t.Fatal(err)
		}
		_, raw, err = conn.Read(ctx)
		if err != nil {
			t.Fatal(err)
		}
		if req["request_id"] == "bad" {
			var response map[string]any
			_ = json.Unmarshal(raw, &response)
			if response["op"] != "error" {
				t.Fatalf("expected rejection: %s", raw)
			}
		}
	}
	stat := s.metrics.snapshot()["response_ready/battle.action"]
	if stat.Count != 1 || stat.Errors != 1 {
		t.Fatalf("rejection missing from metrics: %+v", stat)
	}
	rejected := s.metrics.snapshot()["rejected_response/battle.action"]
	if rejected.Count != 1 || rejected.Errors != 1 {
		t.Fatalf("rejected_response stage missing or miscounted: %+v", rejected)
	}
}

func TestMetricsBoundedLabelsAndBuckets(t *testing.T) {
	m := newRuntimeMetrics(true)
	m.observe("response_ready", "world.move", 10*time.Millisecond, false)
	m.observe("response_ready", "world.move", 80*time.Millisecond, true)
	for i := 0; i < 1000; i++ {
		m.observe("response_ready", string(rune(i))+"secret", time.Millisecond, false)
	}
	got := m.snapshot()
	if len(got) != 2 {
		t.Fatalf("unbounded labels: %d", len(got))
	}
	move := got["response_ready/world.move"]
	if move.Count != 2 || move.Errors != 1 || move.MaxMS != 80 || move.Buckets[2] != 1 || move.Buckets[5] != 1 {
		t.Fatalf("bad measurements: %+v", move)
	}
	off := newRuntimeMetrics(false)
	off.observe("response_ready", "world.move", time.Second, false)
	if len(off.snapshot()) != 0 {
		t.Fatal("disabled instrumentation recorded")
	}
	rej := newRuntimeMetrics(true)
	rej.observe("rejected_response", "world.move", 3*time.Millisecond, true)
	if rej.snapshot()["rejected_response/world.move"].Count != 1 {
		t.Fatal("rejected_response stage not whitelisted")
	}
	rej.observe("rejected_response", "world.move", 0, true)
	if rej.snapshot()["rejected_response/world.move"].Count != 2 {
		t.Fatal("rejected_response cumulative count broken")
	}
}

func TestOutboundBytesAndCheckpointAge(t *testing.T) {
	m := newRuntimeMetrics(true)
	m.recordBytes("battle.action", 123)
	m.recordBytes("unknown-secret", 5)
	if m.byteSnapshot()["battle.action"] != 123 || m.byteSnapshot()["other"] != 5 {
		t.Fatal("missing bounded byte counts")
	}
	off := newRuntimeMetrics(false)
	off.recordBytes("battle.action", 123)
	if len(off.byteSnapshot()) != 0 {
		t.Fatal("disabled bytes recorded")
	}
	s, _ := liveFixture(t)
	s.metrics = m
	if _, err := s.applyLive(context.Background(), "hero", move("queue", "right")); err != nil {
		t.Fatal(err)
	}
	if err := s.flushLive(context.Background(), "hero"); err != nil {
		t.Fatal(err)
	}
	if m.snapshot()["checkpoint_age/world.move"].Count != 1 {
		t.Fatal("missing oldest acknowledged move age at checkpoint")
	}
}
