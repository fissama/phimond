import Phaser from 'phaser'
import { socket } from '../net/socket'

const PLAYER_NAME_KEY = 'phimond.playerName'

export class LoginScene extends Phaser.Scene {
  private inputEl!: HTMLInputElement
  private errorText!: Phaser.GameObjects.Text

  constructor() {
    super('Login')
  }

  create(): void {
    const cx = this.scale.width / 2

    this.add.text(cx, 160, 'Phimond', { fontSize: '40px', color: '#fff' }).setOrigin(0.5)
    this.add
      .text(cx, 220, 'Enter your trainer name', { fontSize: '16px', color: '#aaa' })
      .setOrigin(0.5)

    // Mount an HTML input on top of the canvas so users can type freely.
    this.inputEl = document.createElement('input')
    this.inputEl.type = 'text'
    this.inputEl.maxLength = 16
    this.inputEl.placeholder = 'trainer1'
    this.inputEl.autocomplete = 'off'
    this.inputEl.style.cssText = `
      position: absolute;
      left: 50%;
      top: 280px;
      transform: translateX(-50%);
      padding: 10px 14px;
      font-size: 18px;
      border: 2px solid #fff;
      background: #000;
      color: #fff;
      border-radius: 6px;
      width: 220px;
      text-align: center;
      outline: none;
      z-index: 10;
    `
    const saved = localStorage.getItem(PLAYER_NAME_KEY)
    if (saved) this.inputEl.value = saved
    document.body.appendChild(this.inputEl)
    this.inputEl.focus()

    const submitBtn = this.add
      .text(cx, 360, '  Start  ', {
        fontSize: '20px',
        color: '#000',
        backgroundColor: '#fff',
        padding: { x: 16, y: 8 },
      })
      .setOrigin(0.5)
      .setInteractive({ useHandCursor: true })

    this.errorText = this.add
      .text(cx, 410, '', { fontSize: '14px', color: '#f88' })
      .setOrigin(0.5)

    const submit = () => {
      const name = this.inputEl.value.trim()
      if (!name) {
        this._showError('Name required')
        return
      }
      localStorage.setItem(PLAYER_NAME_KEY, name)
      socket.send({ type: 'HELLO', name })
      // Show a "joining" state and wait for the next STATE message to confirm.
      this._showError('')
      submitBtn.setText('Joining…')
      submitBtn.disableInteractive()
      this.inputEl.disabled = true
      // If the server sends an ERROR after HELLO, restore the form.
      const off = socket.onMessage((msg) => {
        if (msg.type === 'ERROR') {
          this._showError(msg.message)
          submitBtn.setText('  Start  ')
          submitBtn.setInteractive({ useHandCursor: true })
          this.inputEl.disabled = false
          this.inputEl.focus()
          off()
        }
        if (msg.type === 'STATE') {
          this._cleanup()
          off()
          this.scene.start('World')
        }
      })
    }

    submitBtn.on('pointerdown', submit)
    this.inputEl.addEventListener('keydown', (e) => {
      if (e.key === 'Enter') submit()
    })
  }

  private _showError(message: string): void {
    this.errorText.setText(message)
  }

  private _cleanup(): void {
    if (this.inputEl.parentNode) {
      this.inputEl.parentNode.removeChild(this.inputEl)
    }
  }
}
