package character

import (
	"fmt"
	"phimond/server/internal/content"
	"phimond/server/internal/world"
)

// Tầm tương tác hai trục (P01-R04, ADR-P01-01): đứng kề NPC/bệ/trụ, kể cả chéo.
const interactRange = 1

// Thông điệp từ chối dùng tiếng Việt vì client hiển thị nguyên văn.
var (
	errBlocked      = fmt.Errorf("Không đi được vào đó")
	errNotOpen      = fmt.Errorf("Khu vực này chưa mở")
	errNoPortal     = fmt.Errorf("Không có cổng ở gần")
	errNotNearNPC   = fmt.Errorf("Hãy đến gần NPC hơn")
	errNeedStarter  = fmt.Errorf("Hãy chọn linh thú khởi đầu trước")
	errHasStarter   = fmt.Errorf("Bạn đã có linh thú khởi đầu")
	errBeastHidden  = fmt.Errorf("Thú hoang đã rời đi, chờ một lát")
	errBeastFar     = fmt.Errorf("Thú hoang không ở gần")
	errUnknownPlace = fmt.Errorf("Không có điểm đến này")
)

// placeAt đưa nhân vật tới map/ô mới và ghi nhận đã ghé thăm.
func (e *Engine) placeAt(c *Character, mapID string, p world.Point) []Event {
	c.MapID, c.X, c.Y = mapID, p.X, p.Y
	if !has(c.Visited, mapID) {
		c.Visited = append(c.Visited, mapID)
	}
	e.progress(c, "reach_map", mapID)
	return []Event{event("map_enter", e.Data.Maps[mapID].Name)}
}

// normalizeLocation đưa nhân vật về chỗ hợp lệ nếu map/ô cũ không còn (vd dữ liệu trước P01).
// NormalizeLocation là normalizeLocation cho tầng transport: sửa vị trí ngay khi nạp nhân vật để
// snapshot đầu tiên gửi client đã hợp lệ. Trả true nếu có thay đổi.
func (e *Engine) NormalizeLocation(c *Character) bool {
	before := [3]any{c.MapID, c.X, c.Y}
	e.normalizeLocation(c)
	return before != [3]any{c.MapID, c.X, c.Y}
}

func (e *Engine) normalizeLocation(c *Character) {
	m, ok := e.Data.Maps[c.MapID]
	if ok && m.Grid().Walkable(c.X, c.Y) {
		return
	}
	if !ok {
		c.MapID = StartMap
		if len(c.Pets) > 0 {
			c.MapID = "city_square"
		}
		m = e.Data.Maps[c.MapID]
	}
	c.X, c.Y = m.SpawnDefault.X, m.SpawnDefault.Y
}

func (e *Engine) move(c *Character, dir string) ([]Event, error) {
	dx, dy := 0, 0
	switch dir {
	case "left":
		dx = -1
	case "right":
		dx = 1
	case "up":
		dy = -1
	case "down":
		dy = 1
	default:
		return nil, fmt.Errorf("invalid direction")
	}
	if !e.Data.Maps[c.MapID].Grid().Walkable(c.X+dx, c.Y+dy) {
		return nil, errBlocked
	}
	c.X += dx
	c.Y += dy
	return []Event{}, nil
}

func (e *Engine) portal(c *Character, id string) ([]Event, error) {
	m := e.Data.Maps[c.MapID]
	for _, p := range m.Portals {
		if p.ID != id {
			continue
		}
		if p.Locked {
			if !p.Rect.Near(c.X, c.Y, 1) {
				return nil, errNoPortal
			}
			return nil, errNotOpen
		}
		if !p.Rect.Contains(c.X, c.Y) {
			return nil, errNoPortal
		}
		if p.Requires == "has_pet" && len(c.Pets) == 0 {
			return nil, errNeedStarter
		}
		to, arrive := p.To, *p.Arrive
		if r := p.Redirect; r != nil && has(c.Visited, r.IfVisited) {
			to, arrive = r.To, r.Arrive
		}
		dest := e.Data.Maps[to]
		if c.Level < dest.MinLevel || c.ArenaTier < dest.ArenaRequired {
			return nil, fmt.Errorf("Cần cấp %d để vào %s", dest.MinLevel, dest.Name)
		}
		return e.placeAt(c, to, arrive), nil
	}
	return nil, errNoPortal
}

func (e *Engine) npcNear(c *Character, id string) (content.NPC, error) {
	n, ok := e.Data.NPCs[id]
	if !ok || n.MapID != c.MapID || world.Chebyshev(c.X, c.Y, n.X, n.Y) > interactRange {
		return n, errNotNearNPC
	}
	return n, nil
}

