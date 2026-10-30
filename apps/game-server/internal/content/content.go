// Package content loads the versioned reconstruction catalog. It contains no player state.
package content

import (
	"encoding/json"
	"fmt"
	"io/fs"
	"os"
	"path"
	"phimond/server/internal/world"
	"sort"
)

type Evidence struct {
	Confidence string `json:"confidence"`
	Source     string `json:"source"`
}

// Species là một loài trong danh mục P11/P13 (160 loài; số liệu sinh từ tools/p01/apply_p11_p13.py).
// Base/GrowthMilli có đủ 6 chỉ số (hp, atk, mag, def, spd, status_resistance); MP tách riêng (P11 F04).
type Species struct {
	ID            string         `json:"id"`
	Name          string         `json:"name"`
	Race          string         `json:"race"`
	Element       string         `json:"element"`
	Star          int            `json:"star"`
	Class         string         `json:"class"` // normal | special
	Roles         []string       `json:"roles"`
	PrimaryRole   string         `json:"primary_role"`
	SecondaryRole string         `json:"secondary_role,omitempty"`
	Base          map[string]int `json:"base"`
	GrowthMilli   map[string]int `json:"growth_milli"`
	MPBase        int            `json:"mp_base"`
	MPGrowthMilli int            `json:"mp_growth_milli"`
	// Skills là Native Pool (P13): kỹ năng loài này được học; không tự cấp.
	Skills      []string `json:"skills"`
	CaptureRate float64  `json:"capture_rate"`
	Catchable   bool     `json:"catchable"`
	Description string   `json:"description,omitempty"`
	Evidence
}

// Effect là phần hiệu ứng của kỹ năng P13 (xác suất theo phần nghìn, tỉ lệ theo điểm cơ bản, công suất theo phần nghìn).
type Effect struct {
	Status        string `json:"status,omitempty"`
	ChancePM      int    `json:"chance_pm,omitempty"`
	Stat          string `json:"stat,omitempty"`
	AmountBP      int    `json:"amount_bp,omitempty"`
	PenetrationPM int    `json:"penetration_pm,omitempty"`
	Hits          int    `json:"hits,omitempty"`
	SelfBuff      string `json:"self_buff,omitempty"`
	Cleanse       string `json:"cleanse,omitempty"`
	CleanseOne    bool   `json:"cleanse_one,omitempty"`
	TickPowerPM   int    `json:"tick_power_pm,omitempty"`
	ShieldMAGPM   int    `json:"shield_mag_pm,omitempty"`
	ShieldHPPM    int    `json:"shield_hp_pm,omitempty"`
	HealMAGPM     int    `json:"heal_mag_pm,omitempty"`
	HealFlat      int    `json:"heal_flat,omitempty"`
}

// Skill là kỹ năng P13 v7.1. Hành vi chi tiết theo id nằm ở internal/character/combat.go.
type Skill struct {
	ID               string   `json:"id"`
	Name             string   `json:"name"`
	Element          string   `json:"element"`
	Kind             string   `json:"kind"` // physical|magic|control|debuff|buff|heal|shield|cleanse|dispel|resource|revive
	Target           string   `json:"target"`
	MPCost           int      `json:"mp"`
	Cooldown         int      `json:"cooldown"`
	LearnLevel       int      `json:"learn_level"`
	Description      string   `json:"description"`
	Functions        []string `json:"functions"`
	Inheritance      []string `json:"inheritance"`
	PowerPM          int      `json:"power_pm"`
	Effect           Effect   `json:"effect"`
	RankPolicy       string   `json:"rank_policy"`
	Channel          string   `json:"channel"` // physical | magic | utility
	Shape            string   `json:"shape"`
	DamageMode       string   `json:"damage_mode"`
	ExclusiveSpecies string   `json:"exclusive_species,omitempty"`
	Evidence
}

// Status mô tả loại trạng thái để hiển thị; hành vi theo P13 §5 nằm trong code.
type Status struct {
	ID   string `json:"id"`
	Name string `json:"name"`
	Kind string `json:"kind"` // control | restraint | debuff | dot | buff | grace
	Evidence
}
type Race struct {
	ID        string `json:"id"`
	Name      string `json:"name"`
	Element   string `json:"element"`
	Status    string `json:"status"`
	Cleanse   string `json:"cleanse"`
	Specialty string `json:"specialty"`
	Evidence
}

