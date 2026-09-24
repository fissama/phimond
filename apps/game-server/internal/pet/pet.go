package pet

// Pet is the per-character instance of a species, including individual
// variance, lineage, learned skills and tracked combat resources. The type
// is moved verbatim from the legacy internal/game package; all creators,
// recalculation, and level-up methods continue to live in internal/character
// to avoid import cycles through Engine.
type Pet struct {
	ID                string         `json:"id"`
	SpeciesID         string         `json:"species_id"`
	Name              string         `json:"name"`
	Level             int            `json:"level"`
	XP                int            `json:"xp"`
	Gender            string         `json:"gender"`
	Star              int            `json:"star"`
	Generation        int            `json:"generation"`
	Refinement        int            `json:"refinement"`
	Appraised         bool           `json:"appraised"`
	Retired           bool           `json:"retired"`
	Quality           map[string]int `json:"quality,omitempty"`
	Growth            map[string]int `json:"growth,omitempty"`
	Resistances       map[string]int `json:"resistances,omitempty"`
	StatusResistances map[string]int `json:"status_resistances,omitempty"`
	Skills            []string       `json:"skills"`
	Parents           []string       `json:"parents"`
	Strengthening     int            `json:"strengthening"`
	Blessing          int            `json:"blessing"`
	HP                int            `json:"hp"`
	MP                int            `json:"mp"`
	MaxHP             int            `json:"max_hp"`
	MaxMP             int            `json:"max_mp"`
	Attack            int            `json:"attack"`
	Magic             int            `json:"magic"`
	Defense           int            `json:"defense"`
	Speed             int            `json:"speed"`
	Critical          float64        `json:"critical"`
}