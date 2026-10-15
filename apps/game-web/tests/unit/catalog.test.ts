import { readFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { describe, expect, it } from 'vitest';
import { Catalog } from '@phimond/protocol';

// Dựng catalog giống GET /api/content từ thư mục data/ thật (server nạp từ đây).
const data = (p: string) => JSON.parse(readFileSync(resolve(import.meta.dirname, '../../../../data', p), 'utf8'));

describe('catalog thật', () => {
  it('schema nhận dữ liệu 5 map, NPC và 14 loài hiện hành', () => {
    const catalog = Catalog.parse({
      species: data('pets/species.json'),
      skills: data('skills/skills.json'),
      maps: data('maps/maps.json'),
      npcs: data('npcs/npcs.json'),
      items: data('items/items.json'),
      recipes: data('recipes/recipes.json'),
      quests: data('quests/quests.json'),
    });
    expect(Object.keys(catalog.maps).sort()).toEqual(['arena', 'beach', 'forest', 'ranch', 'severa']);
    expect(Object.keys(catalog.species)).toHaveLength(14);
    expect(catalog.maps.severa?.portals.map((p) => p.to).sort()).toEqual(['arena', 'forest', 'ranch']);
  });
});
