#!/usr/bin/env python3
"""Register the owner-requested eight authored species; never activate runtime.

The source registry's species map remains the frozen APK namespace. New IDs
live in authored_species so rebuilding the historical source catalog is safe.
Numeric data is copied as a P13 design candidate, not promoted into P11 rules.
"""
import argparse
import copy
import hashlib
import json
from pathlib import Path

from p10_catalog import encoded, read, require

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "data/p10"
P13 = ROOT / ".ai/plan/phases/P13-skills"
EVIDENCE = ROOT / ".ai/plan/phases/P10-pet-model/extension-20261013"
CANDIDATE = P13 / "P13-candidate-species-catalog-160.json"
SELECTION = ROOT / ".ai/plan/phases/P10-pet-model/redraw-kit/owner-atlas-selection.json"
PROPOSALS = [f"P13-NEW-{n:02d}" for n in range(1, 7)] + ["P13-SPECIAL-01", "P13-SPECIAL-02"]
MAPPING = dict(zip(PROPOSALS, [f"species_{n:04d}" for n in range(153, 161)]))


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def allocate(registry):
    """Fail closed on collisions; allow only an identical existing allocation."""
    existing = registry.get("authored_species", {})
    require(isinstance(existing, dict), "invalid authored namespace")
    require(all(key in MAPPING and MAPPING[key] == value for key, value in existing.items()),
            "conflicting authored allocation")
    allocated = []
    for key, domain in registry.items():
        if isinstance(domain, dict) and key != "authored_species":
            allocated.extend(value for value in domain.values() if isinstance(value, str))
    require(len(allocated) == len(set(allocated)), "duplicate registry allocation")
    require(not set(MAPPING.values()) & set(allocated), "new stable ID collision")
    result = copy.deepcopy(registry)
    result["authored_species"] = dict(MAPPING)
    return result


def build(registry=None, baseline=None, candidate=None):
    registry = read(OUT / "id_registry.json") if registry is None else registry
    baseline = read(OUT / "species.json") if baseline is None else baseline
    candidate = read(CANDIDATE) if candidate is None else candidate
    allocated = allocate(registry)
    require(len(baseline["records"]) == 152, "frozen baseline must contain 152 records")
    require(set(baseline["records"]) == set(registry["species"].values()), "frozen registry mismatch")
    require(set(candidate["records"]) == set(baseline["records"]) | set(PROPOSALS),
            "P13 candidate coverage changed")
    authored = {}
    for proposal, stable in MAPPING.items():
        item = candidate["records"][proposal]
        expected_class = "normal" if proposal.startswith("P13-NEW-") else "special"
        require(item["id"] == proposal and item["star"] == 5 and item["species_class"] == expected_class,
                "proposal identity/class/star mismatch")
        require(item["source_identity"] == {"namespace": "phimond_p13_authored_proposal",
                "proposal_id": proposal, "apk_jar_source": False}, "false authored provenance")
        design = copy.deepcopy(item)
        design["id"] = stable
        design["registry_status"] = "P10_stable_id_registered"
        authored[stable] = {
            "id": stable, "display_name": {"vi": item["name_vi"]},
            "description": {"vi": item["rationale"]},
            "description_status": "phimond_authored_design_candidate",
            "race_id": item["race_id"], "star": 5, "species_class": expected_class,
            "element_id": item["element_id"], "role_ids": item["role_ids"],
            "primary_role": item["primary_role"], "secondary_role": item["secondary_role"],
            "provenance": {"namespace": "phimond_authored", "proposal_id": proposal,
                "authoring_brief": str((P13 / "P13-to-P10-eight-species-prompt.md").relative_to(ROOT)),
                "source_recovered": False, "identity_registration": "owner_requested_2026-10-13"},
            "art": {"status": "candidate_pending_owner_review", "approved": False,
                "species_id": stable,
                "manifest_path": ".ai/plan/phases/P10-pet-model/extension-20261013/art-manifest.json",
                "runtime_activated": False},
            "design_candidate": {"status": "pending_P13_acceptance_not_P11_promotion",
                "catalog_version": candidate["catalog_version"], "record": design},
        }
    package = {"schema_version": 1, "status": "authoring_only_not_runtime",
               "namespace": "phimond_authored", "records": authored}
    effective = {"schema_version": 1, "status": "authoring_only_not_runtime",
        "effective_count": 160, "baseline_count": 152, "authored_count": 8,
        "layers": {"frozen_source": "data/p10/species.json", "authored": "data/p10/species_authored.json"},
        "baseline_sha256": sha(OUT / "species.json"),
        "p13_candidate_sha256": sha(CANDIDATE),
        "runtime_activated": False, "records": {**copy.deepcopy(baseline["records"]), **authored}}
    mapping = {"schema_version": 1, "status": "stable_ids_registered_art_pending_owner_review",
        "effective_count": 160, "proposal_to_stable": MAPPING,
        "names": {proposal: candidate["records"][proposal]["name_vi"] for proposal in PROPOSALS},
        "numeric_authority": "P13_candidate_only_not_P11_promotion",
        "runtime_activated": False,
        "p13_followup": "Remap owner/pool/signature/recipe candidate references; do not activate fusion.",
        "candidate_sha256": sha(CANDIDATE)}
    return allocated, package, effective, mapping


def snapshot():
    files = [OUT / name for name in ("species.json", "items.json", "special_recipes.json")]
    files += [ROOT / "data/pets/roster_apk84.json", SELECTION]
    files += sorted((ROOT / "apps/game-client/assets/pets/apk84").rglob("*"))
    files += [ROOT / item["candidate_path"] for item in read(SELECTION)["species"].values()]
    return {"schema_version": 1, "purpose": "preserve frozen source and approved atlas bytes",
            "files": {str(path.relative_to(ROOT)): sha(path) for path in files if path.is_file()},
            "frozen_registry_fields": {key: value for key, value in read(OUT / "id_registry.json").items()
                                       if key != "authored_species"}}


def verify_preservation(before):
    require(before == snapshot(), "frozen source/approved assets/registry changed")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    registry, authored, effective, mapping = build()
    EVIDENCE.mkdir(parents=True, exist_ok=True)
    preservation = EVIDENCE / "preservation-before.json"
    if args.write and not preservation.exists():
        preservation.write_text(encoded(snapshot()), encoding="utf-8")
    outputs = {OUT / "id_registry.json": registry,
               OUT / "species_authored.json": authored, OUT / "species_effective.json": effective,
               EVIDENCE / "mapping.json": mapping,
               P13 / "P13-to-P10-eight-species-mapping.json": mapping}
    for path, value in outputs.items():
        if args.write:
            path.write_text(encoded(value), encoding="utf-8")
        else:
            require(read(path) == value, f"stale extension output: {path}")
    require(preservation.is_file(), "preservation evidence missing")
    verify_preservation(read(preservation))
    print("PASS: 160 authoring records, 152 frozen preserved, 8 unique authored IDs; no runtime activation")


if __name__ == "__main__":
    main()
