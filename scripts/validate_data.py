#!/usr/bin/env python3
"""Validate CARTA authority and its deterministic Human Reference projection."""
from __future__ import annotations

import argparse
import json
import posixpath
import re
from collections import defaultdict, deque
from pathlib import Path, PurePosixPath
from typing import Any
from urllib.parse import unquote, urlsplit

try:
    import jsonschema
except ImportError:
    raise SystemExit("Install dev dependency: python -m pip install jsonschema")


ROOT = Path(__file__).resolve().parents[1]

SETS = {
    "entities": ("data/entities", "schemas/entity.schema.json"),
    "relationships": ("data/relationships", "schemas/relationship.schema.json"),
    "claims": ("data/claims", "schemas/claim.schema.json"),
    "sources": ("data/sources", "schemas/source.schema.json"),
    "names": ("data/names", "schemas/name-assertion.schema.json"),
    "geometry": ("data/geography/geometry", "schemas/geometry.schema.json"),
    "spatial": ("data/geography/assertions", "schemas/spatial-assertion.schema.json"),
    "profiles": ("data/reference-profiles", "schemas/reference-profile.schema.json"),
}

PROVENANCE_BEGIN = "<!-- BEGIN GENERATED CARTA PROVENANCE -->"
PROVENANCE_END = "<!-- END GENERATED CARTA PROVENANCE -->"
NAVIGATION_BEGIN = "<!-- BEGIN GENERATED CARTA NAVIGATION -->"
NAVIGATION_END = "<!-- END GENERATED CARTA NAVIGATION -->"
INDEX_BEGIN = "<!-- BEGIN GENERATED CARTA INDEX -->"
INDEX_END = "<!-- END GENERATED CARTA INDEX -->"
INDEX_DIRECTORY_BEGIN = "<!-- BEGIN GENERATED CARTA INDEX DIRECTORY -->"
INDEX_DIRECTORY_END = "<!-- END GENERATED CARTA INDEX DIRECTORY -->"

INDEX_PATHS = {
    "grapes": "atlas/indexes/grapes.md",
    "producers": "atlas/indexes/producers-and-people.md",
    "wines": "atlas/indexes/wines.md",
    "places": "atlas/indexes/places-and-law.md",
}

PROFILE_DIRECTORIES = {
    "producer": "atlas/producers",
    "person": "atlas/people",
    "grape": "atlas/grapes",
    "wine": "atlas/wines",
    "landscape": "atlas/landscapes",
    "ecosystem": "atlas/ecosystems",
    "institution": "atlas/institutions",
    "practice": "atlas/practices",
    "classification": "atlas/classifications",
    "historical_event": "atlas/historical-events",
}

ALLOWED_UNGOVERNED_ATLAS_PAGES = {
    "atlas/README.md",
    "atlas/indexes/grapes.md",
    "atlas/indexes/places-and-law.md",
    "atlas/indexes/producers-and-people.md",
    "atlas/indexes/wines.md",
    "atlas/landscapes/README.md",
}

MARKDOWN_LINK_RE = re.compile(r"(?<!!)\[[^\]]*\]\(([^)]+)\)")
PERISHABLE_LANGUAGE_RE = re.compile(
    r"\b(?:current(?:ly)?|recent(?:ly)?|continues?|continuing|now)\b", re.IGNORECASE
)

DEPRECATED_ENTITY_FIELDS = {"claim_ids", "name_assertion_ids", "spatial_refs"}
DEPRECATED_RELATIONSHIP_PREDICATES = {
    "LEGAL_AT_TIME",
    "OWNED_AT_TIME",
    "LOCATED_WITHIN_AT_TIME",
    "STYLISTIC_NEIGHBOR_OF",
    "STRUCTURAL_ANALOGUE_OF",
    "CLIMATE_ANALOGUE_OF",
    "SITE_ANALOGUE_OF",
}
SPATIAL_APPELLATION_SUBJECT_TYPES = {
    "vineyard",
    "place",
    "appellation",
    "geographic_feature",
    "geology",
}

LINKABLE_PUBLICATION_STATUSES = {"published", "stub", "queued"}
NAVIGATION_RELATIONSHIP_STATUSES = {"supported", "provisional"}
NAVIGATION_RELATIONSHIP_PREDICATES = {
    "MENTORED_BY",
    "TRAINED_AT",
    "WORKED_FOR",
    "WORKED_WITH",
    "COLLABORATED_WITH",
    "FOUNDED",
    "MEMBER_OF",
    "OWNED_BY",
    "MADE_BY",
    "FARMED_BY",
    "MADE_FROM",
    "USES_PRACTICE",
    "PLANTED_AT",
    "LOCATED_IN",
    "FARMS_IN",
    "FARMS_PARCEL",
    "WITHIN_APPELLATION",
    "WITHIN",
    "CLASSIFIED_AS",
}
MAX_GRAPH_NAVIGATION_DISTANCE = 2
MAX_RELATED_PROFILES = 16

PROFESSIONAL_NAVIGATION_PREDICATES = {
    "MENTORED_BY",
    "TRAINED_AT",
    "WORKED_FOR",
    "WORKED_WITH",
    "COLLABORATED_WITH",
    "FOUNDED",
}
PRODUCER_SPECIFIC_TWO_HOP_PREDICATES = (
    PROFESSIONAL_NAVIGATION_PREDICATES
    | {
        "FARMS_PARCEL",
        "FARMED_BY",
        "USES_PRACTICE",
    }
)
GEOGRAPHIC_CONTAINMENT_PREDICATES = {
    "WITHIN",
    "LOCATED_IN",
    "WITHIN_APPELLATION",
}

# Every schema profile kind has an explicit two-hop disposition. The named
# policies below are projection semantics, not ontology or relationship scores.
TWO_HOP_POLICY_BY_SOURCE_KIND = {
    "country": "country_orientation",
    "region": "directional_geography",
    "appellation": "directional_geography",
    "landscape": "directional_geography",
    "grape": "grape_context",
    "producer": "producer_world",
    "person": "producer_world",
    "classification": "governed_context",
    "ecosystem": "governed_context",
    "wine": "governed_context",
    "institution": "governed_context",
    "practice": "governed_context",
    "historical_event": "governed_context",
}


def load_jsonl(directory: Path) -> list[dict]:
    records = []
    if not directory.exists():
        return records
    for path in sorted(directory.glob("*.jsonl")):
        for lineno, line in enumerate(path.read_text().splitlines(), 1):
            if not line.strip():
                continue
            try:
                records.append(json.loads(line))
            except json.JSONDecodeError as exc:
                raise SystemExit(f"{path}:{lineno}: invalid JSON: {exc}")
    return records


def load_and_validate_schema() -> tuple[dict[str, list[dict]], dict[str, set[str]]]:
    data = {}
    for label, (directory, schema_path) in SETS.items():
        records = load_jsonl(ROOT / directory)
        schema = json.loads((ROOT / schema_path).read_text())
        validator = jsonschema.Draft202012Validator(
            schema, format_checker=jsonschema.FormatChecker()
        )
        for record in records:
            errors = sorted(validator.iter_errors(record), key=lambda e: list(e.path))
            if errors:
                raise SystemExit(f"{label} {record.get('id')}: {errors[0].message}")
        data[label] = records

    ids = {}
    for label, records in data.items():
        bucket = set()
        for record in records:
            rid = record["id"]
            if rid in bucket:
                raise SystemExit(f"duplicate {label} id: {rid}")
            bucket.add(rid)
        ids[label] = bucket
    return data, ids


