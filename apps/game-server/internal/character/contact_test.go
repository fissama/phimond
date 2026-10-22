package character

import (
	"encoding/json"
	"reflect"
	"testing"
)

func TestContactEncounterMatchesVisibleSpawn(t *testing.T) {
	e := engine(t)
	c := veteran(e, "contact", "Contact", 31)
	s := e.Data.Maps[c.MapID].WildSpawns[0]
	c.X, c.Y = s.X+1, s.Y // đứng kề (kể cả chéo đều được)
	if !e.Data.Maps[c.MapID].Grid().Walkable(c.X, c.Y) {
		c.X, c.Y = s.X, s.Y
	}
	command(t, e, c, "world.encounter", map[string]any{"spawn_id": s.ID})
	if c.Battle == nil || c.Battle.Units[1].SpeciesID != s.SpeciesID || c.Battle.SpawnID != s.ID {
		t.Fatal("contact must encounter the visible spawn")
	}
}

func TestContactEncounterRejectsRemoteAndForeignSpawn(t *testing.T) {
	e0 := engine(t)
	foreign := e0.Data.Maps["emerald_forest_deep_woods"].WildSpawns[0].ID
	for _, id := range []string{"emerald_forest_main_woods:z1:0", foreign, "emerald_forest_main_woods:z1:99"} {
		e := engine(t)
		c := veteran(e, "remote", "Remote", 31) // đứng ở spawn_default, xa vùng quái
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