// Portal là cổng trên map P01 (ADR-P01-01): vùng chữ nhật, điểm đến X/Y, khóa và điều kiện.
type Portal struct {
	ID       string       `json:"id"`
	Rect     world.Rect   `json:"rect"`
	To       string       `json:"to"`
	Arrive   *world.Point `json:"arrive,omitempty"`
	Locked   bool         `json:"locked,omitempty"`
	Requires string       `json:"requires,omitempty"`
	Redirect *Redirect    `json:"redirect,omitempty"`
}

// Redirect đổi đích cổng khi người chơi đã từng tới map IfVisited (vd Rừng Sâu → Quảng Trường sau lần đầu).
type Redirect struct {
	IfVisited string      `json:"if_visited"`
	To        string      `json:"to"`
	Arrive    world.Point `json:"arrive"`
}

// Pillar là trụ đá dịch chuyển; người chơi đứng kề trụ hoặc NPC vận hành để dùng.
type Pillar struct {
	X    int          `json:"x"`
	Y    int          `json:"y"`
	NPC  string       `json:"npc"`
	Dest []PillarDest `json:"dest"`
}
type PillarDest struct {
	Map      string       `json:"map"`
	Arrive   *world.Point `json:"arrive,omitempty"`
	Locked   bool         `json:"locked,omitempty"`
	MinLevel int          `json:"min_level,omitempty"`
}

// Pedestal là bệ triệu hồi ở Triệu Linh Điện; chọn bệ để nhận pet khởi đầu (P01 §7 câu 1).
type Pedestal struct {
	Index   int    `json:"index"`
	X       int    `json:"x"`
	Y       int    `json:"y"`
	Starter string `json:"starter"`
	Species string `json:"species"`
	// Display là thần thú 5★ trưng bày trên bệ (chỉ hiển thị phía client; nhận được pet 1★ Species).
	Display string `json:"display,omitempty"`
}

// NPCPlace là vị trí NPC trong file map; map là nguồn chuẩn cho vị trí.
type NPCPlace struct {
	ID   string `json:"id"`
	X    int    `json:"x"`
	Y    int    `json:"y"`
	Face string `json:"face,omitempty"`
}

// SpawnZone là vùng quái theo kế hoạch P12; điểm quái cụ thể nằm ở WildSpawns.
type SpawnZone struct {
	ID       string     `json:"id"`
	Rect     world.Rect `json:"rect"`
	Species  []string   `json:"species"`
	MaxAlive int        `json:"max_alive"`
	RespawnS int        `json:"respawn_s"`
}

type Map struct {
	ID            string            `json:"id"`
	Name          string            `json:"name"`
	Kind          string            `json:"kind"`
	Theme         string            `json:"theme,omitempty"`
	Level         []int             `json:"level"`
	Width         int               `json:"width"`
	Height        int               `json:"height"`
	SpawnDefault  world.Point       `json:"spawn_default"`
	RespawnTo     string            `json:"respawn_to"`
	Portals       []Portal          `json:"portals"`
	Pillar        *Pillar           `json:"pillar,omitempty"`
	Pedestals     []Pedestal        `json:"pedestals,omitempty"`
	NPCPlaces     []NPCPlace        `json:"npcs"`
	SpawnZones    []SpawnZone       `json:"spawn_zones"`
	WildSpawns    []WildSpawn       `json:"wild_spawns"`
	Walk          string            `json:"walk"`
	Layout        []string          `json:"layout,omitempty"`
	Facades       map[string]string `json:"facades,omitempty"`
	Backdrop      *string           `json:"backdrop"`
	Spawns        []string          `json:"spawns"`
	MinLevel      int               `json:"min_level"`
	ArenaRequired int               `json:"arena_required"`
	Evidence
	grid *world.Grid
}

// Grid trả lưới đi được đã kiểm (nạp lúc Load).
func (m Map) Grid() *world.Grid { return m.grid }

