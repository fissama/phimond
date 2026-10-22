// Danh sách intent hợp lệ và dữ liệu đi kèm. Số phải là JSON integer.
export type Direction = 'left' | 'right' | 'up' | 'down';
export type BattleChoice = 'attack' | 'skill' | 'capture' | 'defend' | 'item' | 'auto' | 'flee';

export interface IntentMap {
  'auth.session': { token: string };
  'character.get': Record<string, never>;
  'world.move': { direction: Direction };
  'world.portal': { portal_id: string };
  'world.encounter': { spawn_id?: string };
  /** P01: chọn bệ đá ở Triệu Linh Điện (đứng kề bệ). */
  'starter.choose': { pedestal: number };
  /** P01: dùng trụ đá dịch chuyển (đứng kề trụ hoặc Trụ Sư). */
  'pillar.travel': { map_id: string };
  'npc.interact': { npc_id: string };
  'pet.appraise': { pet_id: string };
  'pet.activate': { pet_id: string };
  'pet.learn': { pet_id: string; skill_id: string };
  'pet.release': { pet_id: string };
  'pet.strengthen': { pet_id: string; donor_id: string };
  'pet.heal': Record<string, never>;
  'breeding.synthesize': { parent_a: string; parent_b: string; recipe_id: string; blessing: 0 | 1 };
  'recipe.learn': { recipe_id: string };
  'quest.accept': { quest_id: string };
  'quest.claim': { quest_id: string };
  'shop.buy': { item_id: string; quantity: number };
  'arena.challenge': Record<string, never>;
  'battle.action': { battle_id: string; turn: number; choice: BattleChoice; skill_id?: string; item_id?: string };
}
export type IntentOp = keyof IntentMap;

export interface ClientEnvelope<K extends IntentOp = IntentOp> {
  op: K;
  request_id: string;
  data: IntentMap[K];
}
