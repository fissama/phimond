package world

import (
	"fmt"
	"strconv"
	"strings"
)

// Point là một ô trên lưới gameplay (ADR-P01-01): x sang phải, y xuống dưới, 1 ô = 1 đơn vị world.
type Point struct {
	X    int    `json:"x"`
	Y    int    `json:"y"`
	Face string `json:"face,omitempty"`
}

// Rect là vùng chữ nhật [x, y, w, h] tính theo ô.
type Rect [4]int

// Contains báo ô (x, y) có nằm trong vùng không.
func (r Rect) Contains(x, y int) bool {
	return x >= r[0] && x < r[0]+r[2] && y >= r[1] && y < r[1]+r[3]
}

// Near báo ô (x, y) nằm trong vùng hoặc kề vùng (khoảng cách Chebyshev ≤ d tới ô gần nhất).
func (r Rect) Near(x, y, d int) bool {
	return x >= r[0]-d && x < r[0]+r[2]+d && y >= r[1]-d && y < r[1]+r[3]+d
}

// Chebyshev là khoảng cách dùng cho tầm tương tác hai trục (P01-R04).
func Chebyshev(ax, ay, bx, by int) int {
	return max(abs(ax-bx), abs(ay-by))
}

func abs(v int) int {
	if v < 0 {
		return -v
	}
	return v
}

// Grid là lưới đi được của một map. Ô ngoài biên luôn bị chặn.
type Grid struct {
	W, H  int
	cells []bool
}

// ParseWalk đọc lưới từ chuỗi RLE: các hàng nối bằng '/', mỗi hàng là chuỗi "<số><ký tự>",
// '.' = đi được, '#' = chặn. Mỗi hàng phải đủ w ô và có đúng h hàng.
func ParseWalk(s string, w, h int) (*Grid, error) {
	if w < 1 || h < 1 {
		return nil, fmt.Errorf("kích thước lưới không hợp lệ %dx%d", w, h)
	}
	rows := strings.Split(s, "/")
	if len(rows) != h {
		return nil, fmt.Errorf("lưới có %d hàng, cần %d", len(rows), h)
	}
	g := &Grid{W: w, H: h, cells: make([]bool, 0, w*h)}
	for y, row := range rows {
		n := 0
		num := ""
		for _, ch := range row {
			if ch >= '0' && ch <= '9' {
				num += string(ch)
				continue
			}
			k, err := strconv.Atoi(num)
			if err != nil || k < 1 {
				return nil, fmt.Errorf("hàng %d: số lặp không hợp lệ", y)
			}
			if ch != '.' && ch != '#' {
				return nil, fmt.Errorf("hàng %d: ký tự %q không hợp lệ", y, ch)
			}
			for i := 0; i < k; i++ {
				g.cells = append(g.cells, ch == '.')
			}
			n += k
			num = ""
		}
		if num != "" || n != w {
			return nil, fmt.Errorf("hàng %d có %d ô, cần %d", y, n, w)
		}
	}
	return g, nil
}

// Walkable báo ô (x, y) có đi được không.
func (g *Grid) Walkable(x, y int) bool {
	if g == nil || x < 0 || y < 0 || x >= g.W || y >= g.H {
		return false
	}
	return g.cells[y*g.W+x]
}

// Reachable trả tập ô đi tới được từ start theo 4 hướng.
func (g *Grid) Reachable(start Point) map[[2]int]bool {
	seen := map[[2]int]bool{}
	if !g.Walkable(start.X, start.Y) {
		return seen
	}
	q := [][2]int{{start.X, start.Y}}
	seen[q[0]] = true
	for len(q) > 0 {
		c := q[0]
		q = q[1:]
		for _, d := range [4][2]int{{1, 0}, {-1, 0}, {0, 1}, {0, -1}} {
			n := [2]int{c[0] + d[0], c[1] + d[1]}
			if !seen[n] && g.Walkable(n[0], n[1]) {
				seen[n] = true
				q = append(q, n)
			}
		}
	}
	return seen
}

// ReachesNear báo có ô nào trong tập reach nằm cách (x, y) không quá d (Chebyshev).
func ReachesNear(reach map[[2]int]bool, x, y, d int) bool {
	for dy := -d; dy <= d; dy++ {
		for dx := -d; dx <= d; dx++ {
			if reach[[2]int{x + dx, y + dy}] {
				return true
			}
		}
	}
	return false
}
