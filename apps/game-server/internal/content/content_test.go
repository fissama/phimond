package content

import (
	"testing"
)

func TestCatalogLinksAndConfidence(t *testing.T) {
	c, e := Load("../../../../data")
	if e != nil {
		t.Fatal(e)
	}
	if len(c.Species) < 10 || len(c.Skills) < 20 || len(c.Statuses) != 7 || len(c.Races) != 8 {
		t.Fatal("vertical slice catalog incomplete")
	}
	s := c.Species["snail"]
	s.Skills = []string{"nonexistent"}
	c.Species["snail"] = s
	if c.Validate() == nil {
		t.Fatal("dangling skill accepted")
	}
}
func TestRejectBadEffectAndRecipeDefinitions(t *testing.T) {
	for _, change := range []func(*Catalog){func(c *Catalog) { s := c.Skills["attack"]; s.Kind = "unknown_effect"; c.Skills["attack"] = s }, func(c *Catalog) { s := c.Skills["cleanse_doom"]; s.Cleanse = "missing"; c.Skills[s.ID] = s }, func(c *Catalog) { q := c.Quests["first_capture"]; q.Items["missing"] = 1; c.Quests[q.ID] = q }, func(c *Catalog) { c.Rules.SkillInheritance = 2 }} {
		c, e := Load("../../../../data")
		if e != nil {
			t.Fatal(e)
		}
		change(c)
		if c.Validate() == nil {
			t.Fatal("invalid content accepted")
		}
	}
}

// Bố cục Triệu Linh Điện (v1.0.0): nhân vật xuất hiện giữa vòng triệu hồi; Mira đứng bên phải, dưới trụ thần thú
// vàng (trụ thứ ba) nhưng vẫn ở hàng trên vòng triệu hồi của người chơi.
func TestSummoningHallLayout(t *testing.T) {
	c, e := Load("../../../../data")
	if e != nil {
		t.Fatal(e)
	}
	m, ok := c.Maps["summoning_hall_main_hall"]
	if !ok || len(m.Pedestals) != 3 {
		t.Fatal("thiếu bản đồ sảnh hoặc trụ")
	}
	if m.SpawnDefault.X != m.Width/2 {
		t.Fatalf("điểm xuất hiện lệch tâm vòng triệu hồi: x=%d, tâm=%d", m.SpawnDefault.X, m.Width/2)
	}
	gold := m.Pedestals[2]
	mira := c.NPCs["summoner_mira"]
	if mira.X != gold.X+1 || mira.Y != gold.Y+1 {
		t.Fatalf("Mira phải ở chéo phải-dưới trụ vàng (%d,%d), đang ở (%d,%d)", gold.X, gold.Y, mira.X, mira.Y)
	}
	if mira.Y >= m.SpawnDefault.Y {
		t.Fatalf("Mira phải ở trên vòng triệu hồi (hàng %d), đang ở hàng %d", m.SpawnDefault.Y, mira.Y)
	}
}

// Bố cục tương đối theo bản phác APK/P12 đã chốt: trụ teleport dưới-phải Quảng Trường (U1); Quảng Trường đi sang
// Hoàng Môn bằng mép phải và sang Chợ bằng mép trái; Hoàng Môn thứ tự cổng trái→phải: Quảng Trường, cung điện, Chợ;
// Sảnh xếp 3 bệ thành cung (bệ giữa lùi sau).
func TestRelativeLayoutFollowsApkSketch(t *testing.T) {
	c, e := Load("../../../../data")
	if e != nil {
		t.Fatal(e)
	}
	sq, gate, hall := c.Maps["city_square"], c.Maps["city_palace_gate"], c.Maps["summoning_hall_main_hall"]
	if sq.Pillar == nil || sq.Pillar.X <= sq.Width/2 || sq.Pillar.Y <= sq.Height/2 {
		t.Fatalf("trụ teleport phải ở dưới-phải Quảng Trường: %+v", sq.Pillar)
	}
	cx := func(m Map, id string) int {
		for _, p := range m.Portals {
			if p.ID == id {
				return p.Rect[0] + p.Rect[2]/2
			}
		}
		t.Fatalf("thiếu cổng %s", id)
		return 0
	}
	if !(cx(sq, "square_to_market") < sq.Width/2 && cx(sq, "square_to_gate") > sq.Width/2) {
		t.Fatal("Quảng Trường: Chợ bên trái, Hoàng Môn bên phải")
	}
	if !(cx(gate, "gate_to_square") < cx(gate, "gate_to_palace") && cx(gate, "gate_to_palace") < cx(gate, "gate_to_market")) {
		t.Fatal("Hoàng Môn: thứ tự cổng trái→phải phải là Quảng Trường, cung điện, Chợ")
	}
	if !(hall.Pedestals[1].Y < hall.Pedestals[0].Y && hall.Pedestals[1].Y < hall.Pedestals[2].Y) {
		t.Fatal("Sảnh: bệ giữa phải lùi sau hai bệ bên (cung 3 bệ)")
	}
}
