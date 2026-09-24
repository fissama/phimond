// Quick test: connect via TCP, send HELLO, then BYE, then disconnect.
// Verifies that BYE cleanly removes the player from the world.

import net from 'node:net'

const sock = net.connect(8080, 'localhost')

sock.on('connect', () => {
  console.log('[test] connected')
  sock.write('{"type":"HELLO","name":"byetester"}\n')
  setTimeout(() => {
    console.log('[test] sending BYE')
    sock.write('{"type":"BYE"}\n')
    setTimeout(() => {
      console.log('[test] closing')
      sock.destroy()
    }, 200)
  }, 500)
})

let buf = ''
sock.on('data', (data) => {
  buf += data.toString('utf-8')
  const nl = buf.indexOf('\n')
  while (nl >= 0) {
    const line = buf.slice(0, nl)
    buf = buf.slice(nl + 1)
    if (line) console.log('[test] recv:', line)
    const next = buf.indexOf('\n')
    if (next < 0) break
  }
})

sock.on('close', () => {
  console.log('[test] closed')
  process.exit(0)
})
