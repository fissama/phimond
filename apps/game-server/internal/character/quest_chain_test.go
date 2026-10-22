package character

import (
	"encoding/json"
	"testing"
)

// Chuỗi nhiệm vụ Đợt A: phải xong nhiệm vụ trước và đứng gần người giao mới nhận được.
func TestQuestChainRequiresPreviousAndGiver(t *testing.T) {
	e := engine(t)
	c := veteran(e, "q", "Q", 1)
	lio := e.Data.NPCs["forest_guide"]
	c.X, c.Y = lio.X+1, lio.Y
	if _, err := e.Apply(c, "quest.accept", json.RawMessage(`{"quest_id":"first_capture"}`)); err == nil {
		t.Fatal("first_capture must require first_battle")
	}
	command(t, e, c, "quest.accept", map[string]any{"quest_id": "first_battle"})
	c.Quests["first_battle"].Progress, c.Quests["first_battle"].Claimed = 1, true
	command(t, e, c, "quest.accept", map[string]any{"quest_id": "first_capture"})
	c.Quests["first_capture"].Progress, c.Quests["first_capture"].Claimed = 1, true
	c.Quests["meet_rowan"] = &QuestState{Progress: 1, Claimed: true}
	c.Quests["field_training"] = &QuestState{Progress: 3, Claimed: true}
	c.Quests["first_steps"] = &QuestState{Progress: 1, Claimed: true}
	c.Quests["elder_tamo"] = &QuestState{Progress: 1, Claimed: true}
	if _, err := e.Apply(c, "quest.accept", json.RawMessage(`{"quest_id":"wolf_hunt"}`)); err == nil {
		t.Fatal("wolf_hunt must be accepted at its giver in Rừng Sâu")
	}
}

func TestItemUseOutsideBattle(t *testing.T) {
	e := engine(t)
	c := veteran(e, "i", "I", 1)
	p, _ := findPet(c, c.ActivePetID)
	p.HP = 1
	n := c.Inventory["potion"]
	command(t, e, c, "item.use", map[string]any{"item_id": "potion"})
	p, _ = findPet(c, c.ActivePetID)
	if p.HP <= 1 || c.Inventory["potion"] != n-1 {
		t.Fatalf("potion must heal: hp %d", p.HP)
	}
	p.HP = p.MaxHP
	if _, err := e.Apply(c, "item.use", json.RawMessage(`{"item_id":"potion"}`)); err == nil {
		t.Fatal("full HP must refuse")
	}
}
