package character

import "phimond/server/internal/pet"

// MigrateLegacy chuyển nhân vật lưu trước P11/P13 sang mô hình mới. Trả true nếu có thay đổi.
// Quy tắc: id loài cũ → id chuẩn (data/pets/legacy_species.json); pet thiếu bậc nhận toàn bộ bậc B (không tín dụng
// dòng dõi); kỹ năng cũ bị bỏ vì id không còn trong catalog (người chơi học lại, P13 §1); chỉ số tính lại nhưng giữ cấp
// và tỉ lệ HP/MP; trận đang dở bị hủy. Idempotent: chạy lần hai không đổi gì.
func (e *Engine) MigrateLegacy(c *Character) bool {
	changed := false
	for _, p := range c.Pets {
		if e.migratePet(p) {
			changed = true
		}
	}
	if c.Battle != nil {
		legacy := changed // pet vừa đổi mô hình: ảnh chụp đơn vị trong trận đã lỗi thời
		for _, u := range c.Battle.Units {
			if u.Pet == nil || u.Pet.Grades == nil {
				legacy = true
			}
			if _, ok := e.Data.Species[u.SpeciesID]; !ok {
				legacy = true
			}
		}
		if legacy {
			c.Battle = nil
			changed = true
		}
	}
	return changed
}

func (e *Engine) migratePet(p *pet.Pet) bool {
	changed := false
	if to, ok := e.Data.LegacySpecies[p.SpeciesID]; ok {
		if _, exists := e.Data.Species[p.SpeciesID]; !exists {
			p.SpeciesID = to
			changed = true
		}
	}
	s, ok := e.Data.Species[p.SpeciesID]
	if !ok {
		return changed
	}
	if p.Grades == nil || p.Credit == nil || p.Bonus == nil {
		if p.Grades == nil {
			p.Grades = uniformGrades("B")
		}
		if p.Credit == nil {
			p.Credit = map[string]pet.Credit{}
		}
		if p.Bonus == nil {
			p.Bonus = map[string]int{}
		}
		changed = true
	}
	keep := p.Skills[:0:0]
	for _, id := range p.Skills {
		if _, ok := e.Data.Skills[id]; ok {
			keep = append(keep, id)
		}
	}
	if len(keep) != len(p.Skills) || p.Skills == nil {
		p.Skills = keep
		changed = true
	}
	if p.Star != s.Star || p.MaxHP == 0 || p.Attack == 0 {
		p.Star = s.Star
		changed = true
	}
	if changed {
		ratioHP, ratioMP := 1.0, 1.0
		if p.MaxHP > 0 {
			ratioHP = float64(p.HP) / float64(p.MaxHP)
		}
		if p.MaxMP > 0 {
			ratioMP = float64(p.MP) / float64(p.MaxMP)
		}
		lc := e.levelCap(p)
		if p.Level > lc {
			p.Level = lc
		}
		p.MaxHP, p.MaxMP = 0, 0
		e.Recalculate(p)
		p.HP = max(1, int(ratioHP*float64(p.MaxHP)))
		if ratioHP <= 0 {
			p.HP = 0
		}
		p.MP = int(ratioMP * float64(p.MaxMP))
	}
	return changed
}
