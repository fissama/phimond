package transport

import (
	"context"
	"crypto/sha256"
	"encoding/binary"
	"encoding/json"
	"errors"
	"log"
	"phimond/server/internal/character"
	"phimond/server/internal/persistence"
	"sync"
	"time"
)

const checkpointInterval = 2 * time.Second
const sessionValidationInterval = 30 * time.Second
const maxLiveCharacters = 128
const maxPendingMoves = 256

// A fixed-size filter proves that a new request has never been committed.
// Possible matches always consult durable receipts; false positives only cost
// a read, never cause a command to be dropped or applied twice.
type receiptFilter [8192]byte

func (f *receiptFilter) indexes(id string) [4]uint16 {
	h := sha256.Sum256([]byte(id))
	return [4]uint16{binary.LittleEndian.Uint16(h[0:2]), binary.LittleEndian.Uint16(h[2:4]), binary.LittleEndian.Uint16(h[4:6]), binary.LittleEndian.Uint16(h[6:8])}
}
func (f *receiptFilter) add(id string) {
	for _, i := range f.indexes(id) {
		f[i/8] |= 1 << (i % 8)
	}
}
func (f *receiptFilter) maybe(id string) bool {
	for _, i := range f.indexes(id) {
		if f[i/8]&(1<<(i%8)) == 0 {
			return false
		}
	}
	return true
}

type checkpoint struct {
	base, revision int
	raw            json.RawMessage
	ids            []string
}
type liveCharacter struct {
	mu                         sync.Mutex
	persistMu                  sync.Mutex
	raw                        json.RawMessage
	loaded, reload, saveFailed bool
	savedRevision              int
	filter                     receiptFilter
	pending                    []string
	pendingTimes               []time.Time
	pendingSet                 map[string]bool
	job                        *checkpoint
	refs                       int       // protected by Server.liveMu
	lastUsed                   time.Time // protected by Server.liveMu
}
type sessionEntry struct {
	id      string
	until   time.Time
	revoked bool
}

