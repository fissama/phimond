package battle

import "phimond/server/internal/pet"

// ActiveStatus is a per-unit status ailment (poison, sleep, …) tracked by the
// battle state machine. The type is moved verbatim from internal/game.
type ActiveStatus struct {
	ID          string `json:"id"`
	Remaining   int    `json:"remaining"`
	AppliedTurn int    `json:"applied_turn"`
}

// Buff is a temporary stat multiplier on a Unit. The type is moved verbatim
// from internal/game.
type Buff struct {
	Stat        string  `json:"stat"`
	Multiplier  float64 `json:"multiplier"`
	Remaining   int     `json:"remaining"`
	AppliedTurn int     `json:"applied_turn"`
}

// Unit represents one combatant in a Battle. The Pet pointer keeps the
// source-of-truth combat stats reachable for damage formulae. The type is
// moved verbatim from internal/game.
type Unit struct {
	ID        string         `json:"id"`
	Name      string         `json:"name"`
	Side      string         `json:"side"`
	SpeciesID string         `json:"species_id"`
	Level     int            `json:"level"`
	HP        int            `json:"hp"`
	MaxHP     int            `json:"max_hp"`
	MP        int            `json:"mp"`
	MaxMP     int            `json:"max_mp"`
	Statuses  []ActiveStatus `json:"statuses"`
	Buffs     []Buff         `json:"buffs"`
	Pet       *pet.Pet       `json:"pet"`
	Defending bool           `json:"defending"`
	// Power nhân sát thương gây ra (0 = 1). Quái theo đàn yếu hơn quái lẻ (rules.pack_scale).
	Power float64 `json:"power,omitempty"`
}
