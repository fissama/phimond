package character

import (
	"encoding/json"
	"strings"
	"testing"
	"time"
)

func apply(e *Engine, c *Character, op string, d map[string]any) error {
	b, _ := json.Marshal(d)
	_, err := e.Apply(c, op, b)
	return err
}

func mustFail(t *testing.T, e *Engine, c *Character, op string, d map[string]any, want string) {
	t.Helper()
	before, _ := json.Marshal(c)
	err := apply(e, c, op, d)
	if err == nil || !strings.Contains(err.Error(), want) {
		t.Fatalf("%s %v: lỗi = %v, cần chứa %q", op, d, err, want)
	}
	after, _ := json.Marshal(c)
	if string(before) != string(after) {
		t.Fatalf("%s bị từ chối nhưng vẫn đổi trạng thái", op)
	}
}

func TestNewPlayerStartsInHallAndChoosesStarter(t *testing.T) {
	e := engine(t)
	c := e.NewCharacter("n", "Mới", 5)
	hall := e.Data.Maps[StartMap]
	if c.MapID != StartMap || len(c.Pets) != 0 || c.X != hall.SpawnDefault.X || c.Y != hall.SpawnDefault.Y {
		t.Fatal("người chơi mới phải ở Triệu Linh Điện, chưa có pet")
	}
	// Cửa ra cần có pet.
	c.X, c.Y = 9, 9
	mustFail(t, e, c, "world.portal", map[string]any{"portal_id": "hall_exit"}, "chọn linh thú")
	// Bệ ở xa thì không chọn được.
	c.X, c.Y = 9, 7
	mustFail(t, e, c, "starter.choose", map[string]any{"pedestal": 1}, "gần bệ")
	mustFail(t, e, c, "starter.choose", map[string]any{"pedestal": 7}, "Không có bệ")
	// Đứng chéo kề bệ 1 (9,3).
	c.X, c.Y = 10, 4
	ev := command(t, e, c, "starter.choose", map[string]any{"pedestal": 1})
	if len(c.Pets) != 1 || c.Pets[0].SpeciesID != "spider" || c.ActivePetID != c.Pets[0].ID || !c.Pets[0].Appraised {
		t.Fatal("không nhận đúng pet khởi đầu")
	}
	if c.MapID != "emerald_forest_main_woods" || c.X != 3 || c.Y != 6 || !has(c.Visited, c.MapID) {
		t.Fatalf("phải dịch chuyển một chiều tới Bìa Rừng, đang ở %s (%d,%d)", c.MapID, c.X, c.Y)
	}
	if ev[0].Type != "starter_chosen" || ev[len(ev)-1].Type != "map_enter" {
		t.Fatal("thiếu sự kiện chọn pet / vào map")
	}
	mustFail(t, e, c, "starter.choose", map[string]any{"pedestal": 0}, "đã có")
}

func TestMoveBlockedByCollision(t *testing.T) {
	e := engine(t)
	c := e.NewCharacter("m", "M", 1)
	c.X, c.Y = 2, 3 // sát tường trái hành lang
	mustFail(t, e, c, "world.move", map[string]any{"direction": "left"}, "Không đi được")
	rev := c.Revision
	command(t, e, c, "world.move", map[string]any{"direction": "right"})
	if c.X != 3 || c.Y != 3 || c.Revision != rev+1 {
		t.Fatal("bước hợp lệ phải đi một ô")
	}
	c.X, c.Y = 4, 3 // kề bệ 0 (5,3): bệ chặn ô
	mustFail(t, e, c, "world.move", map[string]any{"direction": "right"}, "Không đi được")
}

func TestPortalNeedsRectAndRedirectsAfterFirstVisit(t *testing.T) {
	e := engine(t)
	c := veteran(e, "p", "P", 1)
	c.MapID, c.X, c.Y = "emerald_forest_deep_woods", 35, 5 // ngay ngoài vùng cổng (37, 4..6)
	mustFail(t, e, c, "world.portal", map[string]any{"portal_id": "to_city"}, "Không có cổng")
	c.X = 37
	command(t, e, c, "world.portal", map[string]any{"portal_id": "to_city"})
	if c.MapID != "city_palace_gate" || c.X != 2 || c.Y != 6 {
		t.Fatalf("lần đầu phải tới Hoàng Môn, đang ở %s", c.MapID)
	}
	c.MapID, c.X, c.Y = "emerald_forest_deep_woods", 37, 4
	command(t, e, c, "world.portal", map[string]any{"portal_id": "to_city"})
	if c.MapID != "city_square" || c.X != 2 || c.Y != 6 {
		t.Fatalf("lần sau phải tới Quảng Trường, đang ở %s", c.MapID)
	}
}

func TestLockedPortalExplainsNotOpen(t *testing.T) {
	e := engine(t)
	c := veteran(e, "l", "L", 1)
	c.MapID, c.X, c.Y = "city_square", 30, 5 // kề cổng sang Thương Phố (31, 4..6)
	mustFail(t, e, c, "world.portal", map[string]any{"portal_id": "square_to_market"}, "chưa mở")
	c.X, c.Y = 10, 8
	mustFail(t, e, c, "world.portal", map[string]any{"portal_id": "square_to_market"}, "Không có cổng")
}

