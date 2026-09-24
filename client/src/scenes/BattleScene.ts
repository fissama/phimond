import Phaser from 'phaser'
import { socket } from '../net/socket'
import type {
  BattleMonster,
  BattleInventoryItem,
  BattleSkillDetail,
  BattleItemDetail,
  BattleEvent,
  BattleTurnMessage,
  BattleEndMessage,
} from '../net/protocol'

const W = 640
const H = 480

const MENU_X: number = W - 110
const MENU_Y: number = 280
const MENU_GAP: number = 32

// Per-monster look — flat creature silhouettes drawn from primitives. Each
// monster has a body color + accent color + a "shape key" the renderer reads
// to compose the silhouette (body + ears/tail/horn/leaf as appropriate).
const WILD_COLOR = 0xff5544
const PLAYER_COLOR = 0x4af0ff

type MonsterShape = 'pikachu' | 'charmander' | 'squirtle' | 'sproutling' | 'rattata' | 'caterpie' | 'weedle'

interface MonsterLook {
  body: number
  accent: number
  shape: MonsterShape
}

const MONSTER_LOOK: Record<string, MonsterLook> = {
  pikachu:    { body: 0xffd84a, accent: 0x222222, shape: 'pikachu' },
  charmander: { body: 0xff7733, accent: 0xffdd44, shape: 'charmander' },
  squirtle:   { body: 0x66aaff, accent: 0x2266aa, shape: 'squirtle' },
  sproutling: { body: 0x88cc66, accent: 0x336622, shape: 'sproutling' },
  rattata:    { body: 0xaa88aa, accent: 0x663366, shape: 'rattata' },
  caterpie:   { body: 0x99dd55, accent: 0x447722, shape: 'caterpie' },
  weedle:     { body: 0xc4a050, accent: 0x665020, shape: 'weedle' },
}

type ActionKey = 'attack' | 'skill' | 'item' | 'flee'
type MenuState = 'main' | 'skill' | 'item'

interface MainMenuItem {
  key: ActionKey
  label: string
}

interface BattleInitData {
  wild: BattleMonster
  player: BattleMonster
  inventory: BattleInventoryItem[]
  skills: BattleSkillDetail[]
  items: BattleItemDetail[]
}

const MAIN_MENU: MainMenuItem[] = [
  { key: 'attack', label: 'Attack' },
  { key: 'skill', label: 'Skill' },
  { key: 'item', label: 'Item' },
  { key: 'flee', label: 'Flee' },
]

export class BattleScene extends Phaser.Scene {
  // Server-provided battle state (mutable; mutated by damage/heal events).
  private wild!: BattleMonster
  private player!: BattleMonster

  // Server-provided catalogs the submenus render against.
  private skills: BattleSkillDetail[] = []
  private items: BattleItemDetail[] = []

  // Submenu state machine.
  private menuState: MenuState = 'main'

  // Current HP displayed in the bars (animated separately from this.wild.hp /
  // this.player.hp so we can tween between them).
  private wildHpDisplayed: number = 0
  private playerHpDisplayed: number = 0

  // HP bars + labels.
  private wildHpBar!: Phaser.GameObjects.Rectangle
  private wildHpText!: Phaser.GameObjects.Text
  private playerHpBar!: Phaser.GameObjects.Rectangle
  private playerHpText!: Phaser.GameObjects.Text

  // Dynamic UI lists — we clear + redraw when switching submenus.
  private menuButtons: Phaser.GameObjects.GameObject[] = []

  // Persistent UI (not cleared on submenu swap).
  private logText!: Phaser.GameObjects.Text
  private titleText!: Phaser.GameObjects.Text
  private headerText!: Phaser.GameObjects.Text  // submenu title ("Choose a skill")

  constructor() {
    super('Battle')
  }

  init(data: BattleInitData): void {
    this.wild = data.wild
    this.player = data.player
    this.skills = data.skills ?? []
    this.items = data.items ?? []
    this.wildHpDisplayed = this.wild.hp
    this.playerHpDisplayed = this.player.hp
    this.menuState = 'main'
    // inventory (qty-only) is kept around for diagnostics / future features.
    void data.inventory
  }

