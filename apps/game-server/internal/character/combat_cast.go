package character

import (
	"fmt"
	"math/big"
	"phimond/server/internal/battle"
	"phimond/server/internal/content"
	"sort"
)

// fight là bối cảnh một vòng chiến đấu: tra cứu luật, RNG của trận và phát sự kiện.
type fight struct {
	e     *Engine
	b     *Battle
	round int
	emit  func(Event)
}

var controlTrio = []string{"sleep", "petrify", "confuse"}

func isControl(id string) bool { return has(controlTrio, id) }

func (f *fight) say(kind string, actor, target *battle.Unit, amount int, msg, detail string) {
	ev := Event{Type: kind, Amount: amount, Message: msg, Detail: detail}
	if actor != nil {
		ev.ActorID = actor.ID
	}
	if target != nil {
		ev.TargetID = target.ID
	}
	f.emit(ev)
}

func (f *fight) statusName(id string) string {
	if s, ok := f.e.Data.Statuses[id]; ok {
		return s.Name
	}
	return id
}

func (f *fight) nextSeq() int {
	f.b.StatusSeq++
	return f.b.StatusSeq
}

// ---- tiêu hao, hồi, khiên ----

// hurt trừ khiên trước rồi tới HP; trả lượng mất thật và lượng khiên hấp thụ.
func (f *fight) hurt(t *battle.Unit, amount int) (lost, absorbed int) {
	if t.Shield != nil && t.Shield.Amount > 0 {
		absorbed = min(amount, t.Shield.Amount)
		t.Shield.Amount -= absorbed
		amount -= absorbed
		if t.Shield.Amount == 0 {
			t.Shield = nil
		}
	}
	lost = min(amount, t.HP)
	t.HP -= lost
	return lost, absorbed
}

// heal hồi cho t (xui xẻo giảm 25% lượng nhận); không hồi sinh. Trả lượng thực sự hồi.
func (f *fight) heal(src, t *battle.Unit, raw int) int {
	if t.HP <= 0 {
		return 0
	}
	if hasStatus(t, "misfortune") {
		raw = raw * 75 / 100
	}
	n := min(raw, t.MaxHP-t.HP)
	if n < 0 {
		n = 0
	}
	t.HP += n
	f.say("heal", src, t, n, fmt.Sprintf("%s recovers %d HP", t.Name, n), "")
	return n
}

func (f *fight) setShield(t *battle.Unit, amount, rounds int) {
	exp := f.round + rounds
	if t.Shield == nil || amount >= t.Shield.Amount {
		t.Shield = &battle.Shield{Amount: amount, ExpireRound: exp}
	} else {
		t.Shield.ExpireRound = max(t.Shield.ExpireRound, exp) // cùng loại giữ lượng lớn hơn, làm mới hạn
	}
	f.say("buff_applied", nil, t, amount, t.Name+" gains a shield", "shield")
}

// ---- buff/debuff chỉ số ----

type buffSpec struct {
	stat, group string
	bp          int
}

// buffTable: buff chỉ số theo id kỹ năng (P13 §1/§5); nhóm giữ mức mạnh nhất, không cộng dồn.
var buffTable = map[string][]buffSpec{
	"guard":          {{"def", "armor", 2500}},
	"protect":        {{"def", "armor", 2000}},
	"haste":          {{"spd", "haste", 2000}},
	"beast_instinct": {{"atk", "might", 2000}, {"def", "beast_def", -1000}},
	"magic_focus":    {{"mag", "intellect", 2000}},
	"attack_up":      {{"atk", "might", 2000}},
	"magic_up":       {{"mag", "intellect", 2000}},
	"resilience":     {{"status_resistance", "resilience", 2500}},
}

var statGroup = map[string]string{"atk": "might", "mag": "intellect", "def": "armor", "spd": "haste", "status_resistance": "resilience"}

// addBuff gắn một chỉnh sửa phần trăm trong `rounds` vòng (hết cuối vòng R+rounds).
func (f *fight) addBuff(t *battle.Unit, id string, spec buffSpec, rounds int) {
	nb := battle.Buff{ID: id, Stat: spec.stat, AmountBP: spec.bp, Group: spec.group, Remaining: rounds, AppliedTurn: f.round, ExpireRound: f.round + rounds, Seq: f.nextSeq()}
	for i := range t.Buffs {
		old := &t.Buffs[i]
		if old.Group != spec.group || (old.AmountBP > 0) != (spec.bp > 0) {
			continue
		}
		if abs(old.AmountBP) > abs(spec.bp) { // mạnh hơn: giữ, chỉ làm mới hạn
			old.ExpireRound = max(old.ExpireRound, nb.ExpireRound)
			old.Remaining = old.ExpireRound - f.round
			return
		}
		t.Buffs[i] = nb
		return
	}
	t.Buffs = append(t.Buffs, nb)
}

