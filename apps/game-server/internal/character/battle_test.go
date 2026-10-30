package character

import (
	"encoding/json"
	"math/big"
	"phimond/server/internal/battle"
	"phimond/server/internal/content"
	"testing"
)

// combatFixture dựng một trận hai bên (đội: Xích Ưng hệ Hỏa; địch: Lam Lang hệ Địa) cấp 5 để test lõi P13.
func combatFixture(t *testing.T) (*Engine, *fight, *battle.Unit, *battle.Unit) {
	t.Helper()
	e := engine(t)
	c := veteran(e, "test", "Test", 31)
	p := e.NewPet(c, "species_0071", 5)
	q := e.NewPet(c, "species_0074", 5)
	a, b := unit(p, "player"), unit(q, "enemy")
	bt := &Battle{Turn: 1, RNG: RNG{1}, Units: []*battle.Unit{a, b}}
	f := &fight{e: e, b: bt, round: 1, emit: func(Event) {}}
	return e, f, a, b
}


func forceStat(e *Engine, u *battle.Unit, stat string, v int) {
	p := u.Pet
	if p.Bonus == nil {
		p.Bonus = map[string]int{}
	}
	p.Bonus[stat] = 0
	p.Bonus[stat] = v*1000 - int(e.permanentMilli(p, stat))
}

// Ví dụ P13-D06: ATK 100, DEF 50, uy lực 1.2 → 80 trung tính, 100 khắc hệ, 64 bị khắc; bạo kích ×1.5 nhân sau cùng.
func TestDamageFormulaWorkedExample(t *testing.T) {
	e, f, a, b := combatFixture(t)
	forceStat(e, b, "def", 50)
	var got = map[string]int{}
	for _, tc := range []struct{ element, species, key string }{{"neutral", "species_0074", "neutral"}, {"fire", "species_0074", "x"}} {
		_ = tc
	}
	run := func(element string) map[int]int {
		out := map[int]int{}
		for seed := uint64(1); seed < 400; seed++ {
			b.HP = b.MaxHP
			f.b.RNG = RNG{seed * 0x9e3779b97f4a7c15}
			lost, ok := f.strike(a, b, big.NewRat(100, 1), 12, 10, element, 0, false)
			if ok {
				out[lost]++
			}
		}
		return out
	}
	// Địch hệ Địa: Phong khắc Địa (×1.25), Địa khắc Thủy nên Thủy bị Địa... Hệ khắc Địa là Phong; Địa bị Thủy kháng? Kiểm trực tiếp:
	// neutral 80/120; wind (thuận) 100/150; water (nghịch: Thủy < Địa) 64/96.
	for element, want := range map[string][2]int{"neutral": {80, 120}, "wind": {100, 150}, "water": {64, 96}} {
		h := run(element)
		for dmg := range h {
			if dmg != want[0] && dmg != want[1] {
				t.Fatalf("%s: sát thương %d ngoài {%d,%d}", element, dmg, want[0], want[1])
			}
		}
		if h[want[0]] == 0 || h[want[1]] == 0 {
			t.Fatalf("%s: thiếu một mức (thường/bạo kích): %v", element, h)
		}
		got[element] = h[want[0]]
	}
}

func TestElementChart(t *testing.T) {
	tab := map[[2]string][2]int64{
		{"fire", "wind"}: {5, 4}, {"wind", "earth"}: {5, 4}, {"earth", "water"}: {5, 4}, {"water", "fire"}: {5, 4},
		{"wind", "fire"}: {4, 5}, {"earth", "wind"}: {4, 5}, {"water", "earth"}: {4, 5}, {"fire", "water"}: {4, 5},
		{"light", "dark"}: {5, 4}, {"dark", "light"}: {5, 4},
		{"fire", "earth"}: {1, 1}, {"light", "fire"}: {1, 1}, {"neutral", "fire"}: {1, 1}, {"fire", "neutral"}: {1, 1}, {"fire", "fire"}: {1, 1},
	}
	for k, w := range tab {
		n, d := elementFactor(k[0], k[1])
		if n != w[0] || d != w[1] {
			t.Errorf("%s→%s: %d/%d, cần %d/%d", k[0], k[1], n, d, w[0], w[1])
		}
	}
}