  create(): void {
    // Background — battle field (flat dark blue).
    this.add.rectangle(W / 2, H / 2, W, H, 0x222a3a)

    // Title at top of the scene.
    this.titleText = this.add
      .text(W / 2, 16, `Wild ${this.wild.name} appeared!`, {
        fontSize: '16px',
        color: '#fff',
      })
      .setOrigin(0.5, 0)

    // Wild monster (right, upper).
    this._drawMonster(W - 90, 130, this.wild.name, this.wild.level, WILD_COLOR)
    this.wildHpBar = this._drawHpBar(W - 200, 200, 180, this.wild.hp, this.wild.max_hp)
    this.wildHpText = this.add.text(W - 200, 220, `HP ${this.wild.hp}/${this.wild.max_hp}`, {
      fontSize: '11px',
      color: '#fff',
    })

    // Player monster (left, lower).
    this._drawMonster(90, 290, this.player.name, this.player.level, PLAYER_COLOR)
    this.playerHpBar = this._drawHpBar(20, 360, 180, this.player.hp, this.player.max_hp)
    this.playerHpText = this.add.text(20, 380, `HP ${this.player.hp}/${this.player.max_hp}`, {
      fontSize: '11px',
      color: '#fff',
    })

    // Event log (middle-left).
    this.logText = this.add.text(20, 60, '', {
      fontSize: '12px',
      color: '#ddd',
      wordWrap: { width: 360 },
    })

    // Submenu header (shows above the buttons when in a submenu).
    this.headerText = this.add.text(MENU_X, MENU_Y - 28, '', {
      fontSize: '12px',
      color: '#aaa',
    }).setOrigin(0.5, 0.5)

    // First render of the main menu.
    this._renderMenu()

    // Wire up server messages.
    socket.onMessage((msg) => {
      if (msg.type === 'BATTLE_TURN') this._applyTurn(msg as BattleTurnMessage)
      else if (msg.type === 'BATTLE_END') this._endBattle(msg as BattleEndMessage)
    })
  }

  // --- UI builders ----------------------------------------------------------

  private _drawMonster(x: number, y: number, name: string, level: number, fallbackColor: number): void {
    const look = MONSTER_LOOK[name.toLowerCase()]
    if (look) {
      this._drawCreatureSilhouette(x, y, look)
    } else {
      // Unknown monster — fall back to a simple colored disc with a highlight
      // so it's still visible and recognizable.
      this.add.circle(x, y, 28, fallbackColor)
      this.add.circle(x, y - 8, 6, 0xffffff, 0.6)
    }
    this.add
      .text(x, y + 40, `${name} Lv${level}`, {
        fontSize: '11px',
        color: '#fff',
      })
      .setOrigin(0.5)
  }

