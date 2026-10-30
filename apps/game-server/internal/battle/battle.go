package battle

import "phimond/server/internal/pet"

// ActiveStatus là trạng thái đang gắn trên một đơn vị (P13 §5). ExpireRound: hết hiệu lực cuối vòng đó;
// 0 nghĩa là hết sau cơ hội hành động kế tiếp (sleep/petrify/confuse).
type ActiveStatus struct {
	ID          string `json:"id"`
	Remaining   int    `json:"remaining"` // số vòng còn lại, để hiển thị
	AppliedTurn int    `json:"applied_turn"`
	ExpireRound int    `json:"expire_round,omitempty"`
	// Tick: sát thương mỗi nhịp của DoT (đã chốt lúc áp: 0.30 × tấn công nguồn, nhân 1000); Element của nhịp.
	TickMilli int    `json:"tick_milli,omitempty"`
	Element   string `json:"element,omitempty"`
	SourceID  string `json:"source_id,omitempty"`
	Seq       int    `json:"seq"`
}

// Buff là chỉnh sửa chỉ số phần trăm tạm thời (điểm cơ bản; dương = tăng). Cùng Group chỉ giữ mức mạnh nhất.
type Buff struct {
	ID          string `json:"id"`
	Stat        string `json:"stat"` // atk|mag|def|spd|status_resistance
	AmountBP    int    `json:"amount_bp"`
	Group       string `json:"group"`
	Remaining   int    `json:"remaining"`
	AppliedTurn int    `json:"applied_turn"`
	ExpireRound int    `json:"expire_round"`
	Seq         int    `json:"seq"`
}

// Shield là khiên hấp thụ sát thương, một khiên mỗi đơn vị (giữ lượng lớn hơn, P13 §4).
type Shield struct {
	Amount      int `json:"amount"`
	ExpireRound int `json:"expire_round"`
}

// Regen là hồi máu theo nhịp cuối vòng.
type Regen struct {
	Heal        int `json:"heal"`
	FirstRound  int `json:"first_round"`
	ExpireRound int `json:"expire_round"`
}

// Unit là một chiến binh. Pet giữ chỉ số nguồn; mọi trạng thái trận nằm ở đây.
type Unit struct {
	ID        string         `json:"id"`
	Name      string         `json:"name"`
	Side      string         `json:"side"`
	SpeciesID string         `json:"species_id"`
	Level     int            `json:"level"`
	HP        int            `json:"hp"`
	MaxHP     int            `json:"max_hp"`
	MP        int            `json:"mp"`
	MaxMP     int            `json:"max_mp"`
	Statuses  []ActiveStatus `json:"statuses"`
	Buffs     []Buff         `json:"buffs"`
	Shield    *Shield        `json:"shield,omitempty"`
	Regen     *Regen         `json:"regen,omitempty"`
	// Cooldowns: kỹ năng → vòng đầu tiên dùng lại được (P13 §3: cast vòng R, CD C → dùng lại từ R+C+1).
	Cooldowns map[string]int `json:"cooldowns,omitempty"`
	// Grace: miễn nhiễm sleep/petrify/confuse đến hết vòng này (P13-D11).
	Grace int `json:"grace,omitempty"`
	// Rank: hạng ngẫu nhiên cố định cho mỗi đơn vị khi hòa SPD (P11 §6); chỉ nằm phía server.
	Rank uint64   `json:"-"`
	Pet  *pet.Pet `json:"pet"`
	// Kỹ năng AI của quái (đã lọc theo cấp, đúng thứ tự pool); người chơi dùng Pet.Skills.
	AISkills []string `json:"ai_skills,omitempty"`
	// Power nhân HP/sát thương theo lớp điều chỉnh encounter (rules.pack_scale/wild_scale); 0 = 1.
	Power float64 `json:"power,omitempty"`
	// Acted: đã hành động trong vòng hiện tại (cho kiểm tra phản đòn/đổi thứ tự).
	CounterUntil int `json:"counter_until,omitempty"`
	CounterUsed  int `json:"counter_used,omitempty"`
	Revived      bool `json:"revived,omitempty"`
}