// LevelRange trả khoảng cấp quái; map không có quái trả (1, 1).
func (m Map) LevelRange() (int, int) {
	if len(m.Level) == 2 && m.Level[0] >= 1 && m.Level[1] >= m.Level[0] {
		return m.Level[0], m.Level[1]
	}
	return 1, 1
}

// Stable per-map contact positions are shared by the renderer and encounter validation.
// P01: sinh từ spawn_zones bởi tools/p01/build_maps.py, không phải dữ liệu lịch sử.
type WildSpawn struct {
	ID        string `json:"id"`
	Zone      string `json:"zone,omitempty"`
	SpeciesID string `json:"species_id"`
	X         int    `json:"x"`
	Y         int    `json:"y"`
	RespawnS  int    `json:"respawn_s,omitempty"`
}
type NPC struct {
	ID       string   `json:"id"`
	Name     string   `json:"name"`
	MapID    string   `json:"map_id"`
	X        int      `json:"x"`
	Y        int      `json:"y"`
	Face     string   `json:"face,omitempty"`
	Roles    []string `json:"roles"`
	Dialogue string   `json:"dialogue,omitempty"`
	// Lines: câu thoại thêm, đổi theo tiến độ (số nhiệm vụ đã xong) để NPC không lặp một câu mãi.
	Lines []string `json:"lines,omitempty"`
	Evidence
}
type Item struct {
	ID    string `json:"id"`
	Name  string `json:"name"`
	Kind  string `json:"kind"`
	Price int    `json:"price"`
	Power int    `json:"power"`
	Evidence
}
type Recipe struct {
	ID             string `json:"id"`
	Name           string `json:"name"`
	ParentA        string `json:"parent_a"`
	ParentB        string `json:"parent_b"`
	Result         string `json:"result"`
	MinLevel       int    `json:"min_level"`
	MinPlayerLevel int    `json:"min_player_level"`
	OppositeGender bool   `json:"opposite_gender"`
	SameStar       bool   `json:"same_star"`
	CrossRace      bool   `json:"cross_race"`
	ConsumeParents bool   `json:"consume_parents"`
	SoulCost       int    `json:"soul_cost"`
	GoldCost       int    `json:"gold_cost"`
	Evidence
}
type Quest struct {
	ID          string         `json:"id"`
	Name        string         `json:"name"`
	Description string         `json:"description"`
	Kind        string         `json:"kind"`
	Target      string         `json:"target"`
	Count       int            `json:"count"`
	Gold        int            `json:"gold"`
	XP          int            `json:"xp"`
	Items       map[string]int `json:"items"`
	Recipe      string         `json:"recipe"`
	// Requires: nhiệm vụ phải hoàn thành (đã nhận thưởng) trước khi nhận nhiệm vụ này (chuỗi Đợt A).
	Requires string `json:"requires,omitempty"`
	// Giver: NPC giao nhiệm vụ; nhận phải đứng gần NPC này (báo cáo ở NPC nhiệm vụ nào cũng được).
	Giver string `json:"giver,omitempty"`
	Evidence
}
type Rules struct {
	ID            string `json:"id"`
	AppraisalCost int    `json:"appraisal_cost"`
	HealCost      int    `json:"heal_cost"`
	// SkillSlots: số kỹ năng hiện tại tối đa (P13-D02 = 6). Đòn thường không chiếm ô.
	SkillSlots         int     `json:"skill_slots"`
	CaptureHPScale     float64 `json:"capture_hp_scale"`
	CaptureStatusBonus float64 `json:"capture_status_bonus"`
	CaptureCap         float64 `json:"capture_cap"`
	XPPerLevel         int     `json:"xp_per_level"`
	BattleXP           int     `json:"battle_xp"`
	BattleGold         int     `json:"battle_gold"`
	// LevelCaps[star-1]: cấp tối đa theo Sao (P11: 60/70/80/90/100, chưa tính Plus).
	LevelCaps     []int `json:"level_caps"`
	BattleTurnCap int   `json:"battle_turn_cap"`
	// EncounterWeights[i] = trọng số encounter hoang có i+1 quái cùng loài (rỗng = luôn 1 quái, tương thích dữ liệu cũ).
	EncounterWeights []int `json:"encounter_weights"`
	// PackScale[i] = hệ số HP và sát thương của mỗi quái khi encounter có i+1 quái (rỗng/thiếu = 1).
	// Lớp điều chỉnh encounter áp sau chỉ số nội tại (P11 §7); nợ cân bằng cho P15.
	PackScale []float64 `json:"pack_scale"`
	// WildScale nhân HP và sát thương mọi quái hoang (0 = 1).
	WildScale           float64  `json:"wild_scale"`
	Elements            []string `json:"elements"`
	MovementAllowedKeys []string `json:"movement_allowed_keys"`
	Evidence
}

