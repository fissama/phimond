package character

import (
	"math/big"
	"phimond/server/internal/battle"
	"phimond/server/internal/content"
	"sort"
)

// Lõi chiến đấu P13 (behavior contract §3–§5): chỉ số hiệu lực, xác suất hữu tỉ, bảng hệ. Mọi phép tính xác suất dùng số
// nguyên/hữu tỉ chính xác; RNG lấy mẫu từ chối (không thiên lệch).

// chart: hệ khắc theo vòng Hỏa > Phong > Địa > Thủy > Hỏa (thuận ×1.25, nghịch ×0.80); Quang ↔ Ám khắc nhau ×1.25.
var beats = map[string]string{"fire": "wind", "wind": "earth", "earth": "water", "water": "fire"}

// elementFactor trả (tử, mẫu) của hệ số hệ khi `attacker` đánh `defender`.
func elementFactor(attacker, defender string) (int64, int64) {
	switch {
	case attacker == "" || attacker == "neutral" || defender == "" || defender == "neutral":
		return 1, 1
	case (attacker == "light" && defender == "dark") || (attacker == "dark" && defender == "light"):
		return 5, 4
	case beats[attacker] == defender:
		return 5, 4
	case beats[defender] == attacker:
		return 4, 5
	}
	return 1, 1
}

// bern thực hiện một phép thử Bernoulli chính xác với xác suất num/den (không thiên lệch).
func bern(r *RNG, num, den int64) bool {
	if num <= 0 || den <= 0 {
		return false
	}
	if num >= den {
		return true
	}
	limit := ^uint64(0) - (^uint64(0))%uint64(den)
	for {
		if v := r.Next(); v < limit {
			return int64(v%uint64(den)) < num
		}
	}
}

// statChannel: chỉ số bị buff/debuff theo phần trăm (điểm cơ bản). Dương mạnh nhất + âm mạnh nhất, tổng chặn ±50%.
func (e *Engine) modBP(u *battle.Unit, stat string) int {
	pos, neg := 0, 0
	for _, b := range u.Buffs {
		if b.Stat != stat {
			continue
		}
		if b.AmountBP > pos {
			pos = b.AmountBP
		}
		if b.AmountBP < neg {
			neg = b.AmountBP
		}
	}
	for _, s := range u.Statuses {
		switch {
		case s.ID == "petrify" && stat == "def":
			pos = max(pos, 2500) // Hóa đá tạm thời +25% DEF (P13-D11)
		case s.ID == "frailty" && (stat == "atk" || stat == "mag"):
			neg = min(neg, -1000) // Suy nhược: ATK/MAG −10%
		}
	}
	return max(-5000, min(5000, pos+neg))
}

// eff trả chỉ số hiệu lực dưới dạng hữu tỉ (đơn vị chỉ số): vĩnh viễn × (1 + %). Chặn dưới 0.
func (e *Engine) eff(u *battle.Unit, stat string) *big.Rat {
	perm := e.permanentMilli(u.Pet, stat)
	r := big.NewRat(perm*int64(10000+e.modBP(u, stat)), 10_000_000)
	if r.Sign() < 0 {
		return new(big.Rat)
	}
	return r
}

func ratFloor(r *big.Rat) int {
	q := new(big.Int).Div(r.Num(), r.Denom()) // Euclid: chính xác với số không âm
	return int(q.Int64())
}

// srChance trả tử/mẫu của xác suất cuối cùng sau kháng trạng thái: p × (1 − 0.8·S/(S+100)), p = pm/1000.
func (e *Engine) srChance(target *battle.Unit, pm int) (int64, int64) {
	s := e.eff(target, "status_resistance")
	// p = pm/1000 × (S+500)/(5(S+100))
	num := new(big.Rat).Mul(big.NewRat(int64(pm), 1000), new(big.Rat).Add(s, big.NewRat(500, 1)))
	den := new(big.Rat).Mul(big.NewRat(5, 1), new(big.Rat).Add(s, big.NewRat(100, 1)))
	p := new(big.Rat).Quo(num, den)
	// Quy đồng về mẫu cố định 10⁹ để dùng lấy mẫu từ chối số nguyên: làm tròn xuống, sai số < 10⁻⁹.
	n := new(big.Int).Mul(p.Num(), big.NewInt(1_000_000_000))
	n.Div(n, p.Denom())
	return n.Int64(), 1_000_000_000
}

// alive/phe
func sideOf(b *Battle, u *battle.Unit) []*battle.Unit { return sideUnits(b, u.Side) }
func foesOf(b *Battle, u *battle.Unit) []*battle.Unit {
	if u.Side == "player" {
		return sideUnits(b, "enemy")
	}
	return sideUnits(b, "player")
}
func living(us []*battle.Unit) []*battle.Unit {
	out := []*battle.Unit{}
	for _, u := range us {
		if u.HP > 0 {
			out = append(out, u)
		}
	}
	return out
}

// byID sắp theo id ổn định (P13 §4: mục tiêu xử lý theo id).
func byID(us []*battle.Unit) []*battle.Unit {
	out := append([]*battle.Unit{}, us...)
	sort.Slice(out, func(i, j int) bool { return out[i].ID < out[j].ID })
	return out
}

func hasStatus(u *battle.Unit, id string) bool {
	for _, s := range u.Statuses {
		if s.ID == id {
			return true
		}
	}
	return false
}
func hasBuffGroup(u *battle.Unit, group string) *battle.Buff {
	for i := range u.Buffs {
		if u.Buffs[i].Group == group {
			return &u.Buffs[i]
		}
	}
	return nil
}

// blockedChannel: bind chặn hành động vật lý (gồm đòn thường); silence chặn kênh phép (P13 §5).
func blockedChannel(u *battle.Unit, channel string) string {
	if channel == "physical" && hasStatus(u, "bind") {
		return "bind"
	}
	if channel == "magic" && hasStatus(u, "silence") {
		return "silence"
	}
	return ""
}

// rankScale: power/hồi ×1.15 (rank 2), ×1.30 (rank 3) cho kỹ năng 3 rank; MP ×1.20/1.40 làm tròn lên.
func rankPower(s content.Skill, rank int) (int64, int64) {
	if s.RankPolicy != "damage_heal_3_ranks" {
		return 1, 1
	}
	switch rank {
	case 2:
		return 115, 100
	case 3:
		return 130, 100
	}
	return 1, 1
}
func rankMP(s content.Skill, rank int) int {
	if s.RankPolicy != "damage_heal_3_ranks" {
		return s.MPCost
	}
	switch rank {
	case 2:
		return (s.MPCost*120 + 99) / 100
	case 3:
		return (s.MPCost*140 + 99) / 100
	}
	return s.MPCost
}

func itoa(n int) string { return big.NewInt(int64(n)).String() }
