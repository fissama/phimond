import Phaser from 'phaser'
import { socket } from '../net/socket'
import type { Dir, PlayerState, BattleStartMessage } from '../net/protocol'

const TILE = 32
const WORLD_W = 20
const WORLD_H = 15

const TALL_GRASS_ZONES = [
  { x: 5,  y: 5,  w: 3, h: 3 },
  { x: 12, y: 8,  w: 4, h: 2 },
  { x: 1,  y: 10, w: 5, h: 3 },
]

const MOVE_THROTTLE_MS = 140

// Color palette — flat MVP style. Two greens for grass checker, darker green
// for tall-grass overlay, warm reds/blues for the trainer.
const GRASS_LIGHT = 0x5a8c4e
const GRASS_DARK = 0x4a7c3e
const GRASS_BLADE = 0x3d6c3e
const TALL_BASE = 0x2d5a2d
const TALL_BLADE_DARK = 0x1d4a1d
const TALL_BLADE_LIGHT = 0x4a7a3a
const TRAINER_CAP = 0x2244aa
const TRAINER_FACE = 0xfac8a8
const TRAINER_JACKET_ME = 0x4af0ff
const TRAINER_JACKET_OTHER = 0xff8844
const TRAINER_PANTS = 0x222244

export class WorldScene extends Phaser.Scene {
  private myName: string = ''
  private playerBodies = new Map<string, Phaser.GameObjects.Container>()
  private cursors!: Phaser.Types.Input.Keyboard.CursorKeys
  private lastMoveAt = 0
  private statusText!: Phaser.GameObjects.Text

  constructor() {
    super('World')
  }

  init(): void {
    // Phaser reuses scene instances across restarts (after returning from
    // BattleScene). The playerBodies Map holds references to containers that
    // were destroyed during the previous shutdown, so _applyState would skip
    // recreation and the player wouldn't reappear. Clear stale entries here.
    this.playerBodies.clear()
  }

  create(): void {
    this.myName = localStorage.getItem('phimond.playerName') ?? ''

    this._drawTiles()
    this._drawTallGrass()

    this.statusText = this.add
      .text(8, 8, `Connected as ${this.myName}`, {
        fontSize: '12px',
        color: '#fff',
        backgroundColor: '#000a',
        padding: { x: 6, y: 4 },
      })
      .setScrollFactor(0)
      .setDepth(100)

    // Logout button — sends a clean BYE (so server persists before the
    // proxy's WS-close-triggered BYE) and tears the socket down. Once the
    // socket transitions to 'closed' status, navigate back to LoginScene so
    // the user isn't stuck staring at "Saving…" with no way forward.
    const logoutBtn = this.add
      .text(this.scale.width - 8, 8, 'Logout', {
        fontSize: '12px',
        color: '#fff',
        backgroundColor: '#000a',
        padding: { x: 8, y: 4 },
      })
      .setOrigin(1, 0)
      .setScrollFactor(0)
      .setDepth(100)
      .setInteractive({ useHandCursor: true })
    logoutBtn.on('pointerdown', () => {
      logoutBtn.disableInteractive()
      logoutBtn.setText('Saving…')
      socket.send({ type: 'BYE' })

      // Navigate back to LoginScene once the socket closes (server has
      // persisted by then) or after a hard timeout so a stuck server can't
      // trap the user here.
      const finish = () => {
        if (!this.scene.isActive()) return
        this.scene.start('Login')
      }
      // Listen for the next status change only — onStatus() also fires once
      // with the current status, so we skip that first call.
      const off = socket.onStatus((status) => {
        off()
        if (status === 'closed' || status === 'failed') finish()
      })
      setTimeout(finish, 1500)
      setTimeout(() => socket.disconnect(), 100)
    })

    this.cursors = this.input.keyboard!.createCursorKeys()
    this.input.keyboard!.addKeys('W,A,S,D')

    // Event-based input — fires on every key press (not polling) so it works
    // for both held keys and quick taps.
    const codeToDir: Record<string, Dir> = {
      ArrowUp: 'up', KeyW: 'up',
      ArrowDown: 'down', KeyS: 'down',
      ArrowLeft: 'left', KeyA: 'left',
      ArrowRight: 'right', KeyD: 'right',
    }
    this.input.keyboard!.on('keydown', (event: KeyboardEvent) => {
      const dir = codeToDir[event.code]
      if (dir) this._tryMove(dir)
    })

    socket.onMessage((msg) => {
      switch (msg.type) {
        case 'STATE':
          this._applyState(msg.players as PlayerState[])
          break
        case 'BATTLE_START':
          this._enterBattle(msg as BattleStartMessage)
          break
        case 'ERROR':
          this.statusText.setText(`⚠ ${msg.message}`)
          this.statusText.setColor('#f88')
          setTimeout(() => this.statusText.setColor('#fff'), 1500)
          break
      }
    })

    if (socket.lastPlayers.length > 0) {
      this._applyState(socket.lastPlayers)
    }
  }

  update(): void {
    let dir: Dir | null = null
    if (this.cursors.up?.isDown || this._isDown('W')) dir = 'up'
    else if (this.cursors.down?.isDown || this._isDown('S')) dir = 'down'
    else if (this.cursors.left?.isDown || this._isDown('A')) dir = 'left'
    else if (this.cursors.right?.isDown || this._isDown('D')) dir = 'right'
    if (dir) this._tryMove(dir)
  }

  private _isDown(key: string): boolean {
    const k = (this.input.keyboard!.keys as unknown as Record<string, Phaser.Input.Keyboard.Key>)[key]
    return Boolean(k?.isDown)
  }

  // --- Rendering ------------------------------------------------------------