def validate_references(data: dict[str, list[dict]], ids: dict[str, set[str]]) -> None:
    for relationship in data["relationships"]:
        if (
            relationship["subject_id"] not in ids["entities"]
            or relationship["object_id"] not in ids["entities"]
        ):
            raise SystemExit(f"{relationship['id']}: missing relationship endpoint")
        for claim_id in relationship.get("claim_ids", []):
            if claim_id not in ids["claims"]:
                raise SystemExit(f"{relationship['id']}: missing claim {claim_id}")

    all_subject_ids = (
        ids["entities"]
        | ids["relationships"]
        | ids["claims"]
        | ids["names"]
        | ids["spatial"]
    )
    for claim in data["claims"]:
        if claim["subject_ref"] not in all_subject_ids:
            raise SystemExit(f"{claim['id']}: missing subject {claim['subject_ref']}")
        for source_ref in claim["source_refs"]:
            if source_ref["source_id"] not in ids["sources"]:
                raise SystemExit(
                    f"{claim['id']}: missing source {source_ref['source_id']}"
                )

    for name in data["names"]:
        if name["entity_id"] not in ids["entities"]:
            raise SystemExit(f"{name['id']}: missing entity")
        if name.get("jurisdiction_ref") and name["jurisdiction_ref"] not in ids["entities"]:
            raise SystemExit(f"{name['id']}: missing jurisdiction")
        for claim_id in name["claim_ids"]:
            if claim_id not in ids["claims"]:
                raise SystemExit(f"{name['id']}: missing claim {claim_id}")

    for geometry in data["geometry"]:
        if geometry["entity_id"] not in ids["entities"]:
            raise SystemExit(f"{geometry['id']}: missing entity")
        for source_id in geometry["source_ids"]:
            if source_id not in ids["sources"]:
                raise SystemExit(f"{geometry['id']}: missing source {source_id}")

    for spatial in data["spatial"]:
        if spatial["entity_id"] not in ids["entities"]:
            raise SystemExit(f"{spatial['id']}: missing entity")
        for entity_id in spatial.get("anchor_entity_refs", []):
            if entity_id not in ids["entities"]:
                raise SystemExit(f"{spatial['id']}: missing anchor {entity_id}")
        for source_id in spatial["source_ids"]:
            if source_id not in ids["sources"]:
                raise SystemExit(f"{spatial['id']}: missing source {source_id}")
        for geometry_id in spatial.get("geometry_ids", []):
            if geometry_id not in ids["geometry"]:
                raise SystemExit(f"{spatial['id']}: missing geometry {geometry_id}")
        for claim_id in spatial.get("claim_ids", []):
            if claim_id not in ids["claims"]:
                raise SystemExit(f"{spatial['id']}: missing claim {claim_id}")


def validate_temporal_interval(record: dict) -> None:
    valid_from = record.get("valid_from")
    valid_to = record.get("valid_to")
    if (valid_from or valid_to) and not record.get("time_precision"):
        raise SystemExit(f"{record['id']}: validity interval requires time_precision")
    if valid_from and valid_to and valid_from > valid_to:
        raise SystemExit(f"{record['id']}: valid_from is after valid_to")


def validate_authored_contracts(
    data: dict[str, list[dict]], ids: dict[str, set[str]]
) -> None:
    """Enforce v0.2 maintenance rules kept schema-compatible for deprecation."""
    entity_by_id = {entity["id"]: entity for entity in data["entities"]}
    claim_by_id = {claim["id"]: claim for claim in data["claims"]}

    for entity in data["entities"]:
        reverse_fields = sorted(DEPRECATED_ENTITY_FIELDS & entity.keys())
        if reverse_fields:
            raise SystemExit(
                f"{entity['id']}: deprecated authored reverse field(s): "
                + ", ".join(reverse_fields)
            )
        if entity["type"] == "market_signal":
            raise SystemExit(
                f"{entity['id']}: market_signal is deprecated; attach a dated claim "
                "to a stable subject"
            )

    for relationship in data["relationships"]:
        validate_temporal_interval(relationship)
        predicate = relationship["predicate"]
        if predicate in DEPRECATED_RELATIONSHIP_PREDICATES:
            raise SystemExit(
                f"{relationship['id']}: deprecated authored predicate: {predicate}"
            )

        subject_type = entity_by_id[relationship["subject_id"]]["type"]
        object_type = entity_by_id[relationship["object_id"]]["type"]
        if predicate == "WITHIN_APPELLATION" and (
            object_type != "appellation"
            or subject_type not in SPATIAL_APPELLATION_SUBJECT_TYPES
        ):
            raise SystemExit(
                f"{relationship['id']}: WITHIN_APPELLATION requires a spatial "
                "subject and appellation object"
            )
        if predicate == "CLASSIFIED_AS":
            if object_type not in {"appellation", "classification"}:
                raise SystemExit(
                    f"{relationship['id']}: CLASSIFIED_AS requires an appellation "
                    "or classification object"
                )
            if object_type == "appellation" and subject_type != "wine":
                raise SystemExit(
                    f"{relationship['id']}: appellation designation requires a wine subject"
                )
        if predicate in {"IMPORTED_BY", "DISTRIBUTED_BY"}:
            if object_type != "institution" or not relationship.get("claim_ids"):
                raise SystemExit(
                    f"{relationship['id']}: {predicate} requires an institution object "
                    "and claim evidence"
                )
            for claim_id in relationship["claim_ids"]:
                if claim_by_id[claim_id]["subject_ref"] != relationship["id"]:
                    raise SystemExit(
                        f"{relationship['id']}: access claim must address the relationship"
                    )
        if predicate == "CELLAR_IN" and (
            subject_type not in {"producer", "project", "institution"}
            or object_type != "place"
        ):
            raise SystemExit(
                f"{relationship['id']}: CELLAR_IN requires a producer/project/institution "
                "subject and place object"
            )

    for spatial in data["spatial"]:
        if spatial["representation_kind"] == "network_anchor":
            raise SystemExit(
                f"{spatial['id']}: network_anchor is deprecated presentation metadata"
            )

    for claim in data["claims"]:
        validate_temporal_interval(claim)
        observed_at = claim.get("observed_at")
        quantity = claim.get("quantity")
        if quantity:
            if not observed_at:
                raise SystemExit(f"{claim['id']}: quantitative claim requires observed_at")
            if claim["status"] != "supported":
                raise SystemExit(
                    f"{claim['id']}: learner-facing quantitative claim must be supported"
                )
            if quantity["unit"] == "percent":
                if not 0 <= quantity["value"] <= 100:
                    raise SystemExit(
                        f"{claim['id']}: percentage must be between 0 and 100"
                    )
                if not quantity.get("denominator"):
                    raise SystemExit(
                        f"{claim['id']}: percentage requires an explicit denominator"
                    )
            elif quantity.get("denominator"):
                raise SystemExit(
                    f"{claim['id']}: denominator is reserved for percentage claims"
                )
            if quantity["value"] < 0:
                raise SystemExit(f"{claim['id']}: quantity cannot be negative")
            expected_units = {
                "vineyard_area": "ha",
                "area_in_production": "ha",
                "claimed_vineyard_area": "ha",
                "member_vineyard_area": "ha",
                "grape_share": "percent",
                "wine_color_share": "percent",
                "production_tier_share": "percent",
                "appellation_count": "count",
                "commune_count": "count",
                "geographic_length": "km",
            }
            expected_unit = expected_units[quantity["measure"]]
            if quantity["unit"] != expected_unit:
                raise SystemExit(
                    f"{claim['id']}: {quantity['measure']} requires unit {expected_unit}"
                )
            dimension_ref = quantity.get("dimension_ref")
            if dimension_ref and dimension_ref not in ids["entities"]:
                raise SystemExit(
                    f"{claim['id']}: missing quantity dimension {dimension_ref}"
                )
            if quantity["measure"] == "grape_share" and not dimension_ref:
                raise SystemExit(
                    f"{claim['id']}: grape_share requires dimension_ref"
                )
            if quantity["measure"] in {"wine_color_share", "production_tier_share"} and not quantity.get("dimension_label"):
                raise SystemExit(
                    f"{claim['id']}: {quantity['measure']} requires dimension_label"
                )
        if claim["layer"] == "frontier" and not observed_at:
            raise SystemExit(f"{claim['id']}: Frontier claim requires observed_at")
        if claim["claim_type"] in {"market", "availability", "price"} and not observed_at:
            raise SystemExit(
                f"{claim['id']}: {claim['claim_type']} claim requires observed_at"
            )
        if claim["claim_type"] in {"availability", "price"}:
            if claim["layer"] != "frontier":
                raise SystemExit(
                    f"{claim['id']}: {claim['claim_type']} observation must be Frontier"
                )
            if claim["subject_ref"] not in ids["entities"]:
                raise SystemExit(
                    f"{claim['id']}: {claim['claim_type']} must attach to a stable entity"
                )
        if PERISHABLE_LANGUAGE_RE.search(claim["statement"]) and not observed_at:
            raise SystemExit(
                f"{claim['id']}: perishable temporal language requires observed_at"
            )

    quantitative_keys: dict[tuple, str] = {}
    for claim in data["claims"]:
        quantity = claim.get("quantity")
        if not quantity or claim["status"] != "supported":
            continue
        key = (
            claim["subject_ref"],
            quantity["measure"],
            quantity.get("dimension_ref"),
            quantity.get("dimension_label"),
            claim.get("observed_at"),
            quantity["scope"],
        )
        previous = quantitative_keys.get(key)
        if previous:
            raise SystemExit(
                f"{claim['id']}: contradictory duplicate quantitative key also used by {previous}"
            )
        quantitative_keys[key] = claim["id"]


