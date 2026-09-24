package character

import (
	"encoding/json"
	"reflect"
	"testing"
)

func TestContactEncounterMatchesVisibleSpawn(t *testing.T) {
	e := engine(t)
	c := e.NewCharacter("contact", "Contact", 31)
	c.MapID, c.X, c.Y = "forest", 12, 10
	command(t, e, c, "world.encounter", map[string]any{"spawn_id": "forest:0"})
	if c.Battle == nil || c.Battle.Units[1].SpeciesID != "snail" {
		t.Fatal("contact must encounter visible snail")
	}
}

func TestContactEncounterRejectsRemoteAndForeignSpawn(t *testing.T) {
	for _, id := range []string{"forest:0", "beach:0", "forest:99"} {
		e := engine(t)
		c := e.NewCharacter("remote", "Remote", 31)
		c.MapID, c.X, c.Y = "forest", 1, 1
		raw, _ := json.Marshal(c)
		var before Character
		json.Unmarshal(raw, &before)
		data, _ := json.Marshal(map[string]any{"spawn_id": id})
		if _, err := e.Apply(c, "world.encounter", data); err == nil {
			t.Fatal("remote/invalid contact accepted", id)
		}
		if !reflect.DeepEqual(c, &before) {
			t.Fatal("rejected contact mutated state")
		}
	}
}