// chooseStarter: đứng kề bệ đá ở Triệu Linh Điện, nhận pet khởi đầu rồi dịch chuyển một chiều tới Bìa Rừng.
func (e *Engine) chooseStarter(c *Character, idx *int) ([]Event, error) {
	if len(c.Pets) > 0 {
		return nil, errHasStarter
	}
	m := e.Data.Maps[c.MapID]
	if idx == nil {
		return nil, fmt.Errorf("Chưa chọn bệ")
	}
	for _, p := range m.Pedestals {
		if p.Index != *idx {
			continue
		}
		if world.Chebyshev(c.X, c.Y, p.X, p.Y) > interactRange {
			return nil, fmt.Errorf("Hãy đến gần bệ đá hơn")
		}
		pt := e.GiveStarter(c, p.Species, 3)
		ev := []Event{event("starter_chosen", pt.Name+" đã chọn bạn")}
		for _, exit := range m.Portals {
			if exit.Requires == "has_pet" && exit.Arrive != nil {
				return append(ev, e.placeAt(c, exit.To, *exit.Arrive)...), nil
			}
		}
		return ev, nil
	}
	return nil, fmt.Errorf("Không có bệ đá này ở đây")
}

// pillarTravel: dùng trụ đá dịch chuyển khi đứng kề trụ hoặc NPC vận hành.
func (e *Engine) pillarTravel(c *Character, mapID string) ([]Event, error) {
	p := e.Data.Maps[c.MapID].Pillar
	if p == nil {
		return nil, fmt.Errorf("Không có trụ dịch chuyển ở đây")
	}
	n := e.Data.NPCs[p.NPC]
	if world.Chebyshev(c.X, c.Y, p.X, p.Y) > interactRange && world.Chebyshev(c.X, c.Y, n.X, n.Y) > interactRange {
		return nil, fmt.Errorf("Hãy đến gần trụ dịch chuyển")
	}
	for _, d := range p.Dest {
		if d.Map != mapID {
			continue
		}
		if d.Locked {
			return nil, errNotOpen
		}
		if c.Level < d.MinLevel {
			return nil, fmt.Errorf("Cần cấp %d", d.MinLevel)
		}
		return append([]Event{event("teleport", "Thủy tinh dịch chuyển phát sáng")}, e.placeAt(c, d.Map, *d.Arrive)...), nil
	}
	return nil, errUnknownPlace
}

// encounter: chạm quái hiện trên map (P01-R05). Quái riêng từng người; sau trận bị ẩn tới khi hồi.
func (e *Engine) encounter(c *Character, spawnID string) ([]Event, error) {
	if spawnID == "" {
		// Gặp ngẫu nhiên kiểu cũ (protocol: client cũ bỏ spawn_id) — chỉ ở map có quái.
		return e.startBattle(c, false)
	}
	for _, s := range e.Data.Maps[c.MapID].WildSpawns {
		if s.ID != spawnID {
			continue
		}
		if world.Chebyshev(c.X, c.Y, s.X, s.Y) > interactRange {
			return nil, errBeastFar
		}
		if c.SpawnHidden[s.ID] > e.nowMS() {
			return nil, errBeastHidden
		}
		ev, err := e.startBattle(c, false, s.SpeciesID)
		if err == nil {
			c.Battle.SpawnID = s.ID
		}
		return ev, err
	}
	return nil, errBeastFar
}

// afterWildBattle: mọi kết quả trận hoang đều làm quái ẩn một lúc; thua thì về điểm hồi sinh và hồi phục.
func (e *Engine) afterWildBattle(c *Character, b *Battle, emit func(Event)) {
	now := e.nowMS()
	if b.SpawnID != "" {
		for _, s := range e.Data.Maps[c.MapID].WildSpawns {
			if s.ID == b.SpawnID {
				if c.SpawnHidden == nil {
					c.SpawnHidden = map[string]int64{}
				}
				c.SpawnHidden[s.ID] = now + int64(s.RespawnS)*1000
			}
		}
	}
	for id, until := range c.SpawnHidden {
		if until <= now {
			delete(c.SpawnHidden, id)
		}
	}
	if b.Result != "loss" || b.Arena {
		return
	}
	for _, p := range c.Pets {
		if !p.Retired {
			p.HP, p.MP = p.MaxHP, p.MaxMP
		}
	}
	to := e.Data.Maps[c.MapID].RespawnTo
	for _, ev := range e.placeAt(c, to, e.Data.Maps[to].SpawnDefault) {
		emit(ev)
	}
	emit(event("respawn", "Bạn được đưa về "+e.Data.Maps[to].Name+", linh thú đã hồi phục"))
}
