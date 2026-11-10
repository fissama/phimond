package persistence

import (
	"os"
	"path/filepath"
	"reflect"
	"strings"
	"testing"
)

func TestSplitSQL(t *testing.T) {
	got := splitSQL("-- ghi chú; có chấm phẩy\nCREATE TABLE a (x INT); # nữa; đây\nINSERT INTO a VALUES ('a;b', \"c;d\", 'it''s'); /* khối; chú thích */ ALTER TABLE `a;b` ADD y INT;\n\n")
	want := []string{"CREATE TABLE a (x INT)", "INSERT INTO a VALUES ('a;b', \"c;d\", 'it''s')", "ALTER TABLE `a;b` ADD y INT"}
	if !reflect.DeepEqual(got, want) {
		t.Fatalf("got %q", got)
	}
}

// Mọi migration đã có phải tách ra đúng câu lệnh DDL, không còn mảnh chú thích.
func TestSplitSQLOnCheckedInMigrations(t *testing.T) {
	files, _ := filepath.Glob("../../../../migrations/*.sql")
	if len(files) < 3 {
		t.Fatalf("không thấy migration: %v", files)
	}
	want := map[string]int{"001_initial.sql": -1, "002_character_slots.sql": -1, "003_account_recovery.sql": 3}
	for _, f := range files {
		b, err := os.ReadFile(f)
		if err != nil {
			t.Fatal(err)
		}
		stmts := splitSQL(string(b))
		if len(stmts) == 0 {
			t.Fatalf("%s: không có câu lệnh", f)
		}
		for _, st := range stmts {
			head := strings.ToUpper(strings.Fields(st)[0])
			switch head {
			case "CREATE", "ALTER", "INSERT", "UPDATE", "DROP", "SET":
			default:
				t.Fatalf("%s: câu lệnh lạ %q", f, st)
			}
			if strings.Contains(st, "--") {
				t.Fatalf("%s: còn chú thích trong %q", f, st)
			}
		}
		if n := want[filepath.Base(f)]; n > 0 && len(stmts) != n {
			t.Fatalf("%s: %d câu lệnh, mong đợi %d", f, len(stmts), n)
		}
	}
}
