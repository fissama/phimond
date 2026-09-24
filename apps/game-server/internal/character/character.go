package character

import (
	"fmt"
	"phimond/server/internal/battle"
	"phimond/server/internal/content"
	"phimond/server/internal/pet"
	"sort"
)

// StatKeys is the canonical stat order used for pet quality and growth
// rolls. Moved verbatim from internal/game/model.go.
var StatKeys = []string{"strength", "agility", "stamina", "intelligence", "spirit", "defense", "critical"}

// RNG is the per-character, deterministic PRNG used for combat rolls,
// breeding, capture and appraisal. Moved verbatim from internal/game/model.go.
type RNG struct {
	State uint64 `json:"state"`
}

func (r *RNG) Next() uint64 {
	if r.State == 0 {
		r.State = 0x9e3779b97f4a7c15
	}
	x := r.State
	x ^= x << 13
	x ^= x >> 7
	x ^= x << 17
	r.State = x
	return x
}
func (r *RNG) Int(n int) int {
	if n <= 0 {
		return 0
	}
	return int(r.Next() % uint64(n))
}
func (r *RNG) Float() float64 { return float64(r.Next()>>11) / (1 << 53) }

// QuestState is the per-character progress tracker for a quest id. Moved
// verbatim from internal/game/model.go.
type QuestState struct {
	Progress int  `json:"progress"`
	Claimed  bool `json:"claimed"`
}

// Event is the wire-format description of a domain outcome emitted by Apply.
// Moved verbatim from internal/game/model.go.
type Event struct {
	Seq      int    `json:"seq"`
	Type     string `json:"type"`
	ActorID  string `json:"actor_id,omitempty"`
	TargetID string `json:"target_id,omitempty"`
	Amount   int    `json:"amount,omitempty"`
	Message  string `json:"message"`
}

// Character is the top-level aggregate that the transport persists and the
// Engine mutates. Field types reference the pet/ and battle/ packages per
// the §3 split. Moved verbatim from internal/game/model.go with type
// renames to the new packages.
type Character struct {
	ID          string                 `json:"id"`
	Name        string                 `json:"name"`
	Level       int                    `json:"level"`
	XP          int                    `json:"xp"`
	Gold        int                    `json:"gold"`
	Crystals    int                    `json:"crystals"`
	MapID       string                 `json:"map_id"`
	X           int                    `json:"x"`
	Y           int                    `json:"y"`
	ActivePetID string                 `json:"active_pet_id"`
	Revision    int                    `json:"revision"`
	Pets        []*pet.Pet             `json:"pets"`
	Inventory   map[string]int         `json:"inventory"`
	Recipes     []string               `json:"recipes"`
	Quests      map[string]*QuestState `json:"quests"`
	ArenaTier   int                    `json:"arena_tier"`
	Battle      *Battle                `json:"battle"`
	History     []*Battle              `json:"battle_history,omitempty"`
	RNG         RNG                    `json:"rng"`
	Counter     int                    `json:"counter"`
	Events      []Event                `json:"last_events,omitempty"`
}

// Battle is the live battle aggregate. The Commands and Events slices still
// reference the local Intent/Event types so the live aggregate can be
// decoded without crossing the battle/ package boundary. Moved verbatim from
// internal/game/battle.go with the Units slice targeting the battle/ Unit.
type Battle struct {
	ID       string         `json:"id"`
	Turn     int            `json:"turn"`
	Phase    string         `json:"phase"`
	Result   string         `json:"result"`
	Units    []*battle.Unit `json:"units"`
	Seed     uint64         `json:"seed"`
	RNG      RNG            `json:"rng"`
	Arena    bool           `json:"arena"`
	Commands []Intent       `json:"commands"`
	Events   []Event        `json:"events"`
	Sequence int            `json:"sequence"`
}

// Intent is the request payload parsed from a single WebSocket envelope.
// Moved verbatim from internal/game/service.go.
type Intent struct {
	Direction string `json:"direction"`
	SpawnID   string `json:"spawn_id,omitempty"`
	PortalID  string `json:"portal_id"`
	NPCID     string `json:"npc_id"`
	PetID     string `json:"pet_id"`
	DonorID   string `json:"donor_id"`
	SkillID   string `json:"skill_id"`
	ParentA   string `json:"parent_a"`
	ParentB   string `json:"parent_b"`
	RecipeID  string `json:"recipe_id"`
	Blessing  int    `json:"blessing"`
	QuestID   string `json:"quest_id"`
	ItemID    string `json:"item_id"`
	Quantity  int    `json:"quantity"`
	BattleID  string `json:"battle_id"`
	Turn      int    `json:"turn"`
	Choice    string `json:"choice"`
}

// Engine is the orchestrator over the content catalog. Methods on *Engine
// live alongside the dispatcher in this package because they all read
// content through the shared e.Data pointer; placing them in their domain
// packages would create an import cycle through the methods the Apply
// dispatcher must call. The structural split (data types in pet/ and
// battle/) preserves the §3 layout while keeping the call graph acyclic.
type Engine struct{ Data *content.Catalog }

// id allocates a monotonic per-character id of the given kind. Moved
// verbatim from internal/game/model.go.
func (c *Character) id(kind string) string {
	c.Counter++
	return fmt.Sprintf("%s_%s_%d", c.ID, kind, c.Counter)
}

// findPet returns the pet with the given id that has not been retired.
// Moved verbatim from internal/game/model.go.
func findPet(c *Character, id string) (*pet.Pet, error) {
	for _, p := range c.Pets {
		if p.ID == id && !p.Retired {
			return p, nil
		}
	}
	return nil, fmt.Errorf("pet is not owned or is retired")
}

// LineageNode is the read-only tree shape returned by Engine.Lineage.
// Moved verbatim from internal/game/model.go.
type LineageNode struct {
	Pet     *pet.Pet       `json:"pet"`
	Parents []*LineageNode `json:"parents"`
}

// has reports whether s appears in list. Moved verbatim from
// internal/game/model.go.
func has(list []string, s string) bool {
	for _, v := range list {
		if v == s {
			return true
		}
	}
	return false
}

// sortedKeys returns the keys of m in lexicographic order. Moved verbatim
// from internal/game/model.go.
func sortedKeys[V any](m map[string]V) []string {
	keys := make([]string, 0, len(m))
	for k := range m {
		keys = append(keys, k)
	}
	sort.Strings(keys)
	return keys
}

// event constructs a wire-format event with the given kind/message.
// Moved verbatim from internal/game/model.go.
func event(kind, message string) Event { return Event{Type: kind, Message: message} }
