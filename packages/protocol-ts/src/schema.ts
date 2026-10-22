import { z } from 'zod';

// Chuẩn hóa: server cũ có thể trả null cho mảng; client coi là rỗng.
const list = <T extends z.ZodTypeAny>(item: T) =>
  z.preprocess((v) => (v === null || v === undefined ? [] : v), z.array(item));
const rec = <T extends z.ZodTypeAny>(item: T) =>
  z.preprocess((v) => (v === null || v === undefined ? {} : v), z.record(item));

export const BattleEvent = z
  .object({
    seq: z.number().int(),
    type: z.string(),
    actor_id: z.string().optional().default(''),
    target_id: z.string().optional().default(''),
    amount: z.number().optional().default(0),
    message: z.string().optional().default(''),
  })
  .passthrough();
export type BattleEvent = z.infer<typeof BattleEvent>;

export const BattleUnit = z
  .object({
    id: z.string(),
    name: z.string(),
    side: z.enum(['player', 'enemy']),
    species_id: z.string(),
    hp: z.number(),
    max_hp: z.number(),
    mp: z.number().optional().default(0),
    max_mp: z.number().optional().default(0),
    statuses: list(z.object({ id: z.string(), remaining: z.number() }).passthrough()),
  })
  .passthrough();
export type BattleUnit = z.infer<typeof BattleUnit>;

export const Battle = z
  .object({
    id: z.string(),
    turn: z.number().int(),
    phase: z.string(),
    result: z.string().optional().default(''),
    units: list(BattleUnit),
  })
  .passthrough();
export type Battle = z.infer<typeof Battle>;

export const Pet = z
  .object({
    id: z.string(),
    species_id: z.string(),
    name: z.string(),
    level: z.number(),
    xp: z.number().optional().default(0),
    gender: z.string().optional().default(''),
    star: z.number().optional().default(1),
    appraised: z.boolean().optional().default(false),
    strengthening: z.number().optional().default(0),
    retired: z.boolean().optional().default(false),
    skills: list(z.string()),
    parents: list(z.string()),
    hp: z.number().optional().default(0),
    mp: z.number().optional().default(0),
    max_hp: z.number().optional().default(0),
    max_mp: z.number().optional().default(0),
  })
  .passthrough();
export type Pet = z.infer<typeof Pet>;

export const Character = z
  .object({
    id: z.string(),
    name: z.string(),
    level: z.number(),
    xp: z.number().optional().default(0),
    gold: z.number().optional().default(0),
    crystals: z.number().optional().default(0),
    map_id: z.string(),
    x: z.number(),
    y: z.number().optional().default(0),
    active_pet_id: z.string().optional().default(''),
    revision: z.number().int(),
    pets: list(Pet),
    inventory: rec(z.number()),
    recipes: list(z.string()),
    quests: rec(z.object({ progress: z.number(), claimed: z.boolean() }).passthrough()),
    arena_tier: z.number().optional().default(0),
    battle: Battle.nullable().optional().default(null),
    // P01: map đã ghé, quái đang ẩn (id → Unix ms hiện lại) và giờ server lúc tạo snapshot.
    visited: list(z.string()),
    spawn_hidden: rec(z.number()),
    server_time_ms: z.number().optional().default(0),
  })
  .passthrough();
export type Character = z.infer<typeof Character>;

export const StateData = z
  .object({
    character: Character,
    events: list(BattleEvent),
    presentation: z
      .object({ battle_id: z.string().optional(), completed_battle: Battle.optional() })
      .passthrough()
      .optional(),
  })
  .passthrough();

export const StateMessage = z.object({
  op: z.literal('state'),
  request_id: z.string().optional().default(''),
  sequence: z.number().int(),
  data: StateData,
});
export const ErrorMessage = z.object({
  op: z.literal('error'),
  request_id: z.string().optional().default(''),
  data: z.object({ message: z.string() }).passthrough(),
});
export const ServerMessage = z.discriminatedUnion('op', [StateMessage, ErrorMessage]);
export type ServerMessage = z.infer<typeof ServerMessage>;

export const AuthResponse = z.object({ token: z.string().min(1), character_id: z.string() });

// P01 (ADR-P01-01): tọa độ ô, x sang phải, y xuống dưới. Trường cũ (x/spawn) giữ tùy chọn cho client cũ.
export const Point = z.object({ x: z.number(), y: z.number(), face: z.enum(['up', 'down', 'left', 'right']).optional() }).passthrough();
export type Point = z.infer<typeof Point>;
const Rect = z.tuple([z.number(), z.number(), z.number(), z.number()]);
export const Portal = z
  .object({
    id: z.string(),
    to: z.string(),
    rect: Rect.optional(),
    arrive: Point.optional(),
    locked: z.boolean().optional().default(false),
    requires: z.string().optional(),
    redirect: z.object({ if_visited: z.string(), to: z.string(), arrive: Point }).optional(),
    x: z.number().optional(),
    spawn: z.number().optional(),
  })
  .passthrough();
export type Portal = z.infer<typeof Portal>;
export const WildSpawn = z
  .object({ id: z.string(), species_id: z.string(), x: z.number(), y: z.number(), zone: z.string().optional(), respawn_s: z.number().optional() })
  .passthrough();
export type WildSpawn = z.infer<typeof WildSpawn>;
export const Pillar = z
  .object({
    x: z.number(),
    y: z.number(),
    npc: z.string(),
    dest: list(z.object({ map: z.string(), arrive: Point.optional(), locked: z.boolean().optional().default(false), min_level: z.number().optional() }).passthrough()),
  })
  .passthrough();
export type Pillar = z.infer<typeof Pillar>;
export const Pedestal = z.object({ index: z.number(), x: z.number(), y: z.number(), starter: z.string(), species: z.string() }).passthrough();
export type Pedestal = z.infer<typeof Pedestal>;
export const MapDef = z
  .object({
    id: z.string(),
    name: z.string(),
    kind: z.string().optional().default(''),
    theme: z.string().optional().default(''),
    level: z.array(z.number()).nullable().optional().default(null),
    width: z.number(),
    height: z.number().optional().default(0),
    spawn_default: Point.optional(),
    respawn_to: z.string().optional(),
    portals: list(Portal),
    pillar: Pillar.nullable().optional().default(null),
    pedestals: list(Pedestal),
    wild_spawns: list(WildSpawn),
    spawns: list(z.string()),
    walk: z.string().optional().default(''),
    layout: list(z.string()),
    facades: rec(z.string()),
    backdrop: z.string().nullable().optional().default(null),
  })
  .passthrough();
export type MapDef = z.infer<typeof MapDef>;
export const Npc = z
  .object({
    id: z.string(),
    name: z.string(),
    map_id: z.string(),
    x: z.number(),
    y: z.number().optional().default(0),
    face: z.string().optional(),
    roles: list(z.string()),
    dialogue: z.string().optional().default(''),
  })
  .passthrough();
export type Npc = z.infer<typeof Npc>;
export const Catalog = z
  .object({
    species: rec(z.object({ id: z.string(), name: z.string() }).passthrough()),
    skills: rec(z.object({ id: z.string(), name: z.string() }).passthrough()),
    statuses: rec(z.object({ id: z.string(), name: z.string() }).passthrough()),
    maps: rec(MapDef),
    npcs: rec(Npc),
    items: rec(z.object({ id: z.string(), name: z.string() }).passthrough()),
    recipes: rec(z.object({ id: z.string(), name: z.string() }).passthrough()),
    quests: rec(z.object({ id: z.string(), name: z.string() }).passthrough()),
  })
  .passthrough();
export type Catalog = z.infer<typeof Catalog>;
