package character

import (
	"math"
	"phimond/server/internal/pet"
)

// NewPet allocates a new pet of the given species at the requested level
// and rolls quality, growth, resistances and status resistances. Moved
// verbatim from internal/game/model.go.
func (e *Engine) NewPet(c *Character, species string, level int) *pet.Pet {
	s := e.Data.Species[species]
	p := &pet.Pet{ID: c.id("pet"), SpeciesID: species, Name: s.Name, Level: level, Gender: []string{"female", "male"}[c.RNG.Int(2)], Star: s.Star, Generation: 1, Quality: map[string]int{}, Growth: map[string]int{}, Resistances: map[string]int{}, StatusResistances: map[string]int{}, Skills: []string{"attack"}, Parents: []string{}}
	for _, k := range StatKeys {
		p.Quality[k] = e.Data.Rules.QualityMin + c.RNG.Int(e.Data.Rules.QualityMax-e.Data.Rules.QualityMin+1)
		p.Growth[k] = 80 + c.RNG.Int(41)
	}
	for _, k := range e.Data.Rules.Elements {
		p.Resistances[k] = c.RNG.Int(16)
	}
	keys := sortedKeys(e.Data.Statuses)
	for _, k := range keys {
		p.StatusResistances[k] = c.RNG.Int(11)
	}
	e.Recalculate(p)
	p.HP = p.MaxHP
	p.MP = p.MaxMP
	return p
}

// Recalculate recomputes a pet's derived stats from quality, growth, level
// and star; clamps current HP/MP to the new maxima. Moved verbatim from
// internal/game/model.go.
func (e *Engine) Recalculate(p *pet.Pet) {
	s := e.Data.Species[p.SpeciesID]
	value := func(k string) float64 {
		return float64(s.Base[k])*float64(p.Quality[k])/1000 + float64(p.Level)*float64(p.Growth[k])/100*float64(p.Star)
	}
	r := e.Data.Rules
	p.MaxHP = r.HPBase + int(value("stamina")*r.HPScale)
	p.MaxMP = r.MPBase + int(value("spirit")*r.MPScale)
	p.Attack = int(value("strength"))
	p.Magic = int(value("intelligence"))
	p.Defense = int(value("defense"))
	p.Speed = int(value("agility"))
	p.Critical = math.Min(.5, value("critical")/100)
	p.HP = min(p.HP, p.MaxHP)
	p.MP = min(p.MP, p.MaxMP)
}

// petXP credits the pet with battle XP and triggers level-ups against the
// catalog rules; heals HP/MP on a level transition. Moved verbatim from
// internal/game/service.go.
func (e *Engine) petXP(p *pet.Pet, xp int) {
	p.XP += xp
	level := p.Level
	for p.Level < e.Data.Rules.MaxLevel && p.XP >= p.Level*e.Data.Rules.XPPerLevel {
		p.XP -= p.Level * e.Data.Rules.XPPerLevel
		p.Level++
	}
	if p.Level != level {
		e.Recalculate(p)
		p.HP = p.MaxHP
		p.MP = p.MaxMP
	}
}