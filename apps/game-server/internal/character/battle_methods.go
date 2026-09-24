package character

import (
	"fmt"
	"math"
	"phimond/server/internal/battle"
	"phimond/server/internal/content"
	"phimond/server/internal/pet"
	"sort"
)

// unit constructs a battle Unit from the given pet and side. Moved verbatim
// from internal/game/battle.go. It is kept in this package so the lowercase
// helper stays in scope of the test package without exporting it.
func unit(p *pet.Pet, side string) *battle.Unit {
	return &battle.Unit{ID: p.ID, Name: p.Name, Side: side, SpeciesID: p.SpeciesID, HP: p.HP, MP: p.MP, MaxHP: p.MaxHP, MaxMP: p.MaxMP, Statuses: []battle.ActiveStatus{}, Buffs: []battle.Buff{}, Pet: p}
}

// startBattle rolls a wild pet (or a fixed arena opponent) and returns the
// first battle events. Moved verbatim from internal/game/battle.go.
func (e *Engine) startBattle(c *Character, arena bool, contactSpecies ...string) ([]Event, error) {
	p, err := findPet(c, c.ActivePetID)
	if err != nil {
		return nil, err
	}
	if p.HP <= 0 {
		return nil, fmt.Errorf("heal your active beast before battle")
	}
	pool := e.Data.Maps[c.MapID].Spawns
	if !arena && len(pool) == 0 {
		return nil, fmt.Errorf("no wild encounters here")
	}
	species := "wolf"
	level := 10
	if !arena {
		species = pool[c.RNG.Int(len(pool))]
		if len(contactSpecies) > 0 {
			species = contactSpecies[0]
		}
		level = max(1, min(c.Level, e.Data.Maps[c.MapID].MinLevel+4)-c.RNG.Int(2))
	}
	enemy := e.NewPet(c, species, level)
	if arena {
		enemy.Skills = append(enemy.Skills, "neutral_strike")
	}
	seed := c.RNG.Next()
	b := &Battle{ID: c.id("battle"), Turn: 1, Phase: "WAIT_COMMAND", Units: []*battle.Unit{unit(p, "player"), unit(enemy, "enemy")}, Seed: seed, RNG: RNG{seed}, Arena: arena, Commands: []Intent{}, Events: []Event{}}
	c.Battle = b
	return []Event{event("battle_start", "Encountered "+enemy.Name)}, nil
}

// blocked reports whether u's statuses block actions of the given kind.
// Moved verbatim from internal/game/battle.go.
func (e *Engine) blocked(u *battle.Unit, kind string) bool {
	for _, s := range u.Statuses {
		if has(e.Data.Statuses[s.ID].Blocks, kind) {
			return true
		}
	}
	return false
}

// multiplier returns the cumulative multiplier for stat across u's active
// buffs. Moved verbatim from internal/game/battle.go.
func (e *Engine) multiplier(u *battle.Unit, stat string) float64 {
	v := 1.0
	for _, b := range u.Buffs {
		if b.Stat == stat {
			v *= b.Multiplier
		}
	}
	return v
}

