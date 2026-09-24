import type { Recipe } from "./types";
export type Branch = {
  speciesId: string;
  recipe?: Recipe;
  parents: Branch[];
  cycle?: boolean;
};
export function dependencyTree(
  speciesId: string,
  recipes: Record<string, Recipe>,
  selection: Record<string, string> = {},
  path: string[] = [],
): Branch {
  if (path.includes(speciesId) || path.length >= 20)
    return { speciesId, parents: [], cycle: true };
  const choices = Object.values(recipes)
    .filter((r) => r.result === speciesId)
    .sort((a, b) => a.id.localeCompare(b.id));
  const recipe =
    choices.find((r) => r.id === selection[speciesId]) || choices[0];
  return {
    speciesId,
    recipe,
    parents: recipe
      ? [recipe.parent_a, recipe.parent_b].map((id) =>
          dependencyTree(id, recipes, selection, [...path, speciesId]),
        )
      : [],
  };
}
