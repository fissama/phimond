package transport

import (
	"context"
	"encoding/json"
	"fmt"
	"net/http"
	"net/http/httptest"
	"os"
	"strings"
	"testing"
	"time"

	"github.com/coder/websocket"
	"phimond/server/internal/character"
	"phimond/server/internal/content"
	"phimond/server/internal/persistence"
)

// Real MySQL + real WS, with a network intermediary dropping/delaying responses.
// No production fault switch and no direct edits to existing player records.
func TestMySQLWireRecovery(t *testing.T) {
	if os.Getenv("MYSQL_TEST") != "1" {
		t.Skip("MYSQL_TEST=1 required")
	}
	cfg, err := persistence.ConfigFromEnv()
	if err != nil {
		t.Fatal(err)
	}
	db, err := persistence.Open(context.Background(), cfg)
	if err != nil {
		t.Fatal(err)
	}
	defer db.Close()
	catalog, err := content.Load("../../../../data")
	if err != nil {
		t.Fatal(err)
	}
	engine := character.NewEngine(catalog)
	for _, mode := range []string{"before_forward", "after_commit", "timeout_after_commit", "rtt300"} {
		t.Run(mode, func(t *testing.T) {
			ctx, cancel := context.WithTimeout(context.Background(), 20*time.Second)
			defer cancel()
			token, id, err := db.Register(ctx, fmt.Sprintf("p00f_%x", time.Now().UnixNano()), "integration-password", func(id string) (json.RawMessage, error) {
				return json.Marshal(engine.NewCharacter(id, "Fault test", 5))
			})
			if err != nil {
				t.Fatal(err)
			}
			t.Logf("fixture_account=%s scenario=%s", id, mode)
			server := httptest.NewServer(New(db, engine).Handler())
			defer server.Close()
			upstream := "ws" + strings.TrimPrefix(server.URL, "http") + "/ws"
			finished := make(chan struct{})
			proxy := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
				defer close(finished)
				down, e := websocket.Accept(w, r, nil)
				if e != nil {
					return
				}
				defer down.CloseNow()
				up, _, e := websocket.Dial(ctx, upstream, nil)
				if e != nil {
					return
				}
				defer up.CloseNow()
				// Pass authentication, then intercept exactly the one mutation.
				for i := 0; i < 2; i++ {
					_, raw, e := down.Read(ctx)
					if e != nil {
						return
					}
					if i == 1 && mode == "before_forward" {
						return
					}
					if i == 1 && mode == "rtt300" {
						time.Sleep(150 * time.Millisecond)
					}
					if e = up.Write(ctx, websocket.MessageText, raw); e != nil {
						return
					}
					_, raw, e = up.Read(ctx)
					if e != nil {
						return
					}
					if i == 1 && mode == "after_commit" {
						return
					}
					if i == 1 && mode == "timeout_after_commit" {
						time.Sleep(300 * time.Millisecond)
					}
					if i == 1 && mode == "rtt300" {
						time.Sleep(150 * time.Millisecond)
					}
					if e = down.Write(ctx, websocket.MessageText, raw); e != nil {
						return
					}
				}
			}))
			defer proxy.Close()
			dial := func(endpoint string) *websocket.Conn {
				t.Helper()
				c, _, e := websocket.Dial(ctx, endpoint, nil)
				if e != nil {
					t.Fatal(e)
				}
				raw, _ := json.Marshal(map[string]any{"op": "auth.session", "request_id": "auth", "data": map[string]string{"token": token}})
				if e = c.Write(ctx, websocket.MessageText, raw); e != nil {
					t.Fatal(e)
				}
				_, raw, e = c.Read(ctx)
				if e != nil {
					t.Fatal(e)
				}
				var frame struct {
					Data struct {
						Events       []any `json:"events"`
						Presentation any   `json:"presentation"`
					}
				}
				if json.Unmarshal(raw, &frame) != nil || len(frame.Data.Events) != 0 || frame.Data.Presentation != nil {
					t.Fatalf("reconnect replay: %s", raw)
				}
				return c
			}
			c := dial("ws" + strings.TrimPrefix(proxy.URL, "http") + "/ws")
			cmd := []byte(`{"op":"shop.buy","request_id":"purchase","data":{"item_id":"potion","quantity":1}}`)
			started := time.Now()
			if err = c.Write(ctx, websocket.MessageText, cmd); err != nil {
				t.Fatal(err)
			}
			readCtx := ctx
			readCancel := func() {}
			if mode == "timeout_after_commit" {
				readCtx, readCancel = context.WithTimeout(ctx, 50*time.Millisecond)
			}
			_, _, readErr := c.Read(readCtx)
			readCancel()
			c.CloseNow()
			if mode == "rtt300" {
				if readErr != nil || time.Since(started) < 300*time.Millisecond {
					t.Fatalf("delay/recovery: %v", readErr)
				}
			} else if readErr == nil {
				t.Fatal("fault failed to interrupt ack")
			}
			select {
			case <-finished:
			case <-ctx.Done():
				t.Fatal("proxy did not complete")
			}
			// New authority instance forces a DB reload, not merely the old cache.
			restarted := httptest.NewServer(New(db, engine).Handler())
			defer restarted.Close()
			recovered := dial("ws" + strings.TrimPrefix(restarted.URL, "http") + "/ws")
			defer recovered.CloseNow()
			raw, err := db.Read(ctx, id)
			if err != nil {
				t.Fatal(err)
			}
			before := loadCharacter(t, raw)
			committed := mode != "before_forward"
			wantPotions := 5
			if committed {
				wantPotions = 6
			}
			if before.Inventory["potion"] != wantPotions {
				t.Fatalf("wrong durable outcome: %d", before.Inventory["potion"])
			}
			// Explicit same-ID recovery attempt must apply at most once across restart.
			if err = recovered.Write(ctx, websocket.MessageText, cmd); err != nil {
				t.Fatal(err)
			}
			_, response, err := recovered.Read(ctx)
			if err != nil {
				t.Fatal(err)
			}
			var frame struct {
				Op   string `json:"op"`
				Data struct {
					Events    []any               `json:"events"`
					Character character.Character `json:"character"`
				}
			}
			if json.Unmarshal(response, &frame) != nil || frame.Op != "state" {
				t.Fatalf("bad recovered response: %s", response)
			}
			if frame.Data.Character.Inventory["potion"] != 6 {
				t.Fatal("purchase lost or doubled")
			}
			if committed && (frame.Data.Character.Gold != before.Gold || len(frame.Data.Events) != 0) {
				t.Fatal("duplicate cost or feedback replay")
			}
		})
	}
}