// P13-D: xác suất trạng thái 75% gặp SR 100 → 75% × (1 − 0.8·100/200) = 45%.
func TestStatusResistanceChance(t *testing.T) {
	e, _, _, b := combatFixture(t)
	forceStat(e, b, "status_resistance", 100)
	n, d := e.srChance(b, 750)
	if n*100 != 45*(d/100)*100/100*1 && n != 450_000_000 {
		t.Fatalf("p=%d/%d, cần 45%%", n, d)
	}
	forceStat(e, b, "status_resistance", 0)
	if n, d = e.srChance(b, 750); n != 750_000_000 {
		t.Fatalf("SR 0 phải giữ nguyên 75%%: %d/%d", n, d)
	}
}

func TestCooldownCastRoundPlusCPlusOne(t *testing.T) {
	e, f, a, b := combatFixture(t)
	s := e.Data.Skills["sweep"] // CD 1
	a.MP = a.MaxMP
	f.round = 4
	f.cast(a, s, 1, []*battle.Unit{b})
	if got := a.Cooldowns["sweep"]; got != 4+1+1 {
		t.Fatalf("dùng ở vòng 4, CD 1 → dùng lại được từ vòng 6, lưu %d", got)
	}
	f.round = 5
	if f.usable(a, s, 1) != "cooldown" {
		t.Fatal("vòng 5 phải còn hồi chiêu")
	}
	f.round = 6
	if f.usable(a, s, 1) != "" {
		t.Fatal("vòng 6 phải dùng được")
	}
}

func TestMPAndChannelGates(t *testing.T) {
	e, f, a, _ := combatFixture(t)
	s := e.Data.Skills["strike"]
	a.MP = 0
	if f.usable(a, s, 1) != "mp" {
		t.Fatal("thiếu MP")
	}
	a.MP = a.MaxMP
	a.Statuses = []battle.ActiveStatus{{ID: "bind", ExpireRound: 9}}
	if f.usable(a, s, 1) != "bind" {
		t.Fatal("bị trói không dùng được kỹ năng vật lý")
	}
	a.Statuses = []battle.ActiveStatus{{ID: "silence", ExpireRound: 9}}
	if f.usable(a, s, 1) != "" {
		t.Fatal("câm lặng không chặn kỹ năng vật lý")
	}
	if f.usable(a, e.Data.Skills["bolt_fire"], 1) != "silence" {
		t.Fatal("câm lặng chặn kỹ năng phép")
	}
}

func TestSleepWokenByDamageAndControlConsumed(t *testing.T) {
	_, f, a, b := combatFixture(t)
	b.Statuses = []battle.ActiveStatus{{ID: "sleep", ExpireRound: 3, Remaining: 1}}
	f.strike(a, b, big.NewRat(100, 1), 1, 1, "neutral", 0, false)
	if hasStatus(b, "sleep") && b.HP < b.MaxHP {
		t.Fatal("sát thương phải đánh thức")
	}
	a.Statuses = []battle.ActiveStatus{{ID: "petrify", ExpireRound: 3, Remaining: 1}}
	if blocked, _ := f.consumeControl(a); !blocked || hasStatus(a, "petrify") {
		t.Fatal("hóa đá phải bị tiêu ở hành động kế")
	}
}

func TestBuffClampAndStrongestOnly(t *testing.T) {
	e, _, a, _ := combatFixture(t)
	a.Buffs = []battle.Buff{{ID: "x", Stat: "atk", AmountBP: 3000}, {ID: "y", Stat: "atk", AmountBP: 2000}, {ID: "z", Stat: "atk", AmountBP: -2000}, {ID: "w", Stat: "atk", AmountBP: -4000}}
	if got := e.modBP(a, "atk"); got != 3000-4000 {
		t.Fatalf("dương mạnh nhất + âm mạnh nhất: %d", got)
	}
	a.Buffs = []battle.Buff{{ID: "x", Stat: "atk", AmountBP: 9000}}
	if got := e.modBP(a, "atk"); got != 5000 {
		t.Fatalf("chặn +50%%: %d", got)
	}
}

