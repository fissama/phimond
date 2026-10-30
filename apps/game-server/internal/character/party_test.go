package character

import (
	"reflect"
	"testing"
)

// threePets tạo nhân vật có 3 linh thú; con khởi đầu (c.Pets[0]) là con chính theo dữ liệu cũ (chưa có Party).
func threePets(t *testing.T) (*Engine, *Character, [3]string) {
	t.Helper()
	e := engine(t)
	c := veteran(e, "party", "Party", 7)
	a := c.Pets[0]
	b := e.NewPet(c, "species_0111", 2)
	d := e.NewPet(c, "species_0111", 2)
	c.Pets = append(c.Pets, b, d)
	c.ActivePetID = a.ID
	return e, c, [3]string{a.ID, b.ID, d.ID}
}

func TestLegacyPartyIsDerivedFromActiveAndOrder(t *testing.T) {
	_, c, id := threePets(t)
	if got, want := c.EffectiveParty(), id[:]; !reflect.DeepEqual(got, want) {
		t.Fatalf("đội cũ = %v, cần %v", got, want)
	}
	c.ActivePetID = id[2]
	if got, want := c.EffectiveParty(), []string{id[2], id[0], id[1]}; !reflect.DeepEqual(got, want) {
		t.Fatalf("con chính phải đứng đầu: %v, cần %v", got, want)
	}
}

func TestPartySetReordersAndSetsMain(t *testing.T) {
	e, c, id := threePets(t)
	command(t, e, c, "pet.party_set", map[string]any{"pet_ids": []string{id[1], id[2]}})
	if c.ActivePetID != id[1] || !reflect.DeepEqual(c.EffectiveParty(), []string{id[1], id[2]}) {
		t.Fatalf("đội = %v, chính = %s", c.EffectiveParty(), c.ActivePetID)
	}
	snap := e.Snapshot(c)
	if got := snap["party"].([]string); !reflect.DeepEqual(got, []string{id[1], id[2]}) {
		t.Fatalf("snapshot party = %v", got)
	}
}

func TestPartySetRejectsBadInput(t *testing.T) {
	e, c, id := threePets(t)
	mustFail(t, e, c, "pet.party_set", map[string]any{"pet_ids": []string{}}, "party must have")
	mustFail(t, e, c, "pet.party_set", map[string]any{"pet_ids": []string{id[0], id[0]}}, "duplicate")
	mustFail(t, e, c, "pet.party_set", map[string]any{"pet_ids": []string{"nope"}}, "not owned")
	mustFail(t, e, c, "pet.party_set", map[string]any{"pet_ids": []string{id[0], id[1], id[2], "x"}}, "party must have")
}

func TestActivateKeepsSubsAndReleasedPetLeavesParty(t *testing.T) {
	e, c, id := threePets(t)
	command(t, e, c, "pet.activate", map[string]any{"pet_id": id[2]})
	if got, want := c.EffectiveParty(), []string{id[2], id[0], id[1]}; !reflect.DeepEqual(got, want) {
		t.Fatalf("đổi chính: %v, cần %v", got, want)
	}
	command(t, e, c, "pet.release", map[string]any{"pet_id": id[1]})
	if got, want := c.EffectiveParty(), []string{id[2], id[0]}; !reflect.DeepEqual(got, want) {
		t.Fatalf("sau khi thả: %v, cần %v", got, want)
	}
	mustFail(t, e, c, "pet.party_set", map[string]any{"pet_ids": []string{id[1]}}, "not owned")
}