def validate_profile_path(profile: dict) -> None:
    raw_path = profile["path"]
    path = PurePosixPath(raw_path)
    if (
        path.is_absolute()
        or ".." in path.parts
        or path.as_posix() != raw_path
        or path.suffix != ".md"
        or not path.parts
        or path.parts[0] != "atlas"
    ):
        raise SystemExit(f"{profile['id']}: invalid canonical Atlas path: {raw_path}")

    kind = profile["profile_kind"]
    if kind == "country":
        valid = (
            len(path.parts) == 4
            and path.parts[:2] == ("atlas", "countries")
            and path.name == "README.md"
        )
    elif kind in {"region", "appellation"}:
        folder = "regions" if kind == "region" else "appellations"
        valid = (
            len(path.parts) == 5
            and path.parts[:2] == ("atlas", "countries")
            and path.parts[3] == folder
            and path.name != "README.md"
        )
    else:
        expected_directory = PROFILE_DIRECTORIES[kind]
        valid = path.parent.as_posix() == expected_directory and path.name != "README.md"
    if not valid:
        raise SystemExit(
            f"{profile['id']}: path does not match {kind} profile convention: {raw_path}"
        )


def validate_profiles(
    data: dict[str, list[dict]], ids: dict[str, set[str]]
) -> None:
    paths: dict[str, str] = {}
    primary_entities: dict[str, str] = {}
    entity_by_id = {entity["id"]: entity for entity in data["entities"]}
    profiled_entities: set[str] = set()
    primary_profile_kinds: dict[str, set[str]] = defaultdict(set)

    for profile in data["profiles"]:
        for entity_id in profile["component_entity_ids"]:
            if entity_id not in ids["entities"]:
                raise SystemExit(f"{profile['id']}: missing component entity {entity_id}")
            profiled_entities.add(entity_id)
        primary = profile.get("primary_entity_id")
        if primary and primary not in ids["entities"]:
            raise SystemExit(f"{profile['id']}: missing primary entity {primary}")
        if primary and primary not in profile["component_entity_ids"]:
            raise SystemExit(f"{profile['id']}: primary entity is not a component: {primary}")
        for entity_id in profile.get("country_entity_ids", []):
            if entity_id not in ids["entities"]:
                raise SystemExit(f"{profile['id']}: missing country entity {entity_id}")
            country = entity_by_id[entity_id]
            if country["type"] != "place" or country.get("place_kind") != "country":
                raise SystemExit(
                    f"{profile['id']}: country_entity_ids contains non-country {entity_id}"
                )
        for entity_id in profile.get("representative_anchor_ids", []):
            if entity_id not in ids["entities"]:
                raise SystemExit(
                    f"{profile['id']}: missing representative anchor {entity_id}"
                )
        if profile["publication_status"] == "published" and profile["maturity"] == "node":
            raise SystemExit(
                f"{profile['id']}: node maturity cannot be published as a finished reference"
            )
        if profile["publication_status"] == "machine_only":
            if profile["maturity"] != "node":
                raise SystemExit(
                    f"{profile['id']}: machine_only disposition requires node maturity"
                )
            if "path" in profile:
                raise SystemExit(
                    f"{profile['id']}: machine_only disposition cannot claim an Atlas path"
                )

        if primary:
            primary_profile_kinds[primary].add(profile["profile_kind"])
            primary_entity = entity_by_id[primary]
            primary_type = primary_entity["type"]
            kind = profile["profile_kind"]
            semantic_match = {
                "producer": primary_type in {"producer", "project"},
                "grape": primary_type == "grape",
                "country": primary_type == "place"
                and primary_entity.get("place_kind") == "country",
                "region": primary_type == "place"
                and primary_entity.get("place_kind") != "country",
                "appellation": primary_type == "appellation",
                "landscape": primary_type in {"place", "geographic_feature", "geology"},
                "ecosystem": primary_type == "ecosystem",
                "wine": primary_type == "wine",
                "person": primary_type == "person",
                "institution": primary_type == "institution",
                "practice": primary_type == "practice",
                "classification": primary_type == "classification",
                "historical_event": primary_type == "historical_event",
            }[kind]
            if not semantic_match:
                raise SystemExit(
                    f"{profile['id']}: {kind} profile has incompatible primary entity {primary}"
                )

        path = profile.get("path")
        if path:
            validate_profile_path(profile)
            if path in paths:
                raise SystemExit(
                    f"duplicate canonical profile path: {path} ({paths[path]}, {profile['id']})"
                )
            paths[path] = profile["id"]
        if primary:
            if primary in primary_entities:
                raise SystemExit(
                    "duplicate canonical profile primary entity: "
                    f"{primary} ({primary_entities[primary]}, {profile['id']})"
                )
            primary_entities[primary] = profile["id"]
        if (
            path
            and not (ROOT / path).is_file()
            and profile["publication_status"] != "stub"
        ):
            raise SystemExit(f"{profile['id']}: reference path does not exist: {path}")

    for entity in data["entities"]:
        requires_disposition = (
            entity["layer"] == "reference"
            and entity["status"] == "active"
            and (
                entity["type"] in {"producer", "grape"}
                or (
                    entity["type"] == "place"
                    and entity.get("place_kind") == "country"
                )
            )
        )
        if requires_disposition and entity["id"] not in profiled_entities:
            raise SystemExit(
                f"{entity['id']}: active {entity['type']} lacks an explicit "
                "Human Reference disposition"
            )
        expected_primary_kind = (
            "producer"
            if entity["type"] == "producer"
            else "grape"
            if entity["type"] == "grape"
            else "country"
            if entity["type"] == "place" and entity.get("place_kind") == "country"
            else None
        )
        if (
            requires_disposition
            and expected_primary_kind
            and expected_primary_kind
            not in primary_profile_kinds.get(entity["id"], set())
        ):
            raise SystemExit(
                f"{entity['id']}: active {expected_primary_kind} requires its own "
                "explicit Human Reference disposition"
            )


