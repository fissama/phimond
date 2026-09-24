// Package content loads the versioned reconstruction catalog. It contains no player state.
package content

import (
	"encoding/json"
	"fmt"
	"os"
	"path/filepath"
)

type Evidence struct {
	Confidence string `json:"confidence"`
	Source     string `json:"source"`
}
type Species struct {
	ID          string         `json:"id"`
	Name        string         `json:"name"`
	Race        string         `json:"race"`
	Element     string         `json:"element"`
	Star        int            `json:"star"`
	Archetype   string         `json:"archetype"`
	Base        map[string]int `json:"base"`
	Skills      []string       `json:"skills"`
	CaptureRate float64        `json:"capture_rate"`
	Catchable   bool           `json:"catchable"`
	Evidence
}
type Skill struct {
	ID          string  `json:"id"`
	Name        string  `json:"name"`
	Element     string  `json:"element"`
	Kind        string  `json:"kind"`
	Target      string  `json:"target"`
	Power       int     `json:"power"`
	MPCost      int     `json:"mp_cost"`
	Hit         float64 `json:"hit"`
	Status      string  `json:"status"`
	Duration    int     `json:"duration"`
	Cleanse     string  `json:"cleanse"`
	Stat        string  `json:"stat"`
	Modifier    float64 `json:"modifier"`
	LearnLevel  int     `json:"learn_level"`
	Inheritable bool    `json:"inheritable"`
	Evidence
}
type Status struct {
	ID                string   `json:"id"`
	Name              string   `json:"name"`
	Blocks            []string `json:"blocks"`
	WakeOnDamage      bool     `json:"wake_on_damage"`
	WakeMultiplier    float64  `json:"wake_multiplier"`
	FatalOnExpiry     bool     `json:"fatal_on_expiry"`
	RandomTarget      bool     `json:"random_target"`
	HitMultiplier     float64  `json:"hit_multiplier"`
	DefenseMultiplier float64  `json:"defense_multiplier"`
	Evidence
}
type Race struct {
	ID        string `json:"id"`
	Name      string `json:"name"`
	Element   string `json:"element"`
	Status    string `json:"status"`
	Cleanse   string `json:"cleanse"`
	Specialty string `json:"specialty"`
	Evidence
}
type Portal struct {
	ID    string `json:"id"`
	X     int    `json:"x"`
	To    string `json:"to"`
	Spawn int    `json:"spawn"`
}
type Map struct {
	ID            string      `json:"id"`
	Name          string      `json:"name"`
	Width         int         `json:"width"`
	Height        int         `json:"height"`
	Portals       []Portal    `json:"portals"`
	Spawns        []string    `json:"spawns"`
	WildSpawns    []WildSpawn `json:"wild_spawns"`
	MinLevel      int         `json:"min_level"`
	ArenaRequired int         `json:"arena_required"`
	Evidence
}

