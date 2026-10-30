package character

import (
	"phimond/server/internal/pet"
)

// NewPet tạo một linh thú đủ máu/MP với bậc tăng trưởng rút theo bảng P11 (F01); thưởng kế thừa bằng 0.
// Không có kỹ năng nào được tặng (P13: pet mới 0/6 kỹ năng, chỉ có đòn thường).
func (e *Engine) NewPet(c *Character, species string, level int) *pet.Pet {
	p := e.newPet(c, species, level, rollGrades(&c.RNG))
	return p
}

// newWild tạo quái hoang: cùng công thức, toàn bộ bậc B, Q=0 (P11 §7).
func (e *Engine) newWild(c *Character, species string, level int) *pet.Pet {
	return e.newPet(c, species, level, uniformGrades("B"))
}

func (e *Engine) newPet(c *Character, species string, level int, grades map[string]string) *pet.Pet {
	s := e.Data.Species[species]
	level = max(1, min(level, e.Data.Rules.LevelCap(s.Star)))
	p := &pet.Pet{ID: c.id("pet"), SpeciesID: species, Name: s.Name, Level: level, Gender: []string{"female", "male"}[c.RNG.Int(2)], Star: s.Star, Generation: 1, Grades: grades, Credit: map[string]pet.Credit{}, Bonus: map[string]int{}, Skills: []string{}, Parents: []string{}}
	e.Recalculate(p)
	p.HP = p.MaxHP
	p.MP = p.MaxMP
	return p
}

// petXP cộng XP trận cho pet và lên cấp theo luật catalog, tới cấp tối đa của Sao. Lên cấp không hồi HP/MP
// (P11 §5): máu hiện tại giữ nguyên rồi bị chặn theo mức tối đa mới.
func (e *Engine) petXP(p *pet.Pet, xp int) {
	cap := e.levelCap(p)
	if p.Level >= cap {
		return
	}
	p.XP += xp
	level := p.Level
	for p.Level < cap && p.XP >= p.Level*e.Data.Rules.XPPerLevel {
		p.XP -= p.Level * e.Data.Rules.XPPerLevel
		p.Level++
	}
	if p.Level >= cap {
		p.XP = 0
	}
	if p.Level != level {
		e.Recalculate(p)
	}
}