def profile_claims(profile: dict, data: dict[str, list[dict]]) -> list[dict]:
    seed_entities = set(profile["component_entity_ids"])

    claim_ids = {
        claim["id"] for claim in data["claims"] if claim["subject_ref"] in seed_entities
    }
    for relationship in data["relationships"]:
        if (
            relationship["subject_id"] in seed_entities
            or relationship["object_id"] in seed_entities
        ):
            claim_ids.update(relationship.get("claim_ids", []))
    for name in data["names"]:
        if name["entity_id"] in seed_entities:
            claim_ids.update(name.get("claim_ids", []))
    for spatial in data["spatial"]:
        if spatial["entity_id"] in seed_entities:
            claim_ids.update(spatial.get("claim_ids", []))

    claim_by_id = {claim["id"]: claim for claim in data["claims"]}
    return [claim_by_id[claim_id] for claim_id in sorted(claim_ids)]


def profile_has_surface(profile: dict) -> bool:
    return bool(profile.get("path")) and (
        profile["publication_status"] in LINKABLE_PUBLICATION_STATUSES
    )


def profile_country_entities(profile: dict) -> set[str]:
    """Return structural geographic membership used only in the outbound direction."""
    return set(profile.get("country_entity_ids", []))


def profile_editorial_anchors(profile: dict) -> set[str]:
    """Return governed editorial anchors, which retain reciprocal discovery."""
    return set(profile.get("representative_anchor_ids", []))


def profile_navigation_seeds(profile: dict) -> set[str]:
    """Return all outbound projection seeds (kept for deferred-anchor display)."""
    return profile_country_entities(profile) | profile_editorial_anchors(profile)


def navigation_graph(data: dict[str, list[dict]]) -> dict[str, set[str]]:
    graph: dict[str, set[str]] = defaultdict(set)
    for relationship in data["relationships"]:
        if (
            relationship["layer"] != "reference"
            or relationship["status"] not in NAVIGATION_RELATIONSHIP_STATUSES
            or relationship["predicate"] not in NAVIGATION_RELATIONSHIP_PREDICATES
        ):
            continue
        subject = relationship["subject_id"]
        object_id = relationship["object_id"]
        graph[subject].add(object_id)
        graph[object_id].add(subject)
    return graph


def navigation_adjacency(
    data: dict[str, list[dict]],
) -> dict[str, list[tuple[str, dict[str, Any], str]]]:
    """Return deterministic relationship-record adjacency with traversal direction."""
    adjacency: dict[str, list[tuple[str, dict[str, Any], str]]] = defaultdict(list)
    for relationship in data["relationships"]:
        if (
            relationship["layer"] != "reference"
            or relationship["status"] not in NAVIGATION_RELATIONSHIP_STATUSES
            or relationship["predicate"] not in NAVIGATION_RELATIONSHIP_PREDICATES
        ):
            continue
        subject = relationship["subject_id"]
        object_id = relationship["object_id"]
        adjacency[subject].append((object_id, relationship, "forward"))
        adjacency[object_id].append((subject, relationship, "reverse"))
    for entity_id in adjacency:
        adjacency[entity_id].sort(
            key=lambda item: (item[0], item[1]["predicate"], item[1]["id"], item[2])
        )
    return adjacency


def navigation_path_edge_label(relationship: dict[str, Any], direction: str) -> str:
    arrow = ">" if direction == "forward" else "<"
    return f"{relationship['predicate']}{arrow}"


def enumerate_navigation_paths(
    starts: set[str],
    targets: set[str],
    adjacency: dict[str, list[tuple[str, dict[str, Any], str]]],
) -> list[dict[str, Any]]:
    """Enumerate explainable paths of length zero, one, or two."""
    paths: list[dict[str, Any]] = []
    for shared in sorted(starts & targets):
        paths.append(
            {
                "distance": 0,
                "entities": [shared],
                "relationship_ids": [],
                "predicates": [],
                "directions": [],
                "pattern": "SHARED_COMPONENT",
                "intermediary": None,
            }
        )

    seen: set[tuple[Any, ...]] = set()
    for start in sorted(starts):
        for neighbor, first, first_direction in adjacency.get(start, []):
            first_key = (start, first["id"], neighbor)
            if neighbor in targets and first_key not in seen:
                seen.add(first_key)
                paths.append(
                    {
                        "distance": 1,
                        "entities": [start, neighbor],
                        "relationship_ids": [first["id"]],
                        "predicates": [first["predicate"]],
                        "directions": [first_direction],
                        "pattern": navigation_path_edge_label(first, first_direction),
                        "intermediary": None,
                    }
                )

            # Starting from every component already makes paths through another source
            # component redundant. Backtracking over one relationship is not a path.
            if neighbor in starts or neighbor in targets:
                continue
            for end, second, second_direction in adjacency.get(neighbor, []):
                if end not in targets or second["id"] == first["id"]:
                    continue
                second_key = (start, first["id"], neighbor, second["id"], end)
                if second_key in seen:
                    continue
                seen.add(second_key)
                paths.append(
                    {
                        "distance": 2,
                        "entities": [start, neighbor, end],
                        "relationship_ids": [first["id"], second["id"]],
                        "predicates": [first["predicate"], second["predicate"]],
                        "directions": [first_direction, second_direction],
                        "validity_intervals": [
                            {
                                "valid_from": first.get("valid_from"),
                                "valid_to": first.get("valid_to"),
                            },
                            {
                                "valid_from": second.get("valid_from"),
                                "valid_to": second.get("valid_to"),
                            },
                        ],
                        "pattern": (
                            f"{navigation_path_edge_label(first, first_direction)}/"
                            f"{navigation_path_edge_label(second, second_direction)}"
                        ),
                        "intermediary": neighbor,
                    }
                )
    return sorted(
        paths,
        key=lambda path: (
            path["distance"],
            path["pattern"],
            path["entities"],
            path["relationship_ids"],
        ),
    )