func (s *Server) acquireLive(id string) (*liveCharacter, error) {
	s.liveMu.Lock()
	defer s.liveMu.Unlock()
	e := s.live[id]
	if e == nil {
		if len(s.live) >= maxLiveCharacters {
			return nil, errors.New("world capacity reached; try again shortly")
		}
		e = &liveCharacter{pendingSet: map[string]bool{}, lastUsed: time.Now()}
		s.live[id] = e
	}
	e.refs++
	return e, nil
}
func (s *Server) releaseLive(e *liveCharacter) {
	s.liveMu.Lock()
	e.refs--
	e.lastUsed = time.Now()
	s.liveMu.Unlock()
}
func revision(raw json.RawMessage) (int, error) {
	var c struct {
		Revision int `json:"revision"`
	}
	err := json.Unmarshal(raw, &c)
	return c.Revision, err
}
func (s *Server) loadLive(ctx context.Context, id string, e *liveCharacter) error {
	if e.loaded && !e.reload {
		return nil
	}
	raw, err := s.Store.Read(ctx, id)
	if err != nil {
		return err
	}
	rev, err := revision(raw)
	if err != nil {
		return err
	}
	var filter receiptFilter
	if err = s.Store.Receipts(ctx, id, filter.add); err != nil {
		return err
	}
	e.raw = raw
	e.savedRevision = rev
	e.filter = filter
	e.loaded = true
	e.reload = false
	return nil
}
func (s *Server) readLive(ctx context.Context, id string) (json.RawMessage, error) {
	e, err := s.acquireLive(id)
	if err != nil {
		return nil, err
	}
	defer s.releaseLive(e)
	e.mu.Lock()
	defer e.mu.Unlock()
	if err = s.loadLive(ctx, id, e); err != nil {
		return nil, err
	}
	return e.raw, nil
}
func (s *Server) applyLive(ctx context.Context, id string, m envelope, fresh ...*bool) (json.RawMessage, error) {
	if s.metrics != nil && s.metrics.enabled {
		ctx = persistence.WithObservation(ctx, func(stage string, elapsed time.Duration, failed bool) {
			s.metrics.observe(stage, m.Op, elapsed, failed)
		})
	}
	markFresh := func(value bool) {
		if len(fresh) > 0 && fresh[0] != nil {
			*fresh[0] = value
		}
	}
	markFresh(false)
	if s.stopping.Load() {
		return nil, errors.New("server is shutting down")
	}
	if len(m.RequestID) == 0 || len(m.RequestID) > 128 {
		return nil, errors.New("invalid request ID")
	}
	if m.Op == "character.get" {
		return s.readLive(ctx, id)
	}
	e, err := s.acquireLive(id)
	if err != nil {
		return nil, err
	}
	defer s.releaseLive(e)
	waitStarted := time.Now()
	if m.Op != "world.move" {
		e.persistMu.Lock()
		defer e.persistMu.Unlock()
	}
	e.mu.Lock()
	defer e.mu.Unlock()
	s.metrics.observe("authority_wait", m.Op, time.Since(waitStarted), false)
	if s.stopping.Load() {
		return nil, errors.New("server is shutting down")
	}
	if err = s.loadLive(ctx, id, e); err != nil {
		return nil, err
	}
	if m.Op == "world.move" {
		if e.pendingSet[m.RequestID] {
			return e.raw, nil
		}
		if len(e.pending) >= maxPendingMoves {
			return nil, errors.New("waiting for movement checkpoint")
		}
		if e.filter.maybe(m.RequestID) {
			duplicate, err := s.Store.HasReceipt(ctx, id, m.RequestID)
			if err != nil {
				return nil, err
			}
			if duplicate {
				return e.raw, nil
			}
		}
		next, _, err := s.applyGame(e.raw, m)
		if err != nil {
			return nil, err
		}
		e.raw = next
		e.pending = append(e.pending, m.RequestID)
		e.pendingTimes = append(e.pendingTimes, time.Now())
		e.pendingSet[m.RequestID] = true
		e.filter.add(m.RequestID)
		markFresh(true)
		return e.raw, nil
	}
	// Persist walking before entering any durable action. The action callback
	// works on a copy and is never replayed automatically after an error.
	for len(e.pending) > 0 {
		if err = s.checkpointLocked(ctx, id, e, false); err != nil {
			return nil, err
		}
	}
	applied := false
	mutationStarted := time.Now()
	updated, err := s.Store.Mutate(ctx, id, m.RequestID, func(raw json.RawMessage) (json.RawMessage, []persistence.AuditEvent, error) {
		next, events, err := s.applyGame(raw, m)
		applied = err == nil
		return next, events, err
	})
	s.metrics.observe("durable_mutation", m.Op, time.Since(mutationStarted), err != nil)
	if err != nil {
		var de *domainError
		if !errors.As(err, &de) {
			e.reload = true
		} // COMMIT may have succeeded despite a lost acknowledgement.
		return nil, err
	}
	e.raw = updated
	e.savedRevision, _ = revision(updated)
	e.filter.add(m.RequestID)
	markFresh(applied)
	return e.raw, nil
}
func (s *Server) applyGame(raw json.RawMessage, m envelope) (json.RawMessage, []persistence.AuditEvent, error) {
	var c character.Character
	if err := json.Unmarshal(raw, &c); err != nil {
		return nil, nil, err
	}
	applyStarted := time.Now()
	events, err := s.Game.Apply(&c, m.Op, m.Data)
	s.metrics.observe("apply", m.Op, time.Since(applyStarted), err != nil)
	if err != nil {
		return nil, nil, &domainError{err}
	}
	audit := make([]persistence.AuditEvent, 0, len(events))
	for _, ev := range events {
		data, _ := json.Marshal(ev)
		audit = append(audit, persistence.AuditEvent{Type: ev.Type, Data: data})
	}
	next, err := json.Marshal(c)
	return next, audit, err
}

