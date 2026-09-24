package character

import (
	"encoding/json"
	"phimond/server/internal/content"
	"reflect"
	"testing"
)

func engine(t *testing.T) *Engine {
	t.Helper()
	c, err := content.Load("../../../../data")
	if err != nil {
		t.Fatal(err)
	}
	return NewEngine(c)
}
func command(t *testing.T, e *Engine, c *Character, op string, d map[string]any) []Event {
	t.Helper()
	b, _ := json.Marshal(d)
	ev, err := e.Apply(c, op, b)
	if err != nil {
		t.Fatalf("%s: %v", op, err)
	}
	return ev
}
func TestIndividualVarianceAndAppraisal(t *testing.T) {
	e := engine(t)
	c := e.NewCharacter("trainer", "Trainer", 123)
	p := c.Pets[0]
	q := e.NewPet(c, "snail", 1)
	if reflect.DeepEqual(p.Quality, q.Quality) {
		t.Fatal("identical wild potential")
	}
	p.Appraised = false
	b, _ := json.Marshal(e.Snapshot(c))
	if string(b) == "" {
		t.Fatal("empty")
	}
	var v map[string]any
	json.Unmarshal(b, &v)
	pets := v["pets"].([]any)
	if _, ok := pets[0].(map[string]any)["quality"]; ok {
		t.Fatal("hidden quality exposed")
	}
}
func TestLearnedSkillsOnlyInheritedAndParentsArchived(t *testing.T) {
	e := engine(t)
	c := e.NewCharacter("t", "T", 44)
	a := c.Pets[0]
	a.Level = 30
	a.Gender = "female"
	a.Skills = []string{"attack", "earth_strike"}
	b := e.NewPet(c, "flower_fairy", 30)
	b.Gender = "male"
	b.Skills = []string{"attack"}
	c.Pets = append(c.Pets, b)
	c.Level = 30
	c.MapID = "ranch"
	c.X = 6
	c.Recipes = []string{"snail_refinement"}
	c.Inventory["synthesis_soul"] = 3
	c.Gold = 1000
	c.ActivePetID = ""
	command(t, e, c, "breeding.synthesize", map[string]any{"parent_a": a.ID, "parent_b": b.ID, "recipe_id": "snail_refinement"})
	ch := c.Pets[len(c.Pets)-1]
	if ch.Generation != 2 || len(ch.Parents) != 2 {
		t.Fatal("lineage missing")
	}
	for _, s := range ch.Skills {
		if s != "attack" && s != "earth_strike" {
			t.Fatalf("unlearned skill inherited: %s", s)
		}
	}
	if !c.Pets[0].Retired || !c.Pets[1].Retired {
		t.Fatal("consumed parents not archived")
	}
	if len(e.Lineage(c, ch.ID).Parents) != 2 {
		t.Fatal("ancestors missing")
	}
}
func TestCaptureProbabilityDistribution(t *testing.T) {
	e := engine(t)
	c := e.NewCharacter("t", "T", 7)
	p := e.NewPet(c, "snail", 1)
	low := e.CaptureChance(p, 1, p.MaxHP, 1)
	high := e.CaptureChance(p, p.MaxHP, p.MaxHP, 1)
	if low <= high {
		t.Fatal("weakening does not help")
	}
	hits := 0
	const n = 100000
	for i := 0; i < n; i++ {
		if c.RNG.Float() < low {
			hits++
		}
	}
	rate := float64(hits) / n
	if rate < low-.01 || rate > low+.01 {
		t.Fatalf("capture distribution %f want %f", rate, low)
	}
}
func TestReplayAndInvalidTurn(t *testing.T) {
	e := engine(t)
	a := e.NewCharacter("a", "A", 19)
	a.MapID = "forest"
	a.X = 6
	command(t, e, a, "world.encounter", nil)
	raw, _ := json.Marshal(a)
	var b Character
	json.Unmarshal(raw, &b)
	for i := 0; i < 3 && a.Battle != nil; i++ {
		d := map[string]any{"battle_id": a.Battle.ID, "turn": a.Battle.Turn, "choice": "attack"}
		ea := command(t, e, a, "battle.action", d)
		eb := command(t, e, &b, "battle.action", d)
		if !reflect.DeepEqual(ea, eb) {
			t.Fatal("replay diverged")
		}
	}
	if a.Battle != nil {
		before, _ := json.Marshal(a)
		_, err := e.Apply(a, "battle.action", json.RawMessage(`{"turn":-1,"choice":"attack"}`))
		if err == nil {
			t.Fatal("stale command accepted")
		}
		after, _ := json.Marshal(a)
		if string(before) != string(after) {
			t.Fatal("invalid command changed state")
		}
	}
}
func TestRejectUnknownAndUnauthorizedIntents(t *testing.T) {
	e := engine(t)
	c := e.NewCharacter("t", "T", 1)
	for _, op := range []string{"give_gold", "pet.appraise", "breeding.synthesize", "battle.action"} {
		before, _ := json.Marshal(c)
		_, err := e.Apply(c, op, json.RawMessage(`{"pet_id":"someone_else"}`))
		if err == nil {
			t.Fatalf("accepted %s", op)
		}
		after, _ := json.Marshal(c)
		if string(before) != string(after) {
			t.Fatalf("rejected %s mutated state", op)
		}
	}
}
func TestSynthesisDistribution(t *testing.T) {
	e := engine(t)
	c := e.NewCharacter("t", "T", 42)
	a := e.NewPet(c, "snail", 30)
	b := e.NewPet(c, "flower_fairy", 30)
	a.Quality["strength"] = 1000
	b.Quality["strength"] = 1000
	total := 0
	inherited := 0
	a.Skills = []string{"attack", "earth_strike"}
	min, max := 10000, 0
	for i := 0; i < 100000; i++ {
		p := e.Inherit(c, a, b, "snail", 0)
		v := p.Quality["strength"]
		if has(p.Skills, "earth_strike") {
			inherited++
		}
		total += v
		if v < min {
			min = v
		}
		if v > max {
			max = v
		}
	}
	if inherited < 94000 || inherited > 96000 {
		t.Fatalf("skill inheritance distribution %d", inherited)
	}
	mean := float64(total) / 100000
	if mean < 1010 || mean > 1030 || max == min {
		t.Fatalf("bad inheritance distribution mean=%f range=%d-%d", mean, min, max)
	}
}