// LevelCap trả cấp tối đa của một loài theo Sao.
func (r Rules) LevelCap(star int) int {
	if star >= 1 && star <= len(r.LevelCaps) {
		return r.LevelCaps[star-1]
	}
	return 60
}

type Catalog struct {
	Species  map[string]Species `json:"species"`
	Skills   map[string]Skill   `json:"skills"`
	Statuses map[string]Status  `json:"statuses"`
	Races    map[string]Race    `json:"races"`
	Maps     map[string]Map     `json:"maps"`
	NPCs     map[string]NPC     `json:"npcs"`
	Items    map[string]Item    `json:"items"`
	Recipes  map[string]Recipe  `json:"recipes"`
	Quests   map[string]Quest   `json:"quests"`
	Rules    Rules              `json:"rules"`
	// LegacySpecies ánh xạ id loài trước P11 sang id chuẩn (tùy chọn, chỉ để chuyển save cũ).
	LegacySpecies map[string]string `json:"-"`
}

func read(root fs.FS, name string, out any) error {
	b, e := fs.ReadFile(root, name)
	if e != nil {
		return e
	}
	if e = json.Unmarshal(b, out); e != nil {
		return fmt.Errorf("%s: %w", name, e)
	}
	return nil
}

// Load đọc catalog từ thư mục data trên đĩa.
func Load(root string) (*Catalog, error) { return LoadFS(os.DirFS(root)) }

// LoadFS đọc catalog từ một fs.FS (đĩa hoặc go:embed, dùng cho bản wasm demo).
func LoadFS(root fs.FS) (*Catalog, error) {
	c := &Catalog{}
	for _, v := range []struct {
		p string
		v any
	}{{"pets/species.json", &c.Species}, {"skills/skills.json", &c.Skills}, {"skills/statuses.json", &c.Statuses}, {"pets/races.json", &c.Races}, {"npcs/npcs.json", &c.NPCs}, {"items/items.json", &c.Items}, {"recipes/recipes.json", &c.Recipes}, {"quests/quests.json", &c.Quests}, {"balance/rules.json", &c.Rules}} {
		if e := read(root, v.p, v.v); e != nil {
			return nil, e
		}
	}
	if b, err := fs.ReadFile(root, "pets/legacy_species.json"); err == nil {
		if err := json.Unmarshal(b, &c.LegacySpecies); err != nil {
			return nil, fmt.Errorf("pets/legacy_species.json: %w", err)
		}
	}
	if err := c.loadMaps(root); err != nil {
		return nil, err
	}
	return c, c.Validate()
}