def shortest_navigation_distance(
    graph: dict[str, set[str]], starts: set[str], targets: set[str]
) -> int | None:
    if starts & targets:
        return 0
    seen = set(starts)
    queue = deque((entity_id, 0) for entity_id in starts)
    while queue:
        current, distance = queue.popleft()
        if distance >= MAX_GRAPH_NAVIGATION_DISTANCE:
            continue
        for neighbor in graph.get(current, set()):
            if neighbor in seen:
                continue
            next_distance = distance + 1
            if neighbor in targets:
                return next_distance
            seen.add(neighbor)
            queue.append((neighbor, next_distance))
    return None


def _is_up_then_down_peer_geography(path: dict[str, Any]) -> bool:
    predicates = set(path["predicates"])
    return (
        path["distance"] == 2
        and bool(predicates)
        and predicates.issubset(GEOGRAPHIC_CONTAINMENT_PREDICATES)
        and path["directions"] == ["forward", "reverse"]
    )


def _is_temporally_disjoint_classification_bridge(path: dict[str, Any]) -> bool:
    if (
        path["distance"] != 2
        or path["predicates"] != ["CLASSIFIED_AS", "CLASSIFIED_AS"]
        or path["directions"] != ["reverse", "forward"]
    ):
        return False
    intervals = path.get("validity_intervals", [])
    if len(intervals) != 2:
        return False
    first, second = intervals
    first_start = first.get("valid_from")
    first_end = first.get("valid_to")
    second_start = second.get("valid_from")
    second_end = second.get("valid_to")
    return bool(
        (first_end and second_start and first_end < second_start)
        or (second_end and first_start and second_end < first_start)
    )


def two_hop_navigation_eligibility(
    source_kind: str,
    target_kind: str,
    paths: list[dict[str, Any]],
) -> tuple[bool, str, str]:
    """Apply the source-kind reader policy to a graph-only two-hop candidate.

    Returns ``(eligible, category, reason)`` so generation, tests, and audits use
    the same inspectable decision rather than duplicating the policy.
    """
    policy = TWO_HOP_POLICY_BY_SOURCE_KIND[source_kind]
    two_hop_paths = [path for path in paths if path["distance"] == 2]

    if (
        source_kind in {"appellation", "classification"}
        and target_kind in {"appellation", "classification"}
        and two_hop_paths
        and all(
            _is_temporally_disjoint_classification_bridge(path)
            for path in two_hop_paths
        )
    ):
        return (
            False,
            "temporally_disjoint_classification_bridge",
            "every two-hop classification path crosses disjoint validity intervals on a persistent subject",
        )

    if policy == "country_orientation":
        allowed_targets = {
            "region",
            "appellation",
            "landscape",
            "ecosystem",
            "grape",
            "classification",
        }
        if target_kind not in allowed_targets:
            return (
                False,
                "country_non_orientation_two_hop",
                "country pages admit two-hop graph paths only to geographic, "
                "ecosystem, grape, or classification orientation surfaces",
            )
        return (
            True,
            "country_orientation_two_hop",
            "target kind supports the country page's internal/reference orientation job",
        )

    if (
        policy == "directional_geography"
        and target_kind in {"region", "appellation", "landscape"}
        and two_hop_paths
        and all(_is_up_then_down_peer_geography(path) for path in two_hop_paths)
    ):
        return (
            False,
            "shared_broad_geography",
            "every two-hop path climbs to a broad container and descends to a peer geography",
        )

    if policy == "grape_context" and target_kind in {"grape", "classification"}:
        return (
            False,
            "grape_cooccurrence_two_hop",
            "a two-hop wine/classification bridge does not establish general grape adjacency",
        )

    if policy == "producer_world" and target_kind in {"producer", "person"}:
        specific_paths = [
            path
            for path in two_hop_paths
            if set(path["predicates"]) & PRODUCER_SPECIFIC_TWO_HOP_PREDICATES
        ]
        if not specific_paths:
            return (
                False,
                "broad_composite_producer_two_hop",
                "no two-hop path carries professional, site, farming, or explicit practice semantics",
            )
        return (
            True,
            "specific_producer_two_hop",
            "a two-hop path carries professional, site, farming, or explicit practice semantics",
        )

    return (
        True,
        f"{policy}_two_hop",
        f"the {source_kind} policy preserves this governed two-hop context",
    )


def resolve_navigation_candidate(
    source: dict,
    target: dict,
    graph: dict[str, set[str]],
    adjacency: dict[str, list[tuple[str, dict[str, Any], str]]],
) -> dict[str, Any]:
    """Resolve one source/target profile pair with route and policy explanation."""
    starts = set(source["component_entity_ids"])
    targets = set(target["component_entity_ids"])
    source_editorial_anchors = profile_editorial_anchors(source)
    source_countries = profile_country_entities(source)
    target_editorial_anchors = profile_editorial_anchors(target)
    target_countries = profile_country_entities(target)
    paths = enumerate_navigation_paths(starts, targets, adjacency)
    distance = shortest_navigation_distance(graph, starts, targets)

    editorial_outbound_entities = sorted(source_editorial_anchors & targets)
    structural_country_outbound_entities = sorted(source_countries & targets)
    editorial_reciprocal_entities = sorted(starts & target_editorial_anchors)
    structural_country_reciprocal_entities = sorted(starts & target_countries)

    decision: dict[str, Any] = {
        "source_id": source["id"],
        "target_id": target["id"],
        "source_kind": source["profile_kind"],
        "target_kind": target["profile_kind"],
        "distance": distance,
        "paths": paths,
        "editorial_outbound": bool(editorial_outbound_entities),
        "editorial_outbound_entities": editorial_outbound_entities,
        "structural_country_outbound": bool(structural_country_outbound_entities),
        "structural_country_outbound_entities": structural_country_outbound_entities,
        "editorial_reciprocal": bool(editorial_reciprocal_entities),
        "editorial_reciprocal_entities": editorial_reciprocal_entities,
        "structural_country_reciprocal_entities": structural_country_reciprocal_entities,
    }

    if editorial_outbound_entities:
        decision.update(
            eligible=True,
            route_kind="editorial_anchor_outbound",
            reason="the source explicitly selects a target component as an editorial anchor",
        )
    elif structural_country_outbound_entities:
        decision.update(
            eligible=True,
            route_kind="structural_country_outbound",
            reason="the source's structural country membership provides upward orientation",
        )
    elif editorial_reciprocal_entities:
        decision.update(
            eligible=True,
            route_kind="editorial_anchor_reciprocal",
            reason="the target explicitly selects a source component as an editorial anchor",
        )
    elif (
        structural_country_reciprocal_entities
        and source["profile_kind"] == "country"
        and target["profile_kind"] in {"region", "appellation"}
    ):
        decision.update(
            eligible=True,
            route_kind="structural_country_descendant",
            reason="the target's structural country membership provides downward geographic orientation",
        )
    elif distance == 0:
        decision.update(
            eligible=True,
            route_kind="shared_component",
            reason="the profiles share a governed component entity",
        )
    elif distance == 1:
        decision.update(
            eligible=True,
            route_kind="direct_relationship",
            reason="a direct eligible governed relationship connects the profile components",
        )
    elif distance == 2:
        eligible, category, reason = two_hop_navigation_eligibility(
            source["profile_kind"], target["profile_kind"], paths
        )
        decision.update(
            eligible=eligible,
            route_kind="two_hop_relationship" if eligible else "rejected_two_hop",
            policy_category=category,
            reason=reason,
        )
    elif structural_country_reciprocal_entities:
        decision.update(
            eligible=False,
            route_kind="rejected_structural_country_reciprocal",
            policy_category="structural_country_not_editorial",
            reason="target country membership is structural and does not create reciprocal discovery",
        )
    else:
        decision.update(
            eligible=False,
            route_kind="no_route",
            reason="no editorial, structural-outbound, shared, direct, or eligible two-hop route exists",
        )
    return decision


