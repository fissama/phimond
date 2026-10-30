package character

import (
	"phimond/server/internal/content"
	"phimond/server/internal/pet"
)

// Mô hình chỉ số P11 (final-spec §1, formulas): grown = base + floor(growth × hệ_số_bậc × (cấp−1)); vĩnh viễn =
// grown + thưởng kế thừa. Không có ngẫu nhiên sau khi chốt bậc; không nhân thêm Sao/vai trò/Race.

// StatKeys là thứ tự sáu chỉ số lõi. MP tách riêng, không có bậc.
var StatKeys = []string{"hp", "atk", "mag", "def", "spd", "status_resistance"}

// Grades theo thứ tự D → Perfect với khoảng rút [0,100) (P11 F01).
var gradeTable = []struct {
	name string
	to   int // cận trên (không gồm) của khoảng tích lũy
}{{"D", 3}, {"C", 15}, {"B", 55}, {"A", 83}, {"S", 95}, {"SS", 99}, {"Perfect", 100}}

// Hệ số bậc ×1000: chính (HP/ATK/MAG/DEF) và phụ (SPD/SR).
var gradeMain = map[string]int{"D": 900, "C": 950, "B": 1000, "A": 1030, "S": 1060, "SS": 1080, "Perfect": 1100}
var gradeAux = map[string]int{"D": 970, "C": 985, "B": 1000, "A": 1009, "S": 1018, "SS": 1024, "Perfect": 1030}

func gradeMult(stat, grade string) int {
	m := gradeMain
	if stat == "spd" || stat == "status_resistance" {
		m = gradeAux
	}
	if v, ok := m[grade]; ok {
		return v
	}
	return 1000 // bậc lạ/thiếu: B (dữ liệu hỏng không được làm sập trận)
}

// unbiased rút số nguyên đều trong [0,n) bằng lấy mẫu từ chối (không thiên lệch modulo).
func (r *RNG) unbiased(n int) int {
	if n <= 1 {
		return 0
	}
	limit := ^uint64(0) - (^uint64(0))%uint64(n)
	for {
		if v := r.Next(); v < limit {
			return int(v % uint64(n))
		}
	}
}

// rollGrades rút độc lập sáu bậc theo bảng xác suất (Egg/bắt/nhân giống).
func rollGrades(r *RNG) map[string]string {
	g := map[string]string{}
	for _, k := range StatKeys {
		d := r.unbiased(100)
		for _, row := range gradeTable {
			if d < row.to {
				g[k] = row.name
				break
			}
		}
	}
	return g
}

// uniformGrades gán một bậc cho cả sáu chỉ số (quái hoang: toàn B, P11 §7).
func uniformGrades(grade string) map[string]string {
	g := map[string]string{}
	for _, k := range StatKeys {
		g[k] = grade
	}
	return g
}

// grown trả base + floor(growth × hệ_số × (cấp−1)) cho một chỉ số, số nguyên chính xác.
func grown(s content.Species, p *pet.Pet, stat string) int {
	g := s.GrowthMilli[stat] * gradeMult(stat, p.Grades[stat])
	return s.Base[stat] + g*(max(1, p.Level)-1)/1_000_000
}

// permanentMilli là chỉ số vĩnh viễn (grown + thưởng kế thừa) theo đơn vị 1/1000.
func (e *Engine) permanentMilli(p *pet.Pet, stat string) int64 {
	s := e.Data.Species[p.SpeciesID]
	return int64(grown(s, p, stat))*1000 + int64(p.Bonus[stat])
}

// MaxMPFor là MP tối đa theo công thức F04: base + floor(growth × (cấp−1)).
func maxMPFor(s content.Species, level int) int {
	return s.MPBase + s.MPGrowthMilli*(max(1, level)-1)/1000
}

// levelCap là cấp tối đa của pet theo Sao (chưa tính Plus; Plus chưa mở ở v1.0.0).
func (e *Engine) levelCap(p *pet.Pet) int {
	return e.Data.Rules.LevelCap(e.Data.Species[p.SpeciesID].Star)
}

// Recalculate tính lại chỉ số suy ra từ bậc, thưởng kế thừa và cấp. HP/MP hiện tại giữ nguyên rồi bị chặn xuống mức tối
// đa mới (P11 §5: lên cấp không hồi miễn phí). Hồi phục chỉ qua NewPet/nở/dịch vụ.
func (e *Engine) Recalculate(p *pet.Pet) {
	s := e.Data.Species[p.SpeciesID]
	if p.Grades == nil {
		p.Grades = uniformGrades("B")
	}
	hp := e.permanentMilli(p, "hp") / 1000
	p.MaxHP = int(max(1, hp))
	p.MaxMP = maxMPFor(s, p.Level)
	p.Attack = int(e.permanentMilli(p, "atk") / 1000)
	p.Magic = int(e.permanentMilli(p, "mag") / 1000)
	p.Defense = int(e.permanentMilli(p, "def") / 1000)
	p.Speed = int(e.permanentMilli(p, "spd") / 1000)
	p.StatusResistance = int(e.permanentMilli(p, "status_resistance") / 1000)
	p.HP = min(p.HP, p.MaxHP)
	p.MP = min(p.MP, p.MaxMP)
}