// ---- trạng thái ----

// terminate gỡ một trạng thái; control (sleep/petrify/confuse) để lại miễn nhiễm đến hết vòng kế tiếp (P13-D11).
func (f *fight) terminate(u *battle.Unit, id, why string) bool {
	for i, s := range u.Statuses {
		if s.ID != id {
			continue
		}
		u.Statuses = append(u.Statuses[:i], u.Statuses[i+1:]...)
		if isControl(id) {
			u.Grace = f.round + 1
		}
		f.say(why, nil, u, 0, u.Name+": "+f.statusName(id)+" removed", id)
		return true
	}
	return false
}

// eligible kiểm tra một trạng thái có thể gắn lên t không; trả lý do từ chối ("" = hợp lệ).
func (f *fight) eligible(t *battle.Unit, id string) string {
	switch id {
	case "sleep", "petrify", "confuse":
		if t.Grace >= f.round {
			return "grace"
		}
		for _, c := range controlTrio {
			if hasStatus(t, c) {
				return "active"
			}
		}
	case "bind":
		if hasStatus(t, "silence") {
			return "exclusive"
		}
	case "silence":
		if hasStatus(t, "bind") {
			return "exclusive"
		}
	case "poison", "burn":
		if !hasStatus(t, id) {
			dots := 0
			for _, s := range t.Statuses {
				if s.ID == "poison" || s.ID == "burn" {
					dots++
				}
			}
			if dots >= 2 {
				return "dot_limit"
			}
		}
	}
	return ""
}

// tryStatus thử gắn trạng thái lên t sau một cú trúng: một phép thử Bernoulli duy nhất với p × (1 − kháng).
func (f *fight) tryStatus(src, t *battle.Unit, id string, chancePM int, tickMilli int, element string) {
	if t.HP <= 0 {
		return
	}
	if why := f.eligible(t, id); why != "" {
		f.say("status_blocked", src, t, 0, t.Name+" cannot be affected by "+f.statusName(id), why)
		return
	}
	num, den := f.e.srChance(t, chancePM)
	if !bern(&f.b.RNG, num, den) {
		f.say("status_resisted", src, t, 0, t.Name+" resisted "+f.statusName(id), "resisted")
		return
	}
	rounds := 2
	if isControl(id) {
		rounds = 1
	}
	exp := f.round + rounds
	for i := range t.Statuses {
		s := &t.Statuses[i]
		if s.ID != id {
			continue
		}
		// Cùng loại: DoT giữ potency lớn hơn, mọi loại làm mới hạn (kết thúc cuối R+2).
		if (id == "poison" || id == "burn") && tickMilli > s.TickMilli {
			s.TickMilli, s.Element, s.SourceID = tickMilli, element, src.ID
		}
		s.ExpireRound, s.Remaining, s.AppliedTurn = exp, rounds, f.round
		f.say("status_applied", src, t, 0, t.Name+" is affected by "+f.statusName(id), id)
		return
	}
	t.Statuses = append(t.Statuses, battle.ActiveStatus{ID: id, Remaining: rounds, AppliedTurn: f.round, ExpireRound: exp, TickMilli: tickMilli, Element: element, SourceID: src.ID, Seq: f.nextSeq()})
	f.say("status_applied", src, t, 0, t.Name+" is affected by "+f.statusName(id), id)
}

// tryDebuff thử gắn debuff chỉ số (−20% …) cho t.
func (f *fight) tryDebuff(src, t *battle.Unit, id, stat string, amountBP, chancePM int) {
	if t.HP <= 0 {
		return
	}
	num, den := f.e.srChance(t, chancePM)
	if !bern(&f.b.RNG, num, den) {
		f.say("status_resisted", src, t, 0, t.Name+" resisted "+f.statusName(id), "resisted")
		return
	}
	f.addBuff(t, id, buffSpec{stat: stat, group: "debuff_" + stat, bp: amountBP}, 2)
	f.say("status_applied", src, t, 0, t.Name+" is affected by "+f.statusName(id), id)
}