// Stable per-map contact positions are shared by the renderer and encounter validation.
// They reconstruct the existing spawn previews; they are not historical map data.
type WildSpawn struct {
	ID        string `json:"id"`
	SpeciesID string `json:"species_id"`
	X         int    `json:"x"`
	Y         int    `json:"y"`
}
type NPC struct {
	ID    string   `json:"id"`
	Name  string   `json:"name"`
	MapID string   `json:"map_id"`
	X     int      `json:"x"`
	Y     int      `json:"y"`
	Roles []string `json:"roles"`
	Evidence
}
type Item struct {
	ID    string `json:"id"`
	Name  string `json:"name"`
	Kind  string `json:"kind"`
	Price int    `json:"price"`
	Power int    `json:"power"`
	Evidence
}
type Recipe struct {
	ID             string `json:"id"`
	Name           string `json:"name"`
	ParentA        string `json:"parent_a"`
	ParentB        string `json:"parent_b"`
	Result         string `json:"result"`
	MinLevel       int    `json:"min_level"`
	MinPlayerLevel int    `json:"min_player_level"`
	OppositeGender bool   `json:"opposite_gender"`
	SameStar       bool   `json:"same_star"`
	CrossRace      bool   `json:"cross_race"`
	ConsumeParents bool   `json:"consume_parents"`
	SoulCost       int    `json:"soul_cost"`
	GoldCost       int    `json:"gold_cost"`
	Evidence
}
type Quest struct {
	ID          string         `json:"id"`
	Name        string         `json:"name"`
	Description string         `json:"description"`
	Kind        string         `json:"kind"`
	Target      string         `json:"target"`
	Count       int            `json:"count"`
	Gold        int            `json:"gold"`
	XP          int            `json:"xp"`
	Items       map[string]int `json:"items"`
	Recipe      string         `json:"recipe"`
	Evidence
}
type Rules struct {
	ID                  string   `json:"id"`
	QualityMin          int      `json:"quality_min"`
	QualityMax          int      `json:"quality_max"`
	QualityCap          int      `json:"quality_cap"`
	GenerationBonus     int      `json:"generation_bonus"`
	MutationRange       int      `json:"mutation_range"`
	SkillInheritance    float64  `json:"skill_inheritance"`
	AppraisalCost       int      `json:"appraisal_cost"`
	LearnCost           int      `json:"learn_cost"`
	HealCost            int      `json:"heal_cost"`
	HPBase              int      `json:"hp_base"`
	HPScale             float64  `json:"hp_scale"`
	MPBase              int      `json:"mp_base"`
	MPScale             float64  `json:"mp_scale"`
	DamageScale         float64  `json:"damage_scale"`
	CritMultiplier      float64  `json:"crit_multiplier"`
	CaptureHPScale      float64  `json:"capture_hp_scale"`
	CaptureStatusBonus  float64  `json:"capture_status_bonus"`
	CaptureCap          float64  `json:"capture_cap"`
	XPPerLevel          int      `json:"xp_per_level"`
	BattleXP            int      `json:"battle_xp"`
	BattleGold          int      `json:"battle_gold"`
	MaxLevel            int      `json:"max_level"`
	BattleTurnCap       int      `json:"battle_turn_cap"`
	Elements            []string `json:"elements"`
	MovementAllowedKeys []string `json:"movement_allowed_keys"`
	Evidence
}
type Catalog struct {
	Species  map[string]Species `json:"species"`
	Skills   map[string]Skill   `json:"skills"`
	Statuses map[string]Status  `json:"statuses"`
	Races    map[string]Race    `json:"races"`
	Maps     map[string]Map     `json:"maps"`
	NPCs     map[string]NPC     `json:"npcs"`
	Items    map[string]Item    `json:"items"`
	Recipes  map[string]Recipe  `json:"recipes"`
	Quests   map[string]Quest   `json:"quests"`
	Rules    Rules              `json:"rules"`
}

func read(root, name string, out any) error {
	b, e := os.ReadFile(filepath.Join(root, name))
	if e != nil {
		return e
	}
	if e = json.Unmarshal(b, out); e != nil {
		return fmt.Errorf("%s: %w", name, e)
	}
	return nil
}
func Load(root string) (*Catalog, error) {
	c := &Catalog{}
	for _, v := range []struct {
		p string
		v any
	}{{"pets/species.json", &c.Species}, {"skills/skills.json", &c.Skills}, {"skills/statuses.json", &c.Statuses}, {"pets/races.json", &c.Races}, {"maps/maps.json", &c.Maps}, {"npcs/npcs.json", &c.NPCs}, {"items/items.json", &c.Items}, {"recipes/recipes.json", &c.Recipes}, {"quests/quests.json", &c.Quests}, {"balance/rules.json", &c.Rules}} {
		if e := read(root, v.p, v.v); e != nil {
			return nil, e
		}
	}
	for id, m := range c.Maps {
		h := m.Height
		if h <= 0 {
			h = m.Width
		}
		for i, species := range m.Spawns {
			m.WildSpawns = append(m.WildSpawns, WildSpawn{ID: fmt.Sprintf("%s:%d", id, i), SpeciesID: species, X: min(m.Width-1, 12+i*5), Y: min(h-1, 10+(i%2)*5)})
		}
		c.Maps[id] = m
	}
	return c, c.Validate()
}
func (c *Catalog) Validate() error {
	if len(c.Species) == 0 || len(c.Maps) == 0 || c.Rules.QualityMin <= 0 || c.Rules.QualityMax < c.Rules.QualityMin || c.Rules.MutationRange < 0 || c.Rules.XPPerLevel <= 0 || c.Rules.BattleTurnCap < 1 || len(c.Rules.Elements) == 0 || len(c.Rules.MovementAllowedKeys) == 0 {
		return fmt.Errorf("invalid catalog/rules")
	}
	elementSeen := map[string]bool{}
	for _, e := range c.Rules.Elements {
		if e == "" || elementSeen[e] {
			return fmt.Errorf("invalid element list")
		}
		elementSeen[e] = true
	}
	for id, s := range c.Species {
		if id != s.ID || s.Star < 1 || s.Star > 5 || s.Confidence == "" {
			return fmt.Errorf("invalid species %s", id)
		}
		if _, ok := c.Races[s.Race]; !ok {
			return fmt.Errorf("unknown race %s", s.Race)
		}
		if !elementSeen[s.Element] {
			return fmt.Errorf("species %s uses unknown element %s", id, s.Element)
		}
		for _, k := range s.Skills {
			if _, ok := c.Skills[k]; !ok {
				return fmt.Errorf("unknown skill %s", k)
			}
		}
	}
	for id, s := range c.Skills {
		if id != s.ID || s.MPCost < 0 || s.Hit < 0 || s.Hit > 1 || s.LearnLevel < 1 {
			return fmt.Errorf("invalid skill %s", id)
		}
		if s.Status != "" {
			if _, ok := c.Statuses[s.Status]; !ok {
				return fmt.Errorf("unknown status %s", s.Status)
			}
		}
	}
	for id, r := range c.Recipes {
		if id != r.ID || r.MinLevel < 1 || r.SoulCost < 0 || r.GoldCost < 0 {
			return fmt.Errorf("invalid recipe %s", id)
		}
		for _, s := range []string{r.ParentA, r.ParentB, r.Result} {
			if _, ok := c.Species[s]; !ok {
				return fmt.Errorf("recipe %s unknown species %s", id, s)
			}
		}
	}
	for id, m := range c.Maps {
		if id != m.ID || m.Width < 2 {
			return fmt.Errorf("invalid map %s", id)
		}
		for _, p := range m.Portals {
			target, ok := c.Maps[p.To]
			if !ok || p.X < 0 || p.X >= m.Width || p.Spawn < 0 || p.Spawn >= target.Width {
				return fmt.Errorf("invalid portal %s", p.ID)
			}
		}
		for _, s := range m.Spawns {
			if _, ok := c.Species[s]; !ok {
				return fmt.Errorf("unknown spawn %s", s)
			}
		}
	}
	for _, n := range c.NPCs {
		m, ok := c.Maps[n.MapID]
		if !ok || n.X < 0 || n.X >= m.Width {
			return fmt.Errorf("invalid npc %s", n.ID)
		}
	}
	return c.validateEffects()
}

