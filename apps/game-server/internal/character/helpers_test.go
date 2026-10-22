package character

import "phimond/server/internal/content"

// veteran tạo nhân vật đã có pet khởi đầu (snail cấp 3) và đứng ở Bìa Rừng — tương đương nhân vật
// mới trước P01, để các test luật chiến đấu/nuôi pet không phụ thuộc luồng chọn bệ đá.
func veteran(e *Engine, id, name string, seed uint64) *Character {
	c := e.NewCharacter(id, name, seed)
	e.GiveStarter(c, "snail", 3)
	m := e.Data.Maps["emerald_forest_main_woods"]
	c.MapID, c.X, c.Y = m.ID, m.SpawnDefault.X, m.SpawnDefault.Y
	return c
}

// atService đặt một NPC thử nghiệm có mọi vai dịch vụ ngay cạnh nhân vật (Điền Trang chưa có ở 1.0.0,
// nhưng luật nuôi pet/tổng hợp vẫn phải được kiểm).
func atService(e *Engine, c *Character) {
	e.Data.NPCs["test_keeper"] = content.NPC{ID: "test_keeper", Name: "Test Keeper", MapID: c.MapID, X: c.X + 1, Y: c.Y,
		Roles: []string{"appraise", "breed", "strengthen", "recipe", "heal", "quest", "shop", "learn"}}
}
