import Phaser from 'phaser'
import { BootScene } from './scenes/BootScene'
import { LoginScene } from './scenes/LoginScene'
import { WorldScene } from './scenes/WorldScene'
import { BattleScene } from './scenes/BattleScene'

const config: Phaser.Types.Core.GameConfig = {
  type: Phaser.AUTO,
  parent: 'game',
  width: 640,           // 20 tiles * 32 px
  height: 480,          // 15 tiles * 32 px
  pixelArt: true,
  backgroundColor: '#1a1a1a',
  scale: {
    mode: Phaser.Scale.FIT,
    autoCenter: Phaser.Scale.CENTER_BOTH,
  },
  scene: [BootScene, LoginScene, WorldScene, BattleScene],
}

new Phaser.Game(config)
