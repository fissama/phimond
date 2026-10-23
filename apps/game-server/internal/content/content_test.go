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
