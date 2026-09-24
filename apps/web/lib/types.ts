export type Definition = {
  id: string;
  name: string;
  confidence?: string;
  source?: string;
  [key: string]: unknown;
};
export type Species = Definition & {
  race: string;
  element: string;
  star: number;
  skills: string[];
};
export type Recipe = Definition & {
  parent_a: string;
  parent_b: string;
  result: string;
  min_level: number;
  min_player_level: number;
  gold_cost: number;
  soul_cost: number;
  opposite_gender: boolean;
  same_star: boolean;
  cross_race: boolean;
  consume_parents: boolean;
};
export type Catalog = {
  species: Record<string, Species>;
  skills: Record<string, Definition>;
  items: Record<string, Definition>;
  maps: Record<string, Definition>;
  recipes: Record<string, Recipe>;
  rules: Record<string, unknown>;
};
export type Pet = {
  id: string;
  species_id: string;
  name: string;
  level: number;
  gender: string;
  star: number;
  generation: number;
  appraised: boolean;
  retired: boolean;
  hp: number;
  max_hp: number;
  skills: string[];
  quality?: Record<string, number>;
  growth?: Record<string, number>;
};
export type Character = {
  id: string;
  name: string;
  level: number;
  gold: number;
  map_id: string;
  pets: Pet[];
  inventory: Record<string, number>;
  recipes: string[];
  revision: number;
};
export type Lineage = { pet: Pet; parents: Lineage[] };