func TestSpeedOrderFrozenByEffectiveSPD(t *testing.T) {
	e, f, a, b := combatFixture(t)
	forceStat(e, a, "spd", 10)
	forceStat(e, b, "spd", 90)
	if o := f.order(); o[0] != b {
		t.Fatal("SPD cao đi trước")
	}
	forceStat(e, a, "spd", 90)
	a.Rank, b.Rank = 1, 2
	if o := f.order(); o[0] != a {
		t.Fatal("hòa SPD: hạng ngẫu nhiên nhỏ hơn đi trước")
	}
}

// ---- luồng qua Apply ----

func TestBattleRejectsUnlearnedSkillWithoutSpendingOrRNG(t *testing.T) {
	e := engine(t)
	c := veteran(e, "t", "Test", 3)
	command(t, e, c, "world.encounter", nil)
	raw, _ := json.Marshal(c)
	d, _ := json.Marshal(map[string]any{"battle_id": c.Battle.ID, "turn": 1, "choice": "skill", "skill_id": "strike"})
	if _, err := e.Apply(c, "battle.action", d); err == nil {
		t.Fatal("cast unlearned skill")
	}
	now, _ := json.Marshal(c)
	if string(raw) != string(now) {
		t.Fatal("invalid skill consumed state")
	}
}

func TestDefendNoLongerExists(t *testing.T) {
	e := engine(t)
	c := veteran(e, "t", "Test", 3)
	command(t, e, c, "world.encounter", nil)
	d, _ := json.Marshal(map[string]any{"battle_id": c.Battle.ID, "turn": 1, "choice": "defend"})
	if _, err := e.Apply(c, "battle.action", d); err == nil {
		t.Fatal("defend phải bị bỏ ở P13")
	}
}

func TestBasicAttackWinsAndRewards(t *testing.T) {
	e := engine(t)
	c := veteran(e, "t", "Test", 8)
	command(t, e, c, "world.encounter", nil)
	c.Battle.Units[1].HP = 1
	gold := c.Gold
	command(t, e, c, "battle.action", map[string]any{"battle_id": c.Battle.ID, "turn": 1, "choice": "attack"})
	if c.Battle != nil || len(c.History) != 1 || c.History[0].Result != "win" || c.Gold <= gold {
		t.Fatalf("thắng + thưởng: battle=%v history=%d", c.Battle != nil, len(c.History))
	}
}

func TestCaptureConsumesSealAndRollsFreshGrades(t *testing.T) {
	e := engine(t)
	c := veteran(e, "t", "Test", 8)
	command(t, e, c, "world.encounter", nil)
	wild := c.Battle.Units[1]
	wild.HP = 1
	c.Battle.Units[0].Pet.Speed = 999
	c.Battle.RNG.State = 1
	before := c.Inventory["capture_seal"]
	command(t, e, c, "battle.action", map[string]any{"battle_id": c.Battle.ID, "turn": 1, "choice": "capture"})
	if c.Inventory["capture_seal"] != before-1 {
		t.Fatal("seal not consumed")
	}
	if len(c.Pets) == 2 {
		got := c.Pets[1]
		if len(got.Grades) != 6 || got.Appraised || len(got.Skills) != 0 || len(got.Bonus) != 0 {
			t.Fatalf("pet bắt được: grades=%v appraised=%v skills=%v", got.Grades, got.Appraised, got.Skills)
		}
	}
}

func TestPublicBattleHistoryDoesNotExposeHiddenTraitsOrRNG(t *testing.T) {
	e := engine(t)
	c := veteran(e, "t", "Test", 2)
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

func TestQuestRewardsOnlyOnce(t *testing.T) {
	e := engine(t)
	c := veteran(e, "t", "Test", 2)
	atService(e, c)
	c.Quests["field_training"] = &QuestState{Progress: 3, Claimed: true}
	lio := e.Data.NPCs["forest_guide"]
	c.X, c.Y = lio.X+1, lio.Y
	command(t, e, c, "quest.accept", map[string]any{"quest_id": "first_steps"})
	home := *c
	c.X, c.Y = 33, 6
	command(t, e, c, "world.portal", map[string]any{"portal_id": "to_deep_woods"})
	c.MapID, c.X, c.Y = home.MapID, home.X, home.Y
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

var _ = content.Skill{}