// loadMaps đọc mọi map P01 trong maps/p01/*.json (ADR-P01-01), dựng lưới đi được và
// gắn vị trí NPC từ map vào danh mục NPC (map là nguồn chuẩn cho vị trí).
func (c *Catalog) loadMaps(root fs.FS) error {
	files, err := fs.Glob(root, "maps/p01/*.json")
	if err != nil {
		return err
	}
	if len(files) == 0 {
		return fmt.Errorf("không có map nào trong maps/p01")
	}
	sort.Strings(files)
	c.Maps = map[string]Map{}
	for _, f := range files {
		var m Map
		if err := read(root, f, &m); err != nil {
			return err
		}
		if want := path.Base(f); want != m.ID+".json" {
			return fmt.Errorf("%s: id %q không khớp tên file", f, m.ID)
		}
		if m.grid, err = world.ParseWalk(m.Walk, m.Width, m.Height); err != nil {
			return fmt.Errorf("map %s: %w", m.ID, err)
		}
		// level là cấp quái khuyến nghị (P12), không phải điều kiện vào map.
		seen := map[string]bool{}
		m.Spawns = []string{}
		for _, z := range m.SpawnZones {
			for _, s := range z.Species {
				if !seen[s] {
					seen[s] = true
					m.Spawns = append(m.Spawns, s)
				}
			}
		}
		if m.WildSpawns == nil {
			m.WildSpawns = []WildSpawn{}
		}
		if _, dup := c.Maps[m.ID]; dup {
			return fmt.Errorf("map %s bị trùng", m.ID)
		}
		c.Maps[m.ID] = m
		for _, p := range m.NPCPlaces {
			n, ok := c.NPCs[p.ID]
			if !ok {
				return fmt.Errorf("map %s đặt NPC %s không có trong npcs.json", m.ID, p.ID)
			}
			if n.MapID != "" && n.MapID != m.ID {
				return fmt.Errorf("NPC %s thuộc map %s nhưng được đặt ở %s", p.ID, n.MapID, m.ID)
			}
			n.MapID, n.X, n.Y, n.Face = m.ID, p.X, p.Y, p.Face
			c.NPCs[p.ID] = n
		}
	}
	return nil
}

func (c *Catalog) Validate() error {
	if len(c.Species) == 0 || len(c.Maps) == 0 || c.Rules.SkillSlots < 1 || len(c.Rules.LevelCaps) != 5 || c.Rules.XPPerLevel <= 0 || c.Rules.BattleTurnCap < 1 || len(c.Rules.Elements) == 0 || len(c.Rules.MovementAllowedKeys) == 0 {
		return fmt.Errorf("invalid catalog/rules")
	}
	elementSeen := map[string]bool{}
	for _, e := range c.Rules.Elements {
		if e == "" || elementSeen[e] {
			return fmt.Errorf("invalid element list")
		}
		elementSeen[e] = true
	}
	for id, s := range c.Species {
		if id != s.ID || s.Star < 1 || s.Star > 5 || s.Confidence == "" {
			return fmt.Errorf("invalid species %s", id)
		}
		if _, ok := c.Races[s.Race]; !ok {
			return fmt.Errorf("unknown race %s", s.Race)
		}
		if !elementSeen[s.Element] {
			return fmt.Errorf("species %s uses unknown element %s", id, s.Element)
		}
		if s.Class != "normal" && s.Class != "special" {
			return fmt.Errorf("species %s has invalid class %q", id, s.Class)
		}
		for _, k := range s.Skills {
			if _, ok := c.Skills[k]; !ok {
				return fmt.Errorf("unknown skill %s", k)
			}
		}
	}
	for id, s := range c.Skills {
		if id != s.ID || s.MPCost < 0 || s.Cooldown < 0 || s.PowerPM < 0 || s.LearnLevel < 1 {
			return fmt.Errorf("invalid skill %s", id)
		}
		if st := s.Effect.Status; st != "" {
			if _, ok := c.Statuses[st]; !ok {
				return fmt.Errorf("skill %s uses unknown status %s", id, st)
			}
		}
		if cl := s.Effect.Cleanse; cl != "" {
			if _, ok := c.Statuses[cl]; !ok {
				return fmt.Errorf("skill %s cleanses unknown status %s", id, cl)
			}
		}
		if s.ExclusiveSpecies != "" {
			if _, ok := c.Species[s.ExclusiveSpecies]; !ok {
				return fmt.Errorf("skill %s exclusive to unknown species %s", id, s.ExclusiveSpecies)
			}
		}
	}
	for id, r := range c.Recipes {
		if id != r.ID || r.MinLevel < 1 || r.SoulCost < 0 || r.GoldCost < 0 {
			return fmt.Errorf("invalid recipe %s", id)
		}
		for _, s := range []string{r.ParentA, r.ParentB, r.Result} {
			if _, ok := c.Species[s]; !ok {
				return fmt.Errorf("recipe %s unknown species %s", id, s)
			}
		}
	}
	for id, m := range c.Maps {
		if err := c.validateMap(id, m); err != nil {
			return err
		}
	}
	for _, n := range c.NPCs {
		if _, ok := c.Maps[n.MapID]; !ok {
			return fmt.Errorf("NPC %s chưa được đặt lên map nào", n.ID)
		}
	}
	return c.validateEffects()
}