func TestNPCRangeUsesBothAxes(t *testing.T) {
	e := engine(t)
	c := veteran(e, "n", "N", 1)
	g := e.Data.NPCs["forest_guide"] // (6, 4)
	c.X, c.Y = g.X, g.Y+2            // cùng cột, cách 2 hàng: trục X trùng nhưng phải bị từ chối
	mustFail(t, e, c, "npc.interact", map[string]any{"npc_id": "forest_guide"}, "gần NPC")
	c.X, c.Y = g.X+1, g.Y+1
	ev := command(t, e, c, "npc.interact", map[string]any{"npc_id": "forest_guide"})
	if ev[0].ActorID != "forest_guide" || !strings.Contains(ev[0].Message, "Kiểm Lâm Lio") {
		t.Fatal("hội thoại thiếu NPC/tên", ev[0])
	}
	// Dịch vụ cũng xét hai trục: hồi phục cần đứng kề NPC có vai heal.
	c.X, c.Y = g.X, g.Y+2
	mustFail(t, e, c, "pet.heal", nil, "gần NPC")
	c.Y = g.Y + 1
	command(t, e, c, "pet.heal", nil)
}

func TestPillarTravel(t *testing.T) {
	e := engine(t)
	c := veteran(e, "t", "T", 1)
	c.MapID, c.X, c.Y = "city_square", 16, 6
	mustFail(t, e, c, "pillar.travel", map[string]any{"map_id": "emerald_forest_main_woods"}, "gần trụ")
	c.X, c.Y = 5, 8 // kề trụ (6,8)
	mustFail(t, e, c, "pillar.travel", map[string]any{"map_id": "city_farm"}, "chưa mở")
	mustFail(t, e, c, "pillar.travel", map[string]any{"map_id": "nowhere"}, "Không có điểm đến")
	command(t, e, c, "pillar.travel", map[string]any{"map_id": "emerald_forest_main_woods"})
	if c.MapID != "emerald_forest_main_woods" || c.X != 3 || c.Y != 6 {
		t.Fatal("trụ phải đưa về Bìa Rừng")
	}
}

func TestSpawnCooldownAfterBattle(t *testing.T) {
	e := engine(t)
	now := time.UnixMilli(1_000_000)
	e.Now = func() time.Time { return now }
	c := veteran(e, "s", "S", 3)
	s := e.Data.Maps[c.MapID].WildSpawns[0]
	c.X, c.Y = s.X, s.Y
	command(t, e, c, "world.encounter", map[string]any{"spawn_id": s.ID})
	command(t, e, c, "battle.action", map[string]any{"battle_id": c.Battle.ID, "turn": 1, "choice": "flee"})
	if c.Battle != nil || c.SpawnHidden[s.ID] != now.UnixMilli()+int64(s.RespawnS)*1000 {
		t.Fatal("chạy trốn cũng phải làm quái ẩn tới khi hồi")
	}
	snap := e.Snapshot(c)
	if h := snap["spawn_hidden"].(map[string]int64); h[s.ID] == 0 || snap["server_time_ms"].(int64) != now.UnixMilli() {
		t.Fatal("snapshot phải công bố quái đang ẩn và giờ server")
	}
	mustFail(t, e, c, "world.encounter", map[string]any{"spawn_id": s.ID}, "rời đi")
	now = now.Add(time.Duration(s.RespawnS) * time.Second)
	command(t, e, c, "world.encounter", map[string]any{"spawn_id": s.ID})
	if c.Battle == nil {
		t.Fatal("quái phải hiện lại sau thời gian hồi")
	}
}

func TestLossRespawnsAndHeals(t *testing.T) {
	e := engine(t)
	c := veteran(e, "d", "D", 3)
	c.MapID = "emerald_forest_deep_woods"
	s := e.Data.Maps[c.MapID].WildSpawns[0]
	c.X, c.Y = s.X, s.Y
	command(t, e, c, "world.encounter", map[string]any{"spawn_id": s.ID})
	c.Battle.Units[0].HP = 1
	c.Battle.Units[1].Pet.Speed = 999
	for i := 0; c.Battle != nil && i < 50; i++ {
		command(t, e, c, "battle.action", map[string]any{"battle_id": c.Battle.ID, "turn": c.Battle.Turn, "choice": "defend"})
	}
	main := e.Data.Maps["emerald_forest_main_woods"]
	if c.MapID != main.ID || c.X != main.SpawnDefault.X || c.Y != main.SpawnDefault.Y {
		t.Fatalf("thua phải về điểm hồi sinh Bìa Rừng, đang ở %s (%d,%d)", c.MapID, c.X, c.Y)
	}
	if c.Pets[0].HP != c.Pets[0].MaxHP {
		t.Fatal("thua phải hồi phục pet")
	}
}

func TestUnknownLocationIsNormalized(t *testing.T) {
	e := engine(t)
	c := veteran(e, "o", "O", 1)
	c.MapID, c.X, c.Y = "severa", 16, 12 // map cũ đã gỡ
	command(t, e, c, "character.get", nil)
	command(t, e, c, "world.move", map[string]any{"direction": "down"})
	if c.MapID != "city_square" {
		t.Fatal("map cũ phải được đưa về Quảng Trường", c.MapID)
	}
}
