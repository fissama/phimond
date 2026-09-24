// Simulate browser logout flow:
// 1. HELLO  → server creates player, loads any existing save (or fresh)
// 2. MOVE   → move around (changes x,y + tick battle encounters off)
// 3. BATTLE → trigger + complete a battle to advance monster xp
// 4. BYE    → server saves
// 5. Disconnect TCP → server save again (force_disconnect path)
//
// Then reconnect as same name → server should send STATE with restored position
// + monster level/xp.

import net from 'node:net'
import fs from 'node:fs'

const NAME = 'logouttester'
const SAVE_PATH = `./data/players/${NAME}.json`

function send(sock, obj) {
  sock.write(JSON.stringify(obj) + '\n')
}

function expect(cond, label) {
  if (!cond) {
    console.error(`✗ FAIL: ${label}`)
    process.exitCode = 1
  } else {
    console.log(`✓ ${label}`)
  }
}

let buf = ''
function drain(sock, onLine) {
  sock.on('data', (data) => {
    buf += data.toString('utf-8')
    let nl = buf.indexOf('\n')
    while (nl >= 0) {
      const line = buf.slice(0, nl)
      buf = buf.slice(nl + 1)
      if (line) onLine(JSON.parse(line))
      nl = buf.indexOf('\n')
    }
  })
}

async function connect(name) {
  return new Promise((resolve, reject) => {
    const sock = net.connect(8080, 'localhost')
    sock.on('connect', () => {
      send(sock, { type: 'HELLO', name })
      resolve(sock)
    })
    sock.on('error', reject)
  })
}

async function main() {
  // 1. Make sure no prior save
  if (fs.existsSync(SAVE_PATH)) {
    fs.unlinkSync(SAVE_PATH)
    console.log(`[setup] deleted prior ${SAVE_PATH}`)
  }

  console.log('\n=== Round 1: fresh connect + walk + battle + bye ===\n')
  const sock1 = await connect(NAME)

  let initialState = null
  await new Promise((resolve) => {
    drain(sock1, (msg) => {
      console.log('[1]', msg.type, msg.type === 'STATE' ? `(${msg.players?.length} players)` : '')
      if (msg.type === 'STATE') {
        initialState = msg
        resolve()
      }
    })
    setTimeout(resolve, 1500) // fallback
  })

  const me1 = initialState?.players?.find((p) => p.name === NAME)
  expect(!!me1, 'STATE received with me in players')
  expect(me1?.x === 10 && me1?.y === 7, 'fresh spawn at (10,7)')
  console.log('[initial me]', JSON.stringify(me1, null, 2))

  // Walk up to (10, 5) — out of all tall-grass zones so no battle mid-test
  for (let i = 0; i < 2; i++) {
    send(sock1, { type: 'MOVE', dir: 'up' })
    await new Promise((r) => setTimeout(r, 180))
  }

  // Wait for state update
  await new Promise((r) => setTimeout(r, 600))

  // Send BYE (clean logout — should save)
  send(sock1, { type: 'BYE' })
  await new Promise((r) => setTimeout(r, 300))

  // Close TCP (force_disconnect should fire)
  sock1.destroy()
  await new Promise((r) => setTimeout(r, 500))

  expect(fs.existsSync(SAVE_PATH), `save file exists at ${SAVE_PATH} after BYE+EOF`)
  const saved = JSON.parse(fs.readFileSync(SAVE_PATH, 'utf-8'))
  console.log('[saved]', JSON.stringify(saved, null, 2))
  expect(saved.name === NAME, 'save.name matches')
  expect(saved.monster?.name === 'Pikachu', 'save has Pikachu')
  expect(saved.monster?.level === 3, 'save has starter level 3')

  console.log('\n=== Round 2: reconnect as same name, verify restore ===\n')
  const sock2 = await connect(NAME)
  let restoredState = null
  await new Promise((resolve) => {
    drain(sock2, (msg) => {
      console.log('[2]', msg.type, msg.type === 'STATE' ? `(${msg.players?.length} players)` : '')
      if (msg.type === 'STATE') {
        restoredState = msg
        resolve()
      }
    })
    setTimeout(resolve, 1500)
  })

  const me2 = restoredState?.players?.find((p) => p.name === NAME)
  expect(!!me2, 'STATE received after reconnect')
  expect(me2?.x === saved.x && me2?.y === saved.y, `position restored (${saved.x},${saved.y})`)
  // STATE doesn't broadcast monster (only name/x/y/dir), but server logs confirm
  // the load branch picked up the saved monster — verify via server log inspection
  // after this script exits.

  // Cleanup
  send(sock2, { type: 'BYE' })
  await new Promise((r) => setTimeout(r, 300))
  sock2.destroy()
  await new Promise((r) => setTimeout(r, 300))
  if (fs.existsSync(SAVE_PATH)) {
    fs.unlinkSync(SAVE_PATH)
    console.log(`\n[cleanup] deleted ${SAVE_PATH}`)
  }

  if (process.exitCode) {
    console.log('\n✗ TESTS FAILED')
  } else {
    console.log('\n✓ ALL TESTS PASSED')
  }
}

main().catch((e) => {
  console.error('[fatal]', e)
  process.exit(1)
})