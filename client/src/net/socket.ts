import type { ClientMessage, ServerMessage, PlayerState } from './protocol'

type MessageListener = (msg: ServerMessage) => void
type Status = 'connecting' | 'open' | 'closed' | 'failed'
type StatusListener = (status: Status) => void

/**
 * Tiny WebSocket wrapper.
 *
 * MVP scope:
 *  - auto-reconnect with bounded retries if connection drops
 *  - JSON encode/decode
 *  - pub/sub for inbound messages and connection status
 *  - caches last STATE snapshot so scenes that mount after a STATE
 *    broadcast can still render the current world
 */
const MAX_RETRIES = 3
const RETRY_DELAYS_MS = [1000, 2000, 4000]

class GameSocket {
  private ws: WebSocket | null = null
  private url: string
  private messageListeners: MessageListener[] = []
  private statusListeners: StatusListener[] = []
  private status: Status = 'closed'
  private retryCount = 0
  private shouldReconnect = true
  private _lastPlayers: PlayerState[] = []

  constructor(url: string) {
    this.url = url
  }

  connect(): void {
    this.shouldReconnect = true
    this.retryCount = 0
    this._open()
  }

  /** Manual retry from UI: reset retry counter and try once more. */
  retry(): void {
    this.shouldReconnect = true
    this.retryCount = 0
    if (this.ws) {
      try { this.ws.close() } catch {}
      this.ws = null
    }
    this._open()
  }

  disconnect(): void {
    this.shouldReconnect = false
    this.ws?.close()
    this.ws = null
  }

  send(msg: ClientMessage): void {
    if (this.ws?.readyState !== WebSocket.OPEN) {
      console.warn('[WS] Cannot send, socket not open:', msg)
      return
    }
    this.ws.send(JSON.stringify(msg))
  }

  onMessage(listener: MessageListener): () => void {
    this.messageListeners.push(listener)
    return () => {
      const idx = this.messageListeners.indexOf(listener)
      if (idx >= 0) this.messageListeners.splice(idx, 1)
    }
  }

  onStatus(listener: StatusListener): () => void {
    this.statusListeners.push(listener)
    listener(this.status)
    return () => {
      const idx = this.statusListeners.indexOf(listener)
      if (idx >= 0) this.statusListeners.splice(idx, 1)
    }
  }

  get lastPlayers(): PlayerState[] {
    return this._lastPlayers
  }

  private _open(): void {
    if (this.retryCount >= MAX_RETRIES) {
      console.error(`[WS] Giving up after ${MAX_RETRIES} attempts`)
      this._setStatus('failed')
      return
    }
    this._setStatus('connecting')
    console.log('[WS] Connecting to', this.url)
    const ws = new WebSocket(this.url)
    // Godot's WebSocketPeer.put_packet() sends binary frames. Browsers default
    // binaryType="blob", which makes event.data a Blob and JSON.parse blows up.
    // Switch to ArrayBuffer so we can decode UTF-8 ourselves.
    ws.binaryType = 'arraybuffer'
    this.ws = ws

    ws.onopen = () => {
      this.retryCount = 0
      this._setStatus('open')
      console.log('[WS] Connected')
    }

    ws.onmessage = (event) => {
      let text: string
      if (typeof event.data === 'string') {
        text = event.data
      } else {
        // ArrayBuffer (or Blob fallback) — Godot sends UTF-8 JSON as binary frames.
        text = new TextDecoder('utf-8').decode(event.data as ArrayBuffer)
      }
      try {
        const msg = JSON.parse(text) as ServerMessage
        if (msg.type === 'STATE') {
          this._lastPlayers = msg.players
        }
        for (const listener of this.messageListeners) {
          listener(msg)
        }
      } catch (err) {
        console.error('[WS] Failed to parse message', err, text)
      }
    }

    ws.onerror = (event) => {
      console.error('[WS] Error', event)
    }

    ws.onclose = () => {
      console.log('[WS] Closed')
      this._setStatus('closed')
      this.ws = null
      if (this.shouldReconnect && this.retryCount < MAX_RETRIES) {
        const delay = RETRY_DELAYS_MS[this.retryCount] ?? 4000
        this.retryCount++
        console.log(`[WS] Reconnecting in ${delay}ms (attempt ${this.retryCount}/${MAX_RETRIES})`)
        setTimeout(() => this._open(), delay)
      } else if (this.retryCount >= MAX_RETRIES) {
        this._setStatus('failed')
      }
    }
  }

  private _setStatus(s: Status): void {
    this.status = s
    for (const listener of this.statusListeners) {
      listener(s)
    }
  }
}

const WS_URL: string =
  (import.meta.env.VITE_WS_URL as string | undefined) ?? `ws://${window.location.hostname}:3000/ws`

export const socket = new GameSocket(WS_URL)
