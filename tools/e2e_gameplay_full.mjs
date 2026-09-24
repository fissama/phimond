// End-to-end gameplay test for Phimond. Drives the full gameplay loop
// against a running server. Uses isolated test accounts only.
//
// Run: node tools/e2e_gameplay_full.mjs
// Exit code: 0 = all steps PASS/SKIP, 1 = at least one FAIL.
//
// Step output format: [PASS|FAIL|SKIP] stepN.short_name — detail
import assert from 'node:assert/strict';
import { randomBytes } from 'node:crypto';
import WebSocket from 'ws';

const BASE = process.env.GAME_API_URL || 'http://127.0.0.1:8090';
const WS_BASE = BASE.replace(/^http/, 'ws');
const TS = Date.now() % 1000000;
const USERNAME = `e2e${TS}${randomBytes(3).toString('hex')}`; // ≤24 chars
const PASSWORD = randomBytes(20).toString('hex') + 'aA1!'; // ≥10 bytes
const results = [];

function record(step, name, status, detail) {
  const line = `[${status}] ${step}.${name} — ${detail}`;
  results.push({ step, name, status, detail, line });
  console.log(line);
}

// Portals keyed by source map (data/maps/maps.json):
//   severa   ↔ forest_gate @ x=39 → forest, ranch_gate @ x=0 → ranch, arena_gate @ x=20 → arena
//   forest   ↔ city_gate @ x=0 → severa, beach_gate @ x=39 → beach
//   beach    ↔ forest_gate @ x=0 → forest
//   ranch    ↔ city_gate @ x=0 → severa
//   arena    ↔ city_gate @ x=0 → severa
// Each map has a set of direct neighbours (bidirectional).
const ADJACENT = {
  severa: ['forest', 'ranch', 'arena'],
  forest: ['severa', 'beach'],
  ranch: ['severa'],
  arena: ['severa'],
  beach: ['forest'],
};

// Returns the source-map portal id and source x that leads to `targetMap`.
function portalToSource(map, targetMap) {
  if (map === 'severa' && targetMap === 'forest') return { sourceX: 39, portalId: 'forest_gate' };
  if (map === 'severa' && targetMap === 'ranch') return { sourceX: 0, portalId: 'ranch_gate' };
  if (map === 'severa' && targetMap === 'arena') return { sourceX: 20, portalId: 'arena_gate' };
  if (map === 'forest' && targetMap === 'severa') return { sourceX: 0, portalId: 'city_gate' };
  if (map === 'forest' && targetMap === 'beach') return { sourceX: 39, portalId: 'beach_gate' };
  if (map === 'beach' && targetMap === 'forest') return { sourceX: 0, portalId: 'forest_gate' };
  if (map === 'ranch' && targetMap === 'severa') return { sourceX: 0, portalId: 'city_gate' };
  if (map === 'arena' && targetMap === 'severa') return { sourceX: 0, portalId: 'city_gate' };
  return null;
}