def navigation_candidate_sort_key(candidate: dict[str, Any]) -> tuple[Any, ...]:
    if candidate["editorial_outbound"] or candidate["structural_country_outbound"]:
        tier = 0
    elif (
        candidate["editorial_reciprocal"]
        or candidate["route_kind"] == "structural_country_descendant"
    ):
        tier = 1
    else:
        tier = 2 + (candidate["distance"] or 0)
    return (
        tier,
        candidate["distance"] if candidate["distance"] is not None else 99,
        candidate["title"].casefold(),
        candidate["target_id"],
    )


def render_navigation(profile: dict, data: dict[str, list[dict]]) -> str:
    current_seeds = profile_navigation_seeds(profile)
    graph = navigation_graph(data)
    adjacency = navigation_adjacency(data)
    candidates: list[dict[str, Any]] = []

    for other in data["profiles"]:
        if other["id"] == profile["id"] or not profile_has_surface(other):
            continue
        candidate = resolve_navigation_candidate(profile, other, graph, adjacency)
        if not candidate["eligible"]:
            continue
        candidate["title"] = other["title"]
        candidate["profile"] = other
        candidates.append(candidate)

    related = [
        item["profile"]
        for item in sorted(candidates, key=navigation_candidate_sort_key)[
            :MAX_RELATED_PROFILES
        ]
    ]
    deferred = sorted(
        {
            candidate["title"]
            for candidate in data["profiles"]
            if candidate["publication_status"] == "machine_only"
            and current_seeds & set(candidate["component_entity_ids"])
        },
        key=str.casefold,
    )

    lines = [
        NAVIGATION_BEGIN,
        "## Explore CARTA",
        "",
        (
            "This section is generated from governed profile dispositions, editorial "
            "anchors, and supported graph relationships. It is not a hand-maintained "
            "second knowledge graph."
        ),
        "",
    ]
    if related:
        for other in related:
            relative = posixpath.relpath(
                other["path"], posixpath.dirname(profile["path"])
            )
            depth = (
                "navigation node"
                if other["maturity"] == "node"
                else f"{other['maturity']} reference"
            )
            lines.append(
                f"- [{other['title']}]({relative}) — "
                f"{other['profile_kind']}; {depth}"
            )
    else:
        lines.append("No related Human Reference surface is generated yet.")

    if deferred:
        lines.extend(["", "### Deliberately deferred anchors", ""])
        lines.extend(
            f"- **{title}** — machine authority only; no reader-facing target"
            for title in deferred
        )

    lines.extend([NAVIGATION_END, ""])
    return "\n".join(lines)


def render_provenance(profile: dict, data: dict[str, list[dict]]) -> str:
    claims = profile_claims(profile, data)
    source_by_id = {source["id"]: source for source in data["sources"]}
    source_ids = {
        source_ref["source_id"]
        for claim in claims
        for source_ref in claim["source_refs"]
    }

    seed_entities = set(profile["component_entity_ids"])
    for spatial in data["spatial"]:
        if spatial["entity_id"] in seed_entities:
            source_ids.update(spatial.get("source_ids", []))

    lines = [
        PROVENANCE_BEGIN,
        "## Record & provenance",
        "",
        (
            "This section is generated from CARTA machine authority. Edit the governed "
            "records, then run `python scripts/validate_data.py --write-human-reference`."
        ),
        "",
        f"- **Profile:** `{profile['id']}`",
        (
            f"- **Maturity / publication:** `{profile['maturity']}` / "
            f"`{profile['publication_status']}`"
        ),
    ]
    if profile.get("primary_entity_id"):
        lines.append(f"- **Primary entity:** `{profile['primary_entity_id']}`")

    lines.extend(["", "**Component entities**", ""])
    lines.extend(f"- `{entity_id}`" for entity_id in profile["component_entity_ids"])

    anchors = profile.get("representative_anchor_ids", [])
    if anchors:
        lines.extend(["", "**Representative anchors**", ""])
        lines.extend(f"- `{entity_id}`" for entity_id in anchors)

    lines.extend(["", "<details>", "<summary>Machine claims and sources</summary>", ""])
    lines.extend(["### Material claims", ""])
    if claims:
        lines.extend(
            [
                "| Claim | Layer / observed | Status | Confidence | Sources |",
                "|---|---|---|---|---|",
            ]
        )
        for claim in claims:
            claim_sources = ", ".join(
                f"`{source_ref['source_id']}`" for source_ref in claim["source_refs"]
            )
            layer_and_observed = f"{claim['layer']} / {claim.get('observed_at') or '—'}"
            lines.append(
                f"| `{claim['id']}` | `{layer_and_observed}` | `{claim['status']}` | "
                f"`{claim['confidence']}` | {claim_sources} |"
            )
    else:
        lines.append("No material machine claims are recorded for this profile yet.")

    lines.extend(["", "### Sources", ""])
    if source_ids:
        for source_id in sorted(source_ids):
            title = source_by_id[source_id]["title"].replace("\n", " ")
            lines.append(f"- `{source_id}` — {title}")
    else:
        lines.append("No source records are projected for this profile yet.")
    lines.extend(["", "</details>", "", "### Open questions", ""])

    open_questions = list(profile.get("research_gaps", []))
    unresolved_claims = [
        claim
        for claim in claims
        if claim["status"] in {"provisional", "contested"}
        or claim.get("resolution_needed")
    ]
    for question in open_questions:
        lines.append(f"- {question}")
    for claim in unresolved_claims:
        detail = claim.get("resolution_needed") or claim["statement"]
        lines.append(f"- `{claim['id']}` — {detail}")
    if not open_questions and not unresolved_claims:
        lines.append("- None recorded.")

    lines.extend([PROVENANCE_END, ""])
    return "\n".join(lines)


