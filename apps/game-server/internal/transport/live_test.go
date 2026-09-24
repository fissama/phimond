package transport

import (
	"context"
	"encoding/json"
	"errors"
	"fmt"
	"net/http/httptest"
	"phimond/server/internal/character"
	"phimond/server/internal/content"
	"phimond/server/internal/persistence"
	"strings"
	"sync"
	"testing"
	"time"
)

type memoryStore struct {
	sync.Mutex
	raw                                             json.RawMessage
	receipts                                        map[string]bool
	failSave, failAction, uncertainAction, failAuth bool
	saveStarted, saveRelease                        chan struct{}
	uncertainSave                                   bool
	saves, auths, receiptReads                      int
}

func (m *memoryStore) Register(context.Context, string, string, func(string) (json.RawMessage, error)) (string, string, error) {
	panic("unused")
}
func (m *memoryStore) Login(context.Context, string, string) (string, string, error) { panic("unused") }
func (m *memoryStore) Authenticate(context.Context, string) (string, error) {
	m.Lock()
	defer m.Unlock()
	m.auths++
	if m.failAuth {
		return "", errors.New("database offline")
	}
	return "hero", nil
}
func (m *memoryStore) Logout(context.Context, string) error { return nil }
func (m *memoryStore) Read(context.Context, string) (json.RawMessage, error) {
	m.Lock()
	defer m.Unlock()
	return append(json.RawMessage{}, m.raw...), nil
}
func (m *memoryStore) Receipts(_ context.Context, _ string, visit func(string)) error {
	m.Lock()
	defer m.Unlock()
	for id := range m.receipts {
		visit(id)
	}
	return nil
}
func (m *memoryStore) HasReceipt(_ context.Context, _, id string) (bool, error) {
	m.Lock()
	defer m.Unlock()
	m.receiptReads++
	return m.receipts[id], nil
}
func (m *memoryStore) Checkpoint(_ context.Context, _ string, base int, raw json.RawMessage, ids []string) error {
	m.Lock()
	defer m.Unlock()
	m.saves++
	if m.saveStarted != nil {
		close(m.saveStarted)
		<-m.saveRelease
		m.saveStarted = nil
	}
	if m.failSave {
		return errors.New("database offline")
	}
	if m.receipts[ids[0]] {
		return nil
	}
	var c character.Character
	json.Unmarshal(m.raw, &c)
	if c.Revision != base {
		return errors.New("revision conflict")
	}
	m.raw = append(json.RawMessage{}, raw...)
	for _, id := range ids {
		m.receipts[id] = true
	}
	if m.uncertainSave {
		m.uncertainSave = false
		return errors.New("lost checkpoint acknowledgement")
	}
	return nil
}
func (m *memoryStore) Mutate(_ context.Context, _, id string, fn func(json.RawMessage) (json.RawMessage, []persistence.AuditEvent, error)) (json.RawMessage, error) {
	m.Lock()
	defer m.Unlock()
	if m.receipts[id] {
		return m.raw, nil
	}
	next, _, err := fn(m.raw)
	if err != nil {
		return nil, err
	}
	if m.failAction {
		return nil, errors.New("rollback")
	}
	m.raw = next
	m.receipts[id] = true
	if m.uncertainAction {
		m.uncertainAction = false
		return nil, errors.New("lost commit acknowledgement")
	}
	return next, nil
}
func liveFixture(t *testing.T) (*Server, *memoryStore) {
	t.Helper()
	catalog, err := content.Load("../../../../data")
	if err != nil {
		t.Fatal(err)
	}
	e := character.NewEngine(catalog)
	raw, _ := json.Marshal(e.NewCharacter("hero", "Hero", 5))
	db := &memoryStore{raw: raw, receipts: map[string]bool{}}
	return New(db, e), db
}
func move(id, dir string) envelope {
	return envelope{Op: "world.move", RequestID: id, Data: json.RawMessage(`{"direction":"` + dir + `"}`)}
}
func loadCharacter(t *testing.T, raw json.RawMessage) *character.Character {
	t.Helper()
	var c character.Character
	if err := json.Unmarshal(raw, &c); err != nil {
		t.Fatal(err)
	}
	return &c
}
func TestMovementSharedReadDedupAndCheckpoint(t *testing.T) {
	s, db := liveFixture(t)
	ctx := context.Background()
	raw, err := s.applyLive(ctx, "hero", move("walk1", "right"))
	if err != nil {
		t.Fatal(err)
	}
	if got := loadCharacter(t, raw); got.X != 7 || got.Revision != 1 {
		t.Fatal(got)
	}
	raw, err = s.applyLive(ctx, "hero", move("walk1", "right"))
	if err != nil || loadCharacter(t, raw).X != 7 {
		t.Fatal("duplicate moved", err)
	}
	raw, err = s.readLive(ctx, "hero")
	if err != nil || loadCharacter(t, raw).X != 7 {
		t.Fatal("shared read stale", err)
	}
	if db.saves != 0 || db.receiptReads != 0 {
		t.Fatal("walking performed synchronous database work")
	}
	if err = s.flushLive(ctx, "hero"); err != nil {
		t.Fatal(err)
	}
	if loadCharacter(t, db.raw).X != 7 || !db.receipts["walk1"] {
		t.Fatal("checkpoint missed position or receipt")
	}
	restarted := New(db, s.Game)
	raw, err = restarted.applyLive(ctx, "hero", move("walk1", "right"))
	if err != nil || loadCharacter(t, raw).X != 7 {
		t.Fatal("restart replayed persisted move", err)
	}
}
func TestDurableFailureKeepsSavedMovementButRollsBackEconomy(t *testing.T) {
	s, db := liveFixture(t)
	ctx := context.Background()
	s.applyLive(ctx, "hero", move("walk", "right"))
	db.failAction = true
	_, err := s.applyLive(ctx, "hero", envelope{Op: "shop.buy", RequestID: "buy", Data: json.RawMessage(`{"item_id":"potion","quantity":1}`)})
	if err == nil {
		t.Fatal("expected persistence failure")
	}
	raw, err := s.readLive(ctx, "hero")
	c := loadCharacter(t, raw)
	if err != nil || c.X != 7 || c.Gold != 100 || c.Inventory["potion"] != 5 || db.receipts["buy"] {
		t.Fatal("failed purchase leaked", c, err)
	}
}
func TestUncertainDurableCommitReloadsWithoutReplaying(t *testing.T) {
	s, db := liveFixture(t)
	ctx := context.Background()
	db.uncertainAction = true
	cmd := envelope{Op: "shop.buy", RequestID: "buy", Data: json.RawMessage(`{"item_id":"potion","quantity":1}`)}
	if _, err := s.applyLive(ctx, "hero", cmd); err == nil {
		t.Fatal("expected uncertain outcome")
	}
	raw, err := s.readLive(ctx, "hero")
	if err != nil {
		t.Fatal(err)
	}
	c := loadCharacter(t, raw)
	if c.Inventory["potion"] != 6 {
		t.Fatal("did not reload committed state")
	}
	raw, err = s.applyLive(ctx, "hero", cmd)
	if err != nil || loadCharacter(t, raw).Gold != c.Gold {
		t.Fatal("replayed uncertain purchase", err)
	}
}
func TestCheckpointFailureQueuesMovesAndDrainsOnRecovery(t *testing.T) {
	s, db := liveFixture(t)
	ctx := context.Background()
	s.applyLive(ctx, "hero", move("walk", "right"))
	db.failSave = true
	if err := s.flushLive(ctx, "hero"); err == nil {
		t.Fatal("expected save failure")
	}
	// Fail-soft contract: world.move stays available during a transient
	// checkpoint outage. The in-memory state advances and the receipt is
	// queued; the next successful checkpoint (or flush) commits the receipt
	// and character state together. Movement is non-economy-critical, so
	// eventual consistency is preferred over rejecting user input.
	raw, err := s.applyLive(ctx, "hero", move("walk2", "right"))
	if err != nil {
		t.Fatal("movement should still be accepted while checkpoint is failing", err)
	}
	if c := loadCharacter(t, raw); c.X != 8 {
		t.Fatal("in-memory state did not advance", c.X)
	}
	db.failSave = false
	if err := s.flushLive(ctx, "hero"); err != nil {
		t.Fatal(err)
	}
	raw, err = s.applyLive(ctx, "hero", move("walk3", "right"))
	if err != nil || loadCharacter(t, raw).X != 9 {
		t.Fatal("could not resume", err)
	}
}
func TestConcurrentConnectionsShareRevisionAndDedup(t *testing.T) {
	s, _ := liveFixture(t)
	ctx := context.Background()
	var wg sync.WaitGroup
	for i := 0; i < 3; i++ {
		wg.Add(1)
		go func() {
			defer wg.Done()
			if _, err := s.applyLive(ctx, "hero", move("same", "right")); err != nil {
				t.Error(err)
			}
		}()
	}
	wg.Wait()
	raw, err := s.readLive(ctx, "hero")
	if err != nil || loadCharacter(t, raw).Revision != 1 {
		t.Fatal("concurrent duplicate applied", err)
	}
}
func TestAuthCacheAndLogoutRevocation(t *testing.T) {
	s, db := liveFixture(t)
	ctx := context.Background()
	token := strings.Repeat("a", 64)
	for i := 0; i < 3; i++ {
		if _, err := s.authenticateSession(ctx, token); err != nil {
			t.Fatal(err)
		}
	}
	if db.auths != 1 {
		t.Fatal("requeried session for every action")
	}
	if err := s.logoutSession(ctx, token, "hero"); err != nil {
		t.Fatal(err)
	}
	if _, err := s.authenticateSession(ctx, token); !errors.Is(err, persistence.ErrSession) {
		t.Fatal("logout not revoked")
	}
}
func TestAuthOutageIsNotExpiredSession(t *testing.T) {
	s, db := liveFixture(t)
	db.failAuth = true
	if _, err := s.authenticateSession(context.Background(), strings.Repeat("a", 64)); err == nil || errors.Is(err, persistence.ErrSession) {
		t.Fatal("database failure confused with expiry", err)
	}
}
func TestCheckpointLoopPersistsWithoutAnotherInput(t *testing.T) {
	s, db := liveFixture(t)
	ctx, cancel := context.WithCancel(context.Background())
	defer cancel()
	done := make(chan struct{})
	go func() { s.checkpointLoop(ctx, 10*time.Millisecond); close(done) }()
	s.applyLive(ctx, "hero", move("idle", "right"))
	deadline := time.Now().Add(time.Second)
	for time.Now().Before(deadline) {
		db.Lock()
		saved := db.receipts["idle"]
		db.Unlock()
		if saved {
			cancel()
			<-done
			return
		}
		time.Sleep(5 * time.Millisecond)
	}
	t.Fatal("idle movement not saved")
}