  // Flat creature silhouettes drawn from primitives — each species gets its
  // own recognizable shape (ears, tail flame, leaf, horn, segments). Body
  // fits a ~60×60 footprint centered on (x, y); damage flashes and float
  // numbers stay aligned because the silhouette still occupies that box.
  private _drawCreatureSilhouette(x: number, y: number, look: MonsterLook): void {
    const g = this.add.graphics()
    const body = look.body
    const accent = look.accent
    switch (look.shape) {
      case 'pikachu': {
        // Round yellow body
        g.fillStyle(body, 1)
        g.fillCircle(x, y + 5, 22)
        // Long pointed ears
        g.fillStyle(accent, 1)
        g.fillTriangle(x - 12, y - 22, x - 7, y - 5, x - 17, y - 7)
        g.fillTriangle(x + 12, y - 22, x + 7, y - 5, x + 17, y - 7)
        // Red cheek dots
        g.fillStyle(0xff3344, 1)
        g.fillCircle(x - 11, y + 5, 3)
        g.fillCircle(x + 11, y + 5, 3)
        // Eyes
        g.fillStyle(0xffffff, 1)
        g.fillCircle(x - 6, y - 2, 2.5)
        g.fillCircle(x + 6, y - 2, 2.5)
        g.fillStyle(0x000000, 1)
        g.fillCircle(x - 6, y - 2, 1.2)
        g.fillCircle(x + 6, y - 2, 1.2)
        break
      }
      case 'charmander': {
        // Orange oval body
        g.fillStyle(body, 1)
        g.fillEllipse(x, y + 5, 40, 30)
        // Tail flame
        g.fillStyle(accent, 1)
        g.fillTriangle(x + 22, y + 5, x + 32, y - 6, x + 30, y + 12)
        // Eyes
        g.fillStyle(0xffffff, 1)
        g.fillCircle(x - 7, y - 3, 3)
        g.fillCircle(x + 7, y - 3, 3)
        g.fillStyle(0x000000, 1)
        g.fillCircle(x - 7, y - 3, 1.5)
        g.fillCircle(x + 7, y - 3, 1.5)
        break
      }
      case 'squirtle': {
        // Blue body
        g.fillStyle(body, 1)
        g.fillCircle(x, y + 5, 22)
        // Shell (darker ellipse on back)
        g.fillStyle(accent, 1)
        g.fillEllipse(x, y + 8, 34, 18)
        // Shell swirl (white circle outline)
        g.fillStyle(0xffffff, 1)
        g.fillCircle(x, y + 5, 6)
        g.lineStyle(2, accent, 1)
        g.strokeCircle(x, y + 5, 6)
        // Eyes
        g.fillStyle(0xffffff, 1)
        g.fillCircle(x - 7, y - 5, 3)
        g.fillCircle(x + 7, y - 5, 3)
        g.fillStyle(0x000000, 1)
        g.fillCircle(x - 7, y - 5, 1.5)
        g.fillCircle(x + 7, y - 5, 1.5)
        break
      }
      case 'sproutling': {
        // Green round body
        g.fillStyle(body, 1)
        g.fillCircle(x, y + 8, 20)
        // Leaf on top (triangle)
        g.fillStyle(accent, 1)
        g.fillTriangle(x, y - 22, x - 11, y - 2, x + 11, y - 2)
        // Eyes
        g.fillStyle(0xffffff, 1)
        g.fillCircle(x - 6, y + 5, 2.5)
        g.fillCircle(x + 6, y + 5, 2.5)
        g.fillStyle(0x000000, 1)
        g.fillCircle(x - 6, y + 5, 1.2)
        g.fillCircle(x + 6, y + 5, 1.2)
        break
      }
      case 'rattata': {
        // Purple oval body
        g.fillStyle(body, 1)
        g.fillEllipse(x, y + 5, 40, 28)
        // Small round ears
        g.fillStyle(accent, 1)
        g.fillCircle(x - 15, y - 6, 5)
        g.fillCircle(x + 15, y - 6, 5)
        // Red eyes
        g.fillStyle(0xff3344, 1)
        g.fillCircle(x - 7, y + 2, 2.5)
        g.fillCircle(x + 7, y + 2, 2.5)
        g.fillStyle(0x000000, 1)
        g.fillCircle(x - 7, y + 2, 1)
        g.fillCircle(x + 7, y + 2, 1)
        break
      }
      case 'caterpie': {
        // 3-segment green caterpillar
        g.fillStyle(body, 1)
        g.fillCircle(x - 12, y + 8, 9)
        g.fillCircle(x, y + 5, 11)
        g.fillCircle(x + 12, y + 8, 9)
        // Segment separators
        g.lineStyle(1, accent, 0.6)
        g.lineBetween(x - 6, y + 4, x - 6, y + 11)
        g.lineBetween(x + 6, y + 4, x + 6, y + 11)
        // Center-segment eyes
        g.fillStyle(0x000000, 1)
        g.fillCircle(x - 4, y + 3, 2)
        g.fillCircle(x + 4, y + 3, 2)
        break
      }
      case 'weedle': {
        // Yellow-brown oval body
        g.fillStyle(body, 1)
        g.fillEllipse(x, y + 8, 36, 22)
        // Horn on forehead
        g.fillStyle(accent, 1)
        g.fillTriangle(x, y - 12, x - 5, y + 0, x + 5, y + 0)
        // Red eyes
        g.fillStyle(0xff3344, 1)
        g.fillCircle(x - 7, y + 5, 2.5)
        g.fillCircle(x + 7, y + 5, 2.5)
        g.fillStyle(0x000000, 1)
        g.fillCircle(x - 7, y + 5, 1)
        g.fillCircle(x + 7, y + 5, 1)
        break
      }
    }
  }

