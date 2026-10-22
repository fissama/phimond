package character

import (
	"encoding/json"
	"phimond/server/internal/content"
	"phimond/server/internal/pet"
	"time"
)

// NewEngine builds an Engine backed by the supplied catalog. Moved verbatim
// from internal/game/model.go.
func NewEngine(c *content.Catalog) *Engine { return &Engine{Data: c, Now: time.Now} }

// StartMap là nơi người chơi mới xuất hiện (P01 §7 câu 1): Triệu Linh Điện, chưa có pet.
const StartMap = "summoning_hall_main_hall"

// NewCharacter tạo nhân vật mới ở Triệu Linh Điện, chưa có pet; người chơi chọn bệ đá để nhận
// pet khởi đầu (intent starter.choose). Túi đồ khởi đầu giữ như bản cũ.
func (e *Engine) NewCharacter(id, name string, seed uint64) *Character {
	m := e.Data.Maps[StartMap]
	c := &Character{ID: id, Name: name, Level: 1, Gold: 100, MapID: StartMap, X: m.SpawnDefault.X, Y: m.SpawnDefault.Y, Inventory: map[string]int{"capture_seal": 10, "potion": 5, "ether": 3, "synthesis_soul": 2}, Quests: map[string]*QuestState{}, Recipes: []string{}, Pets: []*pet.Pet{}, RNG: RNG{seed}, Visited: []string{StartMap}}
	return c
}

// GiveStarter thêm pet khởi đầu đã giám định và đặt làm pet chính (dùng cho bệ đá và test).
func (e *Engine) GiveStarter(c *Character, species string, level int) *pet.Pet {
	p := e.NewPet(c, species, level)
	p.Appraised = true
	// Linh thú khởi đầu biết sẵn đòn hệ đầu tiên của loài để trận đầu có kỹ năng dùng được.
	for _, id := range e.Data.Species[species].Skills {
		if s, ok := e.Data.Skills[id]; ok && id != "attack" && s.Target == "enemy" && (s.Kind == "physical" || s.Kind == "magic") {
			p.Skills = append(p.Skills, id)
			break
		}
	}
	c.Pets = append(c.Pets, p)
	c.ActivePetID = p.ID
	return p
}

// Snapshot builds the public, deterministic view of the character by
// stripping the RNG, history, last events and un-appraised pet internals.
// Moved verbatim from internal/game/model.go.
func (e *Engine) Snapshot(c *Character) map[string]any {
	now := e.nowMS()
	b, _ := json.Marshal(c)
	var out map[string]any
	json.Unmarshal(b, &out)
	delete(out, "rng")
	delete(out, "counter")
	delete(out, "battle_history")
	delete(out, "last_events")
	// Chỉ công bố điểm quái còn đang ẩn, kèm giờ server để client tự tính thời gian còn lại.
	hidden := map[string]int64{}
	for id, until := range c.SpawnHidden {
		if until > now {
			hidden[id] = until
		}
	}
	out["spawn_hidden"] = hidden
	out["server_time_ms"] = now
	if out["visited"] == nil {
		out["visited"] = []string{}
	}
	for _, p := range out["pets"].([]any) {
		m := p.(map[string]any)
		if !m["appraised"].(bool) {
			for _, k := range []string{"quality", "growth", "resistances", "status_resistances"} {
				delete(m, k)
			}
		}
	}
	if b, ok := out["battle"].(map[string]any); ok {
		for _, k := range []string{"rng", "seed", "commands", "events", "wild"} {
			delete(b, k)
		}
		for _, u := range b["units"].([]any) {
			m := u.(map[string]any)
			delete(m, "pet")
		}
	}
	return out
}

// Lineage returns the ancestry chain rooted at the given pet id, depth
// limited to 32 to bound cycles. Moved verbatim from internal/game/model.go.
func (e *Engine) Lineage(c *Character, id string) *LineageNode {
	seen := map[string]bool{}
	var visit func(string, int) *LineageNode
	visit = func(id string, depth int) *LineageNode {
		if seen[id] || depth > 32 {
			return nil
		}
		seen[id] = true
		for _, p := range c.Pets {
			if p.ID == id {
				copy := *p
				if !p.Appraised {
					copy.Quality = nil
					copy.Growth = nil
					copy.Resistances = nil
					copy.StatusResistances = nil
				}
				n := &LineageNode{Pet: &copy, Parents: []*LineageNode{}}
				for _, pid := range p.Parents {
					if parent := visit(pid, depth+1); parent != nil {
						n.Parents = append(n.Parents, parent)
					}
				}
				delete(seen, id)
				return n
			}
		}
		return nil
	}
	return visit(id, 0)
}

// PublicHistory returns the public view of every past battle, including the
// skill cast events but excluding the deterministic seed and any hidden
// pet potential. Moved verbatim from internal/game/model.go.
func (e *Engine) PublicHistory(c *Character) []map[string]any {
	out := []map[string]any{}
	for _, b := range c.History {
		copy := *c
		copy.Battle = b
		snapshot := e.Snapshot(&copy)
		h := snapshot["battle"].(map[string]any)
		h["events"] = b.Events
		out = append(out, h)
	}
	return out
}