func TestBackgroundCheckpointDoesNotBlockMovesAndRetainsTail(t *testing.T) {
	s, db := liveFixture(t)
	ctx := context.Background()
	s.applyLive(ctx, "hero", move("one", "right"))
	db.saveStarted = make(chan struct{})
	db.saveRelease = make(chan struct{})
	done := make(chan struct{})
	go func() { s.checkpointAll(ctx); close(done) }()
	<-db.saveStarted
	moved := make(chan error, 1)
	go func() { _, err := s.applyLive(ctx, "hero", move("two", "right")); moved <- err }()
	select {
	case err := <-moved:
		if err != nil {
			t.Fatal(err)
		}
	case <-time.After(time.Second):
		close(db.saveRelease)
		t.Fatal("database save blocked walking")
	}
	close(db.saveRelease)
	<-done
	if err := s.flushLive(ctx, "hero"); err != nil {
		t.Fatal(err)
	}
	if loadCharacter(t, db.raw).X != 8 || !db.receipts["one"] || !db.receipts["two"] {
		t.Fatal("checkpoint discarded movements received during save")
	}
}
func TestUncertainCheckpointRetriesIdenticalBatch(t *testing.T) {
	s, db := liveFixture(t)
	ctx := context.Background()
	s.applyLive(ctx, "hero", move("one", "right"))
	db.uncertainSave = true
	if err := s.flushLive(ctx, "hero"); err == nil {
		t.Fatal("expected uncertain commit")
	}
	if err := s.flushLive(ctx, "hero"); err != nil {
		t.Fatal(err)
	}
	raw, err := s.applyLive(ctx, "hero", move("one", "right"))
	if err != nil || loadCharacter(t, raw).X != 7 {
		t.Fatal("replayed checkpoint", err)
	}
}
func TestReceiptFilterFalsePositiveChecksDatabase(t *testing.T) {
	s, _ := liveFixture(t)
	ctx := context.Background()
	s.readLive(ctx, "hero")
	entry := s.live["hero"]
	for i := range entry.filter {
		entry.filter[i] = 255
	}
	raw, err := s.applyLive(ctx, "hero", move("new", "right"))
	if err != nil || loadCharacter(t, raw).X != 7 {
		t.Fatal("false positive dropped new request", err)
	}
}
func TestInvalidMovementDoesNotConsumeRevisionOrReceipt(t *testing.T) {
	s, db := liveFixture(t)
	ctx := context.Background()
	if _, err := s.applyLive(ctx, "hero", move("bad", "diagonal")); err == nil {
		t.Fatal("invalid move accepted")
	}
	raw, err := s.readLive(ctx, "hero")
	if err != nil || loadCharacter(t, raw).Revision != 0 || len(db.receipts) != 0 {
		t.Fatal("invalid move mutated state", err)
	}
}