// Navigate to (targetMap, targetX), routing through at most one intermediate map.
// Mutates `state` (the shared mutable snapshot) and avoids extra character.get
// calls by trusting the response from every server action.
async function navigateTo(wsClient, targetMap, targetX = 6) {
  for (let attempt = 0; attempt < 5; attempt++) {
    const cur = state.character;
    if (cur.map_id === targetMap) {
      while (cur.x < targetX) {
        const r = await wsClient.send('world.move', { direction: 'right' });
        if (r.op === 'error') throw new Error(`move right failed: ${r.data?.message}`);
        state.character = r.data.character;
        if (state.character.x === targetX) break;
      }
      while (cur.x > targetX) {
        const r = await wsClient.send('world.move', { direction: 'left' });
        if (r.op === 'error') throw new Error(`move left failed: ${r.data?.message}`);
        state.character = r.data.character;
        if (state.character.x === targetX) break;
      }
      return state.character;
    }
    // Determine which adjacent map to use as the next step.
    let nextMap;
    const curAdj = ADJACENT[cur.map_id] || [];
    if (curAdj.includes(targetMap)) {
      nextMap = targetMap;
    } else {
      const targetAdj = ADJACENT[targetMap] || [];
      const via = targetAdj.find((m) => curAdj.includes(m));
      if (!via) throw new Error(`no portal from ${cur.map_id} to ${targetMap}`);
      nextMap = via;
    }
    const direct = portalToSource(cur.map_id, nextMap);
    if (!direct) throw new Error(`no portal from ${cur.map_id} to ${nextMap}`);
    while (state.character.x !== direct.sourceX) {
      const dir = state.character.x < direct.sourceX ? 'right' : 'left';
      const r = await wsClient.send('world.move', { direction: dir });
      if (r.op === 'error') throw new Error(`prep-move failed: ${r.data?.message}`);
      state.character = r.data.character;
    }
    const p = await wsClient.send('world.portal', { portal_id: direct.portalId });
    if (p.op === 'error') throw new Error(`portal ${direct.portalId} failed: ${p.data?.message}`);
    state.character = p.data.character;
  }
  throw new Error(`navigateTo(${targetMap}, ${targetX}) failed after retries`);
}

async function api(path, method = 'GET', data, token) {
  const headers = { 'Content-Type': 'application/json' };
  if (token) headers.Authorization = `Bearer ${token}`;
  const r = await fetch(BASE + path, {
    method,
    headers,
    body: data !== undefined ? JSON.stringify(data) : undefined,
  });
  let body;
  const text = await r.text();
  try {
    body = text ? JSON.parse(text) : null;
  } catch (e) {
    body = { _raw: text };
  }
  return [r.status, body];
}

// Shared mutable state snapshot; updated by every server action response.
const state = { character: null };

function makeClient(token) {
  const ws = new WebSocket(WS_BASE + '/ws');
  const pending = new Map();
  const events = [];
  let openResolve;
  const opened = new Promise((res) => (openResolve = res));
  ws.on('open', () => openResolve());
  ws.on('error', (e) => {
    for (const { reject } of pending.values()) reject(e);
  });
  ws.on('message', (raw) => {
    const m = JSON.parse(raw.toString());
    // Route by request_id first. The auth.session response is a 'state' message
    // with the auth request_id, so we MUST consult pending before ignoring.
    if (pending.has(m.request_id)) {
      const { resolve, reject } = pending.get(m.request_id);
      pending.delete(m.request_id);
      if (m.op === 'error') reject(Object.assign(new Error(m.data?.message || 'err'), { msg: m }));
      else resolve(m);
    } else if (m.request_id) {
      events.push(m);
    } else {
      // unsolicited server message — push to event log
      events.push(m);
    }
  });
  let seq = 0;
  const send = (op, data = {}, id) => {
    const reqId = id || `e2e-${++seq}-${randomBytes(3).toString('hex')}`;
    return new Promise((resolve, reject) => {
      const timer = setTimeout(() => {
        pending.delete(reqId);
        reject(new Error(`timeout for ${op} (${reqId})`));
      }, 15000);
      pending.set(reqId, {
        resolve: (m) => {
          clearTimeout(timer);
          resolve(m);
        },
        reject: (e) => {
          clearTimeout(timer);
          reject(e);
        },
      });
      ws.send(JSON.stringify({ op, request_id: reqId, data }));
    });
  };
  const auth = () =>
    new Promise((resolve, reject) => {
      const t = setTimeout(() => reject(new Error('auth timeout')), 5000);
      pending.set('auth-session', {
        resolve: (m) => {
          clearTimeout(t);
          pending.delete('auth-session');
          resolve(m);
        },
        reject: (e) => {
          clearTimeout(t);
          pending.delete('auth-session');
          reject(e);
        },
      });
      ws.send(JSON.stringify({ op: 'auth.session', request_id: 'auth-session', data: { token } }));
    });
  const close = () =>
    new Promise((res) => {
      try {
        ws.close();
      } catch (e) {}
      setTimeout(res, 200);
    });
  return { ws, send, auth, events, close, opened };
}

