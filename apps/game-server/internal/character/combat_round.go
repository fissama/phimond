package character

import (
	"math/big"
	"phimond/server/internal/battle"
	"phimond/server/internal/content"
	"sort"
)

// loadout là một kỹ năng kèm bậc, theo thứ tự ưu tiên ô/pool.
type loadout struct {
	skill content.Skill
	rank  int
}

func (e *Engine) loadoutOf(u *battle.Unit) []loadout {
	out := []loadout{}
	ids := u.Pet.Skills
	if u.Side == "enemy" {
		ids = u.AISkills
	}
	for _, id := range ids {
		if s, ok := e.Data.Skills[id]; ok {
			out = append(out, loadout{s, u.Pet.Rank(id)})
		}
	}
	return out
}

// aiSkills chọn tập kỹ năng của quái: Native Pool của loài, cấp học ≤ cấp quái, theo thứ tự pool (nhẹ trước), không
// chứa kỹ năng vô nghĩa khi đấu 1 pet (hồi sinh, chuyển MP). Không dùng ngẫu nhiên (P13 §2).
func (e *Engine) aiSkills(sp content.Species, level int) []string {
	out := []string{}
	for _, id := range sp.Skills {
		s := e.Data.Skills[id]
		if s.LearnLevel > level || s.Kind == "revive" || s.Kind == "resource" {
			continue
		}
		out = append(out, id)
	}
	return out
}

// pickDamage chọn kỹ năng sát thương đơn tốt nhất (công suất × hệ số hệ), hòa theo thứ tự ô.
func (f *fight) expected(u *battle.Unit, l loadout, t *battle.Unit) *big.Rat {
	pn, pd := rankPower(l.skill, l.rank)
	en, ed := elementFactor(l.skill.Element, f.e.Data.Species[t.SpeciesID].Element)
	v := big.NewRat(int64(l.skill.PowerPM)*pn*en, 1000*pd*ed)
	return v.Mul(v, big.NewRat(int64(max(1, l.skill.Effect.Hits)), 1))
}

