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

INAO_DATASET_ID = "spatial-dataset:inao-aires-geographiques-siqo-2026-08-24"
NATURAL_EARTH_DATASET_ID = "spatial-dataset:natural-earth-admin-0-countries-5.1.1"
OPENFREEMAP_DATASET_ID = "spatial-dataset:openfreemap-liberty-runtime"

RAW_GIS_SUFFIXES = {".zip", ".7z", ".shp", ".dbf", ".shx", ".gpkg"}


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
    sources = read_jsonl((ROOT / "data/sources").glob("*.jsonl"))
    profiles = read_jsonl((ROOT / "data/reference-profiles").glob("*.jsonl"))
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
        "profile_paths": {
            entity_id: sorted(set(paths)) for entity_id, paths in profile_paths.items()
        },
    }


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
    required = {INAO_DATASET_ID, NATURAL_EARTH_DATASET_ID, OPENFREEMAP_DATASET_ID}
    if not required.issubset(by_id):
        fail("missing required active Atlas manifest(s): " + ", ".join(sorted(required - by_id.keys())))
    return by_id


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


def validate_atlas() -> dict[str, Any]:
    authority = load_authority()
    manifests = load_and_validate_manifests(authority)
    validate_artifacts(manifests)
    mappings = load_and_validate_mappings(manifests, authority)

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
    expected_search_ids = {
        f"inao-denom-{denom_id}" for denom_id in source_ids
    } | {feature["id"] for feature in regions["features"]}
    if set(search_ids) != expected_search_ids:
        fail("search-index.json: results do not match rendered wine features and regions")
    for record in search:
        bounds = record.get("bounds")
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
    if provenance_ids != {INAO_DATASET_ID, NATURAL_EARTH_DATASET_ID, OPENFREEMAP_DATASET_ID}:
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
    }:
        fail("atlas config: expected AOC-default, IGP-off layer policy")
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
