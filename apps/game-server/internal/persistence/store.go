package persistence

import (
	"context"
	"crypto/rand"
	"crypto/sha256"
	"database/sql"
	"encoding/hex"
	"encoding/json"
	"errors"
	"fmt"
	"reflect"
	"regexp"
	"strings"
	"time"

	"golang.org/x/crypto/bcrypt"
)

type Store struct {
	DB *sql.DB
	// MovementAllowedKeys is the character-state key set whose value may differ
	// between two checkpoints (e.g. x, revision, last_events). Loaded from
	// rules.json at startup; defaults to the historical hard-coded set so
	// existing tests and callers remain compatible when unset.
	MovementAllowedKeys []string
}
type AuditEvent struct {
	Type string
	Data json.RawMessage
}

// DefaultMovementAllowedKeys preserves the previously hard-coded behavior for
// stores that never received an explicit list (tests, legacy callers).
var DefaultMovementAllowedKeys = []string{"x", "y", "revision", "last_events"}

func (s *Store) movementAllowedKeys() []string {
	if len(s.MovementAllowedKeys) == 0 {
		return DefaultMovementAllowedKeys
	}
	return s.MovementAllowedKeys
}

var ErrCredentials = errors.New("invalid credentials")
var ErrSession = errors.New("invalid or expired session")
var usernamePattern = regexp.MustCompile(`^[A-Za-z0-9_]{3,24}$`)