// policy là chính sách tự động theo P13 §2. Trả kỹ năng (nil = đòn thường), bậc và mục tiêu đã chọn.
// player=true dùng thứ tự của pet nuôi (hồi → gỡ → khống chế → buff → AoE → đơn → thường);
// player=false dùng thứ tự của quái (khống chế → hồi → AoE → buff → đơn → thường).
func (f *fight) policy(u *battle.Unit, player bool) (*content.Skill, int, *battle.Unit) {
	ls := f.e.loadoutOf(u)
	foes := byID(living(foesOf(f.b, u)))
	allies := byID(living(sideOf(f.b, u)))
	ready := func(l loadout) bool { return f.usable(u, l.skill, l.rank) == "" }

	heal := func() (*content.Skill, int, *battle.Unit) {
		var weak *battle.Unit
		for _, a := range allies {
			if float64(a.HP)/float64(max(1, a.MaxHP)) < 0.4 && (weak == nil || a.HP*weak.MaxHP < weak.HP*a.MaxHP) {
				weak = a
			}
		}
		if weak == nil {
			return nil, 0, nil
		}
		for _, l := range ls {
			if l.skill.Kind != "heal" || !ready(l) {
				continue
			}
			if l.skill.Target == "ally_all" || l.skill.Target == "ally_one" {
				s := l.skill
				return &s, l.rank, weak
			}
		}
		return nil, 0, nil
	}
	cleanse := func() (*content.Skill, int, *battle.Unit) {
		for _, l := range ls {
			if l.skill.Kind != "cleanse" || l.skill.ID == "extinguish" || !ready(l) {
				continue
			}
			for _, a := range allies {
				if ts := []*battle.Unit{a}; f.valid(u, l.skill, ts) {
					s := l.skill
					return &s, l.rank, a
				}
			}
		}
		return nil, 0, nil
	}
	control := func() (*content.Skill, int, *battle.Unit) {
		for _, l := range ls {
			st := l.skill.Effect.Status
			if (l.skill.Kind != "control" && l.skill.Kind != "debuff") || st == "" || !ready(l) {
				continue
			}
			for _, t := range foes {
				if !hasStatus(t, st) && f.eligible(t, st) == "" {
					s := l.skill
					return &s, l.rank, t
				}
			}
		}
		return nil, 0, nil
	}
	buff := func() (*content.Skill, int, *battle.Unit) {
		for _, l := range ls {
			if l.skill.Kind != "buff" || !ready(l) || l.skill.Target == "ally_other" {
				continue
			}
			missing := false
			switch l.skill.ID {
			case "counter":
				missing = u.CounterUntil < f.round
			case "regen":
				missing = u.Regen == nil
			default:
				for _, spec := range buffTable[l.skill.ID] {
					b := hasBuffGroup(u, spec.group)
					missing = missing || b == nil || abs(b.AmountBP) < abs(spec.bp)
				}
			}
			if missing {
				s := l.skill
				return &s, l.rank, u
			}
		}
		return nil, 0, nil
	}
	aoe := func() (*content.Skill, int, *battle.Unit) {
		if len(foes) < 2 {
			return nil, 0, nil
		}
		var best *loadout
		for i, l := range ls {
			if (l.skill.Kind != "physical" && l.skill.Kind != "magic") || l.skill.Target != "enemy_all" || !ready(l) {
				continue
			}
			if best == nil || l.skill.PowerPM*l.rank > best.skill.PowerPM*best.rank {
				best = &ls[i]
			}
		}
		if best == nil {
			return nil, 0, nil
		}
		s := best.skill
		return &s, best.rank, nil
	}
	single := func() (*content.Skill, int, *battle.Unit) {
		if len(foes) == 0 {
			return nil, 0, nil
		}
		// Mục tiêu: địch ít máu nhất (theo tỉ lệ), hòa theo id.
		t := foes[0]
		for _, x := range foes[1:] {
			if x.HP*t.MaxHP < t.HP*x.MaxHP {
				t = x
			}
		}
		var best *loadout
		var bestV *big.Rat
		for i, l := range ls {
			if (l.skill.Kind != "physical" && l.skill.Kind != "magic") || l.skill.Target != "enemy_one" || l.skill.PowerPM == 0 || !ready(l) {
				continue
			}
			if v := f.expected(u, l, t); best == nil || v.Cmp(bestV) > 0 {
				best, bestV = &ls[i], v
			}
		}
		if best == nil {
			return nil, 0, nil
		}
		s := best.skill
		return &s, best.rank, t
	}
	order := []func() (*content.Skill, int, *battle.Unit){control, heal, aoe, buff, single}
	if player {
		order = []func() (*content.Skill, int, *battle.Unit){heal, cleanse, control, buff, aoe, single}
	}
	for _, step := range order {
		if s, r, t := step(); s != nil {
			return s, r, t
		}
	}
	return nil, 0, nil
}

// basic thực hiện đòn thường: vật lý trung tính 1.00×ATK, 0 MP, không hồi chiêu; bị trói thì bỏ lượt.
func (f *fight) basic(u, t *battle.Unit) {
	if t == nil || t.HP <= 0 {
		return
	}
	if blockedChannel(u, "physical") != "" {
		f.say("action_blocked", u, nil, 0, u.Name+" cannot attack while bound", "bind")
		return
	}
	f.say("skill_cast", u, t, 0, u.Name+" used Đánh thường", "basic")
	f.strike(u, t, f.e.eff(u, "atk"), 1, 1, "neutral", 0, true)
}

