package transport

import (
	"context"
	"encoding/json"
	"net/http/httptest"
	"strings"
	"sync/atomic"
	"testing"
	"time"

	"github.com/coder/websocket"
)

// Kết nối đứng yên vẫn nhận ping từ máy chủ và không bị đóng.
func TestWebSocketKeepalivePing(t *testing.T) {
	old := pingInterval
	pingInterval = 40 * time.Millisecond
	defer func() { pingInterval = old }()
	s, _ := liveFixture(t)
	server := httptest.NewServer(s.Handler())
	defer server.Close()
	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	defer cancel()
	var pings atomic.Int32
	conn, _, err := websocket.Dial(ctx, "ws"+strings.TrimPrefix(server.URL, "http")+"/ws", &websocket.DialOptions{
		OnPingReceived: func(context.Context, []byte) bool { pings.Add(1); return true },
	})
	if err != nil {
		t.Fatal(err)
	}
	defer conn.CloseNow()
	raw, _ := json.Marshal(map[string]any{"op": "auth.session", "request_id": "auth", "data": map[string]string{"token": strings.Repeat("a", 64)}})
	if err = conn.Write(ctx, websocket.MessageText, raw); err != nil {
		t.Fatal(err)
	}
	if _, _, err = conn.Read(ctx); err != nil {
		t.Fatal(err)
	}
	// Không gửi gì thêm: chỉ đọc (để xử lý khung điều khiển) trong 300 ms.
	idle, stop := context.WithTimeout(ctx, 300*time.Millisecond)
	defer stop()
	_, _, err = conn.Read(idle)
	if idle.Err() == nil {
		t.Fatalf("kết nối bị đóng khi đứng yên: %v", err)
	}
	if pings.Load() < 3 {
		t.Fatalf("mong đợi ≥3 ping, nhận %d", pings.Load())
	}
}
