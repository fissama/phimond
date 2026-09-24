package character

import (
	"fmt"
	"math"
	"phimond/server/internal/pet"
)

// Inherit applies the (reconstructed) breeding formula to the two parent
// pets, producing a fresh child of the requested species with the supplied
// blessing. Inherits only instance skills the parents actually learned,
// never species skill pools. Moved verbatim from internal/game/breeding.go.
func (e *Engine) Inherit(c *Character, a, b *pet.Pet, species string, blessing int) *pet.Pet {
	child := e.NewPet(c, species, 1)
	r := e.Data.Rules
	child.Generation = max(a.Generation, b.Generation) + 1
	child.Parents = []string{a.ID, b.ID}
	child.Refinement = a.Refinement + min(5, max(1, (a.Level+b.Level-40)/20))
	child.Blessing = blessing
	for _, key := range StatKeys {
		v := (a.Quality[key]+b.Quality[key])/2 + r.GenerationBonus + (a.Strengthening+b.Strengthening)*5 + blessing*10 + c.RNG.Int(r.MutationRange*2+1) - r.MutationRange
		child.Quality[key] = min(r.QualityCap, max(r.QualityMin, v))
		child.Growth[key] = min(160, (a.Growth[key]+b.Growth[key])/2+2+c.RNG.Int(5)-2)
	}
	for _, key := range sortedKeys(child.Resistances) {
		child.Resistances[key] = min(70, (a.Resistances[key]+b.Resistances[key])/2+c.RNG.Int(4))
	}
	for _, key := range sortedKeys(child.StatusResistances) {
		child.StatusResistances[key] = min(70, (a.StatusResistances[key]+b.StatusResistances[key])/2+c.RNG.Int(4))
	}
	inherited := map[string]bool{"attack": true}
	for _, p := range []*pet.Pet{a, b} {
		for _, skill := range p.Skills {
			if e.Data.Skills[skill].Inheritable {
				inherited[skill] = true
			}
		}
	}
	child.Skills = []string{"attack"}
	for _, skill := range sortedKeys(inherited) {
		if skill != "attack" && c.RNG.Float() < r.SkillInheritance {
			child.Skills = append(child.Skills, skill)
		}
	}
	e.Recalculate(child)
	child.HP = child.MaxHP
	child.MP = child.MaxMP
	return child
}

// breed is the breeding.synthesize intent handler. Validates the recipe,
// parents, materials and player level before rolling a child. Moved
// verbatim from internal/game/breeding.go.
func (e *Engine) breed(c *Character, d Intent) ([]Event, error) {
	if err := e.near(c, "breed"); err != nil {
		return nil, err
	}
	r, ok := e.Data.Recipes[d.RecipeID]
	if !ok || !has(c.Recipes, r.ID) {
		return nil, fmt.Errorf("learn this recipe first")
	}
	a, err := findPet(c, d.ParentA)
	if err != nil {
		return nil, err
	}
	b, err := findPet(c, d.ParentB)
	if err != nil {
		return nil, err
	}
	if a.ID == b.ID {
		return nil, fmt.Errorf("two distinct parents required")
	}
	if a.SpeciesID != r.ParentA || b.SpeciesID != r.ParentB {
		return nil, fmt.Errorf("recipe requires ordered main and secondary parents")
	}
	if a.Level < r.MinLevel || b.Level < r.MinLevel || c.Level < r.MinPlayerLevel {
		return nil, fmt.Errorf("parents must reach level %d", r.MinLevel)
	}
	if r.OppositeGender && a.Gender == b.Gender {
		return nil, fmt.Errorf("opposite genders required")
	}
	if r.SameStar && a.Star != b.Star {
		return nil, fmt.Errorf("equal stars required")
	}
	if r.CrossRace && e.Data.Species[a.SpeciesID].Race == e.Data.Species[b.SpeciesID].Race {
		return nil, fmt.Errorf("different races required")
	}
	if d.Blessing < 0 || d.Blessing > 1 {
		return nil, fmt.Errorf("invalid blessing")
	}
	if c.Gold < r.GoldCost || c.Inventory["synthesis_soul"] < r.SoulCost || c.Inventory["blessing_leaf"] < d.Blessing {
		return nil, fmt.Errorf("insufficient synthesis materials or gold")
	}
	child := e.Inherit(c, a, b, r.Result, d.Blessing)
	if r.ConsumeParents {
		a.Retired = true
		b.Retired = true
	}
	c.Gold -= r.GoldCost
	c.Inventory["synthesis_soul"] -= r.SoulCost
	c.Inventory["blessing_leaf"] -= d.Blessing
	c.Pets = append(c.Pets, child)
	if c.ActivePetID == a.ID || c.ActivePetID == b.ID || c.ActivePetID == "" {
		c.ActivePetID = child.ID
	}
	e.progress(c, "pet_breed", child.SpeciesID)
	return []Event{event("pet_breed", fmt.Sprintf("A generation %d %s was born. Both ancestors remain in the lineage archive.", child.Generation, child.Name)), event("currency_spend", fmt.Sprintf("Spent %d gold", r.GoldCost)), event("item_spend", "Synthesis materials consumed")}, nil
}

// CaptureChance returns the capture success probability for the wild pet at
// the given HP / trainer level, factoring in status bonus and star penalty.
// Moved verbatim from internal/game/breeding.go.
func (e *Engine) CaptureChance(p *pet.Pet, hp, maxHP, trainerLevel int) float64 {
	if hp <= 0 || maxHP <= 0 || !e.Data.Species[p.SpeciesID].Catchable {
		return 0
	}
	r := e.Data.Rules
	base := e.Data.Species[p.SpeciesID].CaptureRate
	level := math.Min(1.2, math.Max(.4, 1+float64(trainerLevel-p.Level)*.02))
	return math.Min(r.CaptureCap, base*(1+(1-float64(hp)/float64(maxHP))*r.CaptureHPScale)*level/float64(p.Star))
}