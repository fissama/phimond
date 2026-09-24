package transport

import (
	"encoding/json"
	"phimond/server/internal/character"
)

// Projection belongs to this committed response, never to a later read or
// receipt retry. Snapshot remains the only sanitizer for render units.
func (s *Server) stateEnvelope(m envelope, raw json.RawMessage, fresh bool) (map[string]any, error) {
	var c character.Character
	if err := json.Unmarshal(raw, &c); err != nil {
		return nil, err
	}
	data := map[string]any{"character": s.Game.Snapshot(&c), "events": []character.Event{}}
	if fresh {
		data["events"] = c.Events
		if c.Battle != nil {
			data["presentation"] = map[string]any{"battle_id": c.Battle.ID}
		} else if m.Op == "battle.action" {
			var intent character.Intent
			if err := json.Unmarshal(m.Data, &intent); err != nil {
				return nil, err
			}
			for _, b := range c.History {
				if b.ID != intent.BattleID {
					continue
				}
				copy := c
				copy.Battle = b
				data["presentation"] = map[string]any{"battle_id": b.ID, "completed_battle": s.Game.Snapshot(&copy)["battle"]}
				break
			}
		}
	}
	return map[string]any{"op": "state", "request_id": m.RequestID, "sequence": c.Revision, "data": data}, nil
}