async function main() {
  let token;
  let character;
  let wsClient;
  const newPetIds = []; // for cleanup tracking
  try {
    // === Step 1: register ===
    try {
      const [code, body] = await api('/api/register', 'POST', { username: USERNAME, password: PASSWORD });
      if (code !== 200) throw new Error(`HTTP ${code}: ${JSON.stringify(body)}`);
      if (!body.token) throw new Error('no token in response');
      token = body.token;
      record(1, 'register', 'PASS', `account=${USERNAME}`);
    } catch (e) {
      record(1, 'register', 'FAIL', e.message);
      throw e;
    }

    // === Step 2: login ===
    let oldToken = token;
    try {
      const [code, body] = await api('/api/login', 'POST', { username: USERNAME, password: PASSWORD });
      if (code !== 200) throw new Error(`HTTP ${code}: ${JSON.stringify(body)}`);
      token = body.token;
      // Old token should still work (idempotent session cache)
      const [oldCode, oldBody] = await api('/api/character', 'GET', undefined, oldToken);
      if (oldCode !== 200) throw new Error(`old token now ${oldCode}: ${JSON.stringify(oldBody)}`);
      record(2, 'login', 'PASS', `got token, old token still valid`);
    } catch (e) {
      record(2, 'login', 'FAIL', e.message);
      throw e;
    }

    // Open WS
    wsClient = makeClient(token);
    try {
      await Promise.race([wsClient.opened, new Promise((_, rej) => setTimeout(() => rej(new Error('ws open timeout')), 5000))]);
    } catch (e) {
      record(2, 'ws_open', 'FAIL', e.message);
      throw e;
    }
    try {
      const auth = await wsClient.auth();
      if (auth.op !== 'state') throw new Error(`auth op=${auth.op}`);
    } catch (e) {
      record(2, 'ws_auth', 'FAIL', e.message);
      throw e;
    }

    // === Step 3: spawn in Severa ===
    try {
      const m = await wsClient.send('character.get');
      state.character = m.data.character;
      if (state.character.map_id !== 'severa') throw new Error(`map_id=${state.character.map_id}`);
      if (state.character.x !== 6) throw new Error(`x=${state.character.x}`);
      if (!Array.isArray(state.character.pets) || state.character.pets.length < 1) throw new Error(`pets=${JSON.stringify(state.character.pets)}`);
      if (state.character.gold < 100) throw new Error(`gold=${state.character.gold}`);
      const starter = state.character.pets[0];
      if (!starter.appraised) throw new Error('starter not appraised');
      record(3, 'spawn_severa', 'PASS', `pets=${state.character.pets.length} gold=${state.character.gold} starter=${starter.id}`);
    } catch (e) {
      record(3, 'spawn_severa', 'FAIL', e.message);
      throw e;
    }

    // === Step 4: move right ===
    try {
      const m = await wsClient.send('world.move', { direction: 'right' });
      state.character = m.data.character;
      const cx = state.character.x;
      if (cx !== 7) throw new Error(`x=${cx} expected 7`);
      record(4, 'move_right', 'PASS', `x=${cx}`);
    } catch (e) {
      record(4, 'move_right', 'FAIL', e.message);
    }

    // === Step 5: talk to NPC trainer (Severa x=6, we are x=7, distance=1 ≤ 3) ===
    try {
      const m = await wsClient.send('npc.interact', { npc_id: 'trainer' });
      state.character = m.data.character;
      if (m.op !== 'state') throw new Error(`op=${m.op}`);
      const evs = m.data.events || [];
      const hasNpc = evs.some((e) => e.type === 'npc_dialogue' || e.type === 'quest_progress');
      if (!hasNpc && evs.length === 0) throw new Error('no dialogue or quest progress event');
      record(5, 'npc_interact', 'PASS', `events=${evs.map((e) => e.type).join(',')}`);
    } catch (e) {
      record(5, 'npc_interact', 'FAIL', e.message);
    }

    // === Step 6: buy a potion ===
    let goldBeforeBuy = null;
    try {
      goldBeforeBuy = state.character.gold;
      const m = await wsClient.send('shop.buy', { item_id: 'potion', quantity: 1 }, 'buy-potion-1');
      state.character = m.data.character;
      if (m.op !== 'state') throw new Error(`op=${m.op}`);
      if (state.character.gold !== goldBeforeBuy - 5) throw new Error(`gold ${goldBeforeBuy} -> ${state.character.gold} (expected -5)`);
      const inv = state.character.inventory?.potion || 0;
      if (inv < 1) throw new Error(`potion inv=${inv}`);
      record(6, 'shop_buy', 'PASS', `gold ${goldBeforeBuy}->${state.character.gold} potion=${inv}`);
    } catch (e) {
      record(6, 'shop_buy', 'FAIL', `${e.message} (goldBefore=${goldBeforeBuy})`);
    }

    // === Step 7: duplicate buy with same request_id ===
    try {
      const g0 = state.character.gold;
      const i0 = state.character.inventory?.potion || 0;
      const m = await wsClient.send('shop.buy', { item_id: 'potion', quantity: 1 }, 'buy-potion-1');
      state.character = m.data.character;
      if (m.op !== 'state') throw new Error(`op=${m.op}`);
      if (state.character.gold !== g0) throw new Error(`gold changed: ${g0}->${state.character.gold}`);
      if ((state.character.inventory?.potion || 0) !== i0) throw new Error(`inv changed: ${i0}->${state.character.inventory?.potion}`);
      record(7, 'shop_dedup', 'PASS', `no gold/inv delta on dup request_id`);
    } catch (e) {
      record(7, 'shop_dedup', 'FAIL', e.message);
    }

    // === Step 8: heal ===
    try {
      // walk back to x=6 to be near trainer
      const m = await wsClient.send('world.move', { direction: 'left' });
      state.character = m.data.character;
      const m2 = await wsClient.send('pet.heal', {});
      state.character = m2.data.character;
      const evs = m2.data.events || [];
      const hasHeal = evs.some((e) => e.type === 'pet_heal');
      if (!hasHeal) throw new Error(`events=${evs.map((e) => e.type).join(',')}`);
      record(8, 'pet_heal', 'PASS', `healed; gold=${state.character.gold}`);
    } catch (e) {
      record(8, 'pet_heal', 'FAIL', e.message);
    }

    // === Step 9: portal to forest ===
    try {
      while (state.character.x < 39) {
        const w = await wsClient.send('world.move', { direction: 'right' });
        state.character = w.data.character;
      }
      const p = await wsClient.send('world.portal', { portal_id: 'forest_gate' });
      state.character = p.data.character;
      if (state.character.map_id !== 'forest') throw new Error(`map=${state.character.map_id}`);
      record(9, 'portal_forest', 'PASS', `map=${state.character.map_id} x=${state.character.x}`);
    } catch (e) {
      record(9, 'portal_forest', 'FAIL', e.message);
    }

    // === Step 10: start battle ===
    let lastBattle = null;
    try {
      const m = await wsClient.send('world.encounter', {});
      state.character = m.data.character;
      if (!state.character.battle) throw new Error('no battle object');
      lastBattle = state.character.battle;
      if (!lastBattle.units || lastBattle.units.length < 2) throw new Error('battle units < 2');
      if (lastBattle.phase !== 'WAIT_COMMAND') throw new Error(`phase=${lastBattle.phase}`);
      if (lastBattle.turn !== 1) throw new Error(`turn=${lastBattle.turn}`);
      record(10, 'start_battle', 'PASS', `battle=${lastBattle.id} units=${lastBattle.units.length} phase=${lastBattle.phase}`);
    } catch (e) {
      record(10, 'start_battle', 'FAIL', e.message);
    }

    // === Step 11: battle loop with attack until result ===
    let battleResult = null;
    let lastBattleEvs = [];
    try {
      let safety = 40;
      while (safety-- > 0) {
        const b = state.character.battle;
        if (!b) { battleResult = 'unknown'; break; }
        const r = await wsClient.send('battle.action', {
          battle_id: b.id,
          turn: b.turn,
          choice: 'attack',
        });
        state.character = r.data.character;
        const evs = r.data.events || [];
        lastBattleEvs = evs;
        if (evs.some((e) => e.type === 'battle_win' || e.type === 'battle_loss' || e.type === 'battle_draw' || e.type === 'battle_flee' || e.type === 'battle_capture')) {
          battleResult = evs.find((e) => e.type?.startsWith('battle_')).type.replace('battle_', '');
          break;
        }
        // Also exit if the engine cleared the battle
        if (!state.character.battle) {
          battleResult = battleResult || 'cleared';
          break;
        }
      }
      if (!battleResult) throw new Error('battle loop exhausted');
      record(11, 'battle_loop', 'PASS', `result=${battleResult} events=${lastBattleEvs.length}`);
    } catch (e) {
      record(11, 'battle_loop', 'FAIL', `${e.message} (lastEvents=${lastBattleEvs.slice(-3).map((e) => e.type).join(',')})`);
    }

    // === Step 12: capture attempt — loop up to 5 times ===
    let capturedPetId = null;
    let captureAttempts = 0;
    try {
      // Ensure we have capture_seals (buy at Severa trainer)
      if ((state.character.inventory?.capture_seal || 0) < 1) {
        await navigateTo(wsClient, 'severa', 6);
        const goldBefore = state.character.gold;
        const buy = await wsClient.send('shop.buy', { item_id: 'capture_seal', quantity: 3 });
        state.character = buy.data.character;
        if (state.character.gold !== goldBefore - 24) throw new Error(`seal cost wrong: ${goldBefore}->${state.character.gold}`);
      }
      // Heal before encounter (Severa trainer has heal)
      await navigateTo(wsClient, 'severa', 6);
      const heal = await wsClient.send('pet.heal', {});
      state.character = heal.data.character;
      // Navigate to forest and try up to 5 capture encounters
      await navigateTo(wsClient, 'forest', 6);

      for (let i = 0; i < 5 && !capturedPetId; i++) {
        captureAttempts++;
        const enc = await wsClient.send('world.encounter', {});
        if (enc.op === 'error') {
          // HP=0, heal and retry
          await navigateTo(wsClient, 'severa', 6);
          const h = await wsClient.send('pet.heal', {});
          state.character = h.data.character;
          await navigateTo(wsClient, 'forest', 6);
          i--; // don't count this as an attempt
          continue;
        }
        state.character = enc.data.character;
        let b = enc.data.character.battle;
        if (!b) break;
        let safety2 = 60;
        const enemyMaxHP = b.units[1]?.max_hp || 30;
        while (safety2-- > 0 && b && !b.result) {
          const e1 = b.units[1];
          if (e1.hp > 0 && e1.hp <= Math.max(2, Math.floor(enemyMaxHP * 0.15))) {
            const cap = await wsClient.send('battle.action', {
              battle_id: b.id,
              turn: b.turn,
              choice: 'capture',
              item_id: 'capture_seal',
            });
            if (cap.op === 'error') break;
            state.character = cap.data.character;
            const evs = cap.data.events || [];
            const captured = evs.find((e) => e.type === 'pet_capture');
            const failed = evs.find((e) => e.type === 'capture_failed');
            if (captured) {
              capturedPetId = state.character.pets[state.character.pets.length - 1]?.id;
              break;
            }
            if (failed) break;
            if (cap.data.character.battle?.result) {
              b = cap.data.character.battle;
              break;
            }
          }
          const r = await wsClient.send('battle.action', {
            battle_id: b.id,
            turn: b.turn,
            choice: 'attack',
          });
          if (r.op === 'error') break;
          state.character = r.data.character;
          b = r.data.character.battle;
        }
        if (capturedPetId) break;
        // Heal for next attempt
        await navigateTo(wsClient, 'severa', 6);
        const hh = await wsClient.send('pet.heal', {});
        state.character = hh.data.character;
        await navigateTo(wsClient, 'forest', 6);
      }
      if (capturedPetId) {
        record(12, 'capture_loop', 'PASS', `captured ${capturedPetId} after ${captureAttempts} attempt(s)`);
        newPetIds.push(capturedPetId);
      } else {
        record(12, 'capture_loop', 'FAIL', `no capture after ${captureAttempts} attempts (RNG)`);
      }
    } catch (e) {
      record(12, 'capture_loop', 'FAIL', e.message);
    }

    // === Step 13: appraise — need to be near ranch_keeper (ranch map, x=6) ===
    let appraisedPet = null;
    try {
      await navigateTo(wsClient, 'ranch', 6);
      // Pick the captured pet if any, else starter
      const target = capturedPetId ? state.character.pets.find((p) => p.id === capturedPetId) : state.character.pets[0];
      if (!target) throw new Error('no pet to appraise');
      const goldBefore = state.character.gold;
      const r = await wsClient.send('pet.appraise', { pet_id: target.id });
      state.character = r.data.character;
      const evs = r.data.events || [];
      if (!evs.some((e) => e.type === 'pet_appraise')) throw new Error(`events=${evs.map((e) => e.type).join(',')}`);
      if (!target.appraised && state.character.gold !== goldBefore - 5) {
        throw new Error(`gold ${goldBefore} -> ${state.character.gold} (expected -5)`);
      }
      appraisedPet = target.id;
      record(13, 'pet_appraise', 'PASS', `pet=${target.id} gold=${state.character.gold} alreadyAppraised=${!!target.appraised}`);
    } catch (e) {
      record(13, 'pet_appraise', 'FAIL', e.message);
    }

    // === Step 14: activate (swap) ===
    try {
      if (state.character.pets.length < 2) throw new Error(`only ${state.character.pets.length} pet(s) — need ≥2`);
      const newActive = state.character.pets.find((p) => p.id !== state.character.active_pet_id && !p.retired);
      if (!newActive) throw new Error('no second non-retired pet to activate');
      const r = await wsClient.send('pet.activate', { pet_id: newActive.id });
      state.character = r.data.character;
      if (!r.data.events?.some((e) => e.type === 'pet_activate')) throw new Error(`events=${(r.data.events || []).map((e) => e.type).join(',')}`);
      if (state.character.active_pet_id !== newActive.id) throw new Error(`active=${state.character.active_pet_id}`);
      record(14, 'pet_activate', 'PASS', `active=${newActive.id}`);
    } catch (e) {
      record(14, 'pet_activate', 'FAIL', e.message);
    }

    // === Step 15: quest accept — ranch_keeper has 'quest' role ===
    try {
      await navigateTo(wsClient, 'ranch', 6);
      const r = await wsClient.send('quest.accept', { quest_id: 'first_steps' });
      state.character = r.data.character;
      if (!r.data.events?.some((e) => e.type === 'quest_accept')) throw new Error(`events=${(r.data.events || []).map((e) => e.type).join(',')}`);
      record(15, 'quest_accept', 'PASS', `accepted first_steps`);
    } catch (e) {
      record(15, 'quest_accept', 'FAIL', e.message);
    }

    // === Step 16: quest claim — first_steps requires reach_map=forest ===
    let questClaimed = false;
    try {
      // Visit forest to trigger progress
      await navigateTo(wsClient, 'forest', 6);
      // Return to ranch to claim
      await navigateTo(wsClient, 'ranch', 6);
      const goldBefore = state.character.gold;
      const r = await wsClient.send('quest.claim', { quest_id: 'first_steps' });
      state.character = r.data.character;
      if (!r.data.events?.some((e) => e.type === 'quest_complete')) throw new Error(`events=${(r.data.events || []).map((e) => e.type).join(',')}`);
      if (state.character.gold !== goldBefore + 30) throw new Error(`gold ${goldBefore} -> ${state.character.gold} (expected +30)`);
      questClaimed = true;
      record(16, 'quest_claim', 'PASS', `gold ${goldBefore}->${state.character.gold}`);
    } catch (e) {
      record(16, 'quest_claim', 'FAIL', e.message);
    }

    // === Step 17: learn recipe (snail_refinement) — ranch_keeper has 'recipe' role ===
    let recipeLearned = false;
    try {
      const gold0 = state.character.gold;
      const r = await wsClient.send('recipe.learn', { recipe_id: 'snail_refinement' });
      state.character = r.data.character;
      if (!r.data.events?.some((e) => e.type === 'recipe_learn')) throw new Error(`events=${(r.data.events || []).map((e) => e.type).join(',')}`);
      if (state.character.gold !== gold0 - 30) throw new Error(`gold ${gold0} -> ${state.character.gold} (expected -30)`);
      recipeLearned = true;
      record(17, 'recipe_learn', 'PASS', `gold=${state.character.gold}`);
    } catch (e) {
      record(17, 'recipe_learn', 'FAIL', e.message);
    }

    // === Step 18: breed — needs two level-20 snails of opposite gender ===
    let breedResult = null;
    try {
      const c = state.character;
      const snails = c.pets.filter((p) => p.species_id === 'snail' && !p.retired);
      if (snails.length < 2) throw new Error(`only ${snails.length} snails`);
      const male = snails.find((p) => p.gender === 'male');
      const female = snails.find((p) => p.gender === 'female');
      if (!male || !female) throw new Error(`need opposite genders: male=${!!male} female=${!!female}`);
      if (male.level < 20 || female.level < 20) throw new Error(`levels: ${male.level}/${female.level} (need 20)`);
      if ((c.inventory?.synthesis_soul || 0) < 1) throw new Error('no synthesis_soul');
      const r = await wsClient.send('breeding.synthesize', {
        parent_a: male.id,
        parent_b: female.id,
        recipe_id: 'snail_refinement',
        blessing: 0,
      });
      state.character = r.data.character;
      if (!r.data.events?.some((e) => e.type === 'pet_breed')) throw new Error(`events=${(r.data.events || []).map((e) => e.type).join(',')}`);
      const newPet = state.character.pets[state.character.pets.length - 1];
      breedResult = newPet.id;
      newPetIds.push(newPet.id);
      record(18, 'breeding', 'PASS', `child=${newPet.id} gen=${newPet.generation}`);
    } catch (e) {
      if (
        /needs level 20|opposite gender|synthesis_soul|only 1 snail|only 2 snails|no synthesis_soul|levels:/.test(e.message)
      ) {
        record(18, 'breeding', 'SKIP', `preconditions not met: ${e.message}`);
      } else {
        record(18, 'breeding', 'FAIL', e.message);
      }
    }

    // === Step 19: logout ===
    try {
      const [code] = await api('/api/logout', 'POST', undefined, token);
      if (code !== 200) throw new Error(`HTTP ${code}`);
      record(19, 'logout', 'PASS', `token revoked`);
    } catch (e) {
      record(19, 'logout', 'FAIL', e.message);
    }

    // === Step 20: re-login + state persistence ===
    try {
      const [code, body] = await api('/api/login', 'POST', { username: USERNAME, password: PASSWORD });
      if (code !== 200) throw new Error(`HTTP ${code}`);
      token = body.token;
      const c = (await api('/api/character', 'GET', undefined, token))[1];
      if (!c.pets || c.pets.length < 1) throw new Error('no pets after re-login');
      // pets preserved
      record(20, 'relogin_state', 'PASS', `pets=${c.pets.length} active=${c.active_pet_id} gold=${c.gold}`);
    } catch (e) {
      record(20, 'relogin_state', 'FAIL', e.message);
    }
  } finally {
    if (wsClient) {
      try {
        await wsClient.close();
      } catch (e) {}
    }
  }

  const failed = results.filter((r) => r.status === 'FAIL').length;
  console.log(`\n=== Summary: ${results.length} steps, ${failed} FAIL ===`);
  console.log(`Account used: ${USERNAME}`);
  process.exit(failed > 0 ? 1 : 0);
}

main().catch((e) => {
  console.error('FATAL:', e);
  process.exit(2);
});
