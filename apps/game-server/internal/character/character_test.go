package character

import (
	"encoding/json"
	"math/big"
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
	c.Rules.EncounterWeights = []int{1} // test cũ giả định encounter 1v1; nhiều quái có test riêng
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
func TestGradesDifferAndAreHiddenUntilAppraised(t *testing.T) {
	e := engine(t)
	c := veteran(e, "trainer", "Trainer", 123)
	p := c.Pets[0]
	differ := false
	for i := 0; i < 20 && !differ; i++ {
		q := e.NewPet(c, "species_0111", 1)
		differ = !reflect.DeepEqual(p.Grades, q.Grades)
	}
	if !differ {
		t.Fatal("identical hidden potential")
	}
	p.Appraised = false
	b, _ := json.Marshal(e.Snapshot(c))
	var v map[string]any
	json.Unmarshal(b, &v)
	pet0 := v["pets"].([]any)[0].(map[string]any)
	for _, k := range []string{"grades", "credit", "bonus_milli"} {
		if _, ok := pet0[k]; ok {
			t.Fatalf("hidden %s exposed before appraisal", k)
		}
	}
	p.Appraised = true
	b, _ = json.Marshal(e.Snapshot(c))
	json.Unmarshal(b, &v)
	if _, ok := v["pets"].([]any)[0].(map[string]any)["grades"]; !ok {
		t.Fatal("grades must show after appraisal")
	}
}

// P11 §1: grown = base + floor(growth × hệ_số_bậc × (cấp−1)); không hồi HP khi lên cấp.
func TestStatFormulaAndGrades(t *testing.T) {
	e := engine(t)
	c := veteran(e, "t", "T", 5)
	p := e.newPet(c, "species_0021", 60, uniformGrades("B"))
	if p.MaxHP != 415+490 || p.Speed != 36+54 {
		t.Fatalf("Lv60 hạng B: hp=%d spd=%d", p.MaxHP, p.Speed)
	}
	perfect := e.newPet(c, "species_0021", 60, uniformGrades("Perfect"))
	if want := 415 + 8310*1100*59/1_000_000; perfect.MaxHP != want {
		t.Fatalf("Perfect hp=%d want %d", perfect.MaxHP, want)
	}
	d := e.newPet(c, "species_0021", 60, uniformGrades("D"))
	if d.MaxHP >= p.MaxHP || perfect.MaxHP <= p.MaxHP {
		t.Fatal("bậc phải sắp xếp D < B < Perfect")
	}
	// Lên cấp không hồi máu.
	q := e.newPet(c, "species_0071", 10, uniformGrades("B"))
	q.HP = 5
	e.petXP(q, q.Level*e.Data.Rules.XPPerLevel)
	if q.Level != 11 || q.HP != 5 {
		t.Fatalf("level=%d hp=%d (không hồi khi lên cấp)", q.Level, q.HP)
	}
	// Trần cấp theo Sao.
	r := e.newPet(c, "species_0071", 999, uniformGrades("B"))
	if r.Level != e.Data.Rules.LevelCap(e.Data.Species["species_0071"].Star) {
		t.Fatalf("level cap: %d", r.Level)
	}
}

func TestGradeDistribution(t *testing.T) {
	r := RNG{99}
	n := map[string]int{}
	const total = 200000
	for i := 0; i < total/6; i++ {
		for _, g := range rollGrades(&r) {
			n[g]++
		}
	}
	got := 0
	for _, v := range n {
		got += v
	}
	want := map[string]float64{"D": .03, "C": .12, "B": .40, "A": .28, "S": .12, "SS": .04, "Perfect": .01}
	for g, p := range want {
		f := float64(n[g]) / float64(got)
		if f < p-.01 || f > p+.01 {
			t.Errorf("%s: %.4f, cần %.2f", g, f, p)
		}
	}
}

// bonusMilli: z lớn nhất với z/1000 + (z/1000)²/(2R) ≤ Q; so với duyệt chính xác bằng số hữu tỉ.
func TestBonusMilliExact(t *testing.T) {
	check := func(q *big.Rat, r int64) {
		z := bonusMilli(q, r)
		f := func(z int) *big.Rat {
			x := big.NewRat(int64(z), 1000)
			sq := new(big.Rat).Mul(x, x)
			sq.Quo(sq, big.NewRat(2*r, 1))
			return x.Add(x, sq)
		}
		if f(z).Cmp(q) > 0 || f(z+1).Cmp(q) <= 0 {
			t.Fatalf("Q=%v R=%d: z=%d không phải cực đại", q, r, z)
		}
	}
	for _, r := range []int64{50, 100, 500} {
		for _, q := range []*big.Rat{big.NewRat(0, 1), big.NewRat(1, 3), big.NewRat(7, 2), big.NewRat(123456789, 1000), big.NewRat(1, 1000), big.NewRat(2, 1)} {
			check(q, r)
		}
	}
	if bonusMilli(big.NewRat(0, 1), 50) != 0 {
		t.Fatal("Q=0 → 0")
	}
}

func TestLineageBreedingArchivesParentsAndGrantsNoSkills(t *testing.T) {
	e := engine(t)
	c := veteran(e, "t", "T", 44)
	atService(e, c)
	a := e.newPet(c, "species_0111", 30, uniformGrades("S"))
	a.Gender = "female"
	a.Skills = []string{"strike"}
	b := e.newPet(c, "species_0022", 30, uniformGrades("S"))
	b.Gender = "male"
	b.Skills = []string{"heal"}
	c.Pets = append(c.Pets, a, b)
	c.Level = 30
	c.Recipes = []string{"snail_refinement"}
	c.Inventory["synthesis_soul"] = 3
	c.Gold = 1000
	command(t, e, c, "breeding.synthesize", map[string]any{"parent_a": a.ID, "parent_b": b.ID, "recipe_id": "snail_refinement"})
	ch := c.Pets[len(c.Pets)-1]
	if ch.Generation != 2 || len(ch.Parents) != 2 || ch.Level != 1 {
		t.Fatal("lineage missing")
	}
	if len(ch.Skills) != 0 {
		t.Fatalf("con mới sinh chưa biết kỹ năng nào: %v", ch.Skills)
	}
	if ch.Bonus["hp"] <= 0 || ch.Bonus["atk"] <= 0 {
		t.Fatalf("bố mẹ cấp 30 phải cho thưởng kế thừa: %v", ch.Bonus)
	}
	for _, id := range []string{a.ID, b.ID} {
		retired := false
		for _, p := range c.Pets {
			retired = retired || (p.ID == id && p.Retired)
		}
		if !retired {
			t.Fatal("consumed parents not archived")
		}
	}
	if len(e.Lineage(c, ch.ID).Parents) != 2 {
		t.Fatal("ancestors missing")
	}
}

// Cấp bố mẹ ≤ 20 không có tín dụng mới (P11 F02): thưởng bằng 0.
func TestLowLevelParentsGiveNoBonus(t *testing.T) {
	e := engine(t)
	c := veteran(e, "t", "T", 3)
	a := e.newPet(c, "species_0111", 20, uniformGrades("B"))
	b := e.newPet(c, "species_0022", 20, uniformGrades("B"))
	ch := e.Inherit(c, a, b, "species_0111", 0)
	for k, v := range ch.Bonus {
		if v != 0 {
			t.Fatalf("%s=%d", k, v)
		}
	}
}

func TestInheritedSkillPoolFilteredByRace(t *testing.T) {
	e := engine(t)
	c := veteran(e, "t", "T", 3)
	a := e.newPet(c, "species_0111", 30, uniformGrades("B"))
	b := e.newPet(c, "species_0022", 30, uniformGrades("B"))
	a.Skills = []string{"strike", "heal"}
	ch := e.Inherit(c, a, b, "species_0111", 0)
	race := e.Data.Species["species_0111"].Race
	for _, id := range ch.InheritedPool {
		s := e.Data.Skills[id]
		if !has(s.Inheritance, race) || s.ExclusiveSpecies != "" {
			t.Fatalf("kỹ năng %s không được kế thừa cho race %s", id, race)
		}
	}
	for _, id := range a.Skills {
		s := e.Data.Skills[id]
		if has(s.Inheritance, race) && !has(ch.InheritedPool, id) {
			t.Fatalf("thiếu %s trong pool kế thừa", id)
		}
	}
}

func TestCaptureProbabilityDistribution(t *testing.T) {
	e := engine(t)
	c := veteran(e, "t", "T", 7)
	p := e.NewPet(c, "species_0111", 1)
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
	a := veteran(e, "a", "A", 19)
	a.MapID = "emerald_forest_main_woods"
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
	c := veteran(e, "t", "T", 1)
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
func TestCreateCharacterNameAndGender(t *testing.T) {
	e := engine(t)
	c := e.NewDraft("d1", 1)
	if _, err := e.Apply(c, "world.move", json.RawMessage(`{"direction":"up"}`)); err == nil {
		t.Fatal("ô nháp không được đi")
	}
	for _, bad := range []string{`{"name":"a","gender":"male"}`, `{"name":"Ngọc Anh","gender":"x"}`, `{"name":"<b>hi</b>","gender":"female"}`, `{"name":"  ","gender":"male"}`, `{"name":"abcdefghijklmnopq","gender":"male"}`} {
		if _, err := e.Apply(c, "character.create", json.RawMessage(bad)); err == nil {
			t.Fatalf("phải từ chối %s", bad)
		}
	}
	if _, err := e.Apply(c, "character.create", json.RawMessage(`{"name":"  Ngọc   Anh ","gender":"female"}`)); err != nil {
		t.Fatal(err)
	}
	if c.Draft || c.Name != "Ngọc Anh" || c.Gender != "female" {
		t.Fatalf("%+v", c)
	}
	if c.X != 9 || c.Y != 5 {
		t.Fatalf("phải đứng giữa vòng triệu hồi (9,5): %d,%d", c.X, c.Y)
	}
	if _, err := e.Apply(c, "character.create", json.RawMessage(`{"name":"Khác","gender":"male"}`)); err == nil {
		t.Fatal("không tạo lại được")
	}
}
