package character

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io"
)

// Apply uses copy-on-success so a rejected intent cannot consume RNG,
// items or turns. Moved verbatim from internal/game/service.go. The case
// branches remain inlined rather than dispatched into separate domain
// packages because the *Engine methods they call live here too; sending
// them out would either import cycle the dispatch back into the domain
// packages or duplicate logic across two files.
func (e *Engine) Apply(c *Character, op string, raw json.RawMessage) ([]Event, error) {
	d := Intent{}
	if len(raw) > 0 && string(raw) != "null" {
		decoder := json.NewDecoder(bytes.NewReader(raw))
		decoder.DisallowUnknownFields()
		if err := decoder.Decode(&d); err != nil {
			return nil, fmt.Errorf("invalid intent: %w", err)
		}
		if decoder.Decode(&struct{}{}) != io.EOF {
			return nil, fmt.Errorf("trailing intent data")
		}
	}
	b, err := json.Marshal(c)
	if err != nil {
		return nil, err
	}
	var next Character
	if err = json.Unmarshal(b, &next); err != nil {
		return nil, err
	}
	ev, err := e.apply(&next, op, d)
	if err != nil {
		return nil, err
	}
	next.Revision++
	for i := range ev {
		ev[i].Seq = i + 1
	}
	next.Events = ev
	*c = next
	return ev, nil
}