def render_stub_shell(profile: dict) -> str:
    return "\n".join(
        [
            f"# {profile['title']}",
            "",
            (
                "> **Navigation node:** this honest stub keeps a meaningful CARTA "
                "subject discoverable without presenting it as a finished baseline "
                "reference."
            ),
            "",
            (
                "The machine graph and generated relationships below provide the current "
                "orientation. A generous subject-specific enrichment pass is required "
                "before baseline promotion."
            ),
            "",
        ]
    )


def replace_generated_block(
    text: str,
    block: str,
    begin: str,
    end: str,
    legacy_heading: str | None = None,
) -> str:
    begin_count = text.count(begin)
    end_count = text.count(end)
    if begin_count != end_count or begin_count > 1:
        raise SystemExit(f"malformed generated block markers: {begin} / {end}")
    if begin_count == 1:
        start = text.index(begin)
        finish = text.index(end, start) + len(end)
        return text[:start] + block.rstrip() + text[finish:]

    if legacy_heading:
        legacy_re = re.compile(
            rf"^## {re.escape(legacy_heading)}\s*$.*?(?=^## |\Z)", re.MULTILINE | re.DOTALL
        )
        text = legacy_re.sub("", text, count=1)
    return text.rstrip() + "\n\n" + block.rstrip() + "\n"


def replace_navigation_block(text: str, block: str) -> str:
    begin_count = text.count(NAVIGATION_BEGIN)
    end_count = text.count(NAVIGATION_END)
    if begin_count != end_count or begin_count > 1:
        raise SystemExit(
            f"malformed generated block markers: {NAVIGATION_BEGIN} / {NAVIGATION_END}"
        )
    if begin_count == 1:
        start = text.index(NAVIGATION_BEGIN)
        finish = text.index(NAVIGATION_END, start) + len(NAVIGATION_END)
        return text[:start] + block.rstrip() + text[finish:]

    insertion = text.find(PROVENANCE_BEGIN)
    if insertion >= 0:
        return (
            text[:insertion].rstrip()
            + "\n\n"
            + block.rstrip()
            + "\n\n"
            + text[insertion:].lstrip()
        )
    return text.rstrip() + "\n\n" + block.rstrip() + "\n"


def profile_link(index_path: str, profile: dict) -> str:
    if not profile.get("path"):
        return (
            f"- **{profile['title']}** — "
            f"`{profile['maturity']}` / `{profile['publication_status']}`"
        )
    relative = posixpath.relpath(profile["path"], posixpath.dirname(index_path))
    return (
        f"- [{profile['title']}]({relative}) — "
        f"`{profile['maturity']}` / `{profile['publication_status']}`"
    )


def render_simple_profile_index(
    path: str,
    title: str,
    introduction: str,
    groups: list[tuple[str, set[str]]],
    profiles: list[dict],
) -> str:
    lines = [
        f"# {title}",
        "",
        introduction,
        "",
        INDEX_BEGIN,
    ]
    for heading, kinds in groups:
        selected = sorted(
            (profile for profile in profiles if profile["profile_kind"] in kinds),
            key=lambda profile: (profile["title"].casefold(), profile["id"]),
        )
        if not selected:
            continue
        lines.extend([f"## {heading}", ""])
        surfaced = [profile for profile in selected if profile_has_surface(profile)]
        machine_only = [
            profile
            for profile in selected
            if profile["publication_status"] == "machine_only"
        ]
        if surfaced:
            lines.extend(["### Human Reference surfaces", ""])
            lines.extend(profile_link(path, profile) for profile in surfaced)
            lines.append("")
        if machine_only:
            lines.extend(["### Explicit machine-only dispositions", ""])
            lines.extend(profile_link(path, profile) for profile in machine_only)
            lines.append("")
    lines.extend(
        [
            INDEX_END,
            "",
            (
                "This index is generated from `data/reference-profiles/`. "
                "Edit the governed profile record rather than this file."
            ),
            "",
        ]
    )
    return "\n".join(lines)


def render_wine_index(
    path: str, profiles: list[dict], entities: list[dict]
) -> str:
    profiles_by_component: dict[str, list[dict]] = defaultdict(list)
    for profile in profiles:
        for entity_id in profile["component_entity_ids"]:
            profiles_by_component[entity_id].append(profile)

    wines = sorted(
        (entity for entity in entities if entity["type"] == "wine"),
        key=lambda entity: (entity.get("display_name", entity["name"]).casefold(), entity["id"]),
    )
    standalone_profiles = sorted(
        (profile for profile in profiles if profile["profile_kind"] == "wine"),
        key=lambda profile: (profile["title"].casefold(), profile["id"]),
    )

    lines = [
        "# Wines",
        "",
        (
            "Wine identities are persistent machine records. Most are read through a "
            "governed composite producer profile rather than a parallel wine page."
        ),
        "",
        INDEX_BEGIN,
    ]
    if standalone_profiles:
        lines.extend(["## Standalone wine profiles", ""])
        lines.extend(profile_link(path, profile) for profile in standalone_profiles)
        lines.append("")

    lines.extend(["## Wines in governed composite profiles", ""])
    for wine in wines:
        governing_profiles = sorted(
            profiles_by_component.get(wine["id"], []),
            key=lambda profile: (profile["title"].casefold(), profile["id"]),
        )
        wine_name = wine.get("display_name", wine["name"])
        surfaced_profiles = [
            profile for profile in governing_profiles if profile_has_surface(profile)
        ]
        machine_only_profiles = [
            profile
            for profile in governing_profiles
            if profile["publication_status"] == "machine_only"
        ]
        if surfaced_profiles:
            links = []
            for profile in surfaced_profiles:
                relative = posixpath.relpath(
                    profile["path"], posixpath.dirname(path)
                )
                links.append(f"[{profile['title']}]({relative})")
            lines.append(f"- **{wine_name}** — " + ", ".join(links))
        elif machine_only_profiles:
            dispositions = ", ".join(
                profile["title"] for profile in machine_only_profiles
            )
            lines.append(
                f"- **{wine_name}** — machine-only / deferred with {dispositions}"
            )
        else:
            lines.append(
                f"- **{wine_name}** — machine node; no Human Reference surface"
            )

    lines.extend(
        [
            "",
            INDEX_END,
            "",
            (
                "This index is generated from canonical wine entities and governed "
                "profile components."
            ),
            "",
        ]
    )
    return "\n".join(lines)


def render_indexes(data: dict[str, list[dict]]) -> dict[str, str]:
    profiles = data["profiles"]
    return {
        INDEX_PATHS["grapes"]: render_simple_profile_index(
            INDEX_PATHS["grapes"],
            "Grapes",
            "Governed grape profiles, including honest stubs, are listed here.",
            [("Grape profiles", {"grape"})],
            profiles,
        ),
        INDEX_PATHS["producers"]: render_simple_profile_index(
            INDEX_PATHS["producers"],
            "Producers and people",
            (
                "Human Reference profiles are organized for readers and may compose "
                "multiple producer, person, project, vineyard, and wine records."
            ),
            [
                ("Producer profiles", {"producer"}),
                ("Person profiles", {"person"}),
            ],
            profiles,
        ),
        INDEX_PATHS["places"]: render_simple_profile_index(
            INDEX_PATHS["places"],
            "Places, law, landscapes, and ecosystems",
            (
                "Country-specific regions and appellations are nested beneath countries; "
                "landscapes remain geographic and ecosystems remain relationship-generated. "
                "See the [landscape reference model](../landscapes/README.md)."
            ),
            [
                ("Countries", {"country"}),
                ("Regions", {"region"}),
                ("Appellations", {"appellation"}),
                ("Landscapes", {"landscape"}),
                ("Ecosystems", {"ecosystem"}),
                ("Institutions", {"institution"}),
                ("Practices", {"practice"}),
                ("Classifications", {"classification"}),
                ("Historical events", {"historical_event"}),
            ],
            profiles,
        ),
        INDEX_PATHS["wines"]: render_wine_index(
            INDEX_PATHS["wines"], profiles, data["entities"]
        ),
    }