// ---- sát thương trực tiếp ----

// strike thực hiện một đòn trực tiếp: xúc xắc trúng, bạo kích, công thức P13-D06, khiên, đánh thức, phản kích.
// Trả (lượng HP mất thật, có trúng không).
func (f *fight) strike(src, t *battle.Unit, offense *big.Rat, powNum, powDen int64, element string, penPM int, react bool) (int, bool) {
	hitPM := int64(950)
	if hasStatus(src, "blind") {
		hitPM = 750 // mù: −20 điểm phần trăm, chặn trong 50–95%
	}
	if !bern(&f.b.RNG, hitPM, 1000) {
		f.say("miss", src, t, 0, "The skill missed", "")
		return 0, false
	}
	crit := bern(&f.b.RNG, 50, 1000)
	def := f.e.eff(t, "def")
	if penPM > 0 {
		def = new(big.Rat).Mul(def, big.NewRat(int64(1000-penPM), 1000))
	}
	base := new(big.Rat).Mul(offense, big.NewRat(powNum*100, powDen))
	base.Quo(base, new(big.Rat).Add(def, big.NewRat(100, 1)))
	en, ed := elementFactor(element, f.e.Data.Species[t.SpeciesID].Element)
	base.Mul(base, big.NewRat(en, ed))
	detail := ""
	if en > ed {
		detail = "super"
	} else if en < ed {
		detail = "weak"
	}
	if crit {
		base.Mul(base, big.NewRat(3, 2))
		detail = "crit " + detail
	}
	if src.Power > 0 && src.Power != 1 {
		scale := new(big.Rat)
		scale.SetFloat64(src.Power)
		base.Mul(base, scale)
	}
	dmg := ratFloor(base)
	if offense.Sign() > 0 && dmg < 1 {
		dmg = 1
	}
	lost, absorbed := f.hurt(t, dmg)
	switch {
	case lost > 0 || absorbed == 0:
		f.say("damage", src, t, lost, fmt.Sprintf("%s takes %d damage", t.Name, lost), detail)
	}
	if absorbed > 0 {
		f.say("shield_absorb", src, t, absorbed, fmt.Sprintf("%s's shield absorbs %d", t.Name, absorbed), "")
	}
	// Đánh thức: sát thương trực tiếp thành công, kể cả khi khiên nuốt hết (không nhân đôi sát thương).
	if hasStatus(t, "sleep") {
		f.terminate(t, "sleep", "status_cleansed")
	}
	if element == "water" && hasStatus(t, "burn") {
		f.terminate(t, "burn", "status_cleansed")
	}
	if t.HP <= 0 {
		f.say("unit_down", src, t, 0, t.Name+" is defeated", "")
		return lost, true
	}
	// Phản kích: tối đa một lần/vòng/đơn vị, sau khi sống sót qua đòn trực tiếp; không phản đòn phản kích.
	if react && src.HP > 0 && t.CounterUntil >= f.round && t.CounterUsed != f.round && !hasStatus(t, "bind") {
		t.CounterUsed = f.round
		off := f.e.eff(t, "atk")
		f.say("counter", t, src, 0, t.Name+" counterattacks", "")
		f.strike(t, src, off, 50, 100, "neutral", 0, false)
	}
	return lost, true
}

// ---- thực thi kỹ năng ----

// usable kiểm tra kỹ năng có dùng được ngay không (MP, hồi chiêu, kênh bị chặn); trả lý do nếu không.
func (f *fight) usable(u *battle.Unit, s content.Skill, rank int) string {
	if u.Cooldowns[s.ID] > f.round {
		return "cooldown"
	}
	if u.MP < rankMP(s, rank) {
		return "mp"
	}
	if why := blockedChannel(u, s.Channel); why != "" {
		return why
	}
	return ""
}