func TestMultipleGenerationsPreserveLearnedSkillAndAncestors(t *testing.T) {
	e := engine(t)
	e.Data.Rules.SkillInheritance = 1
	c := e.NewCharacter("family", "Family", 55)
	c.MapID = "ranch"
	c.Level = 30
	c.Gold = 1000
	c.Inventory["synthesis_soul"] = 5
	c.Recipes = []string{"snail_refinement"}
	first := c.Pets[0]
	first.Level = 30
	first.Gender = "female"
	first.Skills = []string{"attack", "earth_strike"}
	mate := e.NewPet(c, "flower_fairy", 30)
	mate.Gender = "male"
	c.Pets = append(c.Pets, mate)
	command(t, e, c, "breeding.synthesize", map[string]any{"parent_a": first.ID, "parent_b": mate.ID, "recipe_id": "snail_refinement"})
	second := c.Pets[2]
	second.Level = 30
	second.Gender = "female"
	mate2 := e.NewPet(c, "flower_fairy", 30)
	mate2.Gender = "male"
	c.Pets = append(c.Pets, mate2)
	command(t, e, c, "breeding.synthesize", map[string]any{"parent_a": second.ID, "parent_b": mate2.ID, "recipe_id": "snail_refinement"})
	child := c.Pets[4]
	tree := e.Lineage(c, child.ID)
	if child.Generation != 3 || len(tree.Parents) != 2 || len(tree.Parents[0].Parents) != 2 || !has(child.Skills, "earth_strike") {
		t.Fatal("multi-generation history or skill was lost")
	}
	if child.Star != 1 || child.Refinement != 2 {
		t.Fatal("star and refinement conflated")
	}
	command(t, e, c, "pet.appraise", map[string]any{"pet_id": child.ID})
	if !c.Pets[4].Appraised {
		t.Fatal("appraisal failed")
	}
}
