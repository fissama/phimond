package transport

import (
	"bytes"
	"context"
	"encoding/json"
	"io"
	"log"
	"net/http/httptest"
	"os"
	"strings"
	"testing"
	"time"

	"github.com/coder/websocket"
)

// TestStagesEvidenceDumpsGameMetrics exercises the metrics path end-to-end so
// the JSON snapshot can be used as evidence without depending on a live
// deployment. It must remain cheap and avoid network I/O.
func TestStagesEvidenceDumpsGameMetrics(t *testing.T) {
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

	// auth.session establishes the connection and populates response_ready + session_validation.
	auth := map[string]any{"op": "auth.session", "request_id": "auth", "data": map[string]string{"token": strings.Repeat("a", 64)}}
	raw, _ := json.Marshal(auth)
	if err = conn.Write(ctx, websocket.MessageText, raw); err != nil {
		t.Fatal(err)
	}
	if _, _, err = conn.Read(ctx); err != nil {
		t.Fatal(err)
	}

	// A bad envelope increments rejected_response/battle.action.
	bad := map[string]any{"op": "battle.action", "request_id": "bad1", "data": map[string]any{}}
	raw, _ = json.Marshal(bad)
	_ = conn.Write(ctx, websocket.MessageText, raw)
	if _, _, err = conn.Read(ctx); err != nil {
		t.Fatal(err)
	}

	// A second rejection to make the rejected_response counter visible.
	bad2 := map[string]any{"op": "battle.action", "request_id": "bad2", "data": map[string]any{}}
	raw, _ = json.Marshal(bad2)
	_ = conn.Write(ctx, websocket.MessageText, raw)
	if _, _, err = conn.Read(ctx); err != nil {
		t.Fatal(err)
	}

	// A real durable mutation through the in-memory store produces authority_wait + apply + durable_mutation.
	buy := map[string]any{"op": "shop.buy", "request_id": "buy1", "data": map[string]any{"item_id": "potion", "quantity": 1}}
	raw, _ = json.Marshal(buy)
	_ = conn.Write(ctx, websocket.MessageText, raw)
	if _, _, err = conn.Read(ctx); err != nil {
		t.Fatal(err)
	}

	// Drive a few world.move to populate apply + checkpoint path.
	for _, dir := range []string{"right", "right", "down"} {
		raw, _ = json.Marshal(map[string]any{"op": "world.move", "request_id": "wm" + dir, "data": map[string]any{"direction": dir}})
		_ = conn.Write(ctx, websocket.MessageText, raw)
		if _, _, err = conn.Read(ctx); err != nil {
			t.Fatal(err)
		}
	}

	// Re-emit a single snapshot using the same shape as metricsLoop. log.Print
	// writes to the default logger (stderr). Capture stderr for the duration of
	// the call so we can assert the new rejected_response label appears.
	buf := &bytes.Buffer{}
	logger := log.New(io.Writer(buf), "", log.LstdFlags)
	prev := log.Default().Writer()
	log.SetOutput(buf)
	log.SetFlags(log.LstdFlags)
	defer func() {
		log.SetOutput(prev)
		log.SetFlags(log.LstdFlags)
	}()
	_ = logger
	report := map[string]any{"kind": "game_metrics", "at": time.Now().UTC(), "latency_upper_bounds_ms": latencyBoundsMS, "latencies": s.metrics.snapshot()}
	raw2, _ := json.Marshal(report)
	log.Print(string(raw2))

	// Final body must mention the new label so the evidence file is useful.
	body := buf.String()
	if !strings.Contains(body, `"rejected_response/battle.action"`) {
		t.Fatalf("rejected_response stage missing in evidence snapshot: %s", body)
	}
	if !strings.Contains(body, `"authority_wait/shop.buy"`) {
		t.Fatalf("authority_wait stage missing in evidence snapshot: %s", body)
	}
	if !strings.Contains(body, `"durable_mutation/shop.buy"`) {
		t.Fatalf("durable_mutation stage missing in evidence snapshot: %s", body)
	}

	// When EVIDENCE_OUT is set, persist the captured JSON snapshot as the
	// refresh file. The test still passes/fails purely on assertions above.
	if path := os.Getenv("EVIDENCE_OUT"); path != "" {
		if err := os.WriteFile(path, []byte(body), 0o644); err != nil {
			t.Fatalf("write evidence: %v", err)
		}
	}
}