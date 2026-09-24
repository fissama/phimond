import { test } from "node:test";
import assert from "node:assert/strict";
import { dependencyTree } from "./planner.ts";
import type { Recipe } from "./types";
const recipe = (id: string, a: string, b: string, result: string) =>
  ({ id, parent_a: a, parent_b: b, result }) as Recipe;
test("expands both parents and nested dependencies", () => {
  const tree = dependencyTree("c", {
    r: recipe("r", "a", "b", "c"),
    s: recipe("s", "x", "y", "a"),
  });
  assert.equal(tree.parents[0].parents[1].speciesId, "y");
  assert.equal(tree.parents[1].speciesId, "b");
});
test("cycles stop without erasing duplicate sibling requirements", () => {
  const tree = dependencyTree("a", { r: recipe("r", "a", "b", "a") });
  assert.equal(tree.parents[0].cycle, true);
  assert.equal(tree.parents[1].cycle, undefined);
});
test("respects chosen recipe and gives raw acquisition leaves", () => {
  const tree = dependencyTree(
    "c",
    { r: recipe("r", "a", "b", "c"), s: recipe("s", "x", "y", "c") },
    { c: "s" },
  );
  assert.equal(tree.parents[0].speciesId, "x");
  assert.equal(tree.parents[0].recipe, undefined);
});