// targets trả danh sách mục tiêu hợp lệ theo dạng kỹ năng; rỗng nghĩa là không hợp lệ.
func (f *fight) targets(u *battle.Unit, s content.Skill, chosen *battle.Unit) []*battle.Unit {
	allies := living(sideOf(f.b, u))
	foes := living(foesOf(f.b, u))
	pick := func(from []*battle.Unit, def *battle.Unit) []*battle.Unit {
		if chosen != nil {
			for _, x := range from {
				if x == chosen {
					return []*battle.Unit{x}
				}
			}
			return nil // mục tiêu thủ công không hợp lệ: không tự đổi hướng (P13 §2)
		}
		if def != nil {
			return []*battle.Unit{def}
		}
		return nil
	}
	switch s.Target {
	case "enemy_one":
		var def *battle.Unit
		if len(foes) > 0 {
			def = foes[0]
		}
		return pick(foes, def)
	case "enemy_all":
		return byID(foes)
	case "self":
		return []*battle.Unit{u}
	case "ally_one":
		return pick(allies, u)
	case "ally_all":
		return byID(allies)
	case "ally_other":
		others := []*battle.Unit{}
		for _, a := range allies {
			if a != u {
				others = append(others, a)
			}
		}
		if chosen != nil && chosen != u {
			return pick(others, nil)
		}
		if len(others) > 0 {
			return others[:1]
		}
	case "ally_fainted":
		for _, a := range sideOf(f.b, u) {
			if a.HP <= 0 && a != u {
				return []*battle.Unit{a}
			}
		}
	}
	return nil
}

// removable liệt kê trạng thái xấu gỡ được theo thứ tự ưu tiên cleanse (khống chế → câm/trói → debuff → DoT).
type cleanseItem struct {
	class, seq int
	id         string
	buff       bool
}

func (f *fight) removable(u *battle.Unit) []cleanseItem {
	out := []cleanseItem{}
	for _, s := range u.Statuses {
		class := map[string]int{"sleep": 0, "petrify": 0, "confuse": 0, "silence": 1, "bind": 1, "blind": 2, "misfortune": 2, "frailty": 2, "poison": 3, "burn": 3}[s.ID]
		out = append(out, cleanseItem{class, s.Seq, s.ID, false})
	}
	for _, b := range u.Buffs {
		if b.AmountBP < 0 {
			out = append(out, cleanseItem{2, b.Seq, b.ID, true})
		}
	}
	sort.SliceStable(out, func(i, j int) bool {
		a, b := out[i], out[j]
		if a.class != b.class {
			return a.class < b.class
		}
		if a.seq != b.seq {
			return a.seq < b.seq
		}
		return a.id < b.id
	})
	return out
}

func (f *fight) removeOne(u *battle.Unit, it cleanseItem) {
	if !it.buff {
		f.terminate(u, it.id, "status_cleansed")
		return
	}
	for i, b := range u.Buffs {
		if b.ID == it.id && b.AmountBP < 0 {
			u.Buffs = append(u.Buffs[:i], u.Buffs[i+1:]...)
			break
		}
	}
	f.say("status_cleansed", nil, u, 0, u.Name+": "+it.id+" removed", it.id)
}

// valid kiểm tra điều kiện riêng của kỹ năng hỗ trợ (cần có thứ để gỡ, thiếu máu…); sai thì không tốn MP/lượt.
func (f *fight) valid(u *battle.Unit, s content.Skill, ts []*battle.Unit) bool {
	if len(ts) == 0 {
		return false
	}
	t := ts[0]
	switch s.ID {
	case "cleanse":
		return len(f.removable(t)) > 0
	case "wake", "free", "song", "sight", "dissolve", "order", "bless":
		return hasStatus(t, s.Effect.Cleanse) || f.hasNegBuffNamed(t, s.Effect.Cleanse)
	case "extinguish":
		return hasStatus(t, "burn")
	case "flower_radiance":
		return t.HP < t.MaxHP || len(f.removable(t)) > 0
	case "dispel":
		return len(t.Buffs) > 0 || t.Shield != nil
	}
	return true
}

func (f *fight) hasNegBuffNamed(u *battle.Unit, id string) bool { return false }