// battleAction is the single battle turn handler. Moved verbatim from
// internal/game/battle.go.
func (e *Engine) battleAction(c *Character, d Intent) ([]Event, error) {
	b := c.Battle
	if b == nil || d.BattleID != b.ID || d.Turn != b.Turn || b.Phase != "WAIT_COMMAND" {
		return nil, fmt.Errorf("battle or turn is stale")
	}
	if e.Data.Rules.BattleTurnCap > 0 && b.Turn >= e.Data.Rules.BattleTurnCap {
		return nil, fmt.Errorf("battle turn limit reached")
	}
	player, enemy := b.Units[0], b.Units[1]
	kind := d.Choice
	skill := content.Skill{}
	item := content.Item{}
	switch d.Choice {
	case "attack", "auto":
		skill = e.Data.Skills["attack"]
		kind = skill.Kind
	case "skill":
		var ok bool
		skill, ok = e.Data.Skills[d.SkillID]
		if !ok || !has(player.Pet.Skills, d.SkillID) {
			return nil, fmt.Errorf("skill has not been learned")
		}
		if player.MP < skill.MPCost {
			return nil, fmt.Errorf("not enough MP")
		}
		kind = skill.Kind
	case "capture":
		if b.Arena || !e.Data.Species[enemy.SpeciesID].Catchable || enemy.HP <= 0 {
			return nil, fmt.Errorf("target cannot be captured")
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
	case "defend", "flee":
	default:
		return nil, fmt.Errorf("unknown battle action")
	}
	b.Commands = append(b.Commands, d)
	b.Phase = "LOCK_COMMANDS"
	ev := []Event{}
	emit := func(v Event) { b.Sequence++; v.Seq = b.Sequence; ev = append(ev, v); b.Events = append(b.Events, v) }
	for _, u := range b.Units {
		u.Defending = false
	}
	// Defend covers this round, including attacks by faster opponents.
	if d.Choice == "defend" && !e.blocked(player, "defend") {
		player.Defending = true
	}
	b.Phase = "CALCULATE_ORDER"
	order := []*battle.Unit{player, enemy}
	sort.SliceStable(order, func(i, j int) bool {
		return float64(order[i].Pet.Speed)*e.multiplier(order[i], "speed") > float64(order[j].Pet.Speed)*e.multiplier(order[j], "speed")
	})
	b.Phase = "EXECUTE_ACTIONS"
	for _, u := range order {
		if player.HP <= 0 || enemy.HP <= 0 || b.Result != "" {
			break
		}
		if u.Side == "enemy" {
			s := e.Data.Skills["attack"]
			for _, id := range u.Pet.Skills {
				candidate := e.Data.Skills[id]
				if candidate.MPCost <= u.MP && !e.blocked(u, candidate.Kind) {
					s = candidate
				}
			}
			e.cast(b, u, player, s, emit)
			continue
		}
		if d.Choice == "flee" {
			b.Result = "flee"
			emit(event("battle_flee", "You returned to the path"))
			break
		}
		if e.blocked(u, kind) {
			emit(event("action_blocked", u.Name+" cannot act"))
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
				p.HP = max(1, enemy.HP)
				p.MP = enemy.MP
				c.Pets = append(c.Pets, p)
				b.Result = "capture"
				e.progress(c, "pet_capture", p.SpeciesID)
				emit(event("pet_capture", p.Name+" joined your ranch. Visit the keeper for appraisal."))
			} else {
				emit(event("capture_failed", "The beast broke free"))
			}
		case "defend":
			u.Defending = true
			emit(event("defend", u.Name+" braces for impact"))
		case "item":
			c.Inventory[item.ID]--
			if item.Kind == "heal" {
				u.HP = min(u.MaxHP, u.HP+item.Power)
			} else {
				u.MP = min(u.MaxMP, u.MP+item.Power)
			}
			emit(event("item_spend", "Used "+item.Name))
		default:
			e.cast(b, u, enemy, skill, emit)
		}
	}
	b.Phase = "APPLY_END_TURN_EFFECTS"
	if b.Result == "" {
		for _, u := range b.Units {
			remaining := []battle.ActiveStatus{}
			for _, s := range u.Statuses {
				if s.AppliedTurn < b.Turn {
					s.Remaining--
				}
				if s.Remaining <= 0 {
					if e.Data.Statuses[s.ID].FatalOnExpiry && u.HP > 0 {
						u.HP = 0
						emit(event("status_fatal", u.Name+" succumbed to "+s.ID))
					} else {
						emit(event("status_expired", s.ID+" faded"))
					}
				} else {
					remaining = append(remaining, s)
				}
			}
			u.Statuses = remaining
			buffs := []battle.Buff{}
			for _, buff := range u.Buffs {
				if buff.AppliedTurn < b.Turn {
					buff.Remaining--
				}
				if buff.Remaining > 0 {
					buffs = append(buffs, buff)
				}
			}
			u.Buffs = buffs
			e.refreshResources(u)
		}
	}
	b.Phase = "CHECK_VICTORY"
	if b.Result == "" {
		if player.HP <= 0 {
			b.Result = "loss"
		} else if enemy.HP <= 0 {
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
			xp := e.Data.Rules.BattleXP * max(1, enemy.Pet.Level)
			e.petXP(p, xp)
			e.trainerXP(c, xp)
			c.Gold += e.Data.Rules.BattleGold
			emit(event("currency_gain", fmt.Sprintf("Earned %d gold and %d experience", e.Data.Rules.BattleGold, xp)))
			if b.Result == "win" {
				e.progress(c, "battle_win", enemy.SpeciesID)
				if b.Arena {
					c.ArenaTier = max(c.ArenaTier, 1)
				}
			}
		}
		emit(event("battle_"+b.Result, "Battle ended: "+b.Result))
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

// cast resolves the skill onto the target; unit, applying status, heal,
// cleanse or buff depending on kind. Moved verbatim from internal/game/battle.go.
func (e *Engine) cast(b *Battle, actor, target *battle.Unit, s content.Skill, emit func(Event)) {
	if e.blocked(actor, s.Kind) {
		emit(event("action_blocked", actor.Name+" cannot use "+s.Name))
		return
	}
	if actor.MP < s.MPCost {
		return
	}
	actor.MP -= s.MPCost
	if s.Target == "self" {
		target = actor
	}
	for _, st := range actor.Statuses {
		if e.Data.Statuses[st.ID].RandomTarget {
			living := []*battle.Unit{}
			for _, u := range b.Units {
				if u.HP > 0 {
					living = append(living, u)
				}
			}
			target = living[b.RNG.Int(len(living))]
			break
		}
	}
	emit(Event{Type: "skill_cast", ActorID: actor.ID, TargetID: target.ID, Message: actor.Name + " used " + s.Name})
	hit := s.Hit
	if actor != target {
		for _, st := range actor.Statuses {
			hit *= e.Data.Statuses[st.ID].HitMultiplier
		}
	}
	if b.RNG.Float() > clamp(hit, .05, 1) {
		emit(Event{Type: "miss", ActorID: actor.ID, TargetID: target.ID, Message: "The skill missed"})
		return
	}
	switch s.Kind {
	case "physical", "magic":
		atk := float64(actor.Pet.Attack) * e.multiplier(actor, "attack")
		if s.Kind == "magic" {
			atk = float64(actor.Pet.Magic) * e.multiplier(actor, "magic")
		}
		def := float64(target.Pet.Defense) * e.multiplier(target, "defense")
		wake := 1.0
		for _, st := range target.Statuses {
			spec := e.Data.Statuses[st.ID]
			def *= spec.DefenseMultiplier
			if spec.WakeOnDamage {
				wake *= spec.WakeMultiplier
			}
		}
		damage := (float64(s.Power) + atk) * e.Data.Rules.DamageScale * 100 / (100 + def*3) * (1 - float64(target.Pet.Resistances[s.Element])/100) * wake * (.9 + b.RNG.Float()*.2)
		if b.RNG.Float() < actor.Pet.Critical*e.multiplier(actor, "critical") {
			damage *= e.Data.Rules.CritMultiplier
		}
		if target.Defending {
			damage *= .5
		}
		amount := min(target.HP, max(1, int(damage)))
		target.HP -= amount
		emit(Event{Type: "damage", ActorID: actor.ID, TargetID: target.ID, Amount: amount, Message: fmt.Sprintf("%s takes %d damage", target.Name, amount)})
		remaining := []battle.ActiveStatus{}
		for _, st := range target.Statuses {
			if !e.Data.Statuses[st.ID].WakeOnDamage {
				remaining = append(remaining, st)
			} else {
				emit(event("status_cleansed", target.Name+" woke up"))
			}
		}
		target.Statuses = remaining
	case "status":
		if b.RNG.Float() < float64(target.Pet.StatusResistances[s.Status])/100 {
			emit(event("status_resisted", target.Name+" resisted "+s.Status))
			return
		}
		found := false
		for i, st := range target.Statuses {
			if st.ID == s.Status {
				target.Statuses[i] = battle.ActiveStatus{ID: s.Status, Remaining: s.Duration, AppliedTurn: b.Turn}
				found = true
			}
		}
		if !found {
			target.Statuses = append(target.Statuses, battle.ActiveStatus{ID: s.Status, Remaining: s.Duration, AppliedTurn: b.Turn})
		}
		emit(Event{Type: "status_applied", TargetID: target.ID, Message: target.Name + " is affected by " + s.Status})
	case "heal":
		amount := min(target.MaxHP-target.HP, s.Power+actor.Pet.Magic)
		target.HP += amount
		emit(Event{Type: "heal", TargetID: target.ID, Amount: amount, Message: fmt.Sprintf("%s recovers %d HP", target.Name, amount)})
	case "cleanse":
		remaining := []battle.ActiveStatus{}
		for _, st := range target.Statuses {
			if st.ID != s.Cleanse {
				remaining = append(remaining, st)
			}
		}
		target.Statuses = remaining
		emit(event("status_cleansed", "Removed "+s.Cleanse))
	case "buff":
		found := false
		for i, buff := range target.Buffs {
			if buff.Stat == s.Stat {
				target.Buffs[i] = battle.Buff{Stat: s.Stat, Multiplier: s.Modifier, Remaining: s.Duration, AppliedTurn: b.Turn}
				found = true
			}
		}
		if !found {
			target.Buffs = append(target.Buffs, battle.Buff{Stat: s.Stat, Multiplier: s.Modifier, Remaining: s.Duration, AppliedTurn: b.Turn})
		}
		e.refreshResources(target)
		emit(event("buff_applied", target.Name+" gains "+s.Stat))
	}
}

// refreshResources updates a Unit's MaxHP/MaxMP from its pet stats and
// current buffs, clamping current resources. Moved verbatim from
// internal/game/battle.go.
func (e *Engine) refreshResources(u *battle.Unit) {
	u.MaxHP = int(float64(u.Pet.MaxHP) * e.multiplier(u, "max_hp"))
	u.MaxMP = int(float64(u.Pet.MaxMP) * e.multiplier(u, "max_mp"))
	u.HP = min(u.HP, u.MaxHP)
	u.MP = min(u.MP, u.MaxMP)
}