  private _drawTiles(): void {
    // Two-tone grass checker with deterministic darker blades scattered in
    // each cell — gives the world some texture without needing an AI texture.
    const g = this.add.graphics()
    for (let y = 0; y < WORLD_H; y++) {
      for (let x = 0; x < WORLD_W; x++) {
        const baseColor = (x + y) % 2 === 0 ? GRASS_LIGHT : GRASS_DARK
        g.fillStyle(baseColor, 1)
        g.fillRect(x * TILE, y * TILE, TILE, TILE)
        // Pseudo-random blade offsets seeded from (x,y).
        g.fillStyle(GRASS_BLADE, 0.55)
        const offsets: Array<[number, number]> = [
          [(x * 7 + y * 13) % 22 + 4, (x * 11 + y * 3) % 22 + 6],
          [(x * 5 + y * 17) % 22 + 8, (x * 3 + y * 7) % 22 + 18],
          [(x * 13 + y * 5) % 22 + 20, (x * 7 + y * 11) % 22 + 10],
        ]
        for (const [dx, dy] of offsets) {
          g.fillRect(x * TILE + dx, y * TILE + dy, 2, 3)
        }
      }
    }
  }

  private _drawTallGrass(): void {
    // Encounter zones get a darker base + short blade strokes drawn over each
    // cell. Blades vary in shade so it reads as 3D-ish without textures.
    const g = this.add.graphics()
    TALL_GRASS_ZONES.forEach((z) => {
      for (let dy = 0; dy < z.h; dy++) {
        for (let dx = 0; dx < z.w; dx++) {
          const tx = (z.x + dx) * TILE
          const ty = (z.y + dy) * TILE
          // Base fill (full cell, no inset — zones abut the grid cleanly).
          g.fillStyle(TALL_BASE, 1)
          g.fillRect(tx, ty, TILE, TILE)
          // Darker blades in the lower half of the cell.
          g.lineStyle(2, TALL_BLADE_DARK, 1)
          const seed = (z.x + dx) * 31 + (z.y + dy) * 17
          for (let i = 0; i < 3; i++) {
            const bx = tx + ((seed + i * 7) % 24) + 4
            const by = ty + ((seed + i * 13) % 14) + 12
            g.lineBetween(bx, by, bx, by - 8)
          }
          // Lighter highlight blades slightly offset for depth.
          g.lineStyle(1, TALL_BLADE_LIGHT, 0.9)
          for (let i = 0; i < 2; i++) {
            const bx = tx + ((seed + i * 11 + 3) % 24) + 5
            const by = ty + ((seed + i * 5 + 7) % 14) + 10
            g.lineBetween(bx, by, bx, by - 6)
          }
        }
      }
    })
  }

  private _tryMove(dir: Dir): void {
    const now = Date.now()
    if (now - this.lastMoveAt < MOVE_THROTTLE_MS) return
    this.lastMoveAt = now
    socket.send({ type: 'MOVE', dir })
  }

  private _applyState(players: PlayerState[]): void {
    const seen = new Set<string>()
    for (const p of players) {
      seen.add(p.name)
      const isMe = p.name === this.myName
      let body = this.playerBodies.get(p.name)
      // Defensive: if the cached body was destroyed (Phaser reuses scene
      // instances and bodies from a prior scene run are no longer alive),
      // drop the stale entry and recreate below.
      if (body && !body.active) {
        this.playerBodies.delete(p.name)
        body = undefined
      }
      if (!body) {
        body = this.add.container(p.x * TILE + TILE / 2, p.y * TILE + TILE / 2)
        this._buildTrainerIcon(body, isMe)
        const label = this.add
          .text(0, -TILE / 2 - 2, p.name, { fontSize: '11px', color: '#fff' })
          .setOrigin(0.5)
        body.add([label])
        body.setDepth(10)
        this.playerBodies.set(p.name, body)
      } else {
        this._tweenTo(body, p.x * TILE + TILE / 2, p.y * TILE + TILE / 2)
      }
    }
    for (const name of Array.from(this.playerBodies.keys())) {
      if (!seen.has(name)) {
        this.playerBodies.get(name)!.destroy()
        this.playerBodies.delete(name)
      }
    }
  }

  // Flat trainer icon: cap (blue dome) + face (skin) + jacket (cyan/orange)
  // + dark pants. Cyan for me, orange for other players. No sprite needed.
  private _buildTrainerIcon(parent: Phaser.GameObjects.Container, isMe: boolean): void {
    const jacket = isMe ? TRAINER_JACKET_ME : TRAINER_JACKET_OTHER
    // Cap (top dome)
    const cap = this.add.ellipse(0, -10, 14, 8, TRAINER_CAP)
    // Face (skin circle peeking under the cap)
    const face = this.add.circle(0, -6, 5, TRAINER_FACE)
    // Body (jacket — rounded rectangle)
    const body = this.add.rectangle(0, 4, 14, 10, jacket)
    // Pants / shadow strip
    const pants = this.add.rectangle(0, 11, 14, 2, TRAINER_PANTS)
    parent.add([pants, body, face, cap])
  }

  private _tweenTo(target: Phaser.GameObjects.Container, x: number, y: number): void {
    this.tweens.add({
      targets: target,
      x,
      y,
      duration: 100,
      ease: 'Linear',
    })
  }

  // --- Battle transition ----------------------------------------------------

  private _enterBattle(msg: BattleStartMessage): void {
    // Hand the battle data to BattleScene via scene data, then transition.
    this.scene.start('Battle', {
      wild: msg.wild,
      player: msg.player,
      inventory: msg.inventory,
      skills: msg.skills ?? [],
      items: msg.items ?? [],
    })
  }
}