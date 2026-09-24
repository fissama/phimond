package character

import (
	"context"
	"encoding/json"
	"fmt"
	"os"
	"phimond/server/internal/persistence"
	"testing"
	"time"
)

// Uses a new fixture account exclusively in a marked Phimond database.
func TestMySQLBreedingSurvivesReconnect(t *testing.T) {
	if os.Getenv("MYSQL_TEST") != "1" {
		t.Skip("MYSQL_TEST=1 required")
	}
	e := engine(t)
	cfg, err := persistence.ConfigFromEnv()
	if err != nil {
		t.Fatal(err)
	}
	ctx := context.Background()
	s, err := persistence.Open(ctx, cfg)
	if err != nil {
		t.Fatal(err)
	}
	defer s.Close()
	name := fmt.Sprintf("lineage_%d", time.Now().UnixNano()%1000000000000)
	_, id, err := s.Register(ctx, name, "integration-password", func(id string) (json.RawMessage, error) {
		c := e.NewCharacter(id, name, 99)
		a := c.Pets[0]
		a.Level = 30
		a.Gender = "female"
		a.Skills = []string{"attack", "earth_strike"}
		b := e.NewPet(c, "flower_fairy", 30)
		b.Gender = "male"
		c.Pets = append(c.Pets, b)
		c.MapID = "ranch"
		c.Level = 30
		c.Recipes = []string{"snail_refinement"}
		c.Gold = 1000
		return json.Marshal(c)
	})
	if err != nil {
		t.Fatal(err)
	}
	var childID string
	callback := func(raw json.RawMessage) (json.RawMessage, []persistence.AuditEvent, error) {
		var c Character
		json.Unmarshal(raw, &c)
		d, _ := json.Marshal(map[string]any{"parent_a": c.Pets[0].ID, "parent_b": c.Pets[1].ID, "recipe_id": "snail_refinement"})
		events, err := e.Apply(&c, "breeding.synthesize", d)
		if err != nil {
			return nil, nil, err
		}
		childID = c.Pets[2].ID
		b, _ := json.Marshal(c)
		audit := []persistence.AuditEvent{}
		for _, ev := range events {
			j, _ := json.Marshal(ev)
			audit = append(audit, persistence.AuditEvent{Type: ev.Type, Data: j})
		}
		return b, audit, nil
	}
	if _, err = s.Mutate(ctx, id, "breed-once", callback); err != nil {
		t.Fatal(err)
	}
	if _, err = s.Mutate(ctx, id, "breed-once", func(json.RawMessage) (json.RawMessage, []persistence.AuditEvent, error) {
		t.Fatal("duplicate breed ran")
		return nil, nil, nil
	}); err != nil {
		t.Fatal(err)
	}
	reopened, err := persistence.Open(ctx, cfg)
	if err != nil {
		t.Fatal(err)
	}
	defer reopened.Close()
	raw, err := reopened.Read(ctx, id)
	if err != nil {
		t.Fatal(err)
	}
	var c Character
	if err = json.Unmarshal(raw, &c); err != nil {
		t.Fatal(err)
	}
	if len(c.Pets) != 3 || c.Pets[2].ID != childID || c.Pets[2].Generation != 2 || c.Gold != 980 || c.Inventory["synthesis_soul"] != 1 {
		t.Fatal("persistent synthesis mismatch")
	}
	if len(e.Lineage(&c, childID).Parents) != 2 {
		t.Fatal("lineage not restored")
	}
	var edges int
	if err = reopened.DB.QueryRowContext(ctx, "SELECT COUNT(*) FROM pet_ancestry WHERE child_id=?", childID).Scan(&edges); err != nil || edges != 2 {
		t.Fatalf("ancestry projection: %d %v", edges, err)
	}
	var audit int
	if err = reopened.DB.QueryRowContext(ctx, "SELECT COUNT(*) FROM audit_events WHERE character_id=? AND event_type='pet_breed'", id).Scan(&audit); err != nil || audit != 1 {
		t.Fatal("duplicate or missing audit")
	}
}
