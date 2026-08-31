#!/usr/bin/env python3
"""Network-independent validation for committed CARTA Atlas data and app assets."""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from collections import defaultdict
from pathlib import Path
from typing import Any, Iterable

try:
    import jsonschema
except ImportError as exc:  # pragma: no cover - dependency guard
    raise SystemExit("Install dev dependency: python -m pip install jsonschema") from exc


ROOT = Path(__file__).resolve().parents[1]
MANIFEST_DIR = ROOT / "data/geography/datasets"
MAPPING_DIR = ROOT / "data/geography/external-id-mappings"
PUBLIC_DATA_DIR = ROOT / "atlas-app/public/data"
EXPERIENCE_LINEAGE = [
    "data/atlas/run-05-jura-final-cut.json",
    "data/atlas/run-06-bearn-jurancon-world.json",
    "data/atlas/run-07-editorial-foundation.json",
    "data/atlas/run-08-beaujolais-canonical-ingestion.json",
    "data/atlas/run-09-beaujolais-world.json",
]

INAO_DATASET_ID = "spatial-dataset:inao-aires-geographiques-siqo-2026-08-24"
NATURAL_EARTH_DATASET_ID = "spatial-dataset:natural-earth-admin-0-countries-5.1.1"
OPENFREEMAP_DATASET_ID = "spatial-dataset:openfreemap-liberty-runtime"
TERRAIN_DATASET_ID = "spatial-dataset:copernicus-dem-glo30-2022-05-09"

# Raw environmental rasters are pinned by checksum in the ignored build cache and
# never committed, exactly like the raw vector archives beside them.
RAW_GIS_SUFFIXES = {".zip", ".7z", ".shp", ".dbf", ".shx", ".gpkg", ".tif", ".tiff"}


def fail(message: str) -> None:
    raise SystemExit(message)


def read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text())
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"{path.relative_to(ROOT)}: invalid or unreadable JSON: {exc}")


def read_jsonl(paths: Iterable[Path]) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for path in sorted(paths):
        for lineno, line in enumerate(path.read_text().splitlines(), 1):
            if not line.strip():
                continue
            try:
                records.append(json.loads(line))
            except json.JSONDecodeError as exc:
                fail(f"{path.relative_to(ROOT)}:{lineno}: invalid JSON: {exc}")
    return records


def nested_values(value: Any, key: str) -> Iterable[Any]:
    if isinstance(value, dict):
        for nested_key, nested_value in value.items():
            if nested_key == key:
                yield nested_value
            yield from nested_values(nested_value, key)
    elif isinstance(value, list):
        for item in value:
            yield from nested_values(item, key)


