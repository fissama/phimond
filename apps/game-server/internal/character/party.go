package character

import (
	"fmt"
	"slices"
)

// MaxParty là số linh thú tối đa trong đội hình (con chính + tối đa 2 con phụ).
const MaxParty = 3

// EffectiveParty trả đội hình hợp lệ: bỏ id không còn/đã thả, bỏ trùng, đưa con chính (ActivePetID) lên đầu.
// Tài khoản chưa có Party (dữ liệu cũ) được dựng từ con chính rồi các linh thú còn lại theo thứ tự sở hữu.
func (c *Character) EffectiveParty() []string {
	alive := map[string]bool{}
	var order []string
	for _, p := range c.Pets {
		if !p.Retired {
			alive[p.ID] = true
			order = append(order, p.ID)
		}
	}
	var out []string
	add := func(id string) {
		if alive[id] && !slices.Contains(out, id) && len(out) < MaxParty {
			out = append(out, id)
		}
	}
	add(c.ActivePetID)
	if len(c.Party) == 0 {
		for _, id := range order {
			add(id)
		}
		return out
	}
	for _, id := range c.Party {
		add(id)
	}
	return out
}

// setMainPet đưa một linh thú lên làm con chính, giữ các con phụ cũ theo thứ tự.
func (c *Character) setMainPet(id string) {
	rest := slices.DeleteFunc(c.EffectiveParty(), func(x string) bool { return x == id })
	party := append([]string{id}, rest...)
	if len(party) > MaxParty {
		party = party[:MaxParty]
	}
	c.Party = party
	c.ActivePetID = id
}

// setParty thay đội hình: id phải là linh thú của mình, chưa thả, không trùng, 1..MaxParty phần tử.
// Phần tử đầu thành con chính.
func (e *Engine) setParty(c *Character, ids []string) error {
	if len(ids) == 0 || len(ids) > MaxParty {
		return fmt.Errorf("party must have 1-%d pets", MaxParty)
	}
	seen := map[string]bool{}
	for _, id := range ids {
		p, err := findPet(c, id)
		if err != nil {
			return err
		}
		if p.Retired {
			return fmt.Errorf("pet is retired")
		}
		if seen[id] {
			return fmt.Errorf("duplicate pet in party")
		}
		seen[id] = true
	}
	c.Party = slices.Clone(ids)
	c.ActivePetID = ids[0]
	return nil
}