func contains(values []string, value string) bool {
	for _, v := range values {
		if v == value {
			return true
		}
	}
	return false
}
func (c *Catalog) validateEffects() error {
	r := c.Rules
	if r.SkillInheritance < 0 || r.SkillInheritance > 1 || r.CaptureCap <= 0 || r.CaptureCap > 1 || r.QualityCap < r.QualityMax || r.HPBase < 1 || r.MPBase < 0 || r.HPScale <= 0 || r.MPScale <= 0 || r.DamageScale <= 0 || r.MaxLevel < 1 {
		return fmt.Errorf("invalid balance ranges")
	}
	for id, s := range c.Skills {
		if !contains([]string{"physical", "magic", "status", "heal", "cleanse", "buff"}, s.Kind) || !contains([]string{"self", "enemy"}, s.Target) || s.Confidence == "" {
			return fmt.Errorf("invalid skill effect %s", id)
		}
		if s.Kind == "status" && (s.Status == "" || s.Duration < 1) {
			return fmt.Errorf("invalid status skill %s", id)
		}
		if s.Kind == "cleanse" {
			if _, ok := c.Statuses[s.Cleanse]; !ok {
				return fmt.Errorf("unknown cleanse %s", id)
			}
		}
		if s.Kind == "buff" && (!contains([]string{"max_hp", "max_mp", "attack", "magic", "speed", "critical", "defense"}, s.Stat) || s.Modifier <= 0 || s.Duration < 1) {
			return fmt.Errorf("invalid buff %s", id)
		}
	}
	for id, s := range c.Statuses {
		if id != s.ID || s.HitMultiplier < 0 || s.HitMultiplier > 1 || s.DefenseMultiplier <= 0 || s.WakeMultiplier <= 0 {
			return fmt.Errorf("invalid status %s", id)
		}
	}
	for id, q := range c.Quests {
		if id != q.ID || q.Count < 1 || q.Gold < 0 || q.XP < 0 {
			return fmt.Errorf("invalid quest %s", id)
		}
		for item, n := range q.Items {
			if _, ok := c.Items[item]; !ok || n < 1 {
				return fmt.Errorf("invalid quest reward %s", item)
			}
		}
		if q.Recipe != "" {
			if _, ok := c.Recipes[q.Recipe]; !ok {
				return fmt.Errorf("unknown quest recipe")
			}
		}
	}
	for id, it := range c.Items {
		if id != it.ID || it.Price < 0 || it.Power < 0 || !contains([]string{"heal", "mp", "capture", "breeding", "blessing"}, it.Kind) {
			return fmt.Errorf("invalid item %s", id)
		}
	}
	for id, sp := range c.Species {
		for _, k := range []string{"strength", "agility", "stamina", "intelligence", "spirit", "defense", "critical"} {
			if sp.Base[k] < 1 {
				return fmt.Errorf("invalid species stat %s/%s", id, k)
			}
		}
		if sp.CaptureRate < 0 || sp.CaptureRate > 1 {
			return fmt.Errorf("invalid capture rate %s", id)
		}
	}
	return nil
}
