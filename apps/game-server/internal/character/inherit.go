package character

import (
	"math/big"
	"phimond/server/internal/pet"
)

// Kế thừa P11 F02/F03: giữ tín dụng dòng dõi mạnh nhất từng chỉ số, cộng tín dụng mới từ mức huấn luyện của cả hai bố
// mẹ, rồi đổi sang thưởng bằng căn bậc hai dịch. Toàn bộ dùng số nguyên chính xác (không so biên bằng số thực).

// inheritR/inheritA: hằng tham chiếu R và hệ số tín dụng a của từng chỉ số (bảng P11, nhân sẵn dạng hữu tỉ).
var inheritR = map[string]int64{"hp": 500, "atk": 50, "mag": 50, "def": 50, "spd": 100, "status_resistance": 50}
var inheritA = map[string]*big.Rat{
	"hp": big.NewRat(3, 20), "atk": big.NewRat(3, 20), "mag": big.NewRat(3, 20), "def": big.NewRat(3, 20),
	"spd": big.NewRat(1, 25), "status_resistance": big.NewRat(1, 25),
}

func creditOf(p *pet.Pet, stat string) *big.Rat {
	c, ok := p.Credit[stat]
	if !ok || c.N == "" {
		return new(big.Rat)
	}
	n, ok1 := new(big.Int).SetString(c.N, 10)
	d, ok2 := new(big.Int).SetString(c.D, 10)
	if !ok1 || !ok2 || d.Sign() <= 0 || n.Sign() < 0 {
		return new(big.Rat) // dữ liệu hỏng: không đoán, coi như chưa có tín dụng
	}
	return new(big.Rat).SetFrac(n, d)
}

func setCredit(p *pet.Pet, stat string, q *big.Rat) {
	if p.Credit == nil {
		p.Credit = map[string]pet.Credit{}
	}
	p.Credit[stat] = pet.Credit{N: q.Num().String(), D: q.Denom().String()}
}

// bonusMilli trả z lớn nhất ≥ 0 thỏa z/1000 + (z/1000)²/(2R) ≤ Q, tức thưởng kế thừa tính theo 1/1000.
func bonusMilli(q *big.Rat, r int64) int {
	if q.Sign() <= 0 {
		return 0
	}
	N, D := q.Num(), q.Denom()
	R := big.NewInt(r)
	// D·(2000·R·z + z²) ≤ 2·R·10⁶·N
	rhs := new(big.Int).Mul(big.NewInt(2_000_000), R)
	rhs.Mul(rhs, N)
	ok := func(z *big.Int) bool {
		t := new(big.Int).Mul(big.NewInt(2000), R)
		t.Mul(t, z)
		t.Add(t, new(big.Int).Mul(z, z))
		t.Mul(t, D)
		return t.Cmp(rhs) <= 0
	}
	// Nghiệm thực: z = (−1000RD + sqrt(10⁶R²D² + 2·10⁶·R·N·D)) / D; lấy phần nguyên rồi hiệu chỉnh bằng so sánh chính xác.
	a := new(big.Int).Mul(big.NewInt(1000), R)
	a.Mul(a, D)
	disc := new(big.Int).Mul(a, a)
	disc.Add(disc, new(big.Int).Mul(new(big.Int).Mul(big.NewInt(2_000_000), R), new(big.Int).Mul(N, D)))
	s := new(big.Int).Sqrt(disc)
	z := new(big.Int).Sub(s, a)
	z.Div(z, D)
	if z.Sign() < 0 {
		z.SetInt64(0)
	}
	for !ok(z) && z.Sign() > 0 {
		z.Sub(z, big.NewInt(1))
	}
	for ok(new(big.Int).Add(z, big.NewInt(1))) {
		z.Add(z, big.NewInt(1))
	}
	return int(z.Int64())
}

// applyLineage tính Q và thưởng của con từ hai bố mẹ (chỉ thao tác Normal; điều kiện cấp ≥ 20 do nơi gọi kiểm).
func (e *Engine) applyLineage(child, m, d *pet.Pet) {
	sm, sd := e.Data.Species[m.SpeciesID], e.Data.Species[d.SpeciesID]
	cm, cd := e.Data.Rules.LevelCap(sm.Star), e.Data.Rules.LevelCap(sd.Star)
	// training = max(0, min((Lm−20)/(Cm−20), (Ld−20)/(Cd−20))); không chặn ở 1.
	tm := big.NewRat(int64(m.Level-20), int64(max(1, cm-20)))
	td := big.NewRat(int64(d.Level-20), int64(max(1, cd-20)))
	t := tm
	if td.Cmp(tm) < 0 {
		t = td
	}
	if t.Sign() < 0 {
		t = new(big.Rat)
	}
	child.Credit = map[string]pet.Credit{}
	child.Bonus = map[string]int{}
	for _, k := range StatKeys {
		g := new(big.Rat).SetFrac64(int64(grown(sm, m, k))+int64(grown(sd, d, k)), 2)
		earn := new(big.Rat).Mul(inheritA[k], g)
		earn.Mul(earn, t)
		qm, qd := creditOf(m, k), creditOf(d, k)
		q := qm
		if qd.Cmp(qm) > 0 {
			q = qd
		}
		q = new(big.Rat).Add(q, earn)
		setCredit(child, k, q)
		child.Bonus[k] = bonusMilli(q, inheritR[k])
	}
}
