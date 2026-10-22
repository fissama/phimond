package character

import (
	"encoding/json"
	"fmt"
	"testing"
)

// Encounter hoang: 1 pet đấu 2–3 quái cùng loài; tỉ lệ 3 quái cao hơn 2 quái.
func TestWildEncounterSpawnsTwoOrThreeIdenticalFoes(t *testing.T) {
	e := engine(t)
	e.Data.Rules.EncounterWeights = []int{0, 40, 60}
	counts := map[int]int{}
	for i := 0; i < 400; i++ {
		c := veteran(e, fmt.Sprintf("t%d", i), "Test", 1)
		c.MapID = "emerald_forest_main_woods"
		c.RNG.State = uint64(i+1) * 0x9e3779b97f4a7c15
		command(t, e, c, "world.encounter", nil)
		foes := sideUnits(c.Battle, "enemy")
		counts[len(foes)]++
		for _, f := range foes {
			if f.SpeciesID != foes[0].SpeciesID || f.Pet.Level != foes[0].Pet.Level {
				t.Fatal("foes must be identical species and level")
			}
		}
		if len(c.Battle.Units) != len(foes)+1 || c.Battle.Units[0].Side != "player" {
			t.Fatal("player unit must lead")
		}
	}
	if counts[1] != 0 || counts[2] == 0 || counts[3] <= counts[2] {
		t.Fatalf("expected only 2–3 foes with 3 more likely: %v", counts)
	}
}

func TestMultiFoeBattleNeedsAllDefeatedAndSumsRewards(t *testing.T) {
	e := engine(t)
	e.Data.Rules.EncounterWeights = []int{0, 0, 1}
	c := veteran(e, "t", "Test", 1)
	c.MapID = "emerald_forest_main_woods"
	command(t, e, c, "world.encounter", nil)
	foes := sideUnits(c.Battle, "enemy")
	if len(foes) != 3 {
		t.Fatalf("want 3 foes got %d", len(foes))
	}
	for _, f := range foes[:2] {
		f.HP = 0
	}
	foes[2].HP = 1
	gold := c.Gold
	// Target a dead foe is rejected.
	if _, err := e.Apply(c, "battle.action", mustJSON(map[string]any{"battle_id": c.Battle.ID, "turn": 1, "choice": "attack", "target_id": foes[0].ID})); err == nil {
		t.Fatal("dead target must be rejected")
	}
	c.Battle.Units[0].Pet.Attack = 9999
	command(t, e, c, "battle.action", map[string]any{"battle_id": c.Battle.ID, "turn": 1, "choice": "attack", "target_id": foes[2].ID})
	if c.Battle != nil || c.History[len(c.History)-1].Result != "win" {
		t.Fatal("killing the last foe must win")
	}
	if c.Gold != gold+3*e.Data.Rules.BattleGold {
		t.Fatalf("gold must scale with foes: %d", c.Gold-gold)
	}
}

func mustJSON(v any) []byte { b, _ := json.Marshal(v); return b }
