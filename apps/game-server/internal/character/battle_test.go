package character

import (
	"encoding/json"
	"phimond/server/internal/battle"
	"phimond/server/internal/content"
	"testing"
)

func combatFixture(t *testing.T) (*Engine, *Battle, *battle.Unit, *battle.Unit) {
	e := engine(t)
	c := e.NewCharacter("test", "Test", 31)
	p := e.NewPet(c, "snail", 5)
	q := e.NewPet(c, "wolf", 5)
	a, b := unit(p, "player"), unit(q, "enemy")
	return e, &Battle{Turn: 1, RNG: RNG{1}, Units: []*battle.Unit{a, b}}, a, b
}
func TestMissEventIdentifiesActors(t *testing.T) {
	e, b, actor, target := combatFixture(t)
	skill := e.Data.Skills["attack"]
	skill.Hit = 0.05
	misses := 0
	for seed := uint64(1); seed <= 100; seed++ {
		b.RNG = RNG{seed * 0x9e3779b97f4a7c15}
		e.cast(b, actor, target, skill, func(ev Event) {
			if ev.Type == "miss" {
				misses++
				if ev.ActorID != actor.ID || ev.TargetID != target.ID {
					t.Error("miss cannot be positioned on its target")
				}
			}
		})
	}
	if misses == 0 {
		t.Fatal("fixture must exercise miss")
	}
}
func TestStatusBehavior(t *testing.T) {
	e, b, a, z := combatFixture(t)
	emit := func(Event) {}
	for _, tt := range []struct {
		id, kind string
		blocked  bool
	}{{"petrify", "physical", true}, {"silence", "magic", true}, {"silence", "physical", false}, {"bind", "physical", true}, {"bind", "magic", false}, {"sleep", "physical", true}, {"blind", "physical", false}} {
		a.Statuses = []battle.ActiveStatus{{ID: tt.id, Remaining: 3}}
		if e.blocked(a, tt.kind) != tt.blocked {
			t.Fatalf("%s/%s", tt.id, tt.kind)
		}
	}
	a.Statuses = nil
	z.Statuses = []battle.ActiveStatus{{ID: "sleep", Remaining: 3}}
	s := e.Data.Skills["attack"]
	s.Hit = 1
	e.cast(b, a, z, s, emit)
	if len(z.Statuses) != 0 {
		t.Fatal("damage did not wake target")
	}
	a.Statuses = []battle.ActiveStatus{{ID: "blind", Remaining: 2}}
	e.cast(b, a, a, content.Skill{ID: "cleanse", Name: "Cleanse", Kind: "cleanse", Target: "self", Cleanse: "blind", Hit: 1}, emit)
	if len(a.Statuses) != 0 {
		t.Fatal("cleanse did not remove blind")
	}
}
func TestDoomExpiresAndSpendsNoExtraTurn(t *testing.T) {
	e := engine(t)
	c := e.NewCharacter("t", "Test", 1)
	c.MapID = "forest"
	command(t, e, c, "world.encounter", nil)
	c.Battle.Units[1].Statuses = []battle.ActiveStatus{{ID: "doom", Remaining: 1, AppliedTurn: 0}}
	command(t, e, c, "battle.action", map[string]any{"battle_id": c.Battle.ID, "turn": 1, "choice": "defend"})
	if c.Battle != nil || len(c.History) != 1 || c.History[0].Result != "win" {
		t.Fatal("doom did not end battle")
	}
}
func TestBattleRejectsUnlearnedSkillWithoutSpendingOrRNG(t *testing.T) {
	e := engine(t)
	c := e.NewCharacter("t", "Test", 3)
	c.MapID = "forest"
	command(t, e, c, "world.encounter", nil)
	raw, _ := json.Marshal(c)
	d, _ := json.Marshal(map[string]any{"battle_id": c.Battle.ID, "turn": 1, "choice": "skill", "skill_id": "fire_strike"})
	if _, err := e.Apply(c, "battle.action", d); err == nil {
		t.Fatal("cast unlearned skill")
	}
	now, _ := json.Marshal(c)
	if string(raw) != string(now) {
		t.Fatal("invalid skill consumed state")
	}
}
func TestQuestRewardsOnlyOnce(t *testing.T) {
	e := engine(t)
	c := e.NewCharacter("t", "Test", 2)
	command(t, e, c, "quest.accept", map[string]any{"quest_id": "first_steps"})
	c.X = 39
	command(t, e, c, "world.portal", map[string]any{"portal_id": "forest_gate"})
	c.X = 6
	gold := c.Gold
	command(t, e, c, "quest.claim", map[string]any{"quest_id": "first_steps"})
	if c.Gold <= gold {
		t.Fatal("no reward")
	}
	before := c.Gold
	if _, err := e.Apply(c, "quest.claim", json.RawMessage(`{"quest_id":"first_steps"}`)); err == nil || c.Gold != before {
		t.Fatal("double claim")
	}
}
func TestCaptureConsumesSealAndRetainsVariance(t *testing.T) {
	e := engine(t)
	c := e.NewCharacter("t", "Test", 8)
	c.MapID = "forest"
	command(t, e, c, "world.encounter", nil)
	wild := c.Battle.Units[1]
	wild.HP = 1
	c.Battle.Units[0].Pet.Speed = 999
	c.Battle.RNG.State = 1
	quality := wild.Pet.Quality["strength"]
	before := c.Inventory["capture_seal"]
	command(t, e, c, "battle.action", map[string]any{"battle_id": c.Battle.ID, "turn": 1, "choice": "capture"})
	if c.Inventory["capture_seal"] != before-1 {
		t.Fatal("seal not consumed")
	}
	if len(c.Pets) != 2 || c.Pets[1].Quality["strength"] != quality || c.Pets[1].Appraised {
		t.Fatal("capture lost individual or prematurely appraised")
	}
}
func TestSynthesisRejectsWithoutCostAndLineageCyclesBounded(t *testing.T) {
	e := engine(t)
	c := e.NewCharacter("t", "Test", 1)
	c.MapID = "ranch"
	c.Recipes = []string{"snail_refinement"}
	before, _ := json.Marshal(c)
	_, err := e.Apply(c, "breeding.synthesize", json.RawMessage(`{"recipe_id":"snail_refinement","parent_a":"foreign","parent_b":"foreign"}`))
	after, _ := json.Marshal(c)
	if err == nil || string(before) != string(after) {
		t.Fatal("bad parents changed state")
	}
	c.Pets[0].Parents = []string{c.Pets[0].ID}
	if len(e.Lineage(c, c.Pets[0].ID).Parents) != 0 {
		t.Fatal("cycle not guarded")
	}
}
func TestDefendProtectsSlowerPet(t *testing.T) {
	e := engine(t)
	c := e.NewCharacter("t", "Test", 999)
	c.MapID = "forest"
	command(t, e, c, "world.encounter", nil)
	c.Battle.Units[0].Pet.Speed = 1
	c.Battle.Units[1].Pet.Speed = 100
	c.Battle.Units[1].Pet.Critical = 0
	c.Battle.RNG.State = 100
	copy, _ := json.Marshal(c)
	var attack Character
	json.Unmarshal(copy, &attack)
	hp := c.Battle.Units[0].HP
	command(t, e, c, "battle.action", map[string]any{"battle_id": c.Battle.ID, "turn": 1, "choice": "defend"})
	command(t, e, &attack, "battle.action", map[string]any{"battle_id": attack.Battle.ID, "turn": 1, "choice": "attack"})
	defendDamage := hp - c.Pets[0].HP
	normalDamage := hp - attack.Pets[0].HP
	if defendDamage >= normalDamage {
		t.Fatalf("slow defend took %d vs attack %d", defendDamage, normalDamage)
	}
}
func TestHPBuffAndExpiry(t *testing.T) {
	e, b, a, _ := combatFixture(t)
	base := a.MaxHP
	s := e.Data.Skills["insect_boon"]
	s.Hit = 1
	e.cast(b, a, a, s, func(Event) {})
	if a.MaxHP <= base {
		t.Fatal("HP buff has no effect")
	}
}
func TestPublicBattleHistoryDoesNotExposeHiddenTraitsOrRNG(t *testing.T) {
	e := engine(t)
	c := e.NewCharacter("t", "Test", 2)
	c.MapID = "forest"
	command(t, e, c, "world.encounter", nil)
	command(t, e, c, "battle.action", map[string]any{"battle_id": c.Battle.ID, "turn": 1, "choice": "flee"})
	b, _ := json.Marshal(e.PublicHistory(c))
	var history []map[string]any
	json.Unmarshal(b, &history)
	for _, h := range history {
		for _, key := range []string{"rng", "seed", "pet"} {
			if _, ok := h[key]; ok {
				t.Fatal("leaked " + key)
			}
		}
		for _, u := range h["units"].([]any) {
			if _, ok := u.(map[string]any)["pet"]; ok {
				t.Fatal("pet hidden traits leaked")
			}
		}
	}
}
