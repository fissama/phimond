// True multi-client test: both connections alive simultaneously.
import WebSocket from './client/node_modules/ws/wrapper.mjs'

function makeClient(name, moves, getStates) {
  const ws = new WebSocket('ws://localhost:8080')
  ws.on('open', () => {
    console.log(`[${name}] connected`)
    ws.send(JSON.stringify({ type: 'HELLO', name }))
    let i = 0
    const interval = setInterval(() => {
      if (i >= moves.length) {
        clearInterval(interval)
        return
      }
      ws.send(JSON.stringify({ type: 'MOVE', dir: moves[i] }))
      i++
    }, 200)
  })
  ws.on('message', (data) => {
    const msg = JSON.parse(data.toString())
    if (msg.type === 'STATE') {
      const summary = msg.players.map((p) => `${p.name}@(${p.x},${p.y})`).join(' | ')
      getStates(name, summary)
    }
  })
  return ws
}

const states = {}
const getStates = (who, s) => { states[who] = s }

const alice = makeClient('alice', ['right', 'right', 'down'], getStates)
const bob   = makeClient('bob',   ['left',  'left',  'up'],   getStates)

setTimeout(() => {
  console.log('--- final visible states ---')
  console.log('alice sees:', states.alice)
  console.log('bob sees:  ', states.bob)
  alice.close()
  bob.close()
  process.exit(0)
}, 2500)
