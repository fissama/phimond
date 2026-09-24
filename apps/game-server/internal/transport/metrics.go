package transport

import (
	"context"
	"encoding/json"
	"log"
	"phimond/server/internal/persistence"
	"runtime"
	"sync"
	"time"
)

var latencyBoundsMS = [...]float64{1, 5, 10, 25, 50, 100, 250, 500, 1000, 5000, 15000}

type latencyStat struct {
	Count   uint64     `json:"count"`
	Errors  uint64     `json:"errors"`
	TotalMS float64    `json:"total_ms"`
	MaxMS   float64    `json:"max_ms"`
	Buckets [12]uint64 `json:"buckets_non_cumulative"`
}
type runtimeMetrics struct {
	enabled bool
	mu      sync.Mutex
	values  map[string]latencyStat
	bytes   map[string]uint64
}

func newRuntimeMetrics(enabled bool) *runtimeMetrics {
	return &runtimeMetrics{enabled: enabled, values: map[string]latencyStat{}, bytes: map[string]uint64{}}
}

func (m *runtimeMetrics) recordBytes(op string, size int) {
	if m == nil || !m.enabled || size < 0 {
		return
	}
	m.mu.Lock()
	defer m.mu.Unlock()
	m.bytes[metricOperation(op)] += uint64(size)
}
func (m *runtimeMetrics) byteSnapshot() map[string]uint64 {
	m.mu.Lock()
	defer m.mu.Unlock()
	out := make(map[string]uint64, len(m.bytes))
	for k, v := range m.bytes {
		out[k] = v
	}
	return out
}
func metricOperation(op string) string {
	switch op {
	case "world.move", "world.encounter", "world.portal", "battle.action", "character.get", "auth.session", "pet.activate", "pet.heal", "shop.buy", "quest.accept", "quest.claim":
		return op
	default:
		return "other"
	}
}
func (m *runtimeMetrics) observe(stage, op string, d time.Duration, failed bool) {
	if m == nil || !m.enabled {
		return
	}
	switch stage {
	case "response_ready", "socket_write", "apply", "durable_mutation", "checkpoint", "checkpoint_age", "session_validation", "db_begin", "db_lock_read", "db_receipt_read", "db_state_write", "db_pet_projection", "db_audit_write", "db_receipt_write", "db_commit", "authority_wait", "rejected_response":
	default:
		stage = "other"
	}
	ms := float64(d) / float64(time.Millisecond)
	key := stage + "/" + metricOperation(op)
	m.mu.Lock()
	defer m.mu.Unlock()
	stat := m.values[key]
	stat.Count++
	if failed {
		stat.Errors++
	}
	stat.TotalMS += ms
	if ms > stat.MaxMS {
		stat.MaxMS = ms
	}
	index := len(latencyBoundsMS)
	for i, bound := range latencyBoundsMS {
		if ms <= bound {
			index = i
			break
		}
	}
	stat.Buckets[index]++
	m.values[key] = stat
}
func (m *runtimeMetrics) snapshot() map[string]latencyStat {
	m.mu.Lock()
	defer m.mu.Unlock()
	out := make(map[string]latencyStat, len(m.values))
	for key, value := range m.values {
		out[key] = value
	}
	return out
}

// Opt-in aggregate logs: fixed labels, no account IDs, tokens, requests or DSNs.
func (s *Server) metricsLoop(ctx context.Context) {
	if !s.metrics.enabled {
		return
	}
	ticker := time.NewTicker(30 * time.Second)
	defer ticker.Stop()
	for {
		select {
		case <-ctx.Done():
			return
		case <-ticker.C:
			var mem runtime.MemStats
			runtime.ReadMemStats(&mem)
			report := map[string]any{"kind": "game_metrics", "at": time.Now().UTC(), "latency_upper_bounds_ms": latencyBoundsMS, "latencies": s.metrics.snapshot(), "heap_bytes": mem.HeapAlloc, "go_sys_bytes": mem.Sys, "gc_cycles": mem.NumGC, "goroutines": runtime.NumGoroutine()}
			report["outbound_payload_bytes"] = s.metrics.byteSnapshot()
			// Only atomic/ref-counted map counters here: don't hold the global map
			// lock while waiting on per-character DB locks just to collect metrics.
			s.liveMu.Lock()
			report["cached_characters"] = len(s.live)
			s.liveMu.Unlock()
			s.mu.Lock()
			connections := 0
			for _, count := range s.connections {
				connections += count
			}
			s.mu.Unlock()
			report["connections"] = connections
			if store, ok := s.Store.(*persistence.Store); ok {
				report["db_pool"] = store.DB.Stats()
			}
			raw, err := json.Marshal(report)
			if err == nil {
				log.Print(string(raw))
			}
		}
	}
}
