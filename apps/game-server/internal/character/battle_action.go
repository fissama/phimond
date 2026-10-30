package character

import (
	"fmt"
	"math"
	"phimond/server/internal/battle"
	"phimond/server/internal/content"
)

// battleAction chạy trọn một vòng: chốt thứ tự theo SPD hiệu lực, người chơi và quái lần lượt hành động, xử lý DoT/hồi/hết
// hạn cuối vòng, kiểm tra thắng thua. Lệnh không hợp lệ bị từ chối trước khi tiêu MP/lượt (copy-on-success của Apply).
func (e *Engine) battleAction(c *Character, d Intent) ([]Event, error) {
	b := c.Battle
	if b == nil || d.BattleID != b.ID || d.Turn != b.Turn || b.Phase != "WAIT_COMMAND" {
		return nil, fmt.Errorf("battle or turn is stale")
	}
	if e.Data.Rules.BattleTurnCap > 0 && b.Turn >= e.Data.Rules.BattleTurnCap {
		return nil, fmt.Errorf("battle turn limit reached")
	}
	player := b.Units[0]
	foes := sideUnits(b, "enemy")
	enemy := firstAlive(foes)
	if enemy == nil {
		return nil, fmt.Errorf("no living enemy")
	}
	f := &fight{e: e, b: b, round: b.Turn}
	// Mục tiêu do người chơi chọn (nếu có): đơn vị còn sống bất kỳ; kiểm hợp lệ theo từng loại hành động bên dưới.
	var chosen *battle.Unit
	if d.TargetID != "" {
		for _, u := range b.Units {
			if u.ID == d.TargetID && u.HP > 0 {
				chosen = u
			}
		}
		if chosen == nil {
			return nil, fmt.Errorf("invalid target")
		}
	}
	item := content.Item{}
	var skill content.Skill
	rank := 1
	switch d.Choice {
	case "attack":
		if chosen != nil && chosen.Side != "enemy" {
			return nil, fmt.Errorf("invalid target")
		}
		if why := blockedChannel(player, "physical"); why != "" {
			return nil, fmt.Errorf("đang bị trói, không thể đánh thường")
		}
		if chosen != nil {
			enemy = chosen
		}
	case "auto":
	case "skill":
		var ok bool
		skill, ok = e.Data.Skills[d.SkillID]
		if !ok || !has(player.Pet.Skills, d.SkillID) {
			return nil, fmt.Errorf("skill has not been learned")
		}
		rank = player.Pet.Rank(skill.ID)
		switch f.usable(player, skill, rank) {
		case "mp":
			return nil, fmt.Errorf("not enough MP")
		case "cooldown":
			return nil, fmt.Errorf("skill is on cooldown")
		case "bind":
			return nil, fmt.Errorf("đang bị trói, không dùng được kỹ năng vật lý")
		case "silence":
			return nil, fmt.Errorf("đang bị câm lặng, không dùng được kỹ năng phép")
		}
		if ts := f.targets(player, skill, chosen); !f.valid(player, skill, ts) {
			return nil, fmt.Errorf("invalid target or nothing to do")
		}
	case "capture":
		if b.Arena || !e.Data.Species[enemy.SpeciesID].Catchable {
			return nil, fmt.Errorf("target cannot be captured")
		}
		if chosen != nil && chosen.Side == "enemy" {
			enemy = chosen
		}
		if c.Inventory["capture_seal"] < 1 {
			return nil, fmt.Errorf("no binding seals")
		}
	case "item":
		var ok bool
		item, ok = e.Data.Items[d.ItemID]
		if !ok || (item.Kind != "heal" && item.Kind != "mp") || c.Inventory[item.ID] < 1 {
			return nil, fmt.Errorf("usable item not available")
		}
	case "flee":
	default:
		return nil, fmt.Errorf("unknown battle action")
	}
	b.Commands = append(b.Commands, d)
	b.Phase = "LOCK_COMMANDS"
	ev := []Event{}
	emit := func(v Event) { b.Sequence++; v.Seq = b.Sequence; ev = append(ev, v); b.Events = append(b.Events, v) }
	f.emit = emit
	b.Phase = "CALCULATE_ORDER"
	order := f.order()
	b.Phase = "EXECUTE_ACTIONS"
	// Chạy luôn đi trước mọi đòn đánh: chạm quái là lựa chọn của người chơi, rút lui không bị phạt máu.
	if d.Choice == "flee" {
		b.Result = "flee"
		emit(event("battle_flee", "You returned to the path"))
	}
	for _, u := range order {
		if player.HP <= 0 || !anyAlive(foes) || b.Result != "" {
			break
		}
		if u.HP <= 0 {
			continue
		}
		blocked, confused := f.consumeControl(u)
		if blocked {
			continue
		}
		if confused {
			// Hỗn loạn: thay hành động bằng đòn thường vào một đối thủ sống do RNG của trận chọn.
			if opp := living(foesOf(b, u)); len(opp) > 0 {
				f.basic(u, opp[b.RNG.Int(len(opp))])
			}
			continue
		}
		if u.Side == "enemy" {
			f.enemyTurn(u)
			continue
		}
		switch d.Choice {
		case "capture":
			c.Inventory["capture_seal"]--
			chance := e.CaptureChance(enemy.Pet, enemy.HP, enemy.MaxHP, c.Level)
			if len(enemy.Statuses) > 0 {
				chance = math.Min(e.Data.Rules.CaptureCap, chance+e.Data.Rules.CaptureStatusBonus)
			}
			emit(event("item_spend", "Used one binding seal"))
			if b.RNG.Float() < chance {
				p := enemy.Pet
				// Bắt được: tạo hồ sơ tăng trưởng mới theo xác suất P11, thưởng kế thừa 0, không có kỹ năng.
				p.Grades = rollGrades(&c.RNG)
				ratio := float64(enemy.HP) / float64(max(1, enemy.MaxHP))
				e.Recalculate(p)
				p.HP = max(1, int(math.Ceil(ratio*float64(p.MaxHP))))
				p.MP = min(enemy.MP, p.MaxMP)
				c.Pets = append(c.Pets, p)
				enemy.HP = 0 // rời sân; XP vẫn tính như quái bị hạ
				if !anyAlive(foes) {
					b.Result = "capture"
				}
				e.progress(c, "pet_capture", p.SpeciesID)
				emit(Event{Type: "pet_capture", ActorID: player.ID, TargetID: enemy.ID, Message: p.Name + " joined your ranch. Visit the keeper for appraisal."})
			} else {
				emit(event("capture_failed", "The beast broke free"))
			}
		case "item":
			c.Inventory[item.ID]--
			if item.Kind == "heal" {
				u.HP = min(u.MaxHP, u.HP+item.Power)
			} else {
				u.MP = min(u.MaxMP, u.MP+item.Power)
			}
			emit(event("item_spend", "Used "+item.Name))
		case "flee":
			b.Result = "flee"
			emit(event("battle_flee", "You returned to the path"))
		case "attack":
			f.basic(u, enemy)
		case "auto":
			f.autoTurn(u, true)
		case "skill":
			// Kiểm lại lúc thực thi: nếu đã đổi (bị khống chế, mục tiêu chết…) thì lùi về chính sách tự động, không đổi hướng thủ công.
			ts := f.targets(u, skill, chosen)
			if f.usable(u, skill, rank) == "" && f.valid(u, skill, ts) {
				f.cast(u, skill, rank, ts)
			} else {
				emit(event("action_fallback", u.Name+" changed action"))
				f.autoTurn(u, true)
			}
		}
	}
	b.Phase = "APPLY_END_TURN_EFFECTS"
	if b.Result == "" {
		f.endRound()
	}
	b.Phase = "CHECK_VICTORY"
	if b.Result == "" {
		if player.HP <= 0 {
			b.Result = "loss"
		} else if !anyAlive(foes) {
			b.Result = "win"
		} else if e.Data.Rules.BattleTurnCap > 0 && b.Turn >= e.Data.Rules.BattleTurnCap {
			b.Result = "draw"
		}
	}
	// The pet in the character aggregate is distinct after JSON restore, so sync explicitly.
	p, _ := findPet(c, player.ID)
	p.HP = min(player.HP, p.MaxHP)
	p.MP = min(player.MP, p.MaxMP)
	if b.Result != "" {
		b.Phase = "FINISHED"
		if b.Result == "win" || b.Result == "capture" {
			// Mỗi quái bị hạ/bắt cộng XP và vàng riêng (quái cùng cấp nên XP = n × một quái).
			xp, gold := 0, 0
			for _, u := range foes {
				if u.HP <= 0 {
					xp += e.Data.Rules.BattleXP * max(1, u.Pet.Level)
					gold += e.Data.Rules.BattleGold
				}
			}
			e.petXP(p, xp)
			e.trainerXP(c, xp)
			c.Gold += gold
			emit(event("currency_gain", fmt.Sprintf("Earned %d gold and %d experience", gold, xp)))
			if b.Result == "win" {
				e.progress(c, "battle_win", enemy.SpeciesID)
				if b.Arena {
					c.ArenaTier = max(c.ArenaTier, 1)
				}
			}
		}
		emit(event("battle_"+b.Result, "Battle ended: "+b.Result))
		if !b.Arena {
			e.afterWildBattle(c, b, emit)
		}
		c.History = append(c.History, b)
		if len(c.History) > 20 {
			c.History = c.History[len(c.History)-20:]
		}
		c.Battle = nil
	} else {
		b.Turn++
		b.Phase = "WAIT_COMMAND"
	}
	return ev, nil
}

// autoTurn hành động theo chính sách tự động: kỹ năng phù hợp nhất, không có thì đòn thường vào địch yếu máu nhất.
func (f *fight) autoTurn(u *battle.Unit, player bool) {
	if s, rank, t := f.policy(u, player); s != nil {
		if ts := f.targets(u, *s, t); f.valid(u, *s, ts) {
			f.cast(u, *s, rank, ts)
			return
		}
	}
	foes := byID(living(foesOf(f.b, u)))
	if len(foes) == 0 {
		return
	}
	t := foes[0]
	for _, x := range foes[1:] {
		if x.HP*t.MaxHP < t.HP*x.MaxHP {
			t = x
		}
	}
	f.basic(u, t)
}

func (f *fight) enemyTurn(u *battle.Unit) { f.autoTurn(u, false) }
