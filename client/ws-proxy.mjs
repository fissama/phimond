// Tiny WS↔TCP proxy: bridges browser WebSocket frames to the Godot TCP server.
//
// Why this exists: Godot 4.7.2's WebSocketServer has a handshake compatibility
// issue with Chromium (browser WS upgrades get rejected with "Not enough
// response headers"). This proxy accepts WS from the browser (standard) and
// forwards newline-delimited JSON over a raw TCP socket to the Godot server.
//
// Run locally:  node ws-proxy.mjs
// In Docker:     see docker-compose.yml (service: proxy)

import { WebSocketServer } from 'ws'
import net from 'node:net'

const WS_PORT = Number(process.env.WS_PORT ?? 3001)
const TCP_HOST = process.env.TCP_HOST ?? 'localhost'
const TCP_PORT = Number(process.env.TCP_PORT ?? 8080)

const wss = new WebSocketServer({ port: WS_PORT })

wss.on('listening', () => {
  console.log(`[proxy] WS server listening on ws://0.0.0.0:${WS_PORT}`)
  console.log(`[proxy] forwarding to TCP ${TCP_HOST}:${TCP_PORT}`)
})

wss.on('connection', (ws) => {
  const sock = net.connect(TCP_PORT, TCP_HOST)

  sock.on('connect', () => {
    console.log('[proxy] TCP upstream connected')
  })

  sock.on('error', (e) => {
    console.error('[proxy] TCP upstream error:', e.message)
    try { ws.close() } catch {}
  })

  sock.on('close', () => {
    console.log('[proxy] TCP upstream closed')
    try { ws.close() } catch {}
  })

  // Browser → server (one WS message → one line of JSON, newline-terminated).
  ws.on('message', (data) => {
    let text
    if (typeof data === 'string') text = data
    else text = Buffer.from(data).toString('utf-8')
    // The server expects each message to end with a newline. Browsers may send
    // text frames without one; we always append it.
    sock.write(text.endsWith('\n') ? text : text + '\n')
  })

  // Server → browser (TCP may deliver multi-line buffers; split on \n so each
  // logical JSON message becomes one WS frame).
  let buf = ''
  sock.on('data', (data) => {
    buf += data.toString('utf-8')
    let nl = buf.indexOf('\n')
    while (nl >= 0) {
      const line = buf.slice(0, nl)
      buf = buf.slice(nl + 1)
      if (line.length > 0) {
        try { ws.send(line) } catch (e) { /* client closed */ }
      }
      nl = buf.indexOf('\n')
    }
  })

  ws.on('close', () => {
    console.log('[proxy] WS client closed')
    // Notify the Godot server that we're going away so it can free the
    // player's slot immediately (instead of waiting for TCP timeout).
    try { sock.write('{"type":"BYE"}\n') } catch {}
    // Give the BYE 50ms to flush, then tear down the TCP socket.
    setTimeout(() => {
      try { sock.destroy() } catch {}
    }, 50)
  })

  ws.on('error', (e) => {
    console.error('[proxy] WS client error:', e.message)
    sock.destroy()
  })
})

wss.on('error', (e) => {
  console.error('[proxy] WS server error:', e.message)
})