  private _drawHpBar(
    x: number,
    y: number,
    width: number,
    hp: number,
    maxHp: number,
  ): Phaser.GameObjects.Rectangle {
    const ratio: number = Math.max(0, Math.min(1, hp / maxHp))
    const fillW: number = Math.max(1, Math.floor(width * ratio))
    // Background (empty track).
    this.add.rectangle(x + width / 2, y, width, 10, 0x333333)
    // Foreground (current HP) — start at the displayed value.
    const bar = this.add.rectangle(
      x + fillW / 2,
      y,
      fillW,
      10,
      this._hpColor(ratio),
    )
    return bar
  }

  private _hpColor(ratio: number): number {
    if (ratio > 0.5) return 0x44dd55
    if (ratio > 0.2) return 0xddcc44
    return 0xdd5544
  }

  private _updateHpBar(
    bar: Phaser.GameObjects.Rectangle,
    x: number,
    y: number,
    width: number,
    hp: number,
    maxHp: number,
  ): void {
    const ratio: number = Math.max(0, Math.min(1, hp / maxHp))
    const fillW: number = Math.max(1, Math.floor(width * ratio))
    bar.setSize(fillW, 10)
    bar.setPosition(x + fillW / 2, y)
    bar.setFillStyle(this._hpColor(ratio))
  }

  // Tween the HP bar from the currently displayed value to the new one over
  // 300ms. The label + displayed counter update in lockstep at the end.
  private _tweenHpBar(
    bar: Phaser.GameObjects.Rectangle,
    x: number,
    y: number,
    width: number,
    fromHp: number,
    toHp: number,
    maxHp: number,
    onComplete: () => void,
  ): void {
    const delta = toHp - fromHp
    if (delta === 0) {
      onComplete()
      return
    }
    this.tweens.addCounter({
      from: 0,
      to: 1,
      duration: 300,
      ease: 'Quad.easeOut',
      onUpdate: (tween) => {
        const v = tween.getValue() as number
        const cur = fromHp + delta * v
        this._updateHpBar(bar, x, y, width, cur, maxHp)
      },
      onComplete: () => {
        this._updateHpBar(bar, x, y, width, toHp, maxHp)
        onComplete()
      },
    })
  }

  // --- Menu rendering -------------------------------------------------------

  // Wipe the current button row + header, then draw whichever menu matches
  // menuState. Called whenever the submenu changes (or first render).
  private _renderMenu(): void {
    this._clearMenu()

    switch (this.menuState) {
      case 'main':
        this._renderMainMenu()
        break
      case 'skill':
        this._renderSkillMenu()
        break
      case 'item':
        this._renderItemMenu()
        break
    }
  }

  private _clearMenu(): void {
    this.menuButtons.forEach((o) => o.destroy())
    this.menuButtons = []
    this.headerText.setText('')
  }

  private _renderMainMenu(): void {
    MAIN_MENU.forEach((entry, i) => {
      const btn = this._makeButton(MENU_Y + i * MENU_GAP, entry.label, () => {
        this._onMainAction(entry.key)
      })
      this.menuButtons.push(btn)
    })
  }

  private _renderSkillMenu(): void {
    this.headerText.setText('Choose a skill')
    if (this.skills.length === 0) {
      this._makeLabel(MENU_Y, '(no skills available)', '#888')
      this._addBackButton(MENU_Y + MENU_GAP)
      return
    }
    this.skills.forEach((s, i) => {
      const label =
        s.kind === 'status'
          ? `${s.name}`
          : `${s.name} (${s.kind === 'special' ? 'sp' : 'atk'}, pwr ${s.power})`
      const btn = this._makeButton(MENU_Y + i * MENU_GAP, label, () => {
        this._sendSkill(s.id)
      })
      this.menuButtons.push(btn)
    })
    this._addBackButton(MENU_Y + this.skills.length * MENU_GAP)
  }