// Caller holds persistMu and mu. A background checkpoint releases mu during
// network I/O so authoritative walking remains responsive while MySQL saves.
func (s *Server) checkpointLocked(ctx context.Context, id string, e *liveCharacter, background bool) error {
	if len(e.pending) == 0 {
		return nil
	}
	if e.job == nil {
		rev, err := revision(e.raw)
		if err != nil {
			return err
		}
		e.job = &checkpoint{base: e.savedRevision, revision: rev, raw: e.raw, ids: append([]string{}, e.pending...)}
	}
	job := e.job
	if background {
		e.mu.Unlock()
	}
	started := time.Now()
	err := s.Store.Checkpoint(ctx, id, job.base, job.raw, job.ids)
	s.metrics.observe("checkpoint", "world.move", time.Since(started), err != nil)
	if background {
		e.mu.Lock()
	}
	if err != nil {
		e.saveFailed = true
		return err
	}
	e.savedRevision = job.revision
	s.metrics.observe("checkpoint_age", "world.move", time.Since(e.pendingTimes[0]), false)
	for _, id := range job.ids {
		delete(e.pendingSet, id)
	}
	e.pending = append([]string{}, e.pending[len(job.ids):]...)
	e.pendingTimes = append([]time.Time{}, e.pendingTimes[len(job.ids):]...)
	e.job = nil
	e.saveFailed = false
	return nil
}
func (s *Server) flushLive(ctx context.Context, id string) error {
	e, err := s.acquireLive(id)
	if err != nil {
		return err
	}
	defer s.releaseLive(e)
	e.persistMu.Lock()
	defer e.persistMu.Unlock()
	e.mu.Lock()
	defer e.mu.Unlock()
	for len(e.pending) > 0 {
		if err = s.checkpointLocked(ctx, id, e, false); err != nil {
			return err
		}
	}
	return nil
}
func (s *Server) checkpointAll(ctx context.Context) {
	s.liveMu.Lock()
	entries := make(map[string]*liveCharacter, len(s.live))
	for id, e := range s.live {
		e.refs++
		entries[id] = e
	}
	s.liveMu.Unlock()
	for id, e := range entries {
		e.persistMu.Lock()
		e.mu.Lock()
		err := s.checkpointLocked(ctx, id, e, true)
		e.mu.Unlock()
		e.persistMu.Unlock()
		if err != nil {
			log.Printf("movement checkpoint failed for character %s; new movement paused", id)
		}
		s.liveMu.Lock()
		e.refs--
		s.liveMu.Unlock()
	}
	// Eviction holds the map lock; refs prevents racing an acquired entry.
	s.liveMu.Lock()
	defer s.liveMu.Unlock()
	for id, e := range s.live {
		if e.refs == 0 && time.Since(e.lastUsed) > 5*time.Minute {
			e.mu.Lock()
			clean := len(e.pending) == 0
			e.mu.Unlock()
			if clean {
				delete(s.live, id)
			}
		}
	}
}
func (s *Server) checkpointLoop(ctx context.Context, interval time.Duration) {
	ticker := time.NewTicker(interval)
	defer ticker.Stop()
	for {
		select {
		case <-ctx.Done():
			return
		case <-ticker.C:
			s.checkpointAll(ctx)
		}
	}
}
func (s *Server) authenticateSession(ctx context.Context, token string) (string, error) {
	if len(token) != 64 || s.Store == nil {
		return "", persistence.ErrSession
	}
	now := time.Now()
	s.sessionMu.Lock()
	entry, ok := s.sessions[token]
	if ok && now.Before(entry.until) {
		s.sessionMu.Unlock()
		if entry.revoked {
			return "", persistence.ErrSession
		}
		return entry.id, nil
	}
	s.sessionMu.Unlock()
	// Never hold the cache lock across network I/O: another player's session
	// refresh must not block already authenticated walking.
	started := time.Now()
	id, err := s.Store.Authenticate(ctx, token)
	s.metrics.observe("session_validation", "auth.session", time.Since(started), err != nil)
	if err != nil {
		return "", err
	}
	s.sessionMu.Lock()
	defer s.sessionMu.Unlock()
	// Logout may have raced the DB query. Its local tombstone wins.
	if entry, ok = s.sessions[token]; ok && entry.revoked && time.Now().Before(entry.until) {
		return "", persistence.ErrSession
	}
	if len(s.sessions) >= 10000 {
		for key, value := range s.sessions {
			if now.After(value.until) {
				delete(s.sessions, key)
			}
		}
	}
	if len(s.sessions) >= 10000 {
		return "", errors.New("session capacity reached")
	}
	s.sessions[token] = sessionEntry{id: id, until: now.Add(sessionValidationInterval)}
	return id, nil
}
func (s *Server) logoutSession(ctx context.Context, token, id string) error {
	s.sessionMu.Lock()
	s.sessions[token] = sessionEntry{revoked: true, until: time.Now().Add(7 * 24 * time.Hour)}
	s.sessionMu.Unlock()
	// Attempt both: a failed movement save must not prevent token revocation.
	saveErr := s.flushLive(ctx, id)
	logoutErr := s.Store.Logout(ctx, token)
	return errors.Join(saveErr, logoutErr)
}