func validateCredentials(username, password string) error {
	if !usernamePattern.MatchString(username) || len(password) < 10 || len(password) > 72 {
		return errors.New("username must be 3-24 ASCII letters, digits or underscores; password must be 10-72 bytes")
	}
	return nil
}
func randomID() (string, error) {
	b := make([]byte, 16)
	_, e := rand.Read(b)
	return hex.EncodeToString(b), e
}
func Open(ctx context.Context, c Config) (*Store, error) {
	db, e := connect(c, true)
	if e != nil {
		return nil, e
	}
	if e = verifyMarker(ctx, db, c.Database); e != nil {
		db.Close()
		return nil, e
	}
	return &Store{DB: db}, nil
}
func (s *Store) Close() error { return s.DB.Close() }
func newSession(ctx context.Context, tx *sql.Tx, id string) (string, error) {
	b := make([]byte, 32)
	if _, e := rand.Read(b); e != nil {
		return "", e
	}
	token := hex.EncodeToString(b)
	h := sha256.Sum256([]byte(token))
	_, e := tx.ExecContext(ctx, "INSERT INTO sessions(token_hash,account_id,expires_at) VALUES (?,?,?)", h[:], id, time.Now().UTC().Add(7*24*time.Hour))
	return token, e
}
func (s *Store) Register(ctx context.Context, username, password string, initial func(string) (json.RawMessage, error)) (string, string, error) {
	if e := validateCredentials(username, password); e != nil {
		return "", "", e
	}
	hash, e := bcrypt.GenerateFromPassword([]byte(password), bcrypt.DefaultCost)
	if e != nil {
		return "", "", e
	}
	id, e := randomID()
	if e != nil {
		return "", "", e
	}
	raw, e := initial(id)
	if e != nil {
		return "", "", e
	}
	if e = validateState(raw, id); e != nil {
		return "", "", e
	}
	tx, e := s.DB.BeginTx(ctx, nil)
	if e != nil {
		return "", "", e
	}
	defer tx.Rollback()
	if _, e = tx.ExecContext(ctx, "INSERT INTO accounts(id,username,password_hash) VALUES (?,?,?)", id, username, hash); e != nil {
		return "", "", errors.New("account registration failed")
	}
	if _, e = tx.ExecContext(ctx, "INSERT INTO characters(id,account_id,state) VALUES (?,?,?)", id, id, string(raw)); e != nil {
		return "", "", e
	}
	if e = projectPets(ctx, tx, id, raw); e != nil {
		return "", "", e
	}
	token, e := newSession(ctx, tx, id)
	if e != nil {
		return "", "", e
	}
	if e = tx.Commit(); e != nil {
		return "", "", e
	}
	return token, id, nil
}
func (s *Store) Login(ctx context.Context, username, password string) (string, string, error) {
	if validateCredentials(username, password) != nil {
		return "", "", ErrCredentials
	}
	var id string
	var hash []byte
	if e := s.DB.QueryRowContext(ctx, "SELECT id,password_hash FROM accounts WHERE username=?", username).Scan(&id, &hash); e != nil {
		return "", "", ErrCredentials
	}
	if bcrypt.CompareHashAndPassword(hash, []byte(password)) != nil {
		return "", "", ErrCredentials
	}
	tx, e := s.DB.BeginTx(ctx, nil)
	if e != nil {
		return "", "", e
	}
	defer tx.Rollback()
	token, e := newSession(ctx, tx, id)
	if e != nil {
		return "", "", e
	}
	if e = tx.Commit(); e != nil {
		return "", "", e
	}
	return token, id, nil
}
func (s *Store) Authenticate(ctx context.Context, token string) (string, error) {
	if len(token) != 64 {
		return "", ErrSession
	}
	h := sha256.Sum256([]byte(token))
	var id string
	if e := s.DB.QueryRowContext(ctx, "SELECT account_id FROM sessions WHERE token_hash=? AND expires_at>UTC_TIMESTAMP(6)", h[:]).Scan(&id); e != nil {
		if errors.Is(e, sql.ErrNoRows) {
			return "", ErrSession
		}
		return "", e
	}
	return id, nil
}
func (s *Store) Logout(ctx context.Context, token string) error {
	h := sha256.Sum256([]byte(token))
	_, e := s.DB.ExecContext(ctx, "DELETE FROM sessions WHERE token_hash=?", h[:])
	return e
}
func (s *Store) Read(ctx context.Context, id string) (json.RawMessage, error) {
	var raw []byte
	e := s.DB.QueryRowContext(ctx, "SELECT state FROM characters WHERE id=?", id).Scan(&raw)
	return json.RawMessage(raw), e
}
func validateState(raw json.RawMessage, id string) error {
	var v struct {
		ID string `json:"id"`
	}
	if json.Unmarshal(raw, &v) != nil || v.ID != id {
		return errors.New("character identity mismatch or invalid JSON")
	}
	return nil
}
func (s *Store) Mutate(ctx context.Context, id, requestID string, fn func(json.RawMessage) (json.RawMessage, []AuditEvent, error)) (json.RawMessage, error) {
	if len(requestID) == 0 || len(requestID) > 128 {
		return nil, errors.New("request_id required, maximum 128 bytes")
	}
	done := observeStage(ctx, "db_begin")
	tx, e := s.DB.BeginTx(ctx, nil)
	done(e)
	if e != nil {
		return nil, e
	}
	defer tx.Rollback()
	var raw []byte
	done = observeStage(ctx, "db_lock_read")
	e = tx.QueryRowContext(ctx, "SELECT state FROM characters WHERE id=? FOR UPDATE", id).Scan(&raw)
	done(e)
	if e != nil {
		return nil, e
	}
	var count int
	done = observeStage(ctx, "db_receipt_read")
	e = tx.QueryRowContext(ctx, "SELECT COUNT(*) FROM command_receipts WHERE character_id=? AND request_id=?", id, requestID).Scan(&count)
	done(e)
	if e != nil {
		return nil, e
	}
	if count > 0 {
		return json.RawMessage(raw), nil
	}
	updated, events, e := fn(json.RawMessage(raw))
	if e != nil {
		return nil, e
	}
	if e = validateState(updated, id); e != nil {
		return nil, e
	}
	done = observeStage(ctx, "db_state_write")
	_, e = tx.ExecContext(ctx, "UPDATE characters SET state=? WHERE id=?", string(updated), id)
	done(e)
	if e != nil {
		return nil, e
	}
	if petsChanged(raw, updated) {
		done = observeStage(ctx, "db_pet_projection")
		e = projectPets(ctx, tx, id, updated)
		done(e)
		if e != nil {
			return nil, e
		}
	}

	if len(events) > 0 {
		values := make([]string, 0, len(events))
		args := make([]any, 0, len(events)*4)
		for _, event := range events {
			data := event.Data
			if len(data) == 0 {
				data = json.RawMessage(`{}`)
			}
			values = append(values, "(?,?,?,?)")
			args = append(args, id, requestID, event.Type, string(data))
		}
		done = observeStage(ctx, "db_audit_write")
		_, e = tx.ExecContext(ctx, "INSERT INTO audit_events(character_id,request_id,event_type,data) VALUES "+strings.Join(values, ","), args...)
		done(e)
		if e != nil {
			return nil, e
		}
	}

	done = observeStage(ctx, "db_receipt_write")
	_, e = tx.ExecContext(ctx, "INSERT INTO command_receipts(character_id,request_id) VALUES (?,?)", id, requestID)
	done(e)
	if e != nil {
		return nil, e
	}
	done = observeStage(ctx, "db_commit")
	e = tx.Commit()
	done(e)
	if e != nil {
		return nil, e
	}
	return updated, nil
}
func projectPets(ctx context.Context, tx *sql.Tx, id string, raw json.RawMessage) error {
	var state struct {
		Pets []json.RawMessage `json:"pets"`
	}
	if e := json.Unmarshal(raw, &state); e != nil {
		return e
	}
	type pet struct {
		ID        string   `json:"id"`
		SpeciesID string   `json:"species_id"`
		Parents   []string `json:"parents"`
		Retired   bool     `json:"retired"`
	}
	pets := make([]pet, 0, len(state.Pets))
	seen := map[string]bool{}
	for _, data := range state.Pets {
		var p pet
		if e := json.Unmarshal(data, &p); e != nil {
			return e
		}
		if p.ID == "" || p.SpeciesID == "" || seen[p.ID] {
			return errors.New("invalid pet projection")
		}
		seen[p.ID] = true
		pets = append(pets, p)
		var owner string
		e := tx.QueryRowContext(ctx, "SELECT character_id FROM pets WHERE id=?", p.ID).Scan(&owner)
		if e != nil && !errors.Is(e, sql.ErrNoRows) {
			return e
		}
		if e == nil && owner != id {
			return errors.New("pet belongs to another character")
		}
		if errors.Is(e, sql.ErrNoRows) {
			_, e = tx.ExecContext(ctx, "INSERT INTO pets(id,character_id,species_id,retired,data) VALUES (?,?,?,?,?)", p.ID, id, p.SpeciesID, p.Retired, string(data))
		} else {
			_, e = tx.ExecContext(ctx, "UPDATE pets SET species_id=?,retired=?,data=? WHERE id=? AND character_id=?", p.SpeciesID, p.Retired, string(data), p.ID, id)
		}
		if e != nil {
			return e
		}
	}
	for _, p := range pets {
		for _, parent := range p.Parents {
			if parent == p.ID {
				return errors.New("pet cannot parent itself")
			}
			var owner string
			if e := tx.QueryRowContext(ctx, "SELECT character_id FROM pets WHERE id=?", parent).Scan(&owner); e != nil {
				return e
			}
			if owner != id {
				return errors.New("parent belongs to another character")
			}
			if _, e := tx.ExecContext(ctx, "INSERT IGNORE INTO pet_ancestry(child_id,parent_id) VALUES (?,?)", p.ID, parent); e != nil {
				return e
			}
		}
	}
	return nil
}