def sha256_path(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def schema_validator(path: str) -> jsonschema.Draft202012Validator:
    schema = read_json(ROOT / path)
    return jsonschema.Draft202012Validator(
        schema, format_checker=jsonschema.FormatChecker()
    )


def validate_record(
    validator: jsonschema.Draft202012Validator,
    record: dict[str, Any],
    label: str,
) -> None:
    errors = sorted(validator.iter_errors(record), key=lambda error: list(error.path))
    if errors:
        fail(f"{label}: {errors[0].message}")


def load_authority() -> dict[str, Any]:
    entities = read_jsonl((ROOT / "data/entities").glob("*.jsonl"))
    claims = read_jsonl((ROOT / "data/claims").glob("*.jsonl"))
    sources = read_jsonl((ROOT / "data/sources").glob("*.jsonl"))
    profiles = read_jsonl((ROOT / "data/reference-profiles").glob("*.jsonl"))
    relationships = read_jsonl((ROOT / "data/relationships").glob("*.jsonl"))
    spatial = read_jsonl((ROOT / "data/geography/assertions").glob("*.jsonl"))
    geometry = read_jsonl((ROOT / "data/geography/geometry").glob("*.jsonl"))
    entity_ids = {record["id"] for record in entities}
    source_ids = {record["id"] for record in sources}
    profile_paths: dict[str, list[str]] = defaultdict(list)
    for profile in profiles:
        if not profile.get("path"):
            continue
        for entity_id in profile["component_entity_ids"]:
            profile_paths[entity_id].append(profile["path"])
    return {
        "entity_ids": entity_ids,
        "source_ids": source_ids,
        "entities": {record["id"]: record for record in entities},
        "claims": {record["id"]: record for record in claims},
        "sources": {record["id"]: record for record in sources},
        "relationships": {record["id"]: record for record in relationships},
        "spatial": {record["id"]: record for record in spatial},
        "geometry": {record["id"]: record for record in geometry},
        "profile_paths": {
            entity_id: sorted(set(paths)) for entity_id, paths in profile_paths.items()
        },
    }


def validate_native_experience(authority: dict[str, Any]) -> dict[str, Any]:
    value = read_json(PUBLIC_DATA_DIR / "atlas-subjects.json")
    expected_inputs = [
        *EXPERIENCE_LINEAGE,
        "data/claims/*.jsonl",
        "data/entities/*.jsonl",
        "data/geography/assertions/*.jsonl",
        "data/geography/geometry/*.jsonl",
        "data/reference-profiles/*.jsonl",
        "data/relationships/*.jsonl",
        "data/sources/*.jsonl",
    ]
    if value.get("generated_from") != expected_inputs:
        fail("atlas-subjects.json: governed projection inputs are stale")
    subjects = value.get("subjects")
    if not isinstance(subjects, dict) or not subjects:
        fail("atlas-subjects.json: expected native subject mapping")
    required = {
        "place:jura",
        "appellation:arbois",
        "appellation:cotes-du-jura",
        "appellation:chateau-chalon",
        "appellation:l-etoile",
        "appellation:cremant-du-jura",
        "appellation:macvin-du-jura",
        "grape:savagnin",
        "grape:petit-manseng",
        "grape:palomino-fino",
        "producer:domaine-de-la-tournelle",
        "producer:domaine-labet",
        "producer:maison-pierre-overnoy",
        "producer:domaine-de-saint-pierre-jura",
        "project:soleras-del-pacifico",
        "person:emmanuel-houillon",
        "person:pierre-overnoy",
        "wine:flor-of-evangelho",
        "appellation:jurancon",
        "place:bearn",
        "appellation:bearn",
        "appellation:pacherenc-du-vic-bilh",
        "appellation:irouleguy",
        "grape:gros-manseng",
        "grape:petit-courbu",
        "grape:courbu",
        "grape:raffiat-de-moncade",
        "producer:camin-larredya",
        "producer:domaine-cauhape",
        "producer:clos-uroulat",
        "producer:domaine-de-souch",
        "appellation:beaujolais",
        "classification:beaujolais-villages-mention",
        "appellation:brouilly",
        "appellation:chenas",
        "appellation:chiroubles",
        "appellation:cote-de-brouilly",
        "appellation:fleurie",
        "appellation:julienas",
        "appellation:morgon",
        "appellation:moulin-a-vent",
        "appellation:regnie",
        "appellation:saint-amour",
        "grape:gamay-noir-a-jus-blanc",
        "producer:domaine-marcel-lapierre",
        "producer:jean-foillard",
        "producer:chateau-thivin",
        "producer:domaine-de-la-grand-cour",
        "producer:domaine-des-terres-dorees",
        "person:jules-chauvet",
        "practice:carbonic-maceration",
        "practice:semi-carbonic-maceration",
        "practice:whole-cluster-fermentation",
        "ecosystem:gang-of-four-beaujolais",
        "geographic_feature:mont-brouilly",
        "geographic_feature:py-hill",
        "vineyard:cote-du-py",
        "place:charnay-rhone",
        "historical_event:gamay-ordinance-1395",
        "classification:beaujolais-primeur-nouveau",
    }
    if not required.issubset(subjects):
        fail("atlas-subjects.json: missing required native subjects")

    for entity_id, subject in subjects.items():
        entity = authority["entities"].get(entity_id)
        if not entity:
            fail(f"atlas-subjects.json:{entity_id}: missing CARTA entity")
        if subject.get("entity_id") != entity_id:
            fail(f"atlas-subjects.json:{entity_id}: identity drifted")
        if subject.get("name") != entity["name"] or subject.get("kind") != entity["type"]:
            fail(f"atlas-subjects.json:{entity_id}: entity projection drifted")
        expected_route = f"#/{entity['type']}/{entity_id.split(':', 1)[1]}"
        if subject.get("route") != expected_route:
            fail(f"atlas-subjects.json:{entity_id}: unstable native route")
        projected_source_ids: set[str] = set()
        for projected in subject.get("claims", []):
            claim_id = projected.get("claim_id")
            claim = authority["claims"].get(claim_id)
            if not claim or claim["status"] not in {"supported", "contested"}:
                fail(f"atlas-subjects.json:{entity_id}: invalid claim {claim_id}")
            if projected.get("statement") != claim["statement"]:
                fail(f"atlas-subjects.json:{claim_id}: statement drifted")
            if projected.get("subject_ref") != claim["subject_ref"]:
                fail(f"atlas-subjects.json:{claim_id}: subject drifted")
            source_ids = [item["source_id"] for item in claim["source_refs"]]
            if projected.get("source_ids") != source_ids:
                fail(f"atlas-subjects.json:{claim_id}: source lineage drifted")
            projected_source_ids.update(source_ids)
        for connection in subject.get("connections", []):
            target_id = connection.get("target_id")
            if target_id not in subjects:
                fail(f"atlas-subjects.json:{entity_id}: non-native connection {target_id}")
            relationship_id = connection.get("relationship_id")
            if relationship_id:
                relationship = authority["relationships"].get(relationship_id)
                if not relationship:
                    fail(f"atlas-subjects.json:{entity_id}: missing relationship {relationship_id}")
                if connection.get("predicate") != relationship["predicate"]:
                    fail(f"atlas-subjects.json:{relationship_id}: predicate drifted")
                if connection.get("claim_ids") != relationship.get("claim_ids", []):
                    fail(f"atlas-subjects.json:{relationship_id}: claim lineage drifted")
        location = subject.get("location")
        if location:
            spatial_id = location.get("spatial_assertion_id")
            spatial = authority["spatial"].get(spatial_id)
            if not spatial or spatial["entity_id"] != entity_id:
                fail(f"atlas-subjects.json:{entity_id}: invalid spatial projection")
            if location.get("description") != spatial["description"]:
                fail(f"atlas-subjects.json:{spatial_id}: description drifted")
            if location.get("source_ids") != spatial["source_ids"]:
                fail(f"atlas-subjects.json:{spatial_id}: source lineage drifted")
            projected_source_ids.update(spatial["source_ids"])
        actual_source_ids = {item["source_id"] for item in subject.get("sources", [])}
        if actual_source_ids != projected_source_ids:
            fail(f"atlas-subjects.json:{entity_id}: source projection incomplete")

    entries = read_json(PUBLIC_DATA_DIR / "atlas-entry-points.json")
    if entries.get("generated_from") != EXPERIENCE_LINEAGE:
        fail("atlas-entry-points.json: experience config lineage is stale")
    if entries.get("release") != "atlas-run-09-beaujolais-world":
        fail("atlas-entry-points.json: release marker is stale")
    if len(entries.get("entry_points", [])) != 5:
        fail("atlas-entry-points.json: Beaujolais needs five focused learner questions")
    entry_ids: set[str] = set()
    for entry in entries["entry_points"]:
        if entry["id"] in entry_ids:
            fail(f"atlas-entry-points.json: duplicate entry {entry['id']}")
        entry_ids.add(entry["id"])
        if entry["subject_id"] not in subjects:
            fail(f"atlas-entry-points.json:{entry['id']}: subject is not native")
        for projected in entry["supporting_claims"]:
            claim = authority["claims"].get(projected["claim_id"])
            if not claim or claim["status"] != "supported":
                fail(f"atlas-entry-points.json:{entry['id']}: invalid supporting claim")
            if projected["statement"] != claim["statement"]:
                fail(f"atlas-entry-points.json:{projected['claim_id']}: statement drifted")
    featured_ids = {item["entity_id"] for item in entries.get("featured_worlds", [])}
    if featured_ids != {
        "place:jura",
        "place:burgundy",
        "place:loire-valley",
        "place:beaujolais",
        "place:bearn",
    }:
        fail("atlas-entry-points.json: five France worlds are not discoverable")
    return {
        "subjects": subjects,
        "subject_count": len(subjects),
        "entry_count": len(entries["entry_points"]),
    }


def validate_editorial_experience(
    authority: dict[str, Any], subjects: dict[str, Any]
) -> int:
    value = read_json(PUBLIC_DATA_DIR / "atlas-editorial.json")
    if value.get("generated_from") != EXPERIENCE_LINEAGE:
        fail("atlas-editorial.json: experience config lineage is stale")
    if value.get("release") != "atlas-run-09-beaujolais-world":
        fail("atlas-editorial.json: release marker is stale")
    legend = value.get("legend", [])
    if {item.get("id") for item in legend} != {
        "iykyk",
        "same-energy",
    } or len(legend) != 2:
        fail("atlas-editorial.json: visible signal key is not restrained")
    glossary = value.get("glossary", {})
    if set(glossary) != {
        "elevage",
        "flor",
        "foehn",
        "marl",
        "mistelle",
        "ouille",
        "passerillage",
        "sec",
        "sous-voile",
        "tries-successives",
        "vendanges-tardives",
        "voile",
        "carbonic-maceration",
        "semi-carbonic",
        "whole-cluster",
        "nouveau",
    }:
        fail("atlas-editorial.json: learner glossary is incomplete")
    for term_id, term in glossary.items():
        if not term.get("definition") or not term.get("matters"):
            fail(f"atlas-editorial.json:{term_id}: definition is incomplete")
        target_id = term.get("explore_target_id")
        if target_id and target_id not in subjects:
            fail(f"atlas-editorial.json:{term_id}: dead glossary route")

    configured_subjects = value.get("subjects", {})
    if not isinstance(configured_subjects, dict) or not configured_subjects:
        fail("atlas-editorial.json: expected subject-specific editorial grammars")
    if not set(configured_subjects).issubset(subjects):
        fail("atlas-editorial.json: editorial subject is not native")
    jura = configured_subjects.get("place:jura", {})
    if jura.get("accent") or any(nested_values(configured_subjects, "surprises")):
        fail("atlas-editorial.json: removed tells or Surprise me data remains")
    if len(jura.get("hero_facts", [])) != 2:
        fail("atlas-editorial.json: Jura opening needs two high-value facts")
    if len(jura.get("people", [])) != 4:
        fail("atlas-editorial.json: Jura People pillar must feature four producers")
    if set(jura.get("pillar_map_reactions", {})) != {
        "place", "grapes", "people", "culture", "rules"
    }:
        fail("atlas-editorial.json: Jura pillar map reactions are incomplete")
    if len(jura.get("featured_connections", [])) != 3:
        fail("atlas-editorial.json: Jura Keep wandering set must contain three routes")
    bearn = configured_subjects.get("place:bearn", {})
    beaujolais = configured_subjects.get("place:beaujolais", {})
    if not all(world.get("regional_world") for world in (jura, bearn, beaujolais)):
        fail("atlas-editorial.json: Jura, Béarn and Beaujolais must share the regional-world contract")
    if len(bearn.get("hero_facts", [])) != 2:
        fail("atlas-editorial.json: Béarn opening needs two high-value facts")
    if len(bearn.get("grape_cards", [])) != 5:
        fail("atlas-editorial.json: Béarn grape grammar must distinguish five cards")
    if len(bearn.get("style_comparison", [])) != 3:
        fail("atlas-editorial.json: Béarn dry/sweet comparison is incomplete")
    if len(bearn.get("people", [])) != 4:
        fail("atlas-editorial.json: Béarn People pillar must feature four producers")
    if set(bearn.get("pillar_map_reactions", {})) != {
        "place", "grapes", "people", "culture", "rules"
    }:
        fail("atlas-editorial.json: Béarn pillar map reactions are incomplete")
    if any(
        signal == "tell"
        for signal in nested_values(bearn, "signal")
    ):
        fail("atlas-editorial.json: Béarn invents a sensory Tell")
    if len(beaujolais.get("hero_facts", [])) != 3:
        fail("atlas-editorial.json: Beaujolais opening needs three bounded facts")
    if len(beaujolais.get("grape_cards", [])) != 2:
        fail("atlas-editorial.json: Beaujolais grape grammar needs Gamay and Chardonnay")
    if len(beaujolais.get("people", [])) != 5:
        fail("atlas-editorial.json: Beaujolais People pillar must feature five distinct producers")
    if len(beaujolais.get("map_moments", [])) != 4:
        fail("atlas-editorial.json: Beaujolais needs four bounded terrain moments")
    if set(beaujolais.get("pillar_map_reactions", {})) != {
        "place", "grapes", "people", "culture", "rules"
    }:
        fail("atlas-editorial.json: Beaujolais pillar map reactions are incomplete")
    if any(signal == "tell" for signal in nested_values(beaujolais, "signal")):
        fail("atlas-editorial.json: Beaujolais invents a sensory Tell")
    if not beaujolais.get("then_now"):
        fail("atlas-editorial.json: Beaujolais must use Then / Now meaningfully")
    # No world may borrow another world's voice: each regional world carries its
    # own pillar copy, Place story and rule grammar, or it does not ship.
    for subject_id, editorial in configured_subjects.items():
        if not editorial.get("regional_world"):
            continue
        pillar_copy = editorial.get("pillar_copy", {})
        if set(pillar_copy) != {"place", "grapes", "people", "culture", "rules"}:
            fail(f"atlas-editorial.json:{subject_id}: world is missing pillar copy")
        for pillar, pillar_text in pillar_copy.items():
            if not pillar_text.get("intro") or not pillar_text.get("lede"):
                fail(f"atlas-editorial.json:{subject_id}: {pillar} copy is incomplete")
        place_story = editorial.get("place_story", {})
        if not all(place_story.get(key) for key in ("kicker", "title", "text", "button")):
            fail(f"atlas-editorial.json:{subject_id}: world has no Place story")
        rules = editorial.get("rules", {})
        if not rules.get("intro") or not rules.get("groups"):
            fail(f"atlas-editorial.json:{subject_id}: world has no rule grammar")
        for group in rules["groups"]:
            for area_id in group.get("ids", []):
                if area_id not in subjects:
                    fail(f"atlas-editorial.json:{subject_id}: dead rule-group area {area_id}")

    priority = value.get("map_click_priority", {})
    if priority.get("appellation:jurancon", 999) >= priority.get("appellation:bearn", 999):
        fail("atlas-editorial.json: Jurançon must outrank overlapping Béarn on click")
    crus = {
        "appellation:brouilly", "appellation:cote-de-brouilly", "appellation:chenas",
        "appellation:chiroubles", "appellation:fleurie", "appellation:julienas",
        "appellation:morgon", "appellation:moulin-a-vent", "appellation:regnie",
        "appellation:saint-amour",
    }
    if not all(
        priority.get(cru, 999) < priority.get("classification:beaujolais-villages-mention", 999)
        < priority.get("appellation:beaujolais", 999)
        for cru in crus
    ):
        fail("atlas-editorial.json: cru > Villages mention > Beaujolais click priority drifted")
    for context_return in value.get("context_returns", []):
        if context_return.get("return_subject_id") not in subjects:
            fail("atlas-editorial.json: dead reciprocal context return")
    savagnin = configured_subjects.get("grape:savagnin", {})
    if len(savagnin.get("style_paths", [])) < 3 or not savagnin.get("affinities"):
        fail("atlas-editorial.json: Savagnin grammar lacks style paths or affinities")
    chardonnay = configured_subjects.get("grape:chardonnay", {})
    if "Different cultural machine" not in chardonnay.get("thesis", ""):
        fail("atlas-editorial.json: Chardonnay cultural contrast is missing")

    projected_claim_ids: set[str] = set()
    for claim_list in nested_values(value, "claim_ids"):
        if isinstance(claim_list, list):
            projected_claim_ids.update(claim_list)
    support = value.get("claim_support", {})
    if set(support) != projected_claim_ids:
        fail("atlas-editorial.json: claim support projection is incomplete or stale")
    for claim_id, projected in support.items():
        claim = authority["claims"].get(claim_id)
        if not claim or claim["status"] not in {"supported", "contested"}:
            fail(f"atlas-editorial.json: invalid claim {claim_id}")
        if projected.get("statement") != claim["statement"]:
            fail(f"atlas-editorial.json:{claim_id}: statement drifted")
        source_ids = [item["source_id"] for item in claim["source_refs"]]
        if projected.get("source_ids") != source_ids:
            fail(f"atlas-editorial.json:{claim_id}: source lineage drifted")
        if [item.get("source_id") for item in projected.get("sources", [])] != source_ids:
            fail(f"atlas-editorial.json:{claim_id}: source metadata drifted")

    for subject_id, editorial in configured_subjects.items():
        direct_targets = {
            connection["target_id"] for connection in subjects[subject_id]["connections"]
        }
        featured = editorial.get("featured_connections", [])
        if len(featured) > 3:
            fail(f"atlas-editorial.json:{subject_id}: too many featured routes")
        for connection in featured:
            target_id = connection.get("target_id")
            if target_id not in subjects:
                fail(f"atlas-editorial.json:{subject_id}: dead featured route")
            if not connection.get("reason") or not connection.get("claim_ids"):
                fail(f"atlas-editorial.json:{subject_id}: unexplained featured route")
            if target_id not in direct_targets and connection.get("signal") != "same-energy":
                fail(f"atlas-editorial.json:{subject_id}: route is not graph-derived")
        for target_id in nested_values(editorial, "target_id"):
            if target_id not in subjects:
                fail(f"atlas-editorial.json:{subject_id}: dead learner route {target_id}")
        reactions = [editorial.get("map_reaction", {})]
        reactions.extend(editorial.get("pillar_map_reactions", {}).values())
        for reaction in reactions:
            for area_id in reaction.get("area_subject_ids", []):
                if not subjects[area_id].get("map_target"):
                    fail(f"atlas-editorial.json:{subject_id}: unmappable active area")
            for producer_id in reaction.get("producer_ids", []):
                if not subjects[producer_id].get("map_target"):
                    fail(f"atlas-editorial.json:{subject_id}: unmappable active producer")
        map_view = editorial.get("map_view")
        if map_view:
            if bool(map_view.get("bounds")) == bool(map_view.get("center")):
                fail(f"atlas-editorial.json:{subject_id}: malformed map view")
            for area_id in map_view.get("area_subject_ids", []):
                if area_id not in subjects or not subjects[area_id].get("map_target"):
                    fail(f"atlas-editorial.json:{subject_id}: unmappable map-view area")
            for producer_id in map_view.get("producer_ids", []):
                if producer_id not in subjects or not subjects[producer_id].get("map_target"):
                    fail(f"atlas-editorial.json:{subject_id}: unmappable map-view producer")
        for moment in editorial.get("map_moments", []):
            target_id = moment.get("subject_id")
            target_editorial = configured_subjects.get(target_id, {})
            if target_id not in subjects or not (
                subjects[target_id].get("map_target") or target_editorial.get("map_view")
            ):
                fail(f"atlas-editorial.json:{subject_id}: dead terrain moment")
    return len(configured_subjects)


def validate_atlas_guides(authority: dict[str, Any]) -> int:
    value = read_json(PUBLIC_DATA_DIR / "atlas-guides.json")
    expected_inputs = [
        "data/claims/*.jsonl",
        "data/entities/*.jsonl",
        "data/reference-profiles/*.jsonl",
        "data/sources/*.jsonl",
    ]
    if value.get("generated_from") != expected_inputs:
        fail("atlas-guides.json: governed projection inputs are stale")
    guides = value.get("guides")
    if not isinstance(guides, dict) or not guides:
        fail("atlas-guides.json: expected non-empty guide mapping")
    required = {
        "place:jura",
        "place:burgundy",
        "place:loire-valley",
        "place:beaujolais",
        "place:bearn",
    }
    if not required.issubset(guides):
        fail("atlas-guides.json: missing one or more required France worlds")

    for entity_id, guide in guides.items():
        if entity_id not in authority["entity_ids"]:
            fail(f"atlas-guides.json:{entity_id}: missing CARTA entity")
        projected_claims = guide.get("sections", []) + guide.get("quantities", [])
        if not projected_claims:
            fail(f"atlas-guides.json:{entity_id}: guide has no governed claims")
        expected_source_ids: set[str] = set()
        for projected in projected_claims:
            claim_id = projected.get("claim_id")
            claim = authority["claims"].get(claim_id)
            if not claim or not claim.get("atlas_presentation"):
                fail(f"atlas-guides.json:{entity_id}: invalid projected claim {claim_id}")
            if projected.get("statement") != claim["statement"]:
                fail(f"atlas-guides.json:{claim_id}: statement drifted from authority")
            if projected.get("subject_ref") != claim["subject_ref"]:
                fail(f"atlas-guides.json:{claim_id}: subject drifted from authority")
            if projected.get("subject_name") != authority["entities"][claim["subject_ref"]]["name"]:
                fail(f"atlas-guides.json:{claim_id}: subject name drifted from authority")
            if projected.get("observed_at") != claim.get("observed_at"):
                fail(f"atlas-guides.json:{claim_id}: observation date drifted")
            source_ids = [item["source_id"] for item in claim["source_refs"]]
            if projected.get("source_ids") != source_ids:
                fail(f"atlas-guides.json:{claim_id}: source projection drifted")
            expected_source_ids.update(source_ids)
            if claim.get("quantity"):
                quantity = dict(projected.get("quantity", {}))
                quantity.pop("dimension_name", None)
                if quantity != claim["quantity"]:
                    fail(f"atlas-guides.json:{claim_id}: quantity drifted from authority")
            elif "quantity" in projected:
                fail(f"atlas-guides.json:{claim_id}: invented quantity")
        actual_source_ids = {item.get("source_id") for item in guide.get("sources", [])}
        if actual_source_ids != expected_source_ids:
            fail(f"atlas-guides.json:{entity_id}: source list is incomplete or stale")
        for source in guide.get("sources", []):
            authority_source = authority["sources"][source["source_id"]]
            if source.get("url") != authority_source.get("url"):
                fail(f"atlas-guides.json:{source['source_id']}: source URL drifted")
    return len(guides)


def load_and_validate_manifests(authority: dict[str, Any]) -> dict[str, dict[str, Any]]:
    validator = schema_validator("schemas/spatial-dataset.schema.json")
    manifests = [read_json(path) for path in sorted(MANIFEST_DIR.glob("*.json"))]
    by_id: dict[str, dict[str, Any]] = {}
    for manifest in manifests:
        validate_record(validator, manifest, manifest.get("id", "manifest"))
        manifest_id = manifest["id"]
        if manifest_id in by_id:
            fail(f"duplicate manifest ID: {manifest_id}")
        if manifest["source_id"] not in authority["source_ids"]:
            fail(f"{manifest_id}: missing CARTA source {manifest['source_id']}")
        orders = [item["order"] for item in manifest["transformations"]]
        if orders != list(range(1, len(orders) + 1)):
            fail(f"{manifest_id}: transformation order must be contiguous from 1")
        by_id[manifest_id] = manifest
    required = {
        INAO_DATASET_ID,
        NATURAL_EARTH_DATASET_ID,
        OPENFREEMAP_DATASET_ID,
        TERRAIN_DATASET_ID,
    }
    if not required.issubset(by_id):
        fail("missing required active Atlas manifest(s): " + ", ".join(sorted(required - by_id.keys())))
    return by_id


def validate_artifact_lineage(manifests: dict[str, dict[str, Any]]) -> int:
    """Every declared `derived_from` reference must resolve to something real.

    A derived environmental product that cannot name its parents is exactly the
    opaque generated file the terrain contract forbids.
    """
    resolved = 0
    for manifest in manifests.values():
        artifact_paths = {artifact["path"] for artifact in manifest["derived_artifacts"]}
        for dataset_id in manifest.get("derived_from", []):
            if dataset_id not in manifests:
                fail(f"{manifest['id']}: derived_from references unknown dataset {dataset_id}")
            resolved += 1
        for artifact in manifest["derived_artifacts"]:
            lineage = artifact.get("derived_from")
            if artifact.get("product_class") and not lineage:
                fail(f"{artifact['path']}: derived artifact declares a tier without lineage")
            for reference in lineage or []:
                if reference in manifests:
                    resolved += 1
                    continue
                if reference in artifact_paths and reference != artifact["path"]:
                    resolved += 1
                    continue
                fail(f"{artifact['path']}: derived_from does not resolve: {reference}")
    return resolved


def validate_artifacts(manifests: dict[str, dict[str, Any]]) -> None:
    seen_paths: set[str] = set()
    for manifest in manifests.values():
        for artifact in manifest["derived_artifacts"]:
            relative = artifact["path"]
            if relative in seen_paths:
                fail(f"derived artifact appears in multiple manifests: {relative}")
            seen_paths.add(relative)
            path = ROOT / relative
            if not path.is_file():
                fail(f"{manifest['id']}: missing derived artifact {relative}")
            if path.stat().st_size != artifact["bytes"]:
                fail(f"{relative}: byte count does not match manifest")
            if sha256_path(path) != artifact["sha256"]:
                fail(f"{relative}: checksum does not match manifest")
            if "feature_count" in artifact:
                document = read_json(path)
                if not isinstance(document, dict) or document.get("type") != "FeatureCollection":
                    fail(f"{relative}: expected GeoJSON FeatureCollection")
                if len(document.get("features", [])) != artifact["feature_count"]:
                    fail(f"{relative}: feature count does not match manifest")
            if "record_count" in artifact:
                if path.suffix == ".jsonl":
                    count = len(read_jsonl([path]))
                else:
                    value = read_json(path)
                    count = len(value) if isinstance(value, list) else -1
                if count != artifact["record_count"]:
                    fail(f"{relative}: record count does not match manifest")


def load_and_validate_mappings(
    manifests: dict[str, dict[str, Any]], authority: dict[str, Any]
) -> list[dict[str, Any]]:
    validator = schema_validator("schemas/external-id-mapping.schema.json")
    mappings = read_jsonl(MAPPING_DIR.glob("*.jsonl"))
    keys: set[tuple[str, str]] = set()
    entity_source_keys: set[tuple[str, str]] = set()
    for mapping in mappings:
        label = f"{mapping.get('source_dataset_id')}:{mapping.get('source_identifier')}"
        validate_record(validator, mapping, label)
        if mapping["source_dataset_id"] not in manifests:
            fail(f"{label}: missing spatial dataset manifest")
        if mapping["carta_entity_id"] not in authority["entity_ids"]:
            fail(f"{label}: missing CARTA entity {mapping['carta_entity_id']}")
        key = (mapping["source_dataset_id"], mapping["source_identifier"])
        if key in keys:
            fail(f"duplicate accepted source mapping: {key}")
        keys.add(key)
        entity_source_key = (mapping["source_dataset_id"], mapping["carta_entity_id"])
        if entity_source_key in entity_source_keys:
            fail(f"duplicate accepted source-to-CARTA identity: {entity_source_key}")
        entity_source_keys.add(entity_source_key)
    return mappings


def coordinate_pairs(coordinates: Any) -> Iterable[tuple[float, float]]:
    if (
        isinstance(coordinates, list)
        and len(coordinates) >= 2
        and isinstance(coordinates[0], (int, float))
        and isinstance(coordinates[1], (int, float))
    ):
        yield float(coordinates[0]), float(coordinates[1])
        return
    if isinstance(coordinates, list):
        for item in coordinates:
            yield from coordinate_pairs(item)


def validate_coordinates(feature: dict[str, Any], label: str) -> None:
    geometry = feature.get("geometry")
    if not isinstance(geometry, dict):
        fail(f"{label}: missing geometry")
    pairs = list(coordinate_pairs(geometry.get("coordinates")))
    if not pairs:
        fail(f"{label}: geometry has no coordinate pairs")
    for longitude, latitude in pairs:
        if not -180 <= longitude <= 180 or not -90 <= latitude <= 90:
            fail(f"{label}: coordinate out of WGS84 range")


def validate_geojson(
    path: Path,
    allowed_geometry_types: set[str],
    required_properties: set[str],
) -> dict[str, Any]:
    document = read_json(path)
    relative = path.relative_to(ROOT).as_posix()
    if not isinstance(document, dict) or document.get("type") != "FeatureCollection":
        fail(f"{relative}: expected GeoJSON FeatureCollection")
    features = document.get("features")
    if not isinstance(features, list):
        fail(f"{relative}: features must be an array")
    ids: set[str] = set()
    for feature in features:
        feature_id = feature.get("id")
        label = f"{relative}:{feature_id}"
        if not isinstance(feature_id, str) or not feature_id:
            fail(f"{relative}: feature missing stable ID")
        if feature_id in ids:
            fail(f"{relative}: duplicate feature ID {feature_id}")
        ids.add(feature_id)
        geometry_type = (feature.get("geometry") or {}).get("type")
        if geometry_type not in allowed_geometry_types:
            fail(f"{label}: unsupported geometry type {geometry_type}")
        validate_coordinates(feature, label)
        properties = feature.get("properties")
        if not isinstance(properties, dict):
            fail(f"{label}: missing properties")
        missing = sorted(required_properties - properties.keys())
        if missing:
            fail(f"{label}: missing required properties: {', '.join(missing)}")
        if properties.get("source_feature_id") != feature_id:
            fail(f"{label}: source_feature_id must equal feature ID")
    return document


def validate_profile_link(
    properties: dict[str, Any], authority: dict[str, Any], label: str
) -> None:
    carta_entity_id = properties.get("carta_entity_id")
    path = properties.get("human_reference_path")
    if not carta_entity_id:
        if path:
            fail(f"{label}: external-only feature cannot have a Human Reference path")
        return
    if carta_entity_id not in authority["entity_ids"]:
        fail(f"{label}: missing CARTA entity {carta_entity_id}")
    allowed_paths = authority["profile_paths"].get(carta_entity_id, [])
    if path:
        if path not in allowed_paths:
            fail(f"{label}: Human Reference path is not governed for {carta_entity_id}")
        if not (ROOT / path).is_file():
            fail(f"{label}: Human Reference path does not exist: {path}")
    elif allowed_paths:
        fail(f"{label}: governed Human Reference path was omitted")


def validate_terrain(
    manifests: dict[str, dict[str, Any]], authority: dict[str, Any]
) -> dict[str, Any]:
    """Prove the terrain foundation without trusting the build script's word for it."""
    manifest = manifests[TERRAIN_DATASET_ID]

    if manifest.get("product_class") != "source_observation":
        fail("terrain: the elevation model must be registered as a source observation")
    if manifest["retrieval_status"] != "acquired":
        fail("terrain: the elevation model must be an acquired dataset")
    for field in ("measurement", "geographic_extent", "source_files", "refresh_policy"):
        if not manifest.get(field):
            fail(f"terrain: manifest is missing required environmental field {field}")
    measurement = manifest["measurement"]
    for field in ("variable", "unit", "native_resolution", "scale_limitations"):
        if not measurement.get(field):
            fail(f"terrain: measurement.{field} is required for an environmental dataset")
    if not measurement.get("vertical_reference"):
        fail("terrain: an elevation dataset must state its vertical reference system")
    if not measurement.get("uncertainty"):
        fail("terrain: an elevation dataset must state its published uncertainty")
    if not manifest["transformations"]:
        fail("terrain: derived assets exist with no recorded processing recipe")

    descriptor = read_json(PUBLIC_DATA_DIR / "atlas-terrain.json")
    if descriptor.get("source_dataset_id") != TERRAIN_DATASET_ID:
        fail("atlas-terrain.json: descriptor is not bound to the registered elevation dataset")
    if descriptor.get("product_class") != "derived_spatial_product":
        fail("atlas-terrain.json: descriptor must declare its tier")
    if descriptor.get("attribution") != manifest["license"]["attribution_text"]:
        fail("atlas-terrain.json: required licence attribution is missing or stale")
    if descriptor.get("recipe") != manifest["transformations"]:
        fail("atlas-terrain.json: published recipe and manifest transformations disagree")
    terrains = descriptor.get("terrains", [])
    if {terrain.get("id") for terrain in terrains} != {"bearn-jurancon", "beaujolais"}:
        fail("atlas-terrain.json: bounded terrain extent set is incomplete")
    if len(manifest["source_files"]) != 8:
        fail("terrain: source file set must contain six Pyrenean and two Beaujolais tiles")

    descriptor_path = "atlas-app/public/data/atlas-terrain.json"
    terrain_asset_paths = {
        f"atlas-app/public/{terrain[kind]['path'].removeprefix('./')}"
        for terrain in terrains
        for kind in ("hillshade", "contours")
    }
    artifacts = {artifact["path"]: artifact for artifact in manifest["derived_artifacts"]}
    expected = terrain_asset_paths | {descriptor_path}
    if set(artifacts) != expected:
        fail("terrain: derived artifact set does not match both bounded terrain extents")
    for path, artifact in artifacts.items():
        if artifact.get("product_class") != "derived_spatial_product":
            fail(f"{path}: terrain assets must be registered as derived spatial products")
        if TERRAIN_DATASET_ID not in artifact.get("derived_from", []):
            fail(f"{path}: terrain asset does not resolve back to its source observation")

    clips = {
        step["parameters"].get("extent_id"): step["parameters"]["clip_bbox_epsg4326"]
        for step in manifest["transformations"]
        if "clip_bbox_epsg4326" in step["parameters"]
    }
    contour_count = 0
    for terrain in terrains:
        terrain_id = terrain["id"]
        clip = clips.get(terrain_id)
        if clip != terrain["proof_extent"]["bbox_epsg4326"]:
            fail(f"atlas-terrain.json:{terrain_id}: proof extent and clip disagree")

        hillshade = terrain["hillshade"]
        hillshade_artifact_path = f"atlas-app/public/{hillshade['path'].removeprefix('./')}"
        hillshade_artifact = artifacts[hillshade_artifact_path]
        header = (ROOT / hillshade_artifact_path).read_bytes()[:24]
        if header[:8] != b"\x89PNG\r\n\x1a\n" or header[12:16] != b"IHDR":
            fail(f"terrain:{terrain_id}: shaded-relief asset is not a PNG")
        width = int.from_bytes(header[16:20], "big")
        height = int.from_bytes(header[20:24], "big")
        if (width, height) != (
            hillshade_artifact.get("pixel_width"),
            hillshade_artifact.get("pixel_height"),
        ) or (hillshade["pixel_width"], hillshade["pixel_height"]) != (width, height):
            fail(f"terrain:{terrain_id}: shaded-relief dimensions drifted")
        west, south, east, north = hillshade["image_bbox_epsg4326"]
        if hillshade["image_coordinates"] != [
            [west, north], [east, north], [east, south], [west, south]
        ]:
            fail(f"terrain:{terrain_id}: image placement corners drifted")
        if not (west <= clip[0] and south <= clip[1] and east >= clip[2] and north >= clip[3]):
            fail(f"terrain:{terrain_id}: rendered image does not cover its proof extent")

        contour_path = PUBLIC_DATA_DIR / Path(terrain["contours"]["path"]).name
        contours = validate_geojson(
            contour_path,
            {"LineString"},
            {
                "source_feature_id", "elevation_metres", "contour_class",
                "feature_type", "representation_type", "representation_label",
                "source_dataset_id",
            },
        )
        interval = terrain["contours"]["interval_metres"]
        index_interval = terrain["contours"]["index_interval_metres"]
        if terrain["contours"]["feature_count"] != len(contours["features"]):
            fail(f"atlas-terrain.json:{terrain_id}: contour count drifted")
        contour_count += len(contours["features"])
        for feature in contours["features"]:
            properties = feature["properties"]
            label = feature["id"]
            elevation = properties["elevation_metres"]
            if not isinstance(elevation, int) or elevation % interval:
                fail(f"{label}: contour elevation is not on the declared interval")
            expected_class = "index" if elevation % index_interval == 0 else "intermediate"
            if properties["contour_class"] != expected_class:
                fail(f"{label}: contour class disagrees with the index interval")
            if properties["source_dataset_id"] != TERRAIN_DATASET_ID:
                fail(f"{label}: contour is not attributed to the registered elevation dataset")
            if properties["feature_type"] != "elevation_contour":
                fail(f"{label}: contour meaning drifted")
            if properties.get("carta_entity_id") or properties.get("human_reference_path"):
                fail(f"{label}: terrain features must not claim a CARTA identity")

    for record in authority["geometry"].values():
        if TERRAIN_DATASET_ID in record.get("source_ids", []):
            fail("terrain: elevation data must not be used as CARTA geometry authority")

    config = read_json(ROOT / "atlas-app/src/atlas-config.json")
    zoom = config["semanticZoom"]
    thresholds = [
        zoom["terrainMin"],
        zoom["terrainFull"],
        zoom["terrainFadeOut"],
        zoom["terrainMax"],
    ]
    if thresholds != sorted(thresholds):
        fail("atlas config: terrain zoom thresholds are not ordered")
    if not (
        zoom["terrainMin"] < zoom["contourIndexMin"] < zoom["contourIntermediateMin"]
        < zoom["contourMax"]
    ):
        fail("atlas config: contour zoom thresholds are not ordered under terrain")
    if zoom["terrainMax"] > zoom["contourMax"]:
        fail("atlas config: relief must not outlive the contours it belongs to")
    if config["defaultLayers"].get("terrain") is not True:
        fail("atlas config: relief is expected on by default inside its extent")

    return {
        "terrain_artifacts": len(artifacts),
        "terrain_contours": contour_count,
        "terrain_extents": len(terrains),
        "terrain_source_files": len(manifest["source_files"]),
        "terrain_bytes": sum(artifact["bytes"] for artifact in artifacts.values()),
    }


def validate_atlas() -> dict[str, Any]:
    authority = load_authority()
    manifests = load_and_validate_manifests(authority)
    validate_artifacts(manifests)
    lineage_references = validate_artifact_lineage(manifests)
    terrain = validate_terrain(manifests, authority)
    mappings = load_and_validate_mappings(manifests, authority)
    atlas_guide_count = validate_atlas_guides(authority)
    native_experience = validate_native_experience(authority)
    editorial_subject_count = validate_editorial_experience(
        authority, native_experience["subjects"]
    )

    world = validate_geojson(
        PUBLIC_DATA_DIR / "world-countries.geojson",
        {"Polygon", "MultiPolygon"},
        {
            "source_feature_id",
            "source_ne_id",
            "name",
            "representation_type",
            "source_dataset_id",
            "governance_status",
            "carta_entity_id",
            "human_reference_path",
        },
    )
    aoc = validate_geojson(
        PUBLIC_DATA_DIR / "france-appellations-aoc.geojson",
        {"Polygon", "MultiPolygon"},
        {
            "source_feature_id",
            "source_appellation_id",
            "source_denomination_id",
            "name",
            "designation",
            "feature_type",
            "representation_type",
            "representation_label",
            "source_dataset_id",
            "source_release_date",
            "geometry_status",
            "carta_entity_id",
            "human_reference_path",
            "governance_status",
        },
    )
    igp = validate_geojson(
        PUBLIC_DATA_DIR / "france-appellations-igp.geojson",
        {"Polygon", "MultiPolygon"},
        {
            "source_feature_id",
            "source_appellation_id",
            "source_denomination_id",
            "name",
            "designation",
            "feature_type",
            "representation_type",
            "representation_label",
            "source_dataset_id",
            "source_release_date",
            "geometry_status",
            "carta_entity_id",
            "human_reference_path",
            "governance_status",
        },
    )
    regions = validate_geojson(
        PUBLIC_DATA_DIR / "france-wine-regions.geojson",
        {"Point"},
        {
            "source_feature_id",
            "name",
            "feature_type",
            "representation_type",
            "representation_label",
            "derivation",
            "child_carta_entity_ids",
            "bounds",
            "carta_entity_id",
            "human_reference_path",
            "governance_status",
        },
    )
    producers = validate_geojson(
        PUBLIC_DATA_DIR / "atlas-producers.geojson",
        {"Point"},
        {
            "source_feature_id",
            "carta_entity_id",
            "name",
            "feature_type",
            "place_label",
            "precision",
            "placement_note",
            "representation_label",
            "spatial_assertion_id",
            "geometry_id",
            "source_ids",
            "native_route",
        },
    )

    all_wine_features = aoc["features"] + igp["features"]
    source_ids: dict[str, list[dict[str, Any]]] = defaultdict(list)
    source_feature_ids: dict[str, dict[str, Any]] = {}
    for feature in all_wine_features:
        properties = feature["properties"]
        label = feature["id"]
        if properties["designation"] not in {"AOC", "IGP"}:
            fail(f"{label}: unexpected designation")
        if properties["representation_type"] != "regulatory_geographical_area":
            fail(f"{label}: wine geometry has incorrect representation type")
        if properties["representation_label"] != "INAO cartographic representation of regulatory geographical area":
            fail(f"{label}: wine geometry has incorrect human representation label")
        validate_profile_link(properties, authority, label)
        source_ids[properties["source_denomination_id"]].append(feature)
        source_feature_ids[feature["id"]] = feature

    for feature in world["features"]:
        validate_profile_link(feature["properties"], authority, feature["id"])

    for feature in regions["features"]:
        properties = feature["properties"]
        label = feature["id"]
        if properties["derivation"] != "representative_point_of_union_of_mapped_child_inao_geometries":
            fail(f"{label}: wine-region anchor is not documented as derived")
        children = properties["child_carta_entity_ids"]
        if not children or any(child not in authority["entity_ids"] for child in children):
            fail(f"{label}: invalid governed child set for derived label")
        validate_profile_link(properties, authority, label)

    for feature in producers["features"]:
        properties = feature["properties"]
        entity_id = properties["carta_entity_id"]
        entity = authority["entities"].get(entity_id)
        if not entity or entity["type"] != "producer":
            fail(f"{feature['id']}: producer point has invalid CARTA identity")
        spatial = authority["spatial"].get(properties["spatial_assertion_id"])
        geometry = authority["geometry"].get(properties["geometry_id"])
        if not spatial or spatial["entity_id"] != entity_id:
            fail(f"{feature['id']}: producer point spatial lineage is invalid")
        if not geometry or geometry["entity_id"] != entity_id:
            fail(f"{feature['id']}: producer point geometry lineage is invalid")
        if geometry["geometry_type"] != "Point":
            fail(f"{feature['id']}: producer geometry is not a point")
        if properties["feature_type"] != "producer_base":
            fail(f"{feature['id']}: producer point meaning drifted")
        if "not vineyard" not in properties["representation_label"].casefold():
            fail(f"{feature['id']}: producer point does not disclose its meaning")

    inao_mappings = [
        mapping for mapping in mappings if mapping["source_dataset_id"] == INAO_DATASET_ID
    ]
    for mapping in inao_mappings:
        matches = source_ids.get(mapping["source_identifier"], [])
        if len(matches) != 1:
            fail(
                f"INAO {mapping['source_identifier']}: accepted mapping resolves to {len(matches)} features"
            )
        properties = matches[0]["properties"]
        if properties["carta_entity_id"] != mapping["carta_entity_id"]:
            fail(f"INAO {mapping['source_identifier']}: GeoJSON CARTA ID mismatch")

    mapped_features = [
        feature for feature in all_wine_features if feature["properties"]["carta_entity_id"]
    ]
    unmapped_features = len(all_wine_features) - len(mapped_features)

    search = read_json(PUBLIC_DATA_DIR / "search-index.json")
    if not isinstance(search, list):
        fail("search-index.json: expected array")
    search_ids = [record.get("id") for record in search]
    if len(search_ids) != len(set(search_ids)):
        fail("search-index.json: duplicate result ID")
    expected_geographic_search_ids = {
        f"inao-denom-{denom_id}" for denom_id in source_ids
    } | {feature["id"] for feature in regions["features"]}
    geographic_entities = {
        record.get("carta_entity_id")
        for record in search
        if record.get("id") in expected_geographic_search_ids
    }
    expected_native_search_ids = {
        f"carta-subject-{entity_id.replace(':', '-')}"
        for entity_id in native_experience["subjects"]
        if entity_id not in geographic_entities
    }
    if set(search_ids) != expected_geographic_search_ids | expected_native_search_ids:
        fail("search-index.json: results do not match geography plus native subjects")
    for record in search:
        bounds = record.get("bounds")
        if record.get("result_type") == "native_subject" and bounds is None:
            if record.get("carta_entity_id") not in native_experience["subjects"]:
                fail(f"search-index.json:{record.get('id')}: subject is not native")
            if not record.get("native_route"):
                fail(f"search-index.json:{record.get('id')}: native route missing")
            continue
        if (
            not isinstance(bounds, list)
            or len(bounds) != 4
            or not all(isinstance(value, (int, float)) for value in bounds)
            or not (-180 <= bounds[0] <= bounds[2] <= 180)
            or not (-90 <= bounds[1] <= bounds[3] <= 90)
        ):
            fail(f"search-index.json:{record.get('id')}: invalid WGS84 bounds")

    geometry_records = read_jsonl(
        (ROOT / "data/geography/geometry").glob("*.jsonl")
    )
    atlas_geometry = [
        record for record in geometry_records if record["id"].startswith("geom:inao-denom-")
    ]
    if len(atlas_geometry) != len(inao_mappings):
        fail("INAO geometry metadata count does not match accepted mappings")
    for record in atlas_geometry:
        marker = "#source_feature_id="
        if marker not in record["geometry_ref"]:
            fail(f"{record['id']}: geometry_ref lacks source feature selector")
        relative, feature_id = record["geometry_ref"].split(marker, 1)
        if relative != "atlas-app/public/data/france-appellations-aoc.geojson":
            fail(f"{record['id']}: unexpected geometry artifact")
        feature = source_feature_ids.get(feature_id)
        if not feature:
            fail(f"{record['id']}: referenced GeoJSON feature does not exist")
        if feature["properties"]["carta_entity_id"] != record["entity_id"]:
            fail(f"{record['id']}: geometry entity and feature CARTA ID disagree")
        if feature["geometry"]["type"] != record["geometry_type"]:
            fail(f"{record['id']}: geometry type and feature disagree")

    provenance = read_json(PUBLIC_DATA_DIR / "provenance.json")
    provenance_ids = {record["id"] for record in provenance.get("datasets", [])}
    if provenance_ids != set(manifests):
        fail("provenance.json: active dataset set is stale")
    if provenance.get("generated_from") != "data/geography/datasets/":
        fail("provenance.json: provenance must be generated from dataset manifests")

    config = read_json(ROOT / "atlas-app/src/atlas-config.json")
    basemap = config.get("basemap", {})
    if basemap.get("datasetId") != OPENFREEMAP_DATASET_ID:
        fail("atlas config: basemap is not linked to the OpenFreeMap manifest")
    if basemap.get("styleUrl") != manifests[OPENFREEMAP_DATASET_ID]["resource_url"]:
        fail("atlas config: basemap style URL and manifest disagree")
    if basemap.get("attribution") != manifests[OPENFREEMAP_DATASET_ID]["license"]["attribution_text"]:
        fail("atlas config: required runtime attribution is missing or stale")
    if config.get("defaultLayers") != {
        "aocAreas": True,
        "igpAreas": False,
        "wineRegions": True,
        "terrain": True,
    }:
        fail("atlas config: expected AOC-default, IGP-off, relief-on layer policy")
    for label, relative in config.get("data", {}).items():
        if not relative.startswith("./data/"):
            fail(f"atlas config:{label}: data path must resolve inside public/data")
        path = ROOT / "atlas-app/public" / relative.removeprefix("./")
        if not path.is_file():
            fail(f"atlas config:{label}: missing asset {relative}")

    tracked = subprocess.run(
        ["git", "ls-files"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.splitlines()
    raw_tracked = sorted(
        path for path in tracked if Path(path).suffix.casefold() in RAW_GIS_SUFFIXES
    )
    if raw_tracked:
        fail("raw GIS archive/source files are tracked: " + ", ".join(raw_tracked))

    return {
        "manifests": len(manifests),
        "country_features": len(world["features"]),
        "aoc_features": len(aoc["features"]),
        "igp_features": len(igp["features"]),
        "wine_region_labels": len(regions["features"]),
        "inao_relevant_features": len(all_wine_features),
        "inao_mapped_features": len(mapped_features),
        "inao_unmapped_features": unmapped_features,
        "inao_ambiguous_features": 0,
        "external_mappings": len(mappings),
        "geometry_records": len(atlas_geometry),
        "search_records": len(search),
        "atlas_guides": atlas_guide_count,
        "native_subjects": native_experience["subject_count"],
        "editorial_subjects": editorial_subject_count,
        "entry_points": native_experience["entry_count"],
        "producer_points": len(producers["features"]),
        "artifact_lineage_references": lineage_references,
        **terrain,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    summary = validate_atlas()
    if args.json:
        print(json.dumps(summary, sort_keys=True))
    else:
        print("PASS " + ", ".join(f"{key}={value}" for key, value in summary.items()))


if __name__ == "__main__":
    main()
