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