// Receipts is streamed into the transport's fixed-size membership filter.
func (s *Store) Receipts(ctx context.Context, id string, visit func(string)) error {
	rows, err := s.DB.QueryContext(ctx, "SELECT request_id FROM command_receipts WHERE character_id=?", id)
	if err != nil {
		return err
	}
	defer rows.Close()
	for rows.Next() {
		var requestID string
		if err = rows.Scan(&requestID); err != nil {
			return err
		}
		visit(requestID)
	}
	return rows.Err()
}
func (s *Store) HasReceipt(ctx context.Context, id, requestID string) (bool, error) {
	var n int
	err := s.DB.QueryRowContext(ctx, "SELECT COUNT(*) FROM command_receipts WHERE character_id=? AND request_id=?", id, requestID).Scan(&n)
	return n > 0, err
}

var ErrRevisionConflict = errors.New("character changed outside the live authority")

// Checkpoint writes position and every acknowledged movement receipt in one
// transaction. Retrying the identical checkpoint is safe after an uncertain
// COMMIT: it verifies both its durable receipt and exact resulting state.
func (s *Store) Checkpoint(ctx context.Context, id string, base int, next json.RawMessage, ids []string) error {
	if len(ids) == 0 || len(ids) > 256 {
		return errors.New("invalid checkpoint size")
	}
	for _, requestID := range ids {
		if len(requestID) == 0 || len(requestID) > 128 {
			return errors.New("invalid movement receipt")
		}
	}
	if err := validateState(next, id); err != nil {
		return err
	}
	tx, err := s.DB.BeginTx(ctx, nil)
	if err != nil {
		return err
	}
	defer tx.Rollback()
	var raw []byte
	if err = tx.QueryRowContext(ctx, "SELECT state FROM characters WHERE id=? FOR UPDATE", id).Scan(&raw); err != nil {
		return err
	}
	var count int
	if err = tx.QueryRowContext(ctx, "SELECT COUNT(*) FROM command_receipts WHERE character_id=? AND request_id=?", id, ids[0]).Scan(&count); err != nil {
		return err
	}
	if count > 0 {
		if sameJSON(raw, next) {
			return nil
		}
		return ErrRevisionConflict
	}
	var oldState, newState map[string]any
	if err = json.Unmarshal(raw, &oldState); err != nil {
		return err
	}
	if err = json.Unmarshal(next, &newState); err != nil {
		return err
	}
	if oldState["revision"] != float64(base) || newState["revision"] != float64(base+len(ids)) {
		return ErrRevisionConflict
	}
	// Walking cannot checkpoint inventory, pets, RNG, quests or economic changes.
	for _, key := range s.movementAllowedKeys() {
		delete(oldState, key)
		delete(newState, key)
	}
	if !reflect.DeepEqual(oldState, newState) {
		return errors.New("checkpoint modified non-movement state")
	}
	if _, err = tx.ExecContext(ctx, "UPDATE characters SET state=? WHERE id=?", string(next), id); err != nil {
		return err
	}
	args := make([]any, 0, len(ids)*2)
	values := make([]string, 0, len(ids))
	for _, requestID := range ids {
		values = append(values, "(?,?)")
		args = append(args, id, requestID)
	}
	if _, err = tx.ExecContext(ctx, "INSERT INTO command_receipts(character_id,request_id) VALUES "+strings.Join(values, ","), args...); err != nil {
		return err
	}
	if err = tx.Commit(); err != nil {
		return fmt.Errorf("checkpoint commit outcome uncertain: %w", err)
	}
	return nil
}
func sameJSON(a, b json.RawMessage) bool {
	var x, y any
	return json.Unmarshal(a, &x) == nil && json.Unmarshal(b, &y) == nil && reflect.DeepEqual(x, y)
}
func petsChanged(a, b json.RawMessage) bool {
	var x, y struct {
		Pets any `json:"pets"`
	}
	return json.Unmarshal(a, &x) != nil || json.Unmarshal(b, &y) != nil || !reflect.DeepEqual(x.Pets, y.Pets)
}
