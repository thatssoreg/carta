#!/usr/bin/env python3
"""Build deterministic, browser-sized CARTA Atlas geography from pinned sources."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import sys
import urllib.request
import zipfile
from collections import defaultdict
from pathlib import Path
from typing import Any, Iterable

GEOSPATIAL_IMPORT_ERROR: ImportError | None = None

try:
    import geopandas as gpd
    import pandas as pd
    from shapely import make_valid, union_all
    from shapely.geometry import GeometryCollection, MultiPolygon, Polygon, mapping, shape
except ImportError as exc:  # pragma: no cover - exercised by clean validation environments
    # Deferred so that copy-only projections (scripts/project_editorial.py) can
    # reuse this module without the GIS stack. Geometry work still refuses to run.
    GEOSPATIAL_IMPORT_ERROR = exc


def require_geospatial() -> None:
    if GEOSPATIAL_IMPORT_ERROR is not None:
        raise SystemExit(
            "Install Atlas build dependencies: python -m pip install -r requirements-atlas.txt"
        ) from GEOSPATIAL_IMPORT_ERROR


ROOT = Path(__file__).resolve().parents[1]
MANIFEST_DIR = ROOT / "data/geography/datasets"
MAPPING_DIR = ROOT / "data/geography/external-id-mappings"
PUBLIC_DATA_DIR = ROOT / "atlas-app/public/data"
GEOMETRY_METADATA_PATH = ROOT / "data/geography/geometry/atlas-france-inao.jsonl"
EXPERIENCE_CONFIG_PATH = ROOT / "data/atlas/run-07-editorial-foundation.json"
EXPERIENCE_LINEAGE = [
    "data/atlas/run-05-jura-final-cut.json",
    "data/atlas/run-06-bearn-jurancon-world.json",
    "data/atlas/run-07-editorial-foundation.json",
]
PRODUCER_BASES_SOURCE_DIR = ROOT / "data/geography/producer-bases"

INAO_DATASET_ID = "spatial-dataset:inao-aires-geographiques-siqo-2026-08-24"
NATURAL_EARTH_DATASET_ID = "spatial-dataset:natural-earth-admin-0-countries-5.1.1"
OPENFREEMAP_DATASET_ID = "spatial-dataset:openfreemap-liberty-runtime"

ARTIFACT_LIMITS = {
    "atlas-app/public/data/world-countries.geojson": 4_000_000,
    "atlas-app/public/data/france-appellations-aoc.geojson": 15_000_000,
    "atlas-app/public/data/france-appellations-igp.geojson": 6_000_000,
}


def read_json(path: Path) -> Any:
    return json.loads(path.read_text())


def deep_merge(base: Any, overlay: Any) -> Any:
    """Merge a small release overlay without duplicating the prior finished world."""
    if isinstance(base, dict) and isinstance(overlay, dict):
        merged = dict(base)
        for key, value in overlay.items():
            if key == "extends":
                continue
            merged[key] = deep_merge(merged[key], value) if key in merged else value
        return merged
    return overlay


def load_experience_config() -> dict[str, Any]:
    """Resolve the full `extends` chain so every prior run stays in force.

    Each release overlay states only what it changes. Merging the whole chain
    oldest-first keeps finished worlds intact instead of silently dropping the
    releases below the newest overlay.
    """
    chain: list[Path] = []
    seen: set[Path] = set()
    path = EXPERIENCE_CONFIG_PATH
    while True:
        resolved = path.resolve()
        if ROOT not in resolved.parents:
            raise SystemExit("experience overlay extends a path outside the repository")
        if resolved in seen:
            raise SystemExit("experience overlay chain is circular")
        seen.add(resolved)
        chain.append(resolved)
        extends = read_json(resolved).get("extends")
        if not extends:
            break
        path = ROOT / extends
    merged: dict[str, Any] = {}
    for resolved in reversed(chain):
        merged = deep_merge(merged, read_json(resolved))
    return merged


def read_jsonl(paths: Iterable[Path]) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for path in sorted(paths):
        for lineno, line in enumerate(path.read_text().splitlines(), 1):
            if not line.strip():
                continue
            try:
                records.append(json.loads(line))
            except json.JSONDecodeError as exc:
                raise SystemExit(f"{path}:{lineno}: invalid JSON: {exc}") from exc
    return records


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
        + "\n"
    )


def write_json_pretty(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n"
    )


def write_jsonl(path: Path, records: Iterable[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        json.dumps(record, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
        for record in records
    ]
    path.write_text("\n".join(lines) + ("\n" if lines else ""))


def sha256_path(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def load_manifests() -> dict[str, dict[str, Any]]:
    manifests = [read_json(path) for path in sorted(MANIFEST_DIR.glob("*.json"))]
    by_id = {manifest["id"]: manifest for manifest in manifests}
    if len(by_id) != len(manifests):
        raise SystemExit("duplicate spatial dataset manifest ID")
    return by_id


def parse_source_archives(values: list[str]) -> dict[str, Path]:
    parsed: dict[str, Path] = {}
    for value in values:
        if "=" not in value:
            raise SystemExit("--source-archive must use DATASET_ID=/absolute/path.zip")
        dataset_id, raw_path = value.split("=", 1)
        path = Path(raw_path).expanduser().resolve()
        if not path.is_file():
            raise SystemExit(f"source archive does not exist: {path}")
        parsed[dataset_id] = path
    return parsed


def acquire_archive(
    manifest: dict[str, Any], cache_dir: Path, supplied: dict[str, Path]
) -> Path:
    dataset_id = manifest["id"]
    if dataset_id in supplied:
        archive = supplied[dataset_id]
    else:
        archive_dir = cache_dir / "archives"
        archive_dir.mkdir(parents=True, exist_ok=True)
        archive = archive_dir / f"{dataset_id.split(':', 1)[1]}.zip"
        if not archive.exists():
            temporary = archive.with_suffix(".partial")
            request = urllib.request.Request(
                manifest["resource_url"],
                headers={"User-Agent": "CARTA-Atlas/0.1 (+https://github.com/thatssoreg/carta)"},
            )
            print(f"DOWNLOAD {dataset_id}")
            with urllib.request.urlopen(request) as response, temporary.open("wb") as target:
                shutil.copyfileobj(response, target)
            os.replace(temporary, archive)

    actual = sha256_path(archive)
    if actual != manifest["checksum"]:
        raise SystemExit(
            f"{dataset_id}: checksum mismatch; expected {manifest['checksum']}, got {actual}"
        )
    return archive


def extract_archive(archive: Path, dataset_id: str, cache_dir: Path) -> Path:
    extracted_root = (cache_dir / "extracted").resolve()
    extracted_root.mkdir(parents=True, exist_ok=True)
    target = (extracted_root / dataset_id.split(":", 1)[1]).resolve()
    if target.parent != extracted_root:
        raise SystemExit("unsafe extraction target")
    marker = target / ".source-sha256"
    checksum = sha256_path(archive)
    if marker.exists() and marker.read_text().strip() == checksum:
        return target
    if target.exists():
        shutil.rmtree(target)
    target.mkdir(parents=True)
    with zipfile.ZipFile(archive) as bundle:
        for member in bundle.infolist():
            destination = (target / member.filename).resolve()
            if target not in destination.parents and destination != target:
                raise SystemExit(f"unsafe ZIP member: {member.filename}")
        bundle.extractall(target)
    marker.write_text(checksum + "\n")
    return target


def only_shapefile(directory: Path) -> Path:
    candidates = sorted(directory.rglob("*.shp"))
    if len(candidates) != 1:
        raise SystemExit(
            f"expected exactly one Shapefile in {directory}, found {len(candidates)}"
        )
    return candidates[0]


def polygonal_geometry(geometry: Any) -> Polygon | MultiPolygon:
    if geometry is None or geometry.is_empty:
        raise SystemExit("source contains empty geometry")
    if not geometry.is_valid:
        geometry = make_valid(geometry)
    if isinstance(geometry, (Polygon, MultiPolygon)):
        return geometry
    if isinstance(geometry, GeometryCollection):
        parts = [part for part in geometry.geoms if isinstance(part, (Polygon, MultiPolygon))]
        if parts:
            dissolved = union_all(parts)
            if isinstance(dissolved, (Polygon, MultiPolygon)):
                return dissolved
    raise SystemExit(f"non-polygonal geometry after validation: {geometry.geom_type}")


def rounded_coordinates(value: Any, places: int = 6) -> Any:
    if isinstance(value, float):
        return round(value, places)
    if isinstance(value, tuple):
        return [rounded_coordinates(item, places) for item in value]
    if isinstance(value, list):
        return [rounded_coordinates(item, places) for item in value]
    return value


def geometry_mapping(geometry: Any) -> dict[str, Any]:
    raw = mapping(polygonal_geometry(geometry))
    raw["coordinates"] = rounded_coordinates(raw["coordinates"])
    rounded = polygonal_geometry(shape(raw))
    final = mapping(rounded)
    final["coordinates"] = rounded_coordinates(final["coordinates"])
    return final


def clean_optional_code(value: Any) -> str | None:
    if value is None or pd.isna(value):
        return None
    text = str(value).strip()
    return None if text in {"", "-99"} else text


def integer_string(value: Any) -> str:
    if value is None or pd.isna(value):
        raise SystemExit("required source identifier is null")
    return str(int(value))


def entity_profile_paths() -> dict[str, str]:
    profiles = read_jsonl((ROOT / "data/reference-profiles").glob("*.jsonl"))
    candidates: dict[str, list[tuple[int, str]]] = defaultdict(list)
    for profile in profiles:
        path = profile.get("path")
        if not path:
            continue
        for entity_id in profile["component_entity_ids"]:
            priority = 0 if profile.get("primary_entity_id") == entity_id else 1
            candidates[entity_id].append((priority, path))
    return {
        entity_id: sorted(paths)[0][1]
        for entity_id, paths in candidates.items()
    }


def load_mappings(dataset_id: str) -> dict[str, dict[str, Any]]:
    mappings = read_jsonl(MAPPING_DIR.glob("*.jsonl"))
    selected = [
        record
        for record in mappings
        if record["source_dataset_id"] == dataset_id
        and record["match_status"] == "accepted"
    ]
    by_source = {record["source_identifier"]: record for record in selected}
    if len(by_source) != len(selected):
        raise SystemExit(f"{dataset_id}: duplicate accepted source identifier mapping")
    return by_source


def build_world_countries(
    shapefile: Path, manifest: dict[str, Any], profile_paths: dict[str, str]
) -> tuple[dict[str, Any], dict[str, Any]]:
    mappings = load_mappings(manifest["id"])
    fields = [
        "ADMIN",
        "NAME",
        "NAME_LONG",
        "NAME_FR",
        "ISO_A2",
        "ISO_A3",
        "ADM0_A3",
        "NE_ID",
    ]
    frame = gpd.read_file(shapefile, columns=fields)
    if frame.crs is None or frame.crs.to_epsg() != 4326:
        raise SystemExit(f"Natural Earth source CRS is not EPSG:4326: {frame.crs}")

    features: list[dict[str, Any]] = []
    for _, row in frame.iterrows():
        geometry = polygonal_geometry(row.geometry).simplify(
            0.03, preserve_topology=True
        )
        geometry = polygonal_geometry(geometry)
        ne_id = integer_string(row.NE_ID)
        mapping_record = mappings.get(ne_id)
        carta_entity_id = (
            mapping_record["carta_entity_id"] if mapping_record else None
        )
        source_feature_id = f"natural-earth-admin0-{ne_id}"
        features.append(
            {
                "type": "Feature",
                "id": source_feature_id,
                "properties": {
                    "source_feature_id": source_feature_id,
                    "source_ne_id": ne_id,
                    "name": str(row.NAME),
                    "name_long": str(row.NAME_LONG),
                    "name_fr": clean_optional_code(row.NAME_FR),
                    "iso_a2": clean_optional_code(row.ISO_A2),
                    "iso_a3": clean_optional_code(row.ISO_A3),
                    "adm0_a3": clean_optional_code(row.ADM0_A3),
                    "carta_entity_id": carta_entity_id,
                    "human_reference_path": profile_paths.get(carta_entity_id),
                    "governance_status": "governed" if carta_entity_id else "external_context",
                    "representation_type": "generalized_country_interaction_area",
                    "source_dataset_id": manifest["id"],
                    "source_release_date": manifest["source_release_date"],
                },
                "geometry": geometry_mapping(geometry),
            }
        )
    features.sort(key=lambda feature: (feature["properties"]["name"].casefold(), feature["id"]))
    collection = {"type": "FeatureCollection", "features": features}
    return collection, {"source_features": len(frame), "repaired_features": 0}


def build_inao_features(
    shapefile: Path, manifest: dict[str, Any], profile_paths: dict[str, str]
) -> tuple[dict[str, list[dict[str, Any]]], dict[str, Any], dict[str, Any]]:
    mappings = load_mappings(manifest["id"])
    frame = gpd.read_file(shapefile)
    if frame.crs is None:
        raise SystemExit("INAO source has no CRS")
    required = {
        "categorie",
        "type_denom",
        "signe",
        "id_app",
        "app",
        "id_denom",
        "denom",
    }
    missing = sorted(required - set(frame.columns))
    if missing:
        raise SystemExit("INAO source missing required fields: " + ", ".join(missing))

    source_feature_count = len(frame)
    frame = frame[
        frame["categorie"].fillna("").str.startswith("Vin")
        & frame["signe"].isin(["AOC", "IGP"])
    ].copy()
    frame["source_fid"] = frame.index.astype(int)
    invalid_source = ~frame.geometry.is_valid
    repaired_fids = set(frame.loc[invalid_source, "source_fid"].tolist())
    if invalid_source.any():
        frame.loc[invalid_source, "geometry"] = frame.loc[
            invalid_source, "geometry"
        ].map(make_valid)

    groups: dict[str, list[dict[str, Any]]] = {"AOC": [], "IGP": []}
    source_geometry_by_entity: dict[str, list[Any]] = defaultdict(list)
    source_feature_by_entity: dict[str, list[dict[str, Any]]] = defaultdict(list)

    for sign, tolerance in (("AOC", 40.0), ("IGP", 120.0)):
        subset = frame[frame["signe"] == sign].copy()
        subset["geometry"] = subset.geometry.map(
            lambda geometry: polygonal_geometry(geometry).simplify(
                tolerance, preserve_topology=True
            )
        )
        invalid_transformed = ~subset.geometry.is_valid
        if invalid_transformed.any():
            repaired_fids.update(
                subset.loc[invalid_transformed, "source_fid"].tolist()
            )
            subset.loc[invalid_transformed, "geometry"] = subset.loc[
                invalid_transformed, "geometry"
            ].map(make_valid)
        subset = subset.to_crs("EPSG:4326")

        for _, row in subset.iterrows():
            denom_id = integer_string(row.id_denom)
            app_id = integer_string(row.id_app)
            mapping_record = mappings.get(denom_id)
            carta_entity_id = (
                mapping_record["carta_entity_id"] if mapping_record else None
            )
            source_fid = int(row.source_fid)
            source_feature_id = f"inao-denom-{denom_id}-fid-{source_fid}"
            geometry = polygonal_geometry(row.geometry)
            geometry_object = geometry_mapping(geometry)
            feature = {
                "type": "Feature",
                "id": source_feature_id,
                "properties": {
                    "source_feature_id": source_feature_id,
                    "source_appellation_id": app_id,
                    "source_denomination_id": denom_id,
                    "source_appellation_name": str(row.app),
                    "name": str(row.denom),
                    "designation": sign,
                    "product_categories": str(row.categorie),
                    "feature_type": (
                        "appellation"
                        if str(row.type_denom).casefold() == "appellation"
                        else "geographical_complement"
                    ),
                    "representation_type": "regulatory_geographical_area",
                    "representation_label": "INAO cartographic representation of regulatory geographical area",
                    "source_dataset_id": manifest["id"],
                    "source_release_date": manifest["source_release_date"],
                    "geometry_status": (
                        "repaired_and_simplified_for_web"
                        if source_fid in repaired_fids
                        else "source_valid_simplified_for_web"
                    ),
                    "carta_entity_id": carta_entity_id,
                    "human_reference_path": profile_paths.get(carta_entity_id),
                    "governance_status": "governed" if carta_entity_id else "external_only",
                },
                "geometry": geometry_object,
            }
            groups[sign].append(feature)
            if carta_entity_id:
                rounded_geometry = polygonal_geometry(shape(geometry_object))
                source_geometry_by_entity[carta_entity_id].append(rounded_geometry)
                source_feature_by_entity[carta_entity_id].append(feature)

    for features in groups.values():
        features.sort(
            key=lambda feature: (
                feature["properties"]["name"].casefold(),
                feature["properties"]["source_denomination_id"],
                feature["id"],
            )
        )

    mapped_source_ids = {
        feature["properties"]["source_denomination_id"]
        for features in groups.values()
        for feature in features
        if feature["properties"]["carta_entity_id"]
    }
    missing_mappings = sorted(set(mappings) - mapped_source_ids)
    if missing_mappings:
        raise SystemExit(
            "accepted INAO mappings not present in filtered source: "
            + ", ".join(missing_mappings)
        )

    statistics = {
        "source_features": source_feature_count,
        "wine_features": sum(len(features) for features in groups.values()),
        "aoc_features": len(groups["AOC"]),
        "igp_features": len(groups["IGP"]),
        "mapped_features": sum(len(features) for features in source_feature_by_entity.values()),
        "mapped_entities": len(source_feature_by_entity),
        "unmapped_features": sum(len(features) for features in groups.values())
        - sum(len(features) for features in source_feature_by_entity.values()),
        "ambiguous_mappings": 0,
        "source_invalid_features": int(invalid_source.sum()),
        "repaired_features": len(repaired_fids),
    }
    linkage = {
        "geometry_by_entity": source_geometry_by_entity,
        "features_by_entity": source_feature_by_entity,
    }
    return groups, statistics, linkage


def france_region_profiles() -> list[dict[str, Any]]:
    profiles = read_jsonl((ROOT / "data/reference-profiles").glob("*.jsonl"))
    return [
        profile
        for profile in profiles
        if profile["profile_kind"] == "region"
        and "place:france" in profile.get("country_entity_ids", [])
        and profile.get("path")
    ]


def build_region_labels(
    geometry_by_entity: dict[str, list[Any]],
) -> dict[str, Any]:
    relationships = read_jsonl((ROOT / "data/relationships").glob("*.jsonl"))
    profiles = france_region_profiles()
    mapped_entities = set(geometry_by_entity)
    features: list[dict[str, Any]] = []

    for profile in profiles:
        region_entity_id = profile.get("primary_entity_id")
        child_ids = {
            entity_id
            for entity_id in profile["component_entity_ids"]
            if entity_id in mapped_entities and entity_id.startswith("appellation:")
        }
        for relationship in relationships:
            if (
                relationship["status"] in {"supported", "provisional"}
                and relationship["predicate"] in {"WITHIN", "LOCATED_IN"}
                and relationship["subject_id"] in mapped_entities
                and relationship["object_id"] == region_entity_id
            ):
                child_ids.add(relationship["subject_id"])
        if not child_ids:
            continue
        geometries = [
            geometry
            for child_id in sorted(child_ids)
            for geometry in geometry_by_entity[child_id]
        ]
        dissolved = polygonal_geometry(union_all(geometries))
        anchor = dissolved.representative_point()
        west, south, east, north = dissolved.bounds
        feature_id = f"carta-wine-region-{region_entity_id.split(':', 1)[1]}"
        features.append(
            {
                "type": "Feature",
                "id": feature_id,
                "properties": {
                    "source_feature_id": feature_id,
                    "name": profile["title"],
                    "feature_type": "wine_region_orientation",
                    "representation_type": "derived_label_anchor",
                    "representation_label": "CARTA wine-region orientation label; not a statutory polygon",
                    "derivation": "representative_point_of_union_of_mapped_child_inao_geometries",
                    "child_carta_entity_ids": sorted(child_ids),
                    "bounds": [
                        round(west, 6),
                        round(south, 6),
                        round(east, 6),
                        round(north, 6),
                    ],
                    "carta_entity_id": region_entity_id,
                    "human_reference_path": profile["path"],
                    "governance_status": "governed",
                    "source_dataset_id": INAO_DATASET_ID,
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [round(anchor.x, 6), round(anchor.y, 6)],
                },
            }
        )
    features.sort(key=lambda feature: feature["properties"]["name"].casefold())
    return {"type": "FeatureCollection", "features": features}


def feature_bounds(feature: dict[str, Any]) -> list[float]:
    west, south, east, north = shape(feature["geometry"]).bounds
    return [round(west, 6), round(south, 6), round(east, 6), round(north, 6)]


def subject_route(entity_id: str) -> str:
    kind, slug = entity_id.split(":", 1)
    return f"#/{kind}/{slug}"


def build_producer_points(
    experience: dict[str, Any],
) -> dict[str, Any]:
    """Project governed producer-base assertions into a map-safe point layer."""
    entities = {
        record["id"]: record
        for record in read_jsonl((ROOT / "data/entities").glob("*.jsonl"))
    }
    geometry_records = {
        record["id"]: record
        for record in read_jsonl((ROOT / "data/geography/geometry").glob("*.jsonl"))
    }
    assertions = read_jsonl(
        (ROOT / "data/geography/assertions").glob("*.jsonl")
    )
    raw_by_ref: dict[tuple[str, str], dict[str, Any]] = {}
    for source_path in sorted(PRODUCER_BASES_SOURCE_DIR.glob("*.geojson")):
        relative = source_path.relative_to(ROOT).as_posix()
        for feature in read_json(source_path)["features"]:
            key = (relative, feature["id"])
            if key in raw_by_ref:
                raise SystemExit(f"duplicate producer source feature: {relative}#{feature['id']}")
            raw_by_ref[key] = feature
    features: list[dict[str, Any]] = []

    for entity_id in experience["producer_ids"]:
        candidates = [
            record
            for record in assertions
            if record["entity_id"] == entity_id
            and record["representation_kind"] == "reference_location"
            and record["status"] == "supported"
            and record.get("geometry_ids")
        ]
        if not candidates:
            raise SystemExit(f"{entity_id}: no supported producer-base spatial assertion")
        candidates.sort(
            key=lambda record: (
                0 if record.get("observed_at") else 1,
                record.get("observed_at") or "",
                record["id"],
            ),
            reverse=True,
        )
        spatial = candidates[0]
        if len(spatial["geometry_ids"]) != 1:
            raise SystemExit(f"{spatial['id']}: producer point requires one geometry")
        geometry_record = geometry_records[spatial["geometry_ids"][0]]
        marker = "#source_feature_id="
        if marker not in geometry_record["geometry_ref"]:
            raise SystemExit(f"{geometry_record['id']}: missing source feature selector")
        relative, raw_feature_id = geometry_record["geometry_ref"].split(marker, 1)
        source_path = (ROOT / relative).resolve()
        if PRODUCER_BASES_SOURCE_DIR.resolve() not in source_path.parents:
            raise SystemExit(f"{geometry_record['id']}: unexpected producer point source")
        source_feature = raw_by_ref.get((relative, raw_feature_id))
        if not source_feature:
            raise SystemExit(f"{geometry_record['id']}: source point does not exist")
        if source_feature["properties"]["entity_id"] != entity_id:
            raise SystemExit(f"{geometry_record['id']}: source point identity drifted")
        place_label = source_feature["properties"]["place_label"]
        precision = spatial.get("precision", "unknown")
        placement_note = (
            f"Approximate location · {place_label}"
            if precision not in {"address", "locality"}
            else f"Production base · {place_label}"
        )
        feature_id = f"carta-producer-{entity_id.split(':', 1)[1]}"
        features.append(
            {
                "type": "Feature",
                "id": feature_id,
                "properties": {
                    "source_feature_id": feature_id,
                    "carta_entity_id": entity_id,
                    "name": entities[entity_id]["name"],
                    "feature_type": "producer_base",
                    "place_label": place_label,
                    "precision": precision,
                    "placement_note": placement_note,
                    "representation_label": "Production or cellar base; not vineyard holdings",
                    "spatial_assertion_id": spatial["id"],
                    "geometry_id": geometry_record["id"],
                    "source_ids": spatial["source_ids"],
                    "native_route": subject_route(entity_id),
                },
                "geometry": source_feature["geometry"],
            }
        )
    features.sort(key=lambda feature: feature["properties"]["name"].casefold())
    return {"type": "FeatureCollection", "features": features}


def build_search_index(
    groups: dict[str, list[dict[str, Any]]], region_labels: dict[str, Any]
) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    for feature in region_labels["features"]:
        properties = feature["properties"]
        results.append(
            {
                "id": feature["id"],
                "name": properties["name"],
                "result_type": "wine_region",
                "feature_type": properties["feature_type"],
                "representation_label": properties["representation_label"],
                "bounds": properties["bounds"],
                "source_feature_ids": [feature["id"]],
                "carta_entity_id": properties["carta_entity_id"],
                "human_reference_path": properties["human_reference_path"],
                "governance_status": "governed",
            }
        )

    grouped: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    for sign, features in groups.items():
        for feature in features:
            grouped[(sign, feature["properties"]["source_denomination_id"])].append(feature)

    for (sign, denom_id), features in grouped.items():
        first = features[0]
        properties = first["properties"]
        geometries = [shape(feature["geometry"]) for feature in features]
        west, south, east, north = union_all(geometries).bounds
        name = (
            properties["source_appellation_name"]
            if len(features) > 1
            else properties["name"]
        )
        results.append(
            {
                "id": f"inao-denom-{denom_id}",
                "name": name,
                "result_type": "aoc_appellation" if sign == "AOC" else "igp_appellation",
                "designation": sign,
                "feature_type": properties["feature_type"],
                "representation_label": properties["representation_label"],
                "source_appellation_id": properties["source_appellation_id"],
                "source_denomination_id": denom_id,
                "source_appellation_name": properties["source_appellation_name"],
                "source_feature_ids": [feature["id"] for feature in features],
                "bounds": [
                    round(west, 6),
                    round(south, 6),
                    round(east, 6),
                    round(north, 6),
                ],
                "carta_entity_id": properties["carta_entity_id"],
                "human_reference_path": properties["human_reference_path"],
                "governance_status": properties["governance_status"],
                "source_dataset_id": properties["source_dataset_id"],
                "source_release_date": properties["source_release_date"],
            }
        )
    results.sort(
        key=lambda result: (
            0 if result["result_type"] == "wine_region" else 1,
            result["name"].casefold(),
            result["id"],
        )
    )
    return results


def build_atlas_guides(profile_paths: dict[str, str]) -> dict[str, Any]:
    """Project sourced CARTA claims into compact learner guides.

    This artifact contains no authored facts: every section and quantity names the
    governed claim it came from, and every link comes from a governed profile anchor.
    """
    entities = read_jsonl((ROOT / "data/entities").glob("*.jsonl"))
    claims = read_jsonl((ROOT / "data/claims").glob("*.jsonl"))
    sources = read_jsonl((ROOT / "data/sources").glob("*.jsonl"))
    profiles = read_jsonl((ROOT / "data/reference-profiles").glob("*.jsonl"))
    entity_by_id = {record["id"]: record for record in entities}
    source_by_id = {record["id"]: record for record in sources}
    eligible_profiles = [
        profile
        for profile in profiles
        if profile.get("publication_status") == "published"
        and profile.get("profile_kind") in {"region", "appellation"}
        and "place:france" in profile.get("country_entity_ids", [])
        and profile.get("primary_entity_id")
    ]

    payloads: dict[str, dict[str, Any]] = {}
    by_profile: dict[str, dict[str, Any]] = {}
    for profile in sorted(eligible_profiles, key=lambda item: item["id"]):
        component_ids = set(profile["component_entity_ids"])
        selected_claims = sorted(
            (
                claim
                for claim in claims
                if claim["subject_ref"] in component_ids
                and claim.get("atlas_presentation")
                and (
                    claim["subject_ref"] == profile["primary_entity_id"]
                    or claim["atlas_presentation"]["section"] != "orientation"
                )
                and claim["status"] == "supported"
            ),
            key=lambda claim: (
                claim["atlas_presentation"]["order"], claim["id"]
            ),
        )
        if not selected_claims:
            continue

        section_claims = []
        quantities = []
        used_source_ids: set[str] = set()
        for claim in selected_claims:
            presentation = claim["atlas_presentation"]
            source_ids = [ref["source_id"] for ref in claim["source_refs"]]
            used_source_ids.update(source_ids)
            projected = {
                "claim_id": claim["id"],
                "subject_ref": claim["subject_ref"],
                "subject_name": entity_by_id[claim["subject_ref"]]["name"],
                "section": presentation["section"],
                "order": presentation["order"],
                "label": presentation.get("label"),
                "statement": claim["statement"],
                "observed_at": claim.get("observed_at"),
                "source_ids": source_ids,
            }
            if claim.get("quantity"):
                quantity = dict(claim["quantity"])
                dimension_ref = quantity.get("dimension_ref")
                if dimension_ref:
                    quantity["dimension_name"] = entity_by_id[dimension_ref]["name"]
                projected["quantity"] = quantity
                quantities.append(projected)
            else:
                section_claims.append(projected)

        anchors = []
        for entity_id in profile.get("representative_anchor_ids", []):
            path = profile_paths.get(entity_id)
            entity = entity_by_id[entity_id]
            if not path or path == profile.get("path"):
                continue
            prefix = {
                "producer": "Meet",
                "project": "Meet",
                "grape": "Learn about",
                "appellation": "Explore",
                "place": "Explore",
            }.get(entity["type"], "Explore")
            anchors.append(
                {
                    "entity_id": entity_id,
                    "name": entity["name"],
                    "kind": entity["type"],
                    "label": f"{prefix} {entity['name']}",
                    "human_reference_path": path,
                }
            )

        payload = {
            "guide_entity_id": profile["primary_entity_id"],
            "title": profile["title"],
            "profile_id": profile["id"],
            "human_reference_path": profile["path"],
            "maturity": profile["maturity"],
            "component_entity_ids": profile["component_entity_ids"],
            "sections": section_claims,
            "quantities": quantities,
            "explore": anchors,
            "sources": [
                {
                    "source_id": source_id,
                    "title": source_by_id[source_id]["title"],
                    "publisher": source_by_id[source_id].get("publisher"),
                    "url": source_by_id[source_id].get("url"),
                    "publication_date": source_by_id[source_id].get("publication_date"),
                    "accessed_at": source_by_id[source_id]["accessed_at"],
                }
                for source_id in sorted(used_source_ids)
            ],
        }
        by_profile[profile["id"]] = payload
        payloads[profile["primary_entity_id"]] = payload

    # Region profiles can teach mapped child appellations that do not yet merit a
    # standalone profile. A primary profile always wins over this alias.
    for profile in sorted(eligible_profiles, key=lambda item: item["id"]):
        payload = by_profile.get(profile["id"])
        if not payload:
            continue
        for entity_id in profile["component_entity_ids"]:
            payloads.setdefault(entity_id, payload)

    return {
        "generated_from": [
            "data/claims/*.jsonl",
            "data/entities/*.jsonl",
            "data/reference-profiles/*.jsonl",
            "data/sources/*.jsonl",
        ],
        "projection_contract": (
            "Every learner statement and number carries a claim_id; consumers must "
            "not parse quantities from prose. Region aliases never change the selected "
            "map feature's CARTA identity."
        ),
        "guides": {key: payloads[key] for key in sorted(payloads)},
    }


def build_atlas_subjects(
    experience: dict[str, Any],
    geographic_search: list[dict[str, Any]],
    producer_points: dict[str, Any],
) -> dict[str, Any]:
    """Build native subject cards and graph routes directly from CARTA authority."""
    entity_records = read_jsonl((ROOT / "data/entities").glob("*.jsonl"))
    claim_records = read_jsonl((ROOT / "data/claims").glob("*.jsonl"))
    source_records = read_jsonl((ROOT / "data/sources").glob("*.jsonl"))
    profile_records = read_jsonl(
        (ROOT / "data/reference-profiles").glob("*.jsonl")
    )
    relationship_records = read_jsonl(
        (ROOT / "data/relationships").glob("*.jsonl")
    )
    spatial_records = read_jsonl(
        (ROOT / "data/geography/assertions").glob("*.jsonl")
    )
    entities = {record["id"]: record for record in entity_records}
    claims = {record["id"]: record for record in claim_records}
    sources = {record["id"]: record for record in source_records}
    profiles = {
        record["primary_entity_id"]: record
        for record in profile_records
        if record.get("primary_entity_id")
    }
    native_ids = experience["native_subject_ids"]
    native_id_set = set(native_ids)
    if len(native_ids) != len(native_id_set):
        raise SystemExit("Atlas experience config contains duplicate native subjects")
    missing = sorted(native_id_set - entities.keys())
    if missing:
        raise SystemExit("Atlas experience config has missing entities: " + ", ".join(missing))

    geo_by_entity: dict[str, dict[str, Any]] = {}
    for record in geographic_search:
        entity_id = record.get("carta_entity_id")
        if entity_id and entity_id not in geo_by_entity:
            geo_by_entity[entity_id] = {
                "kind": "bounds",
                "bounds": record["bounds"],
                "max_zoom": 7.4 if record["result_type"] == "wine_region" else 10.4,
                "map_feature_ids": record.get("source_feature_ids", []),
            }
    point_by_entity: dict[str, dict[str, Any]] = {}
    for feature in producer_points["features"]:
        properties = feature["properties"]
        entity_id = properties["carta_entity_id"]
        point_by_entity[entity_id] = {
            "kind": "point",
            "center": feature["geometry"]["coordinates"],
            "zoom": 11.5,
            "map_feature_ids": [feature["id"]],
        }

    type_labels = {
        "appellation": "Wine area",
        "grape": "Grape",
        "place": "Place",
        "producer": "Producer",
        "project": "Wine project",
        "wine": "Wine",
        "practice": "Cellar practice",
        "person": "Person",
    }
    claim_type_priority = {
        "identity": 0,
        "geography": 1,
        "history": 2,
        "genetics": 3,
        "viticulture": 4,
        "cellar": 5,
        "farming": 6,
        "legal": 7,
        "naming": 8,
        "other": 9,
    }

    payloads: dict[str, dict[str, Any]] = {}
    for entity_id in native_ids:
        entity = entities[entity_id]
        entity_claim_type_priority = claim_type_priority
        if entity["type"] == "producer":
            entity_claim_type_priority = {
                **claim_type_priority,
                "identity": 0,
                "history": 1,
                "farming": 2,
                "viticulture": 3,
                "cellar": 4,
                "geography": 5,
            }
        profile = profiles.get(entity_id)
        component_ids = set(profile.get("component_entity_ids", [])) if profile else {entity_id}
        component_ids.add(entity_id)
        selected_claims = [
            claim
            for claim in claim_records
            if claim["subject_ref"] in component_ids
            and claim["status"] in {"supported", "contested"}
            and claim["subject_ref"] in entities
        ]
        selected_claims.sort(
            key=lambda claim: (
                0
                if claim["subject_ref"] == entity_id
                and claim.get("atlas_presentation", {}).get("emphasis") == "lead"
                else 1,
                0 if claim["subject_ref"] == entity_id else 1,
                0 if claim.get("atlas_presentation", {}).get("order") is not None else 1,
                claim.get("atlas_presentation", {}).get("order", 999),
                entity_claim_type_priority.get(claim.get("claim_type", "other"), 20),
                claim["id"],
            )
        )
        projected_claims: list[dict[str, Any]] = []
        used_source_ids: set[str] = set()
        for claim in selected_claims[:12]:
            source_ids = [reference["source_id"] for reference in claim["source_refs"]]
            used_source_ids.update(source_ids)
            projected_claims.append(
                {
                    "claim_id": claim["id"],
                    "subject_ref": claim["subject_ref"],
                    "subject_name": entities[claim["subject_ref"]]["name"],
                    "claim_type": claim.get("claim_type", "other"),
                    "statement": claim["statement"],
                    "status": claim["status"],
                    "observed_at": claim.get("observed_at"),
                    "source_ids": source_ids,
                    "label": claim.get("atlas_presentation", {}).get("label"),
                }
            )

        connection_candidates: list[dict[str, Any]] = []
        for relationship in relationship_records:
            if relationship["status"] not in {"supported", "provisional"}:
                continue
            subject_in = relationship["subject_id"] in component_ids
            object_in = relationship["object_id"] in component_ids
            if subject_in == object_in:
                continue
            target_id = relationship["object_id"] if subject_in else relationship["subject_id"]
            if target_id not in native_id_set:
                continue
            connection_candidates.append(
                {
                    "target_id": target_id,
                    "predicate": relationship["predicate"],
                    "direction": "outbound" if subject_in else "inbound",
                    "relationship_id": relationship["id"],
                    "claim_ids": relationship.get("claim_ids", []),
                    "status": relationship["status"],
                    "basis": "relationship",
                }
            )
        if profile:
            # A profile's component list is already governed CARTA authority. Project
            # those components as native paths so regional guides expose their mapped
            # appellations without requiring a separate relationship record.
            for target_id in sorted(component_ids - {entity_id}):
                if target_id not in native_id_set:
                    continue
                component_claim_ids = [
                    claim["claim_id"]
                    for claim in projected_claims
                    if claim["subject_ref"] == target_id
                ]
                connection_candidates.append(
                    {
                        "target_id": target_id,
                        "predicate": "PROFILE_COMPONENT",
                        "direction": "outbound",
                        "relationship_id": None,
                        "claim_ids": component_claim_ids,
                        "status": "supported",
                        "basis": "profile_component",
                    }
                )
            for target_id in profile.get("representative_anchor_ids", []):
                if target_id in native_id_set and target_id not in component_ids:
                    connection_candidates.append(
                        {
                            "target_id": target_id,
                            "predicate": "EXPLORE",
                            "direction": "outbound",
                            "relationship_id": None,
                            "claim_ids": [],
                            "status": "supported",
                            "basis": "profile_anchor",
                        }
                    )
        connections_by_target: dict[str, dict[str, Any]] = {}
        for connection in sorted(
            connection_candidates,
            key=lambda item: (
                0 if item["basis"] == "relationship" else 1,
                item["target_id"],
                item["predicate"],
            ),
        ):
            connections_by_target.setdefault(connection["target_id"], connection)
        connections = []
        for target_id, connection in connections_by_target.items():
            target = entities[target_id]
            connections.append(
                {
                    **connection,
                    "target_name": target["name"],
                    "target_kind": target["type"],
                    "target_route": subject_route(target_id),
                    "has_map_target": target_id in geo_by_entity or target_id in point_by_entity,
                }
            )

        spatial = [
            record
            for record in spatial_records
            if record["entity_id"] == entity_id
            and record["status"] == "supported"
            and record["representation_kind"] != "network_anchor"
        ]
        spatial.sort(key=lambda record: (record.get("observed_at") or "", record["id"]), reverse=True)
        primary_spatial = spatial[0] if spatial else None
        if primary_spatial:
            used_source_ids.update(primary_spatial["source_ids"])
        alternate_names = [record["name"] for record in entity.get("alternate_names", [])]
        map_target = point_by_entity.get(entity_id) or geo_by_entity.get(entity_id)
        payloads[entity_id] = {
            "entity_id": entity_id,
            "name": entity["name"],
            "display_name": entity.get("display_name") or entity["name"],
            "kind": entity["type"],
            "kind_label": type_labels.get(entity["type"], entity["type"].replace("_", " ").title()),
            "route": subject_route(entity_id),
            "alternate_names": alternate_names,
            "lead_claim_id": projected_claims[0]["claim_id"] if projected_claims else None,
            "claims": projected_claims,
            "connections": connections,
            "map_target": map_target,
            "location": (
                {
                    "spatial_assertion_id": primary_spatial["id"],
                    "description": primary_spatial["description"],
                    "precision": primary_spatial.get("precision", "unknown"),
                    "anchor_entity_refs": primary_spatial.get("anchor_entity_refs", []),
                    "source_ids": primary_spatial["source_ids"],
                }
                if primary_spatial
                else None
            ),
            "sources": [
                {
                    "source_id": source_id,
                    "title": sources[source_id]["title"],
                    "publisher": sources[source_id].get("publisher"),
                    "url": sources[source_id].get("url"),
                    "source_class": sources[source_id]["source_class"],
                    "accessed_at": sources[source_id]["accessed_at"],
                }
                for source_id in sorted(used_source_ids)
            ],
        }

    return {
        "generated_from": [
            *EXPERIENCE_LINEAGE,
            "data/claims/*.jsonl",
            "data/entities/*.jsonl",
            "data/geography/assertions/*.jsonl",
            "data/geography/geometry/*.jsonl",
            "data/reference-profiles/*.jsonl",
            "data/relationships/*.jsonl",
            "data/sources/*.jsonl",
        ],
        "projection_contract": (
            "Learner statements are verbatim claim projections with claim and source IDs. "
            "Connections are supported/provisional CARTA relationships or governed profile "
            "anchors. Map targets come from rendered geography or spatial assertions."
        ),
        "subjects": {entity_id: payloads[entity_id] for entity_id in sorted(payloads)},
    }


def build_entry_points(
    experience: dict[str, Any], subjects: dict[str, Any]
) -> dict[str, Any]:
    claims = {
        record["id"]: record
        for record in read_jsonl((ROOT / "data/claims").glob("*.jsonl"))
    }
    entries = []
    for configured in experience["entry_points"]:
        subject_id = configured["subject_id"]
        if subject_id not in subjects:
            raise SystemExit(f"{configured['id']}: entry subject is not native")
        projected = []
        for claim_id in configured["claim_ids"]:
            claim = claims.get(claim_id)
            if not claim or claim["status"] != "supported":
                raise SystemExit(f"{configured['id']}: invalid supporting claim {claim_id}")
            projected.append(
                {
                    "claim_id": claim_id,
                    "statement": claim["statement"],
                    "source_ids": [item["source_id"] for item in claim["source_refs"]],
                }
            )
        entries.append(
            {
                **configured,
                "subject_name": subjects[subject_id]["display_name"],
                "subject_kind": subjects[subject_id]["kind"],
                "subject_route": subjects[subject_id]["route"],
                "supporting_claims": projected,
            }
        )
    featured_worlds = []
    for entity_id in experience["featured_world_ids"]:
        subject = subjects[entity_id]
        featured_worlds.append(
            {
                "entity_id": entity_id,
                "name": subject["display_name"],
                "route": subject["route"],
                "map_target": subject["map_target"],
            }
        )
    return {
        "generated_from": EXPERIENCE_LINEAGE,
        "release": experience.get("release"),
        "entry_points": entries,
        "featured_worlds": featured_worlds,
    }


TERM_TOKEN_RE = re.compile(r"\{\{term:([a-z0-9-]+)\|[^{}]+\}\}")


def nested_values(value: Any, key: str) -> Iterable[Any]:
    """Yield values for a named key anywhere in a JSON-like structure."""
    if isinstance(value, dict):
        for nested_key, nested_value in value.items():
            if nested_key == key:
                yield nested_value
            yield from nested_values(nested_value, key)
    elif isinstance(value, list):
        for item in value:
            yield from nested_values(item, key)


def nested_strings(value: Any) -> Iterable[str]:
    if isinstance(value, str):
        yield value
    elif isinstance(value, dict):
        for nested_value in value.values():
            yield from nested_strings(nested_value)
    elif isinstance(value, list):
        for item in value:
            yield from nested_strings(item)


def build_atlas_editorial(
    experience: dict[str, Any], subjects: dict[str, Any]
) -> dict[str, Any]:
    """Validate and project the current teaching and interaction layer.

    Authored copy remains explicitly editorial. Every factual teaching device names
    governed claims, while every action target resolves to a native subject.
    """
    editorial = experience.get("editorial")
    if not editorial:
        raise SystemExit("Atlas experience config is missing its editorial layer")
    claims = {
        record["id"]: record
        for record in read_jsonl((ROOT / "data/claims").glob("*.jsonl"))
    }
    sources = {
        record["id"]: record
        for record in read_jsonl((ROOT / "data/sources").glob("*.jsonl"))
    }
    native_ids = set(subjects)
    legend_ids = [item["id"] for item in editorial.get("legend", [])]
    visible_signals = {"iykyk", "same-energy"}
    if len(legend_ids) != len(set(legend_ids)) or set(legend_ids) != visible_signals:
        raise SystemExit("Atlas legend must contain only the two useful visible signals")
    route_signals = {"rabbit-hole", "tell", "iykyk", "same-energy"}

    configured_subjects = editorial.get("subjects", {})
    missing_subjects = sorted(set(configured_subjects) - native_ids)
    if missing_subjects:
        raise SystemExit(
            "Atlas editorial subjects are not native: " + ", ".join(missing_subjects)
        )

    claim_ids: set[str] = set()
    for value in nested_values(editorial, "claim_ids"):
        if not isinstance(value, list) or not value:
            raise SystemExit("Atlas claim_ids fields must be non-empty arrays")
        claim_ids.update(value)
    for claim_id in sorted(claim_ids):
        claim = claims.get(claim_id)
        if not claim or claim["status"] not in {"supported", "contested"}:
            raise SystemExit(f"Atlas editorial claim is not usable: {claim_id}")

    glossary = editorial.get("glossary", {})
    for copy in nested_strings(editorial):
        for term_id in TERM_TOKEN_RE.findall(copy):
            if term_id not in glossary:
                raise SystemExit(f"Atlas copy references unknown term: {term_id}")
    for term_id, term in glossary.items():
        if not term.get("definition") or not term.get("matters"):
            raise SystemExit(f"Atlas glossary entry is incomplete: {term_id}")
        target_id = term.get("explore_target_id")
        if target_id and target_id not in native_ids:
            raise SystemExit(f"Atlas glossary target is not native: {target_id}")

    # Every regional world states its own argument. No world may inherit another
    # world's voice as an application default, so the pillar grammar, the Place
    # story and the rule groups are required of each world here rather than
    # filled in downstream.
    required_pillars = {"place", "grapes", "people", "culture", "rules"}
    for subject_id, configured in configured_subjects.items():
        if not configured.get("regional_world"):
            continue
        pillar_copy = configured.get("pillar_copy", {})
        if set(pillar_copy) != required_pillars:
            raise SystemExit(f"{subject_id}: regional world needs copy for every pillar")
        for pillar, pillar_text in pillar_copy.items():
            if not pillar_text.get("intro") or not pillar_text.get("lede"):
                raise SystemExit(f"{subject_id}: {pillar} pillar copy is incomplete")
        place_story = configured.get("place_story", {})
        if not all(place_story.get(key) for key in ("kicker", "title", "text", "button")):
            raise SystemExit(f"{subject_id}: regional world needs its own Place story")
        rule_groups = configured.get("rules", {}).get("groups")
        if not configured.get("rules", {}).get("intro") or not rule_groups:
            raise SystemExit(f"{subject_id}: regional world needs its own rule grammar")
        for group in rule_groups:
            if not group.get("label") or not group.get("note") or not group.get("ids"):
                raise SystemExit(f"{subject_id}: rule group is incomplete")
            for area_id in group["ids"]:
                if area_id not in native_ids:
                    raise SystemExit(f"{subject_id}: dead rule-group area {area_id}")

    for subject_id, configured in configured_subjects.items():
        direct_targets = {
            connection["target_id"] for connection in subjects[subject_id]["connections"]
        }
        featured = configured.get("featured_connections", [])
        if len(featured) > 3:
            raise SystemExit(f"{subject_id}: Keep wandering supports at most three routes")
        for connection in featured:
            target_id = connection.get("target_id")
            if target_id not in native_ids:
                raise SystemExit(f"{subject_id}: dead featured target {target_id}")
            if not connection.get("reason") or not connection.get("claim_ids"):
                raise SystemExit(f"{subject_id}: featured route lacks reason or evidence")
            signal = connection.get("signal")
            if signal not in route_signals:
                raise SystemExit(f"{subject_id}: unknown signal {signal}")
            # Same Energy is an explicitly sourced editorial comparison rather than
            # a false Reference relationship. All other recommendations must be
            # direct graph/profile projections.
            if target_id not in direct_targets and signal != "same-energy":
                raise SystemExit(
                    f"{subject_id}: featured target is not graph-derived: {target_id}"
                )
        for target_id in nested_values(configured, "target_id"):
            if target_id not in native_ids:
                raise SystemExit(f"{subject_id}: dead editorial target {target_id}")
        reactions = [configured.get("map_reaction", {})]
        reactions.extend(configured.get("pillar_map_reactions", {}).values())
        for reaction in reactions:
            for area_id in reaction.get("area_subject_ids", []):
                area = subjects.get(area_id)
                if not area or area["kind"] != "appellation" or not area.get("map_target"):
                    raise SystemExit(f"{subject_id}: invalid active map area {area_id}")
            for producer_id in reaction.get("producer_ids", []):
                producer = subjects.get(producer_id)
                if not producer or producer["kind"] != "producer" or not producer.get("map_target"):
                    raise SystemExit(f"{subject_id}: invalid active map producer {producer_id}")

    claim_support = {}
    for claim_id in sorted(claim_ids):
        claim = claims[claim_id]
        source_ids = [reference["source_id"] for reference in claim["source_refs"]]
        claim_support[claim_id] = {
            "statement": claim["statement"],
            "status": claim["status"],
            "subject_ref": claim["subject_ref"],
            "source_ids": source_ids,
            "sources": [
                {
                    "source_id": source_id,
                    "title": sources[source_id]["title"],
                    "publisher": sources[source_id].get("publisher"),
                    "url": sources[source_id].get("url"),
                }
                for source_id in source_ids
            ],
        }
    return {
        "generated_from": EXPERIENCE_LINEAGE,
        "release": experience.get("release"),
        "projection_contract": (
            "Authored teaching copy is editorial, not Reference authority. Every factual "
            "definition, lens, affinity, signal, and recommendation carries "
            "governed claim IDs; every action resolves to a native subject."
        ),
        "legend": editorial["legend"],
        "glossary": editorial["glossary"],
        "map_click_priority": editorial.get("map_click_priority", {}),
        "context_returns": editorial.get("context_returns", []),
        "subjects": {key: configured_subjects[key] for key in sorted(configured_subjects)},
        "claim_support": claim_support,
    }


def extend_search_index(
    geographic_search: list[dict[str, Any]], subjects: dict[str, Any]
) -> list[dict[str, Any]]:
    """Attach native routes to geography and add conceptual native subjects."""
    results: list[dict[str, Any]] = []
    represented_entities: set[str] = set()
    for raw in geographic_search:
        record = dict(raw)
        entity_id = record.get("carta_entity_id")
        subject = subjects.get(entity_id)
        if subject:
            record["native_route"] = subject["route"]
            record["subject_kind"] = subject["kind"]
            record["experience_level"] = "native_guide"
            represented_entities.add(entity_id)
        else:
            record["experience_level"] = "map_coverage"
        results.append(record)
    for entity_id, subject in subjects.items():
        if entity_id in represented_entities:
            continue
        map_target = subject.get("map_target")
        context_names = [
            connection["target_name"]
            for connection in subject["connections"]
            if connection["target_kind"] in {"place", "appellation"}
        ][:2]
        record = {
            "id": f"carta-subject-{entity_id.replace(':', '-')}",
            "name": subject["display_name"],
            "result_type": "native_subject",
            "subject_kind": subject["kind"],
            "context_label": " · ".join(context_names),
            "carta_entity_id": entity_id,
            "native_route": subject["route"],
            "experience_level": "native_guide",
            "governance_status": "governed",
            "bounds": map_target.get("bounds") if map_target and map_target["kind"] == "bounds" else None,
        }
        results.append(record)
    results.sort(
        key=lambda result: (
            0 if result["experience_level"] == "native_guide" else 1,
            result["name"].casefold(),
            result["id"],
        )
    )
    return results


def build_geometry_metadata(
    features_by_entity: dict[str, list[dict[str, Any]]]
) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for entity_id, features in sorted(features_by_entity.items()):
        if len(features) != 1:
            raise SystemExit(
                f"accepted mapping for {entity_id} resolves to {len(features)} source features"
            )
        feature = features[0]
        source_feature_id = feature["properties"]["source_feature_id"]
        records.append(
            {
                "id": f"geom:inao-denom-{feature['properties']['source_denomination_id']}",
                "entity_id": entity_id,
                "geometry_ref": (
                    "atlas-app/public/data/france-appellations-aoc.geojson"
                    f"#source_feature_id={source_feature_id}"
                ),
                "geometry_type": feature["geometry"]["type"],
                "source_ids": ["source:inao-aires-geographiques-siqo-2026-08-24"],
                "confidence": "high",
                "precision": "official_boundary",
                "observed_at": "2026-08-24",
                "notes": (
                    "INAO cartographic representation of the regulatory geographical area, "
                    "reprojected and topology-preserving simplified for browser delivery. "
                    "The legal cahier des charges and commune list remain authoritative."
                ),
            }
        )
    return records


def artifact_metadata(
    path: Path,
    role: str,
    *,
    feature_count: int | None = None,
    record_count: int | None = None,
) -> dict[str, Any]:
    relative = path.relative_to(ROOT).as_posix()
    value: dict[str, Any] = {
        "path": relative,
        "format": "GeoJSON" if path.suffix == ".geojson" else "JSONL" if path.suffix == ".jsonl" else "JSON",
        "sha256": sha256_path(path),
        "bytes": path.stat().st_size,
        "role": role,
    }
    if feature_count is not None:
        value["feature_count"] = feature_count
    if record_count is not None:
        value["record_count"] = record_count
    limit = ARTIFACT_LIMITS.get(relative)
    if limit and value["bytes"] > limit:
        raise SystemExit(
            f"{relative}: {value['bytes']} bytes exceeds Run 01 limit {limit}"
        )
    return value


def update_manifest(path: Path, artifacts: list[dict[str, Any]]) -> dict[str, Any]:
    manifest = read_json(path)
    manifest["derived_artifacts"] = sorted(artifacts, key=lambda item: item["path"])
    write_json_pretty(path, manifest)
    return manifest


PROVENANCE_OPTIONAL_FIELDS = (
    "product_class",
    "derived_from",
    "measurement",
    "geographic_extent",
    "refresh_policy",
)


def provenance_dataset(manifest: dict[str, Any]) -> dict[str, Any]:
    record = {
        "id": manifest["id"],
        "dataset_title": manifest["dataset_title"],
        "publisher": manifest["publisher"],
        "dataset_url": manifest["dataset_url"],
        "resource_url": manifest["resource_url"],
        "source_release_date": manifest["source_release_date"],
        "retrieved_at": manifest["retrieved_at"],
        "geographic_meaning": manifest["geographic_meaning"],
        "authority_class": manifest["authority_class"],
        "license": manifest["license"],
        "transformations": manifest["transformations"],
        "derived_artifacts": manifest["derived_artifacts"],
    }
    for field in PROVENANCE_OPTIONAL_FIELDS:
        if field in manifest:
            record[field] = manifest[field]
    return record


def build_provenance(manifests: list[dict[str, Any]], statistics: dict[str, Any]) -> dict[str, Any]:
    """Project every registered spatial dataset manifest, not a hardcoded subset.

    Reading the manifest directory keeps `build_atlas.py` and `build_terrain.py`
    producing the same provenance document, so adding an environmental dataset
    never requires a second provenance surface beside this one.
    """
    return {
        "generated_from": "data/geography/datasets/",
        "datasets": [
            provenance_dataset(manifest)
            for manifest in sorted(manifests, key=lambda item: item["id"])
        ],
        "inao_reconciliation": statistics,
        "semantic_distinctions": [
            "Wine-region labels are derived CARTA orientation points, not statutory polygons.",
            "INAO areas are cartographic representations of regulatory geographical areas, not parcel eligibility or actual vineyard land.",
            "Eligible communes, approved viticultural parcels, actual vineyard land, cadastral parcels, and lieux-dits remain distinct concepts.",
            "External sourced geography may be displayed without becoming a native CARTA guide or subject.",
            "Terrain is context before it is interpretation: relief, slope or elevation shown on the map never authorises a claim about grape growing, ripening, drainage, climate or wine quality."
        ]
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--cache-dir",
        type=Path,
        default=ROOT / ".cache/atlas",
        help="Download/extraction cache; raw archives are never committed.",
    )
    parser.add_argument(
        "--source-archive",
        action="append",
        default=[],
        metavar="DATASET_ID=PATH",
        help="Use an already-downloaded ZIP for a pinned dataset.",
    )
    args = parser.parse_args()

    require_geospatial()
    manifests = load_manifests()
    supplied = parse_source_archives(args.source_archive)
    cache_dir = args.cache_dir.resolve()
    cache_dir.mkdir(parents=True, exist_ok=True)

    profile_paths = entity_profile_paths()
    inao_manifest = manifests[INAO_DATASET_ID]
    natural_manifest = manifests[NATURAL_EARTH_DATASET_ID]

    inao_archive = acquire_archive(inao_manifest, cache_dir, supplied)
    natural_archive = acquire_archive(natural_manifest, cache_dir, supplied)
    inao_shape = only_shapefile(
        extract_archive(inao_archive, INAO_DATASET_ID, cache_dir)
    )
    natural_shape = only_shapefile(
        extract_archive(natural_archive, NATURAL_EARTH_DATASET_ID, cache_dir)
    )

    world, world_stats = build_world_countries(
        natural_shape, natural_manifest, profile_paths
    )
    groups, inao_stats, linkage = build_inao_features(
        inao_shape, inao_manifest, profile_paths
    )
    region_labels = build_region_labels(linkage["geometry_by_entity"])
    geographic_search = build_search_index(groups, region_labels)
    geometry_records = build_geometry_metadata(linkage["features_by_entity"])
    atlas_guides = build_atlas_guides(profile_paths)
    experience = load_experience_config()
    producer_points = build_producer_points(experience)
    atlas_subjects = build_atlas_subjects(
        experience, geographic_search, producer_points
    )
    entry_points = build_entry_points(experience, atlas_subjects["subjects"])
    editorial = build_atlas_editorial(experience, atlas_subjects["subjects"])
    search_index = extend_search_index(geographic_search, atlas_subjects["subjects"])

    world_path = PUBLIC_DATA_DIR / "world-countries.geojson"
    aoc_path = PUBLIC_DATA_DIR / "france-appellations-aoc.geojson"
    igp_path = PUBLIC_DATA_DIR / "france-appellations-igp.geojson"
    region_path = PUBLIC_DATA_DIR / "france-wine-regions.geojson"
    search_path = PUBLIC_DATA_DIR / "search-index.json"
    guide_path = PUBLIC_DATA_DIR / "atlas-guides.json"
    subject_path = PUBLIC_DATA_DIR / "atlas-subjects.json"
    entry_path = PUBLIC_DATA_DIR / "atlas-entry-points.json"
    editorial_path = PUBLIC_DATA_DIR / "atlas-editorial.json"
    producer_path = PUBLIC_DATA_DIR / "atlas-producers.geojson"

    write_json(world_path, world)
    write_json(aoc_path, {"type": "FeatureCollection", "features": groups["AOC"]})
    write_json(igp_path, {"type": "FeatureCollection", "features": groups["IGP"]})
    write_json(region_path, region_labels)
    write_json(search_path, search_index)
    write_json(guide_path, atlas_guides)
    write_json(subject_path, atlas_subjects)
    write_json(entry_path, entry_points)
    write_json(editorial_path, editorial)
    write_json(producer_path, producer_points)
    write_jsonl(GEOMETRY_METADATA_PATH, geometry_records)

    natural_artifacts = [
        artifact_metadata(
            world_path,
            "Generalized world country interaction layer",
            feature_count=len(world["features"]),
        )
    ]
    inao_artifacts = [
        artifact_metadata(
            aoc_path,
            "Default AOC/AOP regulatory geographical-area layer",
            feature_count=len(groups["AOC"]),
        ),
        artifact_metadata(
            igp_path,
            "Optional IGP regulatory geographical-area layer",
            feature_count=len(groups["IGP"]),
        ),
        artifact_metadata(
            region_path,
            "Derived governed CARTA wine-region label anchors and camera bounds",
            feature_count=len(region_labels["features"]),
        ),
        artifact_metadata(
            search_path,
            "Search records derived from rendered INAO features and governed region labels",
            record_count=len(search_index),
        ),
        artifact_metadata(
            GEOMETRY_METADATA_PATH,
            "CARTA geometry metadata for accepted INAO-to-CARTA mappings",
            record_count=len(geometry_records),
        ),
    ]

    updated_natural = update_manifest(
        MANIFEST_DIR / "natural-earth-admin-0-countries-5.1.1.json",
        natural_artifacts,
    )
    updated_inao = update_manifest(
        MANIFEST_DIR / "inao-aires-geographiques-siqo-2026-08-24.json",
        inao_artifacts,
    )
    # Re-read every manifest so registered environmental datasets (terrain and
    # anything that follows it) stay in provenance without a second code path.
    all_manifests = [read_json(path) for path in sorted(MANIFEST_DIR.glob("*.json"))]
    by_id = {manifest["id"]: manifest for manifest in all_manifests}
    by_id[updated_inao["id"]] = updated_inao
    by_id[updated_natural["id"]] = updated_natural
    write_json(
        PUBLIC_DATA_DIR / "provenance.json",
        build_provenance(list(by_id.values()), inao_stats),
    )

    print(
        "PASS "
        + ", ".join(
            [
                f"countries={len(world['features'])}",
                f"aoc={len(groups['AOC'])}",
                f"igp={len(groups['IGP'])}",
                f"regions={len(region_labels['features'])}",
                f"mapped={inao_stats['mapped_features']}",
                f"unmapped={inao_stats['unmapped_features']}",
                f"search={len(search_index)}",
                f"guides={len(atlas_guides['guides'])}",
                f"subjects={len(atlas_subjects['subjects'])}",
                f"editorial_subjects={len(editorial['subjects'])}",
                f"producer_points={len(producer_points['features'])}",
                f"world_source={world_stats['source_features']}",
            ]
        )
    )


if __name__ == "__main__":
    main()
