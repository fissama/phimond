import { describe, expect, it } from 'vitest';
import { Character, ServerMessage } from '@phimond/protocol';

const character = {
  id: 'c1', name: 'tester', level: 1, xp: 0, gold: 10, crystals: 0, map_id: 'severa', x: 6, y: 12,
  active_pet_id: 'p1', revision: 3, pets: [{ id: 'p1', species_id: 'snail', name: 'Moss', level: 1, skills: null, parents: null }],
  inventory: null, recipes: null, quests: null, arena_tier: 0, battle: null,
};

describe('server messages', () => {
  it('chuẩn hóa null thành rỗng', () => {
    const msg = ServerMessage.parse({ op: 'state', request_id: 'r1', sequence: 3, data: { character, events: null } });
    expect(msg.op).toBe('state');
    if (msg.op !== 'state') return;
    expect(msg.data.events).toEqual([]);
    expect(msg.data.character.pets[0]?.skills).toEqual([]);
    expect(msg.data.character.inventory).toEqual({});
  });

  it('nhận lỗi từ server', () => {
    const msg = ServerMessage.parse({ op: 'error', request_id: 'r2', data: { message: 'too far' } });
    expect(msg.op).toBe('error');
  });

  it('từ chối snapshot thiếu revision', () => {
    const { revision: _r, ...bad } = character;
    expect(() => Character.parse(bad)).toThrow();
  });
});
