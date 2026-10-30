package character

import (
	"fmt"
	"math"
	"phimond/server/internal/battle"
	"phimond/server/internal/pet"
)

// unit constructs a battle Unit from the given pet and side. Moved verbatim
// from internal/game/battle.go. It is kept in this package so the lowercase
// helper stays in scope of the test package without exporting it.
func unit(p *pet.Pet, side string) *battle.Unit {
	return &battle.Unit{ID: p.ID, Name: p.Name, Side: side, SpeciesID: p.SpeciesID, Level: p.Level, HP: p.HP, MP: p.MP, MaxHP: p.MaxHP, MaxMP: p.MaxMP, Statuses: []battle.ActiveStatus{}, Buffs: []battle.Buff{}, Pet: p}
}

// arenaSpecies là đối thủ cố định của Đấu trường I.
const arenaSpecies = "species_0074"

// startBattle rolls a wild pet (or a fixed arena opponent) and returns the
// first battle events. Moved verbatim from internal/game/battle.go.
func (e *Engine) startBattle(c *Character, arena bool, contactSpecies ...string) ([]Event, error) {
	p, err := findPet(c, c.ActivePetID)
	if err != nil {
		return nil, err
	}
	if p.HP <= 0 {
		return nil, fmt.Errorf("heal your active beast before battle")
	}
	pool := e.Data.Maps[c.MapID].Spawns
	if !arena && len(pool) == 0 {
		return nil, fmt.Errorf("no wild encounters here")
	}
	species := arenaSpecies
	level := 10
	if !arena {
		species = pool[c.RNG.Int(len(pool))]
		if len(contactSpecies) > 0 {
			species = contactSpecies[0]
		}
		lo, hi := e.Data.Maps[c.MapID].LevelRange()
		level = max(lo, min(hi, c.Level+1-c.RNG.Int(3)))
	}
	// Encounter hoang dã: 1 pet của người chơi đấu 1–3 quái CÙNG LOÀI (trọng số trong rules.encounter_weights, mặc
	// định 40% hai quái / 60% ba quái); đấu trường luôn 1 đối thủ.
	count := 1
	if !arena {
		count = e.encounterSize(c)
	}
	units := []*battle.Unit{unit(p, "player")}
	units[0].Rank = c.RNG.Next()
	var first *pet.Pet
	for i := 0; i < count; i++ {
		enemy := e.newWild(c, species, level)
		if first == nil {
			first = enemy
		}
		u := unit(enemy, "enemy")
		u.AISkills = e.aiSkills(e.Data.Species[species], enemy.Level)
		// Quái hoang yếu hơn pet nuôi cùng cấp (rules.wild_scale), đàn quái yếu thêm theo rules.pack_scale
		// để 1 pet vẫn thắng được 2–3 quái cùng cấp. Chỉ áp lên đơn vị trong trận; pet bắt được giữ chỉ số gốc.
		if !arena {
			scale := 1.0
			if w := e.Data.Rules.WildScale; w > 0 {
				scale *= w
			}
			if ps := e.Data.Rules.PackScale; count > 1 && count <= len(ps) && ps[count-1] > 0 {
				scale *= ps[count-1]
			}
			if scale != 1 {
				u.MaxHP = max(1, int(math.Round(float64(u.MaxHP)*scale)))
				u.HP = u.MaxHP
				u.Power = scale
			}
		}
		u.Rank = c.RNG.Next()
		units = append(units, u)
	}
	seed := c.RNG.Next()
	b := &Battle{ID: c.id("battle"), Turn: 1, Phase: "WAIT_COMMAND", Units: units, Seed: seed, RNG: RNG{seed}, Arena: arena, Commands: []Intent{}, Events: []Event{}}
	c.Battle = b
	return []Event{event("battle_start", "Encountered "+first.Name)}, nil
}

// encounterSize rolls how many wild monsters join the encounter, from rules.encounter_weights.
func (e *Engine) encounterSize(c *Character) int {
	w := e.Data.Rules.EncounterWeights
	total := 0
	for _, v := range w {
		total += max(0, v)
	}
	if total <= 0 {
		return 1
	}
	r := c.RNG.Int(total)
	for i, v := range w {
		if r < max(0, v) {
			return i + 1
		}
		r -= max(0, v)
	}
	return 1
}

// sideUnits returns the units on one side (stable battle order).
func sideUnits(b *Battle, side string) []*battle.Unit {
	out := []*battle.Unit{}
	for _, u := range b.Units {
		if u.Side == side {
			out = append(out, u)
		}
	}
	return out
}

// firstAlive returns the first living unit among us, or nil.
func firstAlive(us []*battle.Unit) *battle.Unit {
	for _, u := range us {
		if u.HP > 0 {
			return u
		}
	}
	return nil
}

func anyAlive(us []*battle.Unit) bool { return firstAlive(us) != nil }