// apply dispatches a parsed intent to its per-op handler. Each case branch
// lives in this file (rather than in the package that the domain comment
// describes in §3) because the *Engine methods they exercise are also
// defined in this package; splitting them out would create an import
// cycle through the dispatcher. The case bodies are otherwise unchanged
// from internal/game/service.go. Moved verbatim with type renames.
func (e *Engine) apply(c *Character, op string, d Intent) ([]Event, error) {
	if op == "character.get" {
		return []Event{}, nil
	}
	if op == "battle.action" {
		return e.battleAction(c, d)
	}
	if c.Battle != nil {
		return nil, fmt.Errorf("finish your battle first")
	}
	switch op {
	case "world.move":
		dx, dy := 0, 0
		switch d.Direction {
		case "left":
			dx = -1
		case "right":
			dx = 1
		case "up":
			dy = -1
		case "down":
			dy = 1
		default:
			return nil, fmt.Errorf("invalid direction")
		}
		m := e.Data.Maps[c.MapID]
		nx := c.X + dx
		ny := c.Y + dy
		// Default to a square grid if a map has no explicit Height (legacy
		// content) so existing JSON files don't break loading.
		h := m.Height
		if h <= 0 {
			h = m.Width
		}
		if nx < 0 || nx >= m.Width || ny < 0 || ny >= h {
			return nil, fmt.Errorf("use a portal at the map edge")
		}
		c.X = nx
		c.Y = ny
		return []Event{}, nil
	case "world.portal":
		for _, p := range e.Data.Maps[c.MapID].Portals {
			if p.ID == d.PortalID && abs(c.X-p.X) <= 2 {
				dest := e.Data.Maps[p.To]
				if c.Level < dest.MinLevel || c.ArenaTier < dest.ArenaRequired {
					return nil, fmt.Errorf("requires trainer level %d and arena tier %d", dest.MinLevel, dest.ArenaRequired)
				}
				c.MapID = p.To
				c.X = p.Spawn
				e.progress(c, "reach_map", p.To)
				return []Event{event("map_enter", dest.Name)}, nil
			}
		}
		return nil, fmt.Errorf("no nearby portal")
	case "world.encounter":
		if d.SpawnID != "" {
			for _, spawn := range e.Data.Maps[c.MapID].WildSpawns {
				if spawn.ID == d.SpawnID && abs(c.X-spawn.X) <= 1 && abs(c.Y-spawn.Y) <= 1 {
					return e.startBattle(c, false, spawn.SpeciesID)
				}
			}
			return nil, fmt.Errorf("wild beast is not nearby")
		}
		return e.startBattle(c, false)
	case "arena.challenge":
		if err := e.near(c, "arena"); err != nil {
			return nil, err
		}
		if c.Level < 10 {
			return nil, fmt.Errorf("Arena I requires trainer level 10")
		}
		return e.startBattle(c, true)
	case "npc.interact":
		n, ok := e.Data.NPCs[d.NPCID]
		if !ok || n.MapID != c.MapID || abs(c.X-n.X) > 3 {
			return nil, fmt.Errorf("NPC is not nearby")
		}
		e.progress(c, "talk_npc", n.ID)
		return []Event{event("npc_dialogue", n.Name+": A beast carries the story of every generation before it.")}, nil
	case "pet.appraise":
		if err := e.near(c, "appraise"); err != nil {
			return nil, err
		}
		p, err := findPet(c, d.PetID)
		if err != nil {
			return nil, err
		}
		if p.Appraised {
			return nil, fmt.Errorf("already appraised")
		}
		if c.Gold < e.Data.Rules.AppraisalCost {
			return nil, fmt.Errorf("insufficient gold")
		}
		c.Gold -= e.Data.Rules.AppraisalCost
		p.Appraised = true
		return []Event{event("pet_appraise", p.Name+" potential revealed"), event("currency_spend", "Appraisal fee paid")}, nil
	case "pet.activate":
		p, err := findPet(c, d.PetID)
		if err != nil {
			return nil, err
		}
		c.ActivePetID = p.ID
		return []Event{event("pet_activate", p.Name+" is following you")}, nil
	case "pet.learn":
		if err := e.near(c, "learn"); err != nil {
			return nil, err
		}
		p, err := findPet(c, d.PetID)
		if err != nil {
			return nil, err
		}
		skill, ok := e.Data.Skills[d.SkillID]
		if !ok || !has(e.Data.Species[p.SpeciesID].Skills, d.SkillID) || has(p.Skills, d.SkillID) {
			return nil, fmt.Errorf("skill unavailable or already learned")
		}
		if p.Level < skill.LearnLevel {
			return nil, fmt.Errorf("pet needs level %d", skill.LearnLevel)
		}
		if c.Gold < e.Data.Rules.LearnCost {
			return nil, fmt.Errorf("insufficient gold")
		}
		c.Gold -= e.Data.Rules.LearnCost
		p.Skills = append(p.Skills, d.SkillID)
		return []Event{event("pet_learn", p.Name+" learned "+skill.Name), event("currency_spend", "Skill tuition paid")}, nil
	case "pet.release":
		p, err := findPet(c, d.PetID)
		if err != nil {
			return nil, err
		}
		if p.ID == c.ActivePetID {
			return nil, fmt.Errorf("switch active pet before releasing")
		}
		p.Retired = true
		return []Event{event("pet_release", p.Name+" released; ancestry retained")}, nil
	case "pet.strengthen":
		if err := e.near(c, "strengthen"); err != nil {
			return nil, err
		}
		p, err := findPet(c, d.PetID)
		if err != nil {
			return nil, err
		}
		donor, err := findPet(c, d.DonorID)
		if err != nil {
			return nil, err
		}
		if p.ID == donor.ID || p.Star != donor.Star || donor.ID == c.ActivePetID || p.Strengthening >= 10 {
			return nil, fmt.Errorf("requires distinct inactive donor of same star; maximum 10 strengthens")
		}
		donor.Retired = true
		p.Strengthening++
		return []Event{event("pet_strengthen", p.Name+" inheritance foundation strengthened")}, nil
	case "breeding.synthesize":
		return e.breed(c, d)
	case "recipe.learn":
		if err := e.near(c, "recipe"); err != nil {
			return nil, err
		}
		if _, ok := e.Data.Recipes[d.RecipeID]; !ok || has(c.Recipes, d.RecipeID) {
			return nil, fmt.Errorf("recipe unavailable or already learned")
		}
		if c.Gold < 30 {
			return nil, fmt.Errorf("recipe study costs 30 gold")
		}
		c.Gold -= 30
		c.Recipes = append(c.Recipes, d.RecipeID)
		return []Event{event("recipe_learn", "Recipe permanently learned"), event("currency_spend", "Recipe study fee paid")}, nil
	case "pet.heal":
		if err := e.near(c, "heal"); err != nil {
			return nil, err
		}
		if c.Gold < e.Data.Rules.HealCost {
			return nil, fmt.Errorf("insufficient gold")
		}
		c.Gold -= e.Data.Rules.HealCost
		for _, p := range c.Pets {
			if !p.Retired {
				p.HP = p.MaxHP
				p.MP = p.MaxMP
			}
		}
		return []Event{event("pet_heal", "Your beasts are rested")}, nil
	case "shop.buy":
		if err := e.near(c, "shop"); err != nil {
			return nil, err
		}
		it, ok := e.Data.Items[d.ItemID]
		if !ok || d.Quantity < 1 || d.Quantity > 99 {
			return nil, fmt.Errorf("invalid item or quantity")
		}
		cost := it.Price * d.Quantity
		if c.Gold < cost {
			return nil, fmt.Errorf("insufficient gold")
		}
		c.Gold -= cost
		c.Inventory[it.ID] += d.Quantity
		return []Event{event("item_gain", fmt.Sprintf("%s ×%d", it.Name, d.Quantity)), event("currency_spend", fmt.Sprintf("Spent %d gold", cost))}, nil
	case "quest.accept":
		if err := e.near(c, "quest"); err != nil {
			return nil, err
		}
		q, ok := e.Data.Quests[d.QuestID]
		if !ok {
			return nil, fmt.Errorf("unknown quest")
		}
		if _, ok = c.Quests[q.ID]; ok {
			return nil, fmt.Errorf("quest already accepted")
		}
		c.Quests[q.ID] = &QuestState{}
		if q.Kind == "reach_map" && q.Target == c.MapID {
			c.Quests[q.ID].Progress = 1
		}
		return []Event{event("quest_accept", q.Name)}, nil
	case "quest.claim":
		if err := e.near(c, "quest"); err != nil {
			return nil, err
		}
		q, ok := e.Data.Quests[d.QuestID]
		state := c.Quests[d.QuestID]
		if !ok || state == nil || state.Claimed || state.Progress < q.Count {
			return nil, fmt.Errorf("quest is not ready for reward")
		}
		state.Claimed = true
		c.Gold += q.Gold
		e.trainerXP(c, q.XP)
		for id, n := range q.Items {
			c.Inventory[id] += n
		}
		if q.Recipe != "" && !has(c.Recipes, q.Recipe) {
			c.Recipes = append(c.Recipes, q.Recipe)
		}
		return []Event{event("quest_complete", q.Name), event("currency_gain", fmt.Sprintf("Received %d gold", q.Gold)), event("item_gain", "Quest supplies received")}, nil
	}
	return nil, fmt.Errorf("unknown operation %q", op)
}
