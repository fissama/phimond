import Phaser from 'phaser'
import { socket } from '../net/socket'

export class BootScene extends Phaser.Scene {
  private statusText!: Phaser.GameObjects.Text
  private retryBtn!: Phaser.GameObjects.Text

  constructor() {
    super('Boot')
  }

  create(): void {
    const cx = this.scale.width / 2
    const cy = this.scale.height / 2

    this.add
      .text(cx, cy - 40, 'Phimond', { fontSize: '40px', color: '#fff' })
      .setOrigin(0.5)

    this.statusText = this.add
      .text(cx, cy + 20, 'Connecting…', { fontSize: '18px', color: '#aaa' })
      .setOrigin(0.5)

    this.retryBtn = this.add
      .text(cx, cy + 60, '  Retry  ', {
        fontSize: '14px',
        color: '#000',
        backgroundColor: '#fff',
        padding: { x: 12, y: 6 },
      })
      .setOrigin(0.5)
      .setVisible(false)
      .setInteractive({ useHandCursor: true })

    this.retryBtn.on('pointerdown', () => {
      this.retryBtn.setVisible(false)
      this.statusText.setText('Connecting…')
      this.statusText.setColor('#aaa')
      socket.retry()
    })

    socket.connect()
    socket.onStatus((s) => {
      switch (s) {
        case 'open':
          this.scene.start('Login')
          break
        case 'closed':
          this.statusText.setText('Disconnected — retrying…')
          this.statusText.setColor('#f88')
          this.retryBtn.setVisible(false)
          break
        case 'failed':
          this.statusText.setText('Could not connect. Check that the server is running.')
          this.statusText.setColor('#f88')
          this.retryBtn.setVisible(true)
          break
      }
    })
  }
}