  private _renderItemMenu(): void {
    this.headerText.setText('Choose an item')
    if (this.items.length === 0) {
      this._makeLabel(MENU_Y, '(bag is empty)', '#888')
      this._addBackButton(MENU_Y + MENU_GAP)
      return
    }
    this.items.forEach((it, i) => {
      const label = `${it.name} ×${it.qty}`
      const btn = this._makeButton(MENU_Y + i * MENU_GAP, label, () => {
        this._sendItem(it.id)
      })
      this.menuButtons.push(btn)
    })
    this._addBackButton(MENU_Y + this.items.length * MENU_GAP)
  }

  private _makeButton(
    y: number,
    label: string,
    onClick: () => void,
  ): Phaser.GameObjects.Text {
    const btn = this.add
      .text(MENU_X, y, label, {
        fontSize: '14px',
        color: '#000',
        backgroundColor: '#fff',
        padding: { x: 12, y: 6 },
      })
      .setOrigin(0.5, 0.5)
      .setInteractive({ useHandCursor: true })
    btn.on('pointerdown', onClick)
    return btn
  }

  private _makeLabel(y: number, text: string, color: string): Phaser.GameObjects.Text {
    const t = this.add.text(MENU_X, y, text, {
      fontSize: '13px',
      color,
    }).setOrigin(0.5, 0.5)
    return t
  }

  private _addBackButton(y: number): void {
    const btn = this._makeButton(y, '← Back', () => {
      this.menuState = 'main'
      this._renderMenu()
    })
    this.menuButtons.push(btn)
  }

  private _setMenuEnabled(enabled: boolean): void {
    this.menuButtons.forEach((o) => {
      // Only Text supports setInteractive/disableInteractive; labels are inert.
      if (o instanceof Phaser.GameObjects.Text) {
        if (enabled) o.setInteractive({ useHandCursor: true })
        else o.disableInteractive()
      }
    })
  }

  // --- Action dispatch ------------------------------------------------------

  private _onMainAction(key: ActionKey): void {
    if (key === 'attack') {
      this._sendAttack()
    } else if (key === 'skill') {
      this.menuState = 'skill'
      this._renderMenu()
    } else if (key === 'item') {
      this.menuState = 'item'
      this._renderMenu()
    } else if (key === 'flee') {
      this._sendFlee()
    }
  }

  private _sendAttack(): void {
    this._setMenuEnabled(false)
    socket.send({ type: 'ACTION', choice: 'attack' })
  }

  private _sendSkill(skillId: string): void {
    this._setMenuEnabled(false)
    socket.send({ type: 'ACTION', choice: 'skill', skillId })
  }

  private _sendItem(itemId: string): void {
    this._setMenuEnabled(false)
    socket.send({ type: 'ACTION', choice: 'item', itemId })
  }

  private _sendFlee(): void {
    this._setMenuEnabled(false)
    socket.send({ type: 'ACTION', choice: 'flee' })
  }

  // --- Event handlers -------------------------------------------------------

