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

export const Portal = z.object({ id: z.string(), x: z.number(), to: z.string(), spawn: z.number().optional() }).passthrough();
export const WildSpawn = z.object({ id: z.string(), species_id: z.string(), x: z.number(), y: z.number() }).passthrough();
export const MapDef = z
  .object({
    id: z.string(),
    name: z.string(),
    width: z.number(),
    height: z.number().optional().default(0),
    portals: list(Portal),
    wild_spawns: list(WildSpawn),
    spawns: list(z.string()),
  })
  .passthrough();
export const Npc = z
  .object({ id: z.string(), name: z.string(), map_id: z.string(), x: z.number(), y: z.number().optional().default(0), roles: list(z.string()) })
  .passthrough();
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
