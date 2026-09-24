package transport

import (
	"context"
	"encoding/json"
	"net/http/httptest"
	"os"
	"path/filepath"
	"strings"
	"testing"
	"time"

	"github.com/coder/websocket"
	"phimond/server/internal/character"
)

// Real websocket/engine with memory persistence: catches replay on auth/read
// and missing terminal units when authoritative battle becomes null.
func TestStatePresentationContract(t *testing.T) {
	s, db := liveFixture(t)
	c := loadCharacter(t, db.raw)
	c.MapID = "forest"
	if _, err := s.Game.Apply(c, "world.encounter", json.RawMessage(`{}`)); err != nil {
		t.Fatal(err)
	}
	db.raw, _ = json.Marshal(c)
	server := httptest.NewServer(s.Handler())
	defer server.Close()
	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	defer cancel()
	conn, _, err := websocket.Dial(ctx, "ws"+strings.TrimPrefix(server.URL, "http")+"/ws", nil)
	if err != nil {
		t.Fatal(err)
	}
	defer conn.CloseNow()
	send := func(id, op string, data any) map[string]any {
		t.Helper()
		b, _ := json.Marshal(map[string]any{"op": op, "request_id": id, "data": data})
		if err := conn.Write(ctx, websocket.MessageText, b); err != nil {
			t.Fatal(err)
		}
		_, b, err = conn.Read(ctx)
		if err != nil {
			t.Fatal(err)
		}
		var result map[string]any
		if err := json.Unmarshal(b, &result); err != nil {
			t.Fatal(err)
		}
		if result["op"] != "state" {
			t.Fatalf("expected state: %s", b)
		}
		return result["data"].(map[string]any)
	}
	auth := send("auth", "auth.session", map[string]string{"token": strings.Repeat("a", 64)})
	if events, ok := auth["events"].([]any); !ok || len(events) != 0 {
		t.Errorf("auth must not replay persisted events: %v", auth["events"])
	}
	read := send("read", "character.get", map[string]any{})
	if events, ok := read["events"].([]any); !ok || len(events) != 0 {
		t.Errorf("read must not replay persisted events: %v", read["events"])
	}
	action := character.Intent{BattleID: c.Battle.ID, Turn: 1, Choice: "flee"}
	result := send("finish", "battle.action", action)
	if result["character"].(map[string]any)["battle"] != nil {
		t.Fatal("flee must end battle")
	}
	p, ok := result["presentation"].(map[string]any)
	if !ok {
		t.Fatal("terminal response missing presentation")
	}
	b, ok := p["completed_battle"].(map[string]any)
	if !ok || b["id"] != c.Battle.ID || b["result"] != "flee" {
		t.Fatalf("wrong terminal battle: %v", p)
	}
	if len(b["units"].([]any)) != 2 {
		t.Fatal("missing public render units")
	}
	encoded, _ := json.Marshal(result)
	for _, private := range []string{`"rng"`, `"seed"`, `"commands"`, `"wild"`, `"pet"`, `"battle_history"`, `"last_events"`} {
		if strings.Contains(string(encoded), private) {
			t.Fatalf("private field leaked: %s", private)
		}
	}
	duplicate := send("finish", "battle.action", action)
	if len(duplicate["events"].([]any)) != 0 || duplicate["presentation"] != nil {
		t.Fatal("duplicate receipt must be state-only")
	}
}

