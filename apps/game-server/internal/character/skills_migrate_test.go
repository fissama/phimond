package character

import (
	"encoding/json"
	"phimond/server/internal/pet"
	"testing"
)

func TestLearnSkillPriceSlotsAndRelearn(t *testing.T) {
	e := engine(t)
	c := veteran(e, "t", "T", 4)
	atService(e, c)
	p := c.Pets[0]
	c.Gold = 1000
	command(t, e, c, "pet.learn", map[string]any{"pet_id": p.ID, "skill_id": "strike"})
	if c.Gold != 1000-30 || !has(c.Pets[0].Skills, "strike") {
		t.Fatalf("giá bậc 1 = 20 + 10×cấp học (30): gold=%d", c.Gold)
	}
	if _, err := e.Apply(c, "pet.learn", json.RawMessage(`{"pet_id":"`+p.ID+`","skill_id":"strike"}`)); err == nil {
		t.Fatal("không học trùng")
	}
	// Kỹ năng ngoài Native Pool/kế thừa/nhóm chung bị từ chối.
	if _, err := e.Apply(c, "pet.learn", json.RawMessage(`{"pet_id":"`+p.ID+`","skill_id":"wave_water"}`)); err == nil {
		t.Fatal("kỹ năng ngoài pool phải bị từ chối")
	}
	// Đủ 6/6: phải chọn kỹ năng thay; học lại kỹ năng đã quên giảm còn 20%.
	cp := c.Pets[0]
	cp.Level = 40
	cp.Skills = []string{"strike", "sweep", "pierce", "double", "drain", "beast_instinct"}
	cp.Learned = append([]string{}, cp.Skills...)
	if _, err := e.Apply(c, "pet.learn", json.RawMessage(`{"pet_id":"`+p.ID+`","skill_id":"claw_fire"}`)); err == nil {
		t.Fatal("6/6 mà không chọn kỹ năng thay phải bị từ chối")
	}
	gold := c.Gold
	command(t, e, c, "pet.learn", map[string]any{"pet_id": p.ID, "skill_id": "claw_fire", "replace_id": "strike"})
	if len(c.Pets[0].Skills) != 6 || has(c.Pets[0].Skills, "strike") || !has(c.Pets[0].Skills, "claw_fire") {
		t.Fatalf("thay kỹ năng: %v", c.Pets[0].Skills)
	}
	spent := gold - c.Gold
	if spent != 20+10*e.Data.Skills["claw_fire"].LearnLevel {
		t.Fatalf("học mới: %d", spent)
	}
	gold = c.Gold
	command(t, e, c, "pet.learn", map[string]any{"pet_id": p.ID, "skill_id": "strike", "replace_id": "claw_fire"})
	if want := (30*20 + 99) / 100; gold-c.Gold != want {
		t.Fatalf("học lại giảm còn 20%%: trả %d, cần %d", gold-c.Gold, want)
	}
}

func TestUpgradeSkillRankGateAndCost(t *testing.T) {
	e := engine(t)
	c := veteran(e, "t", "T", 4)
	atService(e, c)
	p := c.Pets[0]
	p.Skills = []string{"strike"}
	c.Gold = 1000
	if _, err := e.Apply(c, "pet.skill_upgrade", json.RawMessage(`{"pet_id":"`+p.ID+`","skill_id":"strike"}`)); err == nil {
		t.Fatal("cấp 3 chưa đủ cổng bậc 2")
	}
	c.Pets[0].Level = 20
	command(t, e, c, "pet.skill_upgrade", map[string]any{"pet_id": p.ID, "skill_id": "strike"})
	if c.Pets[0].Rank("strike") != 2 || c.Gold != 1000-90 {
		t.Fatalf("bậc 2 tốn 3× giá bậc 1: rank=%d gold=%d", c.Pets[0].Rank("strike"), c.Gold)
	}
	if _, err := e.Apply(c, "pet.skill_upgrade", json.RawMessage(`{"pet_id":"`+p.ID+`","skill_id":"strike"}`)); err == nil {
		t.Fatal("bậc 3 cần cấp 40")
	}
	c.Pets[0].Level = 40
	command(t, e, c, "pet.skill_upgrade", map[string]any{"pet_id": p.ID, "skill_id": "strike"})
	if c.Pets[0].Rank("strike") != 3 || c.Gold != 1000-90-180 {
		t.Fatalf("bậc 3 tốn 6×: rank=%d gold=%d", c.Pets[0].Rank("strike"), c.Gold)
	}
	if _, err := e.Apply(c, "pet.skill_upgrade", json.RawMessage(`{"pet_id":"`+p.ID+`","skill_id":"strike"}`)); err == nil {
		t.Fatal("đã tối đa bậc")
	}
}

func TestMigrateLegacySaveIsIdempotent(t *testing.T) {
	e := engine(t)
	c := veteran(e, "old", "Old", 2)
	old := &pet.Pet{ID: "p_old", SpeciesID: "snail", Name: "Cũ", Level: 12, Star: 1, HP: 30, MaxHP: 60, MP: 10, MaxMP: 20, Skills: []string{"attack", "earth_strike"}}
	c.Pets = []*pet.Pet{old}
	c.ActivePetID = old.ID
	c.Battle = &Battle{ID: "b", Turn: 2}
	if !e.MigrateLegacy(c) {
		t.Fatal("save cũ phải được chuyển")
	}
	p := c.Pets[0]
	if p.SpeciesID != "species_0111" || len(p.Grades) != 6 || p.Grades["hp"] != "B" || len(p.Skills) != 0 || p.Level != 12 {
		t.Fatalf("sau chuyển: %+v", p)
	}
	if p.MaxHP < 300 || p.HP < 1 || p.HP > p.MaxHP {
		t.Fatalf("HP tính lại theo chỉ số mới: %d/%d", p.HP, p.MaxHP)
	}
	if c.Battle != nil {
		t.Fatal("trận dở dang phải bị hủy")
	}
	before, _ := json.Marshal(c)
	if e.MigrateLegacy(c) {
		t.Fatal("chạy lần hai không được đổi gì")
	}
	after, _ := json.Marshal(c)
	if string(before) != string(after) {
		t.Fatal("migrate không idempotent")
	}
}