func contains(values []string, value string) bool {
	for _, v := range values {
		if v == value {
			return true
		}
	}
	return false
}
func (c *Catalog) validateEffects() error {
	r := c.Rules
	if r.CaptureCap <= 0 || r.CaptureCap > 1 {
		return fmt.Errorf("invalid balance ranges")
	}
	for i := 1; i < len(r.LevelCaps); i++ {
		if r.LevelCaps[i] < r.LevelCaps[i-1] {
			return fmt.Errorf("level_caps must not decrease")
		}
	}
	kinds := []string{"physical", "magic", "control", "debuff", "buff", "heal", "shield", "cleanse", "dispel", "resource", "revive"}
	targets := []string{"enemy_one", "enemy_all", "self", "ally_one", "ally_all", "ally_other", "ally_fainted"}
	for id, s := range c.Skills {
		if !contains(kinds, s.Kind) || !contains(targets, s.Target) || !contains([]string{"physical", "magic", "utility"}, s.Channel) || s.Confidence == "" {
			return fmt.Errorf("invalid skill effect %s", id)
		}
	}
	for id, s := range c.Statuses {
		if id != s.ID || s.Name == "" {
			return fmt.Errorf("invalid status %s", id)
		}
	}
	for id, q := range c.Quests {
		if id != q.ID || q.Count < 1 || q.Gold < 0 || q.XP < 0 {
			return fmt.Errorf("invalid quest %s", id)
		}
		for item, n := range q.Items {
			if _, ok := c.Items[item]; !ok || n < 1 {
				return fmt.Errorf("invalid quest reward %s", item)
			}
		}
		if q.Recipe != "" {
			if _, ok := c.Recipes[q.Recipe]; !ok {
				return fmt.Errorf("unknown quest recipe")
			}
		}
		if q.Requires != "" {
			if _, ok := c.Quests[q.Requires]; !ok || q.Requires == id {
				return fmt.Errorf("quest %s requires unknown quest %s", id, q.Requires)
			}
		}
		if q.Giver != "" {
			if n, ok := c.NPCs[q.Giver]; !ok || !contains(n.Roles, "quest") {
				return fmt.Errorf("quest %s giver %s is not a quest NPC", id, q.Giver)
			}
		}
	}
	for id, it := range c.Items {
		if id != it.ID || it.Price < 0 || it.Power < 0 || !contains([]string{"heal", "mp", "capture", "breeding", "blessing"}, it.Kind) {
			return fmt.Errorf("invalid item %s", id)
		}
	}
	for id, sp := range c.Species {
		for _, k := range []string{"hp", "atk", "mag", "def", "spd", "status_resistance"} {
			if sp.Base[k] < 1 || sp.GrowthMilli[k] < 1 {
				return fmt.Errorf("invalid species stat %s/%s", id, k)
			}
		}
		if sp.MPBase < 1 || sp.MPGrowthMilli < 0 {
			return fmt.Errorf("invalid species mp %s", id)
		}
		if sp.CaptureRate < 0 || sp.CaptureRate > 1 {
			return fmt.Errorf("invalid capture rate %s", id)
		}
	}
	return nil
}

