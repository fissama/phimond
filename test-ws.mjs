// Quick smoke test for the Godot WS server.
// Usage: cd client && node ../test-ws.mjs
import WebSocket from './client/node_modules/ws/wrapper.mjs'

const ws = new WebSocket('ws://localhost:8080')

ws.on('open', () => {
  console.log('[test] connected')
  ws.send(JSON.stringify({ type: 'HELLO', name: 'tester' }))
  setTimeout(() => ws.send(JSON.stringify({ type: 'MOVE', dir: 'right' })), 200)
  setTimeout(() => ws.send(JSON.stringify({ type: 'MOVE', dir: 'down' })), 400)
  setTimeout(() => ws.close(), 1500)
})

ws.on('message', (data) => {
  console.log('[test] recv:', data.toString())
})

ws.on('error', (e) => {
  console.error('[test] error:', e.message)
  process.exit(1)
})

ws.on('close', () => {
  console.log('[test] closed')
  process.exit(0)
})
