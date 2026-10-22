package world

import "testing"

func TestParseWalkAndQueries(t *testing.T) {
	g, err := ParseWalk("4#/1#2.1#/4#", 4, 3)
	if err != nil {
		t.Fatal(err)
	}
	if !g.Walkable(1, 1) || !g.Walkable(2, 1) || g.Walkable(0, 1) || g.Walkable(1, 0) {
		t.Fatal("ô đi được sai")
	}
	if g.Walkable(-1, 1) || g.Walkable(4, 1) || g.Walkable(1, 3) {
		t.Fatal("ngoài biên phải bị chặn")
	}
	reach := g.Reachable(Point{X: 1, Y: 1})
	if len(reach) != 2 {
		t.Fatalf("reach = %d, cần 2", len(reach))
	}
	if !ReachesNear(reach, 3, 2, 1) || ReachesNear(reach, 3, 3, 0) {
		t.Fatal("ReachesNear sai")
	}
}

func TestParseWalkRejectsBadInput(t *testing.T) {
	for _, s := range []string{"3./3.", "4./3.", "4.x/4.", "a./4.", "0./4.", "2.2"} {
		if _, err := ParseWalk(s, 4, 2); err == nil {
			t.Fatalf("%q phải bị từ chối", s)
		}
	}
}

func TestRectAndDistance(t *testing.T) {
	r := Rect{2, 3, 2, 1}
	if !r.Contains(2, 3) || !r.Contains(3, 3) || r.Contains(4, 3) || r.Contains(2, 4) {
		t.Fatal("Contains sai")
	}
	if !r.Near(4, 4, 1) || r.Near(5, 3, 1) {
		t.Fatal("Near sai")
	}
	if Chebyshev(0, 0, 2, -1) != 2 || Chebyshev(3, 3, 3, 3) != 0 {
		t.Fatal("Chebyshev sai")
	}
}
