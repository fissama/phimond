package character

import (
	"fmt"
	"phimond/server/internal/content"
	"phimond/server/internal/pet"
)

// Học và nâng bậc kỹ năng theo P13 §1: hợp lệ khi thuộc Native Pool, kế thừa hoặc nhóm chung (strike/heal/guard); cần cấp,
// vàng và một ô trống (hoặc chọn kỹ năng thay thế khi đủ 6/6). Giá bậc 1 = 20 + 10 × cấp học; học lại kỹ năng cũ của
// chính pet giảm còn 20%; nâng bậc 2/3 tốn 3×/6× giá bậc 1 mỗi lần và yêu cầu cấp riêng.

var commonSkills = []string{"strike", "heal", "guard"}

// canLearn cho biết kỹ năng có nằm trong những thứ pet này được phép học không.
func (e *Engine) canLearn(p *pet.Pet, s content.Skill) bool {
	if s.ExclusiveSpecies != "" {
		return s.ExclusiveSpecies == p.SpeciesID
	}
	return has(e.Data.Species[p.SpeciesID].Skills, s.ID) || has(p.InheritedPool, s.ID) || has(commonSkills, s.ID)
}

func rank1Price(s content.Skill) int { return 20 + 10*s.LearnLevel }

// learnPrice trả giá học và cờ "học lại".
func learnPrice(p *pet.Pet, s content.Skill) (int, bool) {
	base := rank1Price(s)
	if has(p.Learned, s.ID) {
		return (base*20 + 99) / 100, true
	}
	return base, false
}

func (e *Engine) learnSkill(c *Character, d Intent) ([]Event, error) {
	if err := e.near(c, "learn"); err != nil {
		return nil, err
	}
	p, err := findPet(c, d.PetID)
	if err != nil {
		return nil, err
	}
	s, ok := e.Data.Skills[d.SkillID]
	if !ok || !e.canLearn(p, s) {
		return nil, fmt.Errorf("linh thú này không thể học kỹ năng đó")
	}
	if has(p.Skills, s.ID) {
		return nil, fmt.Errorf("đã học kỹ năng này")
	}
	if p.Level < s.LearnLevel {
		return nil, fmt.Errorf("pet needs level %d", s.LearnLevel)
	}
	price, relearn := learnPrice(p, s)
	if c.Gold < price {
		return nil, fmt.Errorf("insufficient gold")
	}
	slots := e.Data.Rules.SkillSlots
	if len(p.Skills) >= slots {
		if d.ReplaceID == "" || !has(p.Skills, d.ReplaceID) {
			return nil, fmt.Errorf("đã đủ %d kỹ năng: hãy chọn kỹ năng để thay", slots)
		}
		kept := []string{}
		for _, id := range p.Skills {
			if id != d.ReplaceID {
				kept = append(kept, id)
			}
		}
		p.Skills = kept
		delete(p.SkillRanks, d.ReplaceID) // quên kỹ năng đã nâng thì mất bậc (P13 §1)
	} else if d.ReplaceID != "" {
		return nil, fmt.Errorf("còn ô trống, không cần thay kỹ năng")
	}
	c.Gold -= price
	p.Skills = append(p.Skills, s.ID)
	if !has(p.Learned, s.ID) {
		p.Learned = append(p.Learned, s.ID)
	}
	msg := p.Name + " learned " + s.Name
	if relearn {
		msg += " (relearned)"
	}
	return []Event{event("pet_learn", msg), event("currency_spend", fmt.Sprintf("Skill tuition paid: %d gold", price))}, nil
}

func (e *Engine) upgradeSkill(c *Character, d Intent) ([]Event, error) {
	if err := e.near(c, "learn"); err != nil {
		return nil, err
	}
	p, err := findPet(c, d.PetID)
	if err != nil {
		return nil, err
	}
	s, ok := e.Data.Skills[d.SkillID]
	if !ok || !has(p.Skills, s.ID) {
		return nil, fmt.Errorf("skill has not been learned")
	}
	if s.RankPolicy != "damage_heal_3_ranks" {
		return nil, fmt.Errorf("kỹ năng này không có bậc nâng")
	}
	rank := p.Rank(s.ID)
	if rank >= 3 {
		return nil, fmt.Errorf("kỹ năng đã đạt bậc tối đa")
	}
	gate, mult := max(20, s.LearnLevel+15), 3
	if rank == 2 {
		gate, mult = max(40, s.LearnLevel+30), 6
	}
	if p.Level < gate {
		return nil, fmt.Errorf("pet needs level %d", gate)
	}
	price := rank1Price(s) * mult
	if c.Gold < price {
		return nil, fmt.Errorf("insufficient gold")
	}
	c.Gold -= price
	if p.SkillRanks == nil {
		p.SkillRanks = map[string]int{}
	}
	p.SkillRanks[s.ID] = rank + 1
	return []Event{event("pet_upgrade", fmt.Sprintf("%s: %s rank %d", p.Name, s.Name, rank+1)), event("currency_spend", fmt.Sprintf("Skill upgrade paid: %d gold", price))}, nil
}

// giftStarterAttack tặng pet đang theo một đòn tấn công cấp 1 (đầu tiên trong pool gốc loại vật lý/phép, không thì Cường kích)
// khi nhận nhiệm vụ đầu; bỏ qua nếu hết ô hoặc đã có. Miễn phí, tính là đã học (học lại sau này được giảm giá).
func (e *Engine) giftStarterAttack(c *Character) []Event {
	p, err := findPet(c, c.ActivePetID)
	if err != nil || len(p.Skills) >= e.Data.Rules.SkillSlots {
		return nil
	}
	pick := "strike"
	for _, id := range e.Data.Species[p.SpeciesID].Skills {
		if s, ok := e.Data.Skills[id]; ok && s.LearnLevel <= 1 && (s.Kind == "physical" || s.Kind == "magic") {
			pick = id
			break
		}
	}
	if has(p.Skills, pick) {
		return nil
	}
	p.Skills = append(p.Skills, pick)
	if !has(p.Learned, pick) {
		p.Learned = append(p.Learned, pick)
	}
	return []Event{event("pet_learn", p.Name+" learned "+e.Data.Skills[pick].Name)}
}
