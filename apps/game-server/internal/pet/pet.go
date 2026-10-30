package pet

// Credit là tín dụng dòng dõi Q của một chỉ số (P11 F02): số hữu tỉ không âm N/D, lưu dạng chuỗi số nguyên thập
// phân đã rút gọn; không bao giờ dựng lại từ phần thưởng đã làm tròn.
type Credit struct {
	N string `json:"n"`
	D string `json:"d"`
}

// Pet is the per-character instance of a species, including its resolved growth grades (P11), lineage,
// learned skills and tracked combat resources. All creators, recalculation, and level-up methods continue
// to live in internal/character to avoid import cycles through Engine.
type Pet struct {
	ID         string `json:"id"`
	SpeciesID  string `json:"species_id"`
	Name       string `json:"name"`
	Level      int    `json:"level"`
	XP         int    `json:"xp"`
	Gender     string `json:"gender"`
	Star       int    `json:"star"`
	Generation int    `json:"generation"`
	Refinement int    `json:"refinement"`
	Appraised  bool   `json:"appraised"`
	Retired    bool   `json:"retired"`
	// Grades: bậc tăng trưởng đã chốt cho 6 chỉ số (D/C/B/A/S/SS/Perfect), tạo một lần khi tạo pet/trứng
	// và không bao giờ đổi khi lên cấp hay vào trận (P11 §1). Ẩn với người chơi đến khi giám định.
	Grades map[string]string `json:"grades,omitempty"`
	// Credit: tín dụng dòng dõi Q từng chỉ số; Bonus: phần thưởng kế thừa suy ra (đơn vị 1/1000 chỉ số).
	Credit map[string]Credit `json:"credit,omitempty"`
	Bonus  map[string]int    `json:"bonus_milli,omitempty"`
	// Skills: kỹ năng hiện tại (tối đa rules.skill_slots); đòn thường không chiếm ô. Rank > 1 lưu ở SkillRanks.
	Skills     []string       `json:"skills"`
	SkillRanks map[string]int `json:"skill_ranks,omitempty"`
	// Learned: mọi kỹ năng pet này từng học (để giảm giá học lại, P13 §1). InheritedPool: kỹ năng được phép học
	// nhờ kế thừa (chỉ id, sắp xếp ổn định).
	Learned       []string `json:"learned,omitempty"`
	InheritedPool []string `json:"inherited_pool,omitempty"`
	Parents       []string `json:"parents"`
	Strengthening int      `json:"strengthening"`
	Blessing      int      `json:"blessing"`
	HP            int      `json:"hp"`
	MP            int      `json:"mp"`
	MaxHP         int      `json:"max_hp"`
	MaxMP         int      `json:"max_mp"`
	// Chỉ số vĩnh viễn (phần nguyên): grown + kế thừa. Trận đấu dùng giá trị chính xác từ Grades/Bonus.
	Attack           int `json:"attack"`
	Magic            int `json:"magic"`
	Defense          int `json:"defense"`
	Speed            int `json:"speed"`
	StatusResistance int `json:"status_resistance"`
}

// Rank trả bậc của một kỹ năng đã học (mặc định 1).
func (p *Pet) Rank(skill string) int {
	if r := p.SkillRanks[skill]; r > 1 {
		return r
	}
	return 1
}