// cast thực thi một kỹ năng đã hợp lệ: trả MP một lần, đặt hồi chiêu, chốt chỉ số nguồn rồi xử lý từng mục tiêu theo id.
func (f *fight) cast(u *battle.Unit, s content.Skill, rank int, ts []*battle.Unit) {
	u.MP -= rankMP(s, rank)
	if u.Cooldowns == nil {
		u.Cooldowns = map[string]int{}
	}
	u.Cooldowns[s.ID] = f.round + s.Cooldown + 1
	f.say("skill_cast", u, ts[0], 0, u.Name+" used "+s.Name, s.ID)
	e := f.e
	mag := e.eff(u, "mag")
	pn, pd := rankPower(s, rank)
	switch s.Kind {
	case "physical", "magic":
		off := e.eff(u, "atk")
		if s.Kind == "magic" {
			off = mag
		}
		hits := max(1, s.Effect.Hits)
		any := false
		for _, t := range ts {
			hit := false
			for h := 0; h < hits && t.HP > 0 && u.HP > 0; h++ {
				lost, ok := f.strike(u, t, off, int64(s.PowerPM)*pn, 1000*pd, s.Element, s.Effect.PenetrationPM, true)
				hit = hit || ok
				if ok && s.ID == "drain" && lost > 0 {
					f.heal(u, u, max(1, lost/4))
				}
				if ok && s.ID == "mana_burn" && t.HP > 0 {
					take := min(min(t.MP, 10), ratFloor(new(big.Rat).Mul(mag, big.NewRat(1, 5))))
					t.MP -= take
					f.say("mp_burn", u, t, take, fmt.Sprintf("%s loses %d MP", t.Name, take), "")
				}
			}
			any = any || hit
			if hit && t.HP > 0 {
				f.afterDamageEffect(u, t, s, off)
			}
		}
		if any && s.Effect.SelfBuff != "" && u.HP > 0 {
			f.addBuff(u, s.ID, buffSpec{stat: s.Effect.SelfBuff, group: statGroup[s.Effect.SelfBuff], bp: s.Effect.AmountBP}, 2)
			f.say("buff_applied", u, u, 0, u.Name+" gains "+s.Effect.SelfBuff, s.ID)
		}
	case "control", "debuff", "dispel":
		for _, t := range ts {
			hitPM := int64(950)
			if hasStatus(u, "blind") {
				hitPM = 750
			}
			if !bern(&f.b.RNG, hitPM, 1000) {
				f.say("miss", u, t, 0, "The skill missed", "")
				continue
			}
			if s.Kind == "dispel" {
				f.dispel(u, t)
				continue
			}
			f.applyEffect(u, t, s)
		}
	case "buff":
		f.castBuff(u, s, ts)
	case "heal":
		for _, t := range ts {
			var raw int
			switch s.ID {
			case "group_heal":
				raw = ratFloor(new(big.Rat).Add(new(big.Rat).Mul(mag, big.NewRat(85, 100)), big.NewRat(6, 1)))
			case "group_heal_super":
				raw = ratFloor(new(big.Rat).Add(new(big.Rat).Mul(mag, big.NewRat(110, 100)), big.NewRat(10, 1)))
			case "flower_radiance":
				if it := f.removable(t); len(it) > 0 {
					f.removeOne(t, it[0])
				}
				raw = ratFloor(new(big.Rat).Add(new(big.Rat).Mul(mag, big.NewRat(150, 100)), big.NewRat(10, 1)))
			default: // heal: floor(1.50×MAG+10), rank ×1.15/1.30 trên lượng hồi hoàn chỉnh
				raw = ratFloor(new(big.Rat).Mul(new(big.Rat).Add(new(big.Rat).Mul(mag, big.NewRat(150, 100)), big.NewRat(10, 1)), big.NewRat(pn, pd)))
			}
			f.heal(u, t, raw)
		}
	case "shield":
		t := ts[0]
		switch s.ID {
		case "love_kiss":
			f.setShield(t, ratFloor(new(big.Rat).Add(new(big.Rat).Mul(mag, big.NewRat(180, 100)), new(big.Rat).Mul(big.NewRat(int64(u.MaxHP), 1), big.NewRat(10, 100)))), 1)
		case "turtle_tide":
			if hasStatus(t, "burn") {
				f.terminate(t, "burn", "status_cleansed")
			}
			f.setShield(t, ratFloor(new(big.Rat).Add(new(big.Rat).Mul(mag, big.NewRat(120, 100)), new(big.Rat).Mul(big.NewRat(int64(u.MaxHP), 1), big.NewRat(8, 100)))), 2)
		default:
			f.setShield(t, ratFloor(new(big.Rat).Add(new(big.Rat).Mul(mag, big.NewRat(120, 100)), new(big.Rat).Mul(big.NewRat(int64(u.MaxHP), 1), big.NewRat(8, 100)))), 2)
		}
	case "cleanse":
		t := ts[0]
		switch {
		case s.ID == "cleanse":
			if it := f.removable(t); len(it) > 0 {
				f.removeOne(t, it[0])
			}
		case s.ID == "extinguish":
			f.terminate(t, "burn", "status_cleansed")
			f.setShield(t, ratFloor(new(big.Rat).Mul(mag, big.NewRat(1, 2))), 1)
		default:
			f.terminate(t, s.Effect.Cleanse, "status_cleansed")
		}
	}
}

