package character

import (
	"fmt"
	"math"
)

// abs returns the absolute value of v. Moved verbatim from
// internal/game/service.go.
func abs(v int) int {
	if v < 0 {
		return -v
	}
	return v
}

// clamp constrains x to the inclusive range [a, b]. Moved verbatim from
// internal/game/service.go.
func clamp(x, a, b float64) float64 { return math.Max(a, math.Min(b, x)) }

// near reports whether the character is adjacent (within three tiles) to
// an NPC with the given role on the current map. Moved verbatim from
// internal/game/service.go.
func (e *Engine) near(c *Character, role string) error {
	for _, n := range e.Data.NPCs {
		if n.MapID == c.MapID && abs(n.X-c.X) <= 3 && has(n.Roles, role) {
			return nil
		}
	}
	return fmt.Errorf("move close to an NPC offering %s", role)
}

// progress credits quest counters when a tracked kind/target event fires
// for the character. Moved verbatim from internal/game/service.go.
func (e *Engine) progress(c *Character, kind, target string) {
	for id, q := range e.Data.Quests {
		if state := c.Quests[id]; state != nil && !state.Claimed && q.Kind == kind && (q.Target == "" || q.Target == target) {
			state.Progress = min(q.Count, state.Progress+1)
		}
	}
}

// trainerXP credits the trainer level, applying level-ups against the
// catalog rules. Moved verbatim from internal/game/service.go.
func (e *Engine) trainerXP(c *Character, xp int) {
	c.XP += xp
	for c.Level < e.Data.Rules.MaxLevel && c.XP >= c.Level*e.Data.Rules.XPPerLevel {
		c.XP -= c.Level * e.Data.Rules.XPPerLevel
		c.Level++
	}
}