  private _applyTurn(msg: BattleTurnMessage): void {
    const lines: string[] = []
    let pendingWildTween: { from: number; to: number } | null = null
    let pendingPlayerTween: { from: number; to: number } | null = null

    msg.events.forEach((ev: BattleEvent) => {
      if (ev.kind === 'text') {
        lines.push(ev.msg)
        return
      }
      if (ev.kind === 'damage' || ev.kind === 'heal') {
        // Collect HP transitions so we can tween + animate simultaneously
        // rather than snapping each event.
        if (ev.target === 'wild') {
          if (!pendingWildTween) pendingWildTween = { from: this.wild.hp, to: ev.hp.cur }
          else pendingWildTween.to = ev.hp.cur
        } else {
          if (!pendingPlayerTween) pendingPlayerTween = { from: this.player.hp, to: ev.hp.cur }
          else pendingPlayerTween.to = ev.hp.cur
        }
        // Flash + float damage number on the most recent hit.
        this._flashTarget(ev.target)
        const prefix = ev.kind === 'heal' ? '+' : '-'
        this._floatNumber(ev.target, `${prefix}${ev.amount}`)
      }
    })

    // Apply HP changes immediately to the model — animation tweens the
    // displayed value to the new one. Labels are updated at tween end so they
    // don't flicker mid-animation.
    if (pendingWildTween) {
      const tween: { from: number; to: number } = pendingWildTween
      const fromDisplayed = this.wildHpDisplayed
      const toDisplayed = tween.to
      this.wild.hp = toDisplayed
      this._tweenHpBar(
        this.wildHpBar,
        W - 200,
        200,
        180,
        fromDisplayed,
        toDisplayed,
        this.wild.max_hp,
        () => {
          this.wildHpDisplayed = toDisplayed
          this.wildHpText.setText(`HP ${this.wild.hp}/${this.wild.max_hp}`)
        },
      )
    }
    if (pendingPlayerTween) {
      const tween: { from: number; to: number } = pendingPlayerTween
      const fromDisplayed = this.playerHpDisplayed
      const toDisplayed = tween.to
      this.player.hp = toDisplayed
      this._tweenHpBar(
        this.playerHpBar,
        20,
        360,
        180,
        fromDisplayed,
        toDisplayed,
        this.player.max_hp,
        () => {
          this.playerHpDisplayed = toDisplayed
          this.playerHpText.setText(`HP ${this.player.hp}/${this.player.max_hp}`)
        },
      )
    }

    this.logText.setText(lines.join('\n'))

    // If the battle is still ongoing, reset to the main menu and re-enable
    // interaction (battle may have ended mid-events — in that case the
    // awaitingInput flag is false and we'll just wait for BATTLE_END).
    if (msg.awaitingInput) {
      this.menuState = 'main'
      this._renderMenu()
      this._setMenuEnabled(true)
    } else {
      this._setMenuEnabled(false)
    }
  }

  // White flash overlay that fades out fast — visual punch on damage.
  private _flashTarget(target: 'player' | 'wild'): void {
    const x: number = target === 'wild' ? W - 90 : 90
    const y: number = target === 'wild' ? 130 : 290
    const flash = this.add.rectangle(x, y, 60, 60, 0xffffff, 0.7)
    this.tweens.add({
      targets: flash,
      alpha: 0,
      duration: 200,
      onComplete: () => flash.destroy(),
    })
  }

  // Floating damage / heal number — drifts up and fades out.
  private _floatNumber(target: 'player' | 'wild', text: string): void {
    const x: number = target === 'wild' ? W - 90 : 90
    const y: number = target === 'wild' ? 130 : 290
    const isHeal = text.startsWith('+')
    const label = this.add
      .text(x, y - 20, text, {
        fontSize: '18px',
        color: isHeal ? '#88ff88' : '#ff8888',
        fontStyle: 'bold',
        stroke: '#000',
        strokeThickness: 3,
      })
      .setOrigin(0.5)
    this.tweens.add({
      targets: label,
      y: y - 50,
      alpha: 0,
      duration: 900,
      ease: 'Quad.easeOut',
      onComplete: () => label.destroy(),
    })
  }

  private _endBattle(msg: BattleEndMessage): void {
    const summary: string =
      msg.result === 'win'
        ? `You won! (+${msg.xpGained} XP)`
        : msg.result === 'lose'
        ? 'You blacked out…'
        : 'Got away safely.'
    this.logText.setText((this.logText.text ?? '') + '\n' + summary)
    this.titleText.setText('Battle over')
    this._setMenuEnabled(false)
    // Brief delay so the player sees the result, then return to the overworld.
    this.time.delayedCall(1200, () => {
      this.scene.start('World')
    })
  }
}
