package character

import (
	"fmt"
	"testing"
)

// Mục tiêu cân bằng v1.0.0 (REVIEW-v1.0.0-TOAN-DIEN P0-1): pet khởi đầu Lv1 chỉ bấm Tự động phải thắng
// ≥90% trận ở Bìa Rừng với 1, 2 hay 3 quái, mỗi trận 3–7 lượt.
func TestBalanceStarterAutoWinsBiaRung(t *testing.T) {
	e := engine(t)
	for _, sp := range []string{"tien_chuong", "sa_hat", "xich_ung"} {
		for n := 1; n <= 3; n++ {
			w := make([]int, n)
			w[n-1] = 1
			e.Data.Rules.EncounterWeights = w
			wins, turns := 0, 0
			const runs = 200
			for i := 0; i < runs; i++ {
				c := e.NewCharacter(fmt.Sprintf("b%d", i), "B", uint64(i+7))
				e.GiveStarter(c, sp, 1)
				c.MapID = "emerald_forest_main_woods"
				c.RNG.State = uint64(i+1) * 0x9e3779b97f4a7c15
				command(t, e, c, "world.encounter", nil)
				for c.Battle != nil {
					command(t, e, c, "battle.action", map[string]any{"battle_id": c.Battle.ID, "turn": c.Battle.Turn, "choice": "auto"})
				}
				h := c.History[len(c.History)-1]
				if h.Result == "win" {
					wins++
				}
				turns += h.Turn
			}
			avg := float64(turns) / runs
			if wins*100/runs < 90 || avg < 3 || avg > 7 {
				t.Errorf("%s 1v%d: win %d%% avg turns %.1f (want ≥90%%, 3–7)", sp, n, wins*100/runs, avg)
			}
		}
	}
}

// Chạy trốn đi trước: không quái nào kịp ra đòn.
func TestFleeResolvesBeforeEnemies(t *testing.T) {
	e := engine(t)
	e.Data.Rules.EncounterWeights = []int{0, 0, 1}
	c := veteran(e, "f", "F", 1)
	command(t, e, c, "world.encounter", nil)
	p, _ := findPet(c, c.ActivePetID)
	hp := p.HP
	command(t, e, c, "battle.action", map[string]any{"battle_id": c.Battle.ID, "turn": 1, "choice": "flee"})
	p, _ = findPet(c, c.ActivePetID)
	if c.Battle != nil || p.HP != hp {
		t.Fatalf("flee must end battle without damage: hp %d→%d", hp, p.HP)
	}
}

// HP tối đa của quái theo đàn không bị trả về giá trị gốc sau lượt đầu.
func TestPackScaledMaxHPPersistsAcrossTurns(t *testing.T) {
	e := engine(t)
	e.Data.Rules.EncounterWeights = []int{0, 0, 1}
	c := veteran(e, "m", "M", 1)
	command(t, e, c, "world.encounter", nil)
	foe := sideUnits(c.Battle, "enemy")[0]
	want := foe.MaxHP
	if want >= foe.Pet.MaxHP {
		t.Fatalf("pack foe must be scaled: %d vs %d", want, foe.Pet.MaxHP)
	}
	command(t, e, c, "battle.action", map[string]any{"battle_id": c.Battle.ID, "turn": 1, "choice": "defend"})
	if c.Battle != nil && sideUnits(c.Battle, "enemy")[0].MaxHP != want {
		t.Fatalf("max hp changed after turn: %d → %d", want, sideUnits(c.Battle, "enemy")[0].MaxHP)
	}
}
