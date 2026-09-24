// Mirror of shared/PROTOCOL.md — keep in sync when the wire format changes.

export type Dir = 'up' | 'down' | 'left' | 'right'
export type BattleChoice = 'attack' | 'skill' | 'item' | 'flee'

// --- Client → Server -------------------------------------------------------

export interface HelloMessage {
  type: 'HELLO'
  name: string
}

export interface MoveMessage {
  type: 'MOVE'
  dir: Dir
}

export interface ActionMessage {
  type: 'ACTION'
  choice: BattleChoice
  skillId?: string
  itemId?: string
}

export type ClientMessage = HelloMessage | MoveMessage | ActionMessage

// --- Server → Client -------------------------------------------------------

export interface PlayerState {
  name: string
  x: number
  y: number
  dir: Dir
}

export interface StateMessage {
  type: 'STATE'
  players: PlayerState[]
}

export interface ErrorMessage {
  type: 'ERROR'
  message: string
}

// --- Battle payloads -------------------------------------------------------

export interface BattleMonster {
  id: string
  name: string
  level: number
  hp: number
  max_hp: number
  attack: number
  defense: number
  speed: number
  skills: string[]
}

export interface BattleInventoryItem {
  id: string
  qty: number
}

// Full metadata for one skill — server sends this so the SkillPicker can
// render a meaningful label (e.g. "Thunder Shock [special, pwr 11]") without
// needing its own copy of skills.json.
export interface BattleSkillDetail {
  id: string
  name: string
  kind: 'physical' | 'special' | 'status'
  power: number
}

// Same idea for items — name + qty so the ItemPicker shows "Potion ×3".
export interface BattleItemDetail {
  id: string
  name: string
  qty: number
}

export type BattleEvent =
  | { kind: 'text'; msg: string }
  | { kind: 'damage'; target: 'player' | 'wild'; amount: number; hp: { cur: number; max: number } }
  | { kind: 'heal'; target: 'player' | 'wild'; amount: number; hp: { cur: number; max: number } }

export interface BattleStartMessage {
  type: 'BATTLE_START'
  wild: BattleMonster
  player: BattleMonster
  inventory: BattleInventoryItem[]
  skills: BattleSkillDetail[]
  items: BattleItemDetail[]
}

export interface BattleTurnMessage {
  type: 'BATTLE_TURN'
  events: BattleEvent[]
  awaitingInput: boolean
}

export interface BattleEndMessage {
  type: 'BATTLE_END'
  result: 'win' | 'lose' | 'flee'
  xpGained: number
}

export type ServerMessage =
  | StateMessage
  | ErrorMessage
  | BattleStartMessage
  | BattleTurnMessage
  | BattleEndMessage