// Exported evidence is generated only by tests, never by a production endpoint.
// Test accounts learn extra skills and start hurt; catalog formulas stay intact.
func TestPublicBattleFeedbackFixtures(t *testing.T) {
	for _, scenario := range []struct{ name, choice, skill, want string }{
		{"damage", "attack", "", "damage"}, {"heal", "skill", "mend", "heal"},
		{"status", "skill", "petrify", "status_applied"}, {"miss", "attack", "", "miss"},
		{"win", "attack", "", "battle_win"}, {"loss", "defend", "", "battle_loss"},
		{"capture", "capture", "", "pet_capture"}, {"flee", "flee", "", "battle_flee"},
	} {
		t.Run(scenario.name, func(t *testing.T) {
			found := false
			for seed := uint64(1); seed < 300 && !found; seed++ {
				s, db := liveFixture(t)
				c := loadCharacter(t, db.raw)
				c.MapID = "forest"
				if _, err := s.Game.Apply(c, "world.encounter", json.RawMessage(`{}`)); err != nil {
					t.Fatal(err)
				}
				b := c.Battle
				b.RNG = character.RNG{State: seed * 0x9e3779b97f4a7c15}
				p := b.Units[0]
				p.Pet.Skills = append(p.Pet.Skills, "mend", "petrify")
				p.MP = 100
				if scenario.name == "heal" {
					p.HP = p.MaxHP / 2
				}
				if scenario.name == "win" {
					b.Units[1].HP = 1
				}
				if scenario.name == "loss" {
					p.HP = 1
				}
				raw, _ := json.Marshal(c)
				initialRaw := append(json.RawMessage{}, raw...)
				initial, err := s.stateEnvelope(envelope{Op: "auth.session"}, raw, false)
				if err != nil {
					t.Fatal(err)
				}
				intent, _ := json.Marshal(character.Intent{BattleID: b.ID, Turn: b.Turn, Choice: scenario.choice, SkillID: scenario.skill})
				m := envelope{Op: "battle.action", RequestID: "fixture", Data: intent}
				raw, _, err = s.applyGame(raw, m)
				if err != nil {
					t.Fatal(err)
				}
				out := loadCharacter(t, raw)
				for _, ev := range out.Events {
					if ev.Type != scenario.want {
						continue
					}
					found = true
					if scenario.want == "miss" || scenario.want == "heal" || scenario.want == "damage" || scenario.want == "status_applied" {
						if ev.TargetID == "" {
							t.Fatal("feedback has no target")
						}
					}
				}
				if !found {
					continue
				}
				// Re-run the selected seeded scenario through the real websocket
				// handler; exported frames are exactly the received wire payloads.
				db.raw = initialRaw
				server := httptest.NewServer(s.Handler())
				ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
				conn, _, err := websocket.Dial(ctx, "ws"+strings.TrimPrefix(server.URL, "http")+"/ws", nil)
				if err != nil {
					cancel()
					server.Close()
					t.Fatal(err)
				}
				exchange := func(request envelope) map[string]any {
					t.Helper()
					bytes, _ := json.Marshal(request)
					if err := conn.Write(ctx, websocket.MessageText, bytes); err != nil {
						t.Fatal(err)
					}
					_, bytes, err := conn.Read(ctx)
					if err != nil {
						t.Fatal(err)
					}
					var response map[string]any
					if err := json.Unmarshal(bytes, &response); err != nil {
						t.Fatal(err)
					}
					if response["op"] != "state" {
						t.Fatalf("unexpected wire response %s", bytes)
					}
					return response
				}
				authData, _ := json.Marshal(map[string]string{"token": strings.Repeat("a", 64)})
				initial = exchange(envelope{Op: "auth.session", RequestID: "auth", Data: authData})
				action := exchange(m)
				conn.CloseNow()
				cancel()
				server.Close()
				if dir := os.Getenv("P00_WIRE_FIXTURES"); dir != "" {
					if err := os.MkdirAll(dir, 0700); err != nil {
						t.Fatal(err)
					}
					bytes, _ := json.MarshalIndent(map[string]any{"initial": initial, "action": action, "expected": scenario.want, "seeded_test_fixture": true}, "", "  ")
					if err := os.WriteFile(filepath.Join(dir, scenario.name+".json"), bytes, 0600); err != nil {
						t.Fatal(err)
					}
				}
			}
			if !found {
				t.Fatal("no matching seeded scenario")
			}
		})
	}
}