// afterDamageEffect xử lý hiệu ứng phụ của kỹ năng sát thương lên mục tiêu còn sống (chỉ sau khi trúng).
func (f *fight) afterDamageEffect(u, t *battle.Unit, s content.Skill, off *big.Rat) {
	ef := s.Effect
	switch {
	case ef.Status == "poison" || ef.Status == "burn":
		tick := new(big.Rat).Mul(off, big.NewRat(30, 100)) // 0.30 × tấn công nguồn tại lúc áp
		if ef.TickPowerPM > 0 {
			tick = new(big.Rat).Mul(off, big.NewRat(int64(ef.TickPowerPM), 1000))
		}
		milli := ratFloor(new(big.Rat).Mul(tick, big.NewRat(1000, 1)))
		el := "neutral"
		if ef.Status == "burn" {
			el = "fire"
		}
		f.tryStatus(u, t, ef.Status, ef.ChancePM, milli, el)
	case ef.Status == "slow":
		f.tryDebuff(u, t, "slow", "spd", ef.AmountBP, ef.ChancePM)
	case ef.Status != "":
		f.tryStatus(u, t, ef.Status, ef.ChancePM, 0, "")
	case ef.Stat != "":
		f.tryDebuff(u, t, s.ID, ef.Stat, ef.AmountBP, ef.ChancePM)
	}
}

// applyEffect: kỹ năng khống chế/debuff thuần (không sát thương) sau cú trúng.
func (f *fight) applyEffect(u, t *battle.Unit, s content.Skill) {
	ef := s.Effect
	switch {
	case ef.Status == "slow":
		f.tryDebuff(u, t, "slow", "spd", ef.AmountBP, ef.ChancePM)
	case ef.Status != "":
		f.tryStatus(u, t, ef.Status, ef.ChancePM, 0, "")
	case ef.Stat != "":
		f.tryDebuff(u, t, s.ID, ef.Stat, ef.AmountBP, ef.ChancePM)
	}
}

// dispel gỡ một buff của t: khiên → ATK/MAG → DEF → SPD/SR; hòa theo cũ hơn rồi id. Không qua SR.
func (f *fight) dispel(u, t *battle.Unit) {
	if t.Shield != nil {
		t.Shield = nil
		f.say("status_cleansed", u, t, 0, t.Name+" shield dispelled", "dispel")
		return
	}
	rank := map[string]int{"atk": 1, "mag": 1, "def": 2, "spd": 3, "status_resistance": 3}
	best := -1
	for i, b := range t.Buffs {
		if b.AmountBP <= 0 {
			continue
		}
		if best < 0 {
			best = i
			continue
		}
		o := t.Buffs[best]
		if rank[b.Stat] < rank[o.Stat] || (rank[b.Stat] == rank[o.Stat] && (b.Seq < o.Seq || (b.Seq == o.Seq && b.ID < o.ID))) {
			best = i
		}
	}
	if best < 0 {
		return
	}
	id := t.Buffs[best].ID
	t.Buffs = append(t.Buffs[:best], t.Buffs[best+1:]...)
	f.say("status_cleansed", u, t, 0, t.Name+": "+id+" dispelled", "dispel")
}

// castBuff áp các buff cố định theo bảng (guard, haste…), phản kích và hồi theo nhịp.
func (f *fight) castBuff(u *battle.Unit, s content.Skill, ts []*battle.Unit) {
	mag := f.e.eff(u, "mag")
	for _, t := range ts {
		switch s.ID {
		case "counter":
			t.CounterUntil = f.round + 2
			f.say("buff_applied", u, t, 0, t.Name+" readies a counter", "counter")
			continue
		case "regen":
			heal := ratFloor(new(big.Rat).Add(new(big.Rat).Mul(mag, big.NewRat(60, 100)), big.NewRat(4, 1)))
			t.Regen = &battle.Regen{Heal: heal, FirstRound: f.round + 1, ExpireRound: f.round + 2}
			f.say("buff_applied", u, t, 0, t.Name+" begins to regenerate", "regen")
			continue
		}
		for _, spec := range buffTable[s.ID] {
			f.addBuff(t, s.ID, spec, 2)
		}
		f.say("buff_applied", u, t, 0, t.Name+" is empowered ("+s.Name+")", s.ID)
	}
}