// Test2DMovement4Directions exercises all four cardinal world.move directions
// and verifies state.x / state.y advance correctly. The fixture's Severa map
// is 40×24 so all four moves are in-bounds.
func Test2DMovement4Directions(t *testing.T) {
	s, _ := liveFixture(t)
	ctx := context.Background()
	steps := []struct {
		dir    string
		expect struct{ x, y int }
	}{
		{"right", struct{ x, y int }{7, 12}},
		{"down", struct{ x, y int }{7, 13}},
		{"left", struct{ x, y int }{6, 13}},
		{"up", struct{ x, y int }{6, 12}},
	}
	for i, step := range steps {
		raw, err := s.applyLive(ctx, "hero", move(fmt.Sprintf("mv%d", i), step.dir))
		if err != nil {
			t.Fatalf("step %d (%s) failed: %v", i, step.dir, err)
		}
		got := loadCharacter(t, raw)
		if got.X != step.expect.x || got.Y != step.expect.y {
			t.Fatalf("step %d (%s): expected x=%d y=%d, got x=%d y=%d",
				i, step.dir, step.expect.x, step.expect.y, got.X, got.Y)
		}
	}
}

// Test2DMovementOutOfBounds rejects vertical/horizontal moves that fall off
// the map (24 rows tall, 40 wide).
func Test2DMovementOutOfBounds(t *testing.T) {
	s, _ := liveFixture(t)
	ctx := context.Background()
	// Walk up 12 times — should reach y=0 then fail.
	for i := 0; i < 12; i++ {
		if _, err := s.applyLive(ctx, "hero", move(fmt.Sprintf("up%d", i), "up")); err != nil {
			t.Fatalf("step %d: %v", i, err)
		}
	}
	// Now y=0; one more up should fail.
	if _, err := s.applyLive(ctx, "hero", move("upTop", "up")); err == nil {
		t.Fatal("expected up at y=0 to be rejected")
	}
}

func TestHTTPAuthOutageReturns503(t *testing.T) {
	s, db := liveFixture(t)
	db.failAuth = true
	r := httptest.NewRequest("GET", "/api/character", nil)
	r.Header.Set("Authorization", "Bearer "+strings.Repeat("a", 64))
	w := httptest.NewRecorder()
	s.Handler().ServeHTTP(w, r)
	if w.Code != 503 {
		t.Fatalf("database outage status=%d, want503", w.Code)
	}
}
func TestSessionCacheRevalidatesAfterBoundedInterval(t *testing.T) {
	s, db := liveFixture(t)
	ctx := context.Background()
	token := strings.Repeat("a", 64)
	s.authenticateSession(ctx, token)
	s.sessions[token] = sessionEntry{id: "hero", until: time.Now().Add(-time.Second)}
	db.failAuth = true
	if _, err := s.authenticateSession(ctx, token); err == nil || errors.Is(err, persistence.ErrSession) {
		t.Fatal("expired cache masked database failure", err)
	}
}
