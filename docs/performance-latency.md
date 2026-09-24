# Gameplay latency and persistence

Measured on 2026-09-17 against the running localhost HTTP/WebSocket server and the existing dedicated remote MySQL schema. The benchmark creates isolated random accounts and prints no passwords or tokens. Accounts remain as test fixtures; their sessions are logged out.

## Baseline

`rtk proxy node tools/latency.mjs` (20 movement samples, 100 ms between requests):

| Operation | Samples | Median | p95 |
| --- | ---: | ---: | ---: |
| Walking | 20 | 950.09 ms | 1310.92 ms |
| HTTP character read | 5 | 211.84 ms | 261.54 ms |
| Shop purchase | 1 | 1170.65 ms | 1170.65 ms |

`rtk proxy env LATENCY_SAMPLES=10 LATENCY_BATTLE=1 node tools/latency.mjs` additionally walks a fresh character through the forest portal and executes five defend turns:

| Operation | Samples | Median | p95 |
| --- | ---: | ---: | ---: |
| Walking | 10 | 833.19 ms | 1148.19 ms |
| Battle action | 5 | 1196.29 ms | 1238.02 ms |
| Encounter | 1 | 965.28 ms | 965.28 ms |
| Portal | 1 | 969.55 ms | 969.55 ms |

## Changes

- Authoritative `world.move` uses the existing game validation and copy-on-success logic, then updates shared per-character state. All HTTP reads and WebSocket connections consult that same state. No client position, reward, combat result or damage value is trusted.
- A background checkpoint runs every two seconds. Its database work releases the movement mutex, so new validated movement continues during a save. The checkpoint atomically persists a position snapshot and all corresponding request receipts. Movement received during the save remains queued for the next checkpoint.
- Durable operations acquire a persistence barrier, save outstanding movement, and then use the existing transactional mutation path. A rejected or rolled-back purchase cannot alter gold or inventory. After an uncertain durable commit, the next operation reloads database state and receipts; the action is never automatically replayed.
- Checkpoints retain their exact snapshot and receipt batch until success. A retry checks the durable receipt and state, preventing double application after a lost commit acknowledgement. Revision conflicts fail closed.
- Receipt deduplication retains the full historical database receipt contract. Each active character has an 8 KiB Bloom filter loaded from all durable receipts. A negative result avoids database I/O; possible matches query durable receipts. Pending movement IDs are checked directly. Filter false positives can only add a database read.
- Successful session validation is cached for at most 30 seconds. Local logout revokes the token immediately, including validation queries racing with logout. Database authentication failures produce HTTP 503 / WebSocket 1011 rather than falsely reporting session expiry.
- Unchanged pets are no longer rewritten by ordinary actions. Audit rows are inserted in one batch per action. MySQL driver parameter interpolation safely escapes parameters while avoiding separate prepare/execute/close round trips. JSON values are passed as text, preserving MySQL JSON charset compatibility.
- Logout, disconnect and graceful shutdown attempt to flush pending movement. New actions stop during shutdown. The existing 400-actions-per-minute and three-connections-per-character limits remain unchanged.

## Operational limits

This live authority is for a **single game-server process**. Do not run independent authoritative processes against the same characters without adding shared ownership/coordination. Checkpoints detect revision conflicts rather than overwrite another writer.

Walking acknowledgements are intentionally not individual durable commits. A hard process crash can lose position changes since the last completed checkpoint: normally the two-second interval plus save time. A prolonged database failure pauses new movement after the first failed checkpoint; pending state is retained for recovery. Economy, inventory, quests, portals and battle actions remain transactional and durable before successful acknowledgement.

The live cache allows 128 character entries, evicts clean entries after five minutes without user activity, and bounds each pending movement queue at 256 commands. Dirty entries are retained if persistence fails. Session cache capacity is 10,000; local revocation tombstones last up to the original session lifetime. Filter saturation increases duplicate-check reads but does not weaken correctness. Character admission can temporarily fail at cache capacity. External session expiry/revocation is recognized within 30 seconds; local logout is immediate.

## Verification

- `rtk proxy go test -race ./...` from `apps/game-server`.
- `MYSQL_TEST=1 go test -race ./...` with the existing root `.env` loaded privately: atomic mutations, concurrent deduplication, actual movement checkpoints, revision conflict rejection, rollback, persisted breeding/ancestry, audit batches and escaped Unicode JSON all pass.
- `rtk proxy go vet ./...`.
- Transport tests cover shared reads, dedup after restart, concurrent connections, movement while a background save is blocked, retaining movement queued during a save, failed saves pausing movement, uncertain checkpoint retry, uncertain durable commit recovery, rejected movement, bounded auth refresh, local logout and HTTP 503 on auth outages.