// order chốt thứ tự hành động đầu vòng: SPD hiệu lực giảm dần, hòa theo hạng ngẫu nhiên cố định, rồi id.
func (f *fight) order() []*battle.Unit {
	us := living(f.b.Units)
	spd := map[string]*big.Rat{}
	for _, u := range us {
		spd[u.ID] = f.e.eff(u, "spd")
	}
	sort.SliceStable(us, func(i, j int) bool {
		a, b := us[i], us[j]
		if c := spd[a.ID].Cmp(spd[b.ID]); c != 0 {
			return c > 0
		}
		if a.Rank != b.Rank {
			return a.Rank < b.Rank
		}
		return a.ID < b.ID
	})
	return us
}

// consumeControl xử lý khống chế đang chờ trước hành động của u. Trả true nếu hành động bị chiếm (bỏ lượt/hỗn loạn).
func (f *fight) consumeControl(u *battle.Unit) (blocked bool, confused bool) {
	for _, id := range []string{"sleep", "petrify"} {
		if hasStatus(u, id) {
			f.terminate(u, id, "status_expired")
			f.say("action_blocked", u, nil, 0, u.Name+" cannot act ("+f.statusName(id)+")", id)
			return true, false
		}
	}
	if hasStatus(u, "confuse") {
		f.terminate(u, "confuse", "status_expired")
		return false, true
	}
	return false, false
}

// endRound: DoT (độc rồi cháy, theo id), hồi theo nhịp, rồi hết hạn trạng thái/buff/khiên (P13 §5).
func (f *fight) endRound() {
	us := byID(living(f.b.Units))
	for _, id := range []string{"poison", "burn"} {
		for _, u := range us {
			if u.HP <= 0 {
				continue
			}
			for _, s := range u.Statuses {
				if s.ID != id || s.AppliedTurn >= f.round || f.round > s.ExpireRound {
					continue
				}
				// Nhịp: 0.30× tấn công đã chốt khi áp; DEF và hệ của mục tiêu lấy lúc này; không bạo kích.
				off := big.NewRat(int64(s.TickMilli), 1000)
				base := new(big.Rat).Mul(off, big.NewRat(100, 1))
				base.Quo(base, new(big.Rat).Add(f.e.eff(u, "def"), big.NewRat(100, 1)))
				en, ed := elementFactor(s.Element, f.e.Data.Species[u.SpeciesID].Element)
				base.Mul(base, big.NewRat(en, ed))
				dmg := ratFloor(base)
				if off.Sign() > 0 && dmg < 1 {
					dmg = 1
				}
				lost, absorbed := f.hurt(u, dmg)
				f.say("damage", nil, u, lost, u.Name+" takes "+itoa(lost)+" damage ("+f.statusName(id)+")", id)
				if absorbed > 0 {
					f.say("shield_absorb", nil, u, absorbed, u.Name+"'s shield absorbs "+itoa(absorbed), id)
				}
				if u.HP <= 0 {
					f.say("unit_down", nil, u, 0, u.Name+" is defeated", "")
				}
			}
		}
	}
	for _, u := range us {
		if u.HP > 0 && u.Regen != nil && f.round >= u.Regen.FirstRound && f.round <= u.Regen.ExpireRound {
			f.heal(nil, u, u.Regen.Heal)
		}
	}
	for _, u := range f.b.Units {
		keep := u.Statuses[:0]
		for _, s := range u.Statuses {
			if s.ExpireRound <= f.round {
				if isControl(s.ID) {
					u.Grace = f.round + 1
				}
				f.say("status_expired", nil, u, 0, f.statusName(s.ID)+" faded", s.ID)
				continue
			}
			s.Remaining = s.ExpireRound - f.round
			keep = append(keep, s)
		}
		u.Statuses = keep
		kb := u.Buffs[:0]
		for _, b := range u.Buffs {
			if b.ExpireRound > f.round {
				b.Remaining = b.ExpireRound - f.round
				kb = append(kb, b)
			}
		}
		u.Buffs = kb
		if u.Shield != nil && u.Shield.ExpireRound <= f.round {
			u.Shield = nil
		}
		if u.Regen != nil && u.Regen.ExpireRound <= f.round {
			u.Regen = nil
		}
	}
}