// validateMap áp luật ADR-P01-01: điểm đặt đi được, điểm đến không nằm trong/kề cổng của map đích,
// mọi cổng/NPC/bệ/điểm quái tới được từ spawn_default, đích cổng tồn tại hoặc bị khóa.
func (c *Catalog) validateMap(id string, m Map) error {
	g := m.grid
	if id != m.ID || g == nil {
		return fmt.Errorf("invalid map %s", id)
	}
	if !g.Walkable(m.SpawnDefault.X, m.SpawnDefault.Y) {
		return fmt.Errorf("map %s: spawn_default bị chặn", id)
	}
	if _, ok := c.Maps[m.RespawnTo]; !ok {
		return fmt.Errorf("map %s: respawn_to %q không có", id, m.RespawnTo)
	}
	reach := g.Reachable(m.SpawnDefault)
	arrival := func(to string, a *world.Point, what string) error {
		t, ok := c.Maps[to]
		if !ok {
			return fmt.Errorf("map %s/%s: map đích %q không có (thiếu locked?)", id, what, to)
		}
		if a == nil || !t.grid.Walkable(a.X, a.Y) {
			return fmt.Errorf("map %s/%s: điểm đến ở %s không đi được", id, what, to)
		}
		for _, q := range t.Portals {
			if q.Rect.Near(a.X, a.Y, 1) {
				return fmt.Errorf("map %s/%s: điểm đến nằm trong/kề cổng %s của %s", id, what, q.ID, to)
			}
		}
		return nil
	}
	ids := map[string]bool{}
	for _, p := range m.Portals {
		if p.ID == "" || ids[p.ID] || p.Rect[2] < 1 || p.Rect[3] < 1 {
			return fmt.Errorf("map %s: cổng %q không hợp lệ", id, p.ID)
		}
		ids[p.ID] = true
		found, reachDist := false, 0
		if p.Locked {
			reachDist = 1 // cổng khóa chỉ cần đứng kề để đọc thông báo "chưa mở"
		}
		for y := p.Rect[1]; y < p.Rect[1]+p.Rect[3]; y++ {
			for x := p.Rect[0]; x < p.Rect[0]+p.Rect[2]; x++ {
				found = found || world.ReachesNear(reach, x, y, reachDist)
			}
		}
		if !found {
			return fmt.Errorf("map %s: không tới được cổng %s", id, p.ID)
		}
		if p.Locked {
			continue
		}
		if err := arrival(p.To, p.Arrive, p.ID); err != nil {
			return err
		}
		if p.Requires != "" && p.Requires != "has_pet" {
			return fmt.Errorf("map %s: cổng %s có điều kiện lạ %q", id, p.ID, p.Requires)
		}
		if r := p.Redirect; r != nil {
			if _, ok := c.Maps[r.IfVisited]; !ok {
				return fmt.Errorf("map %s: redirect của %s dùng map lạ %q", id, p.ID, r.IfVisited)
			}
			a := r.Arrive
			if err := arrival(r.To, &a, p.ID+"/redirect"); err != nil {
				return err
			}
		}
	}
	if p := m.Pillar; p != nil {
		if !world.ReachesNear(reach, p.X, p.Y, 1) {
			return fmt.Errorf("map %s: không tới được trụ đá", id)
		}
		for _, d := range p.Dest {
			if !d.Locked {
				if err := arrival(d.Map, d.Arrive, "pillar"); err != nil {
					return err
				}
			}
		}
	}
	for _, n := range m.NPCPlaces {
		if g.Walkable(n.X, n.Y) || !world.ReachesNear(reach, n.X, n.Y, 1) {
			return fmt.Errorf("map %s: NPC %s phải chặn ô đứng và tới gần được", id, n.ID)
		}
	}
	for _, p := range m.Pedestals {
		if _, ok := c.Species[p.Species]; !ok || !world.ReachesNear(reach, p.X, p.Y, 1) {
			return fmt.Errorf("map %s: bệ %d không hợp lệ", id, p.Index)
		}
	}
	spawnIDs := map[string]bool{}
	for _, s := range m.WildSpawns {
		if _, ok := c.Species[s.SpeciesID]; !ok || spawnIDs[s.ID] || !reach[[2]int{s.X, s.Y}] || s.RespawnS < 1 {
			return fmt.Errorf("map %s: điểm quái %s không hợp lệ", id, s.ID)
		}
		spawnIDs[s.ID] = true
	}
	for _, s := range m.Spawns {
		if _, ok := c.Species[s]; !ok {
			return fmt.Errorf("unknown spawn %s", s)
		}
	}
	return nil
}