def render_index_directory() -> str:
    return "\n".join(
        [
            INDEX_DIRECTORY_BEGIN,
            "## Complete indexes",
            "",
            "- [Grapes](indexes/grapes.md)",
            "- [Producers and people](indexes/producers-and-people.md)",
            "- [Wines](indexes/wines.md)",
            "- [Places, law, landscapes, and ecosystems](indexes/places-and-law.md)",
            INDEX_DIRECTORY_END,
            "",
        ]
    )


def sync_human_reference(data: dict[str, list[dict]], write: bool) -> None:
    expected_indexes = render_indexes(data)
    for relative_path, expected in sorted(expected_indexes.items()):
        path = ROOT / relative_path
        current = path.read_text() if path.exists() else ""
        if current != expected:
            if not write:
                raise SystemExit(
                    f"generated index is stale: {relative_path}; run "
                    "python scripts/validate_data.py --write-human-reference"
                )
            path.write_text(expected)
            print(f"UPDATED {relative_path}")

    atlas_readme_path = ROOT / "atlas/README.md"
    atlas_readme = atlas_readme_path.read_text()
    expected_readme = replace_generated_block(
        atlas_readme,
        render_index_directory(),
        INDEX_DIRECTORY_BEGIN,
        INDEX_DIRECTORY_END,
        legacy_heading="Indexes",
    )
    if atlas_readme != expected_readme:
        if not write:
            raise SystemExit(
                "generated Atlas index directory is stale; run "
                "python scripts/validate_data.py --write-human-reference"
            )
        atlas_readme_path.write_text(expected_readme)
        print("UPDATED atlas/README.md")

    surfaced_profiles = sorted(
        (profile for profile in data["profiles"] if profile_has_surface(profile)),
        key=lambda item: item["path"],
    )
    for profile in surfaced_profiles:
        path = ROOT / profile["path"]
        if path.exists():
            current = path.read_text()
        elif not write:
            raise SystemExit(
                f"{profile['id']}: reference path does not exist: {profile['path']}; "
                "run python scripts/validate_data.py --write-human-reference"
            )
        elif profile["publication_status"] == "stub":
            current = render_stub_shell(profile)
        else:
            raise SystemExit(
                f"{profile['id']}: reference path does not exist: {profile['path']}"
            )
        expected = replace_navigation_block(
            current, render_navigation(profile, data)
        )
        expected = replace_generated_block(
            expected,
            render_provenance(profile, data),
            PROVENANCE_BEGIN,
            PROVENANCE_END,
            legacy_heading="Record & provenance",
        )
        if current != expected:
            if not write:
                raise SystemExit(
                    f"generated provenance is stale: {profile['path']}; run "
                    "python scripts/validate_data.py --write-human-reference"
                )
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(expected)
            print(f"UPDATED {profile['path']}")


def validate_atlas_page_governance(data: dict[str, list[dict]]) -> None:
    governed = {
        profile["path"] for profile in data["profiles"] if profile.get("path")
    }
    atlas_pages = {
        path.relative_to(ROOT).as_posix() for path in (ROOT / "atlas").rglob("*.md")
    }
    unexpected = sorted(atlas_pages - governed - ALLOWED_UNGOVERNED_ATLAS_PAGES)
    if unexpected:
        raise SystemExit(
            "ungoverned non-navigation Atlas page(s): " + ", ".join(unexpected)
        )


def local_markdown_target(source: Path, raw_target: str) -> Path | None:
    target = raw_target.strip()
    if target.startswith("<") and target.endswith(">"):
        target = target[1:-1]
    target = target.split(maxsplit=1)[0]
    parsed = urlsplit(target)
    if parsed.scheme or parsed.netloc or target.startswith(("mailto:", "#")):
        return None
    path_part = unquote(parsed.path)
    if not path_part:
        return source.resolve()
    if path_part.startswith("/"):
        destination = (ROOT / path_part.lstrip("/")).resolve()
    else:
        destination = (source.parent / path_part).resolve()
    return destination


def markdown_links(source: Path) -> list[tuple[str, Path]]:
    text = source.read_text()
    links = []
    for match in MARKDOWN_LINK_RE.finditer(text):
        raw_target = match.group(1)
        destination = local_markdown_target(source, raw_target)
        if destination is not None:
            links.append((raw_target, destination))
    return links


def validate_markdown_links_and_reachability(data: dict[str, list[dict]]) -> None:
    atlas_root = (ROOT / "atlas").resolve()
    atlas_pages = sorted((ROOT / "atlas").rglob("*.md"))
    graph: dict[Path, set[Path]] = defaultdict(set)

    for source in atlas_pages:
        for raw_target, destination in markdown_links(source):
            try:
                destination.relative_to(ROOT.resolve())
            except ValueError:
                raise SystemExit(
                    f"{source.relative_to(ROOT)}: local link escapes repository: {raw_target}"
                )
            if not destination.exists():
                raise SystemExit(
                    f"{source.relative_to(ROOT)}: broken local link: {raw_target}"
                )
            if destination.is_file() and destination.suffix == ".md":
                try:
                    destination.relative_to(atlas_root)
                except ValueError:
                    continue
                graph[source.resolve()].add(destination)

    start = (ROOT / "atlas/README.md").resolve()
    reachable = {start}
    queue = deque([start])
    while queue:
        current = queue.popleft()
        for destination in graph.get(current, set()):
            if destination not in reachable:
                reachable.add(destination)
                queue.append(destination)

    unreachable_profiles = sorted(
        profile["path"]
        for profile in data["profiles"]
        if profile.get("path")
        if (ROOT / profile["path"]).resolve() not in reachable
    )
    if unreachable_profiles:
        raise SystemExit(
            "governed profile(s) unreachable from atlas/README.md: "
            + ", ".join(unreachable_profiles)
        )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--write-human-reference",
        action="store_true",
        help="Update deterministic Atlas indexes and profile provenance blocks.",
    )
    args = parser.parse_args()

    data, ids = load_and_validate_schema()
    validate_references(data, ids)
    validate_authored_contracts(data, ids)
    validate_profiles(data, ids)
    sync_human_reference(data, args.write_human_reference)
    validate_atlas_page_governance(data)
    validate_markdown_links_and_reachability(data)

    print("PASS", ", ".join(f"{key}={len(value)}" for key, value in data.items()))


if __name__ == "__main__":
    main()
