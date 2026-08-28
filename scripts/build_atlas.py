#!/usr/bin/env python3
"""Build deterministic, browser-sized CARTA Atlas geography from pinned sources."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import sys
import urllib.request
import zipfile
from collections import defaultdict
from pathlib import Path
from typing import Any, Iterable

try:
    import geopandas as gpd
    import pandas as pd
    from shapely import make_valid, union_all
    from shapely.geometry import GeometryCollection, MultiPolygon, Polygon, mapping, shape
except ImportError as exc:  # pragma: no cover - exercised by clean validation environments
    raise SystemExit(
        "Install Atlas build dependencies: python -m pip install -r requirements-atlas.txt"
    ) from exc


ROOT = Path(__file__).resolve().parents[1]
MANIFEST_DIR = ROOT / "data/geography/datasets"
MAPPING_DIR = ROOT / "data/geography/external-id-mappings"
PUBLIC_DATA_DIR = ROOT / "atlas-app/public/data"
GEOMETRY_METADATA_PATH = ROOT / "data/geography/geometry/atlas-france-inao.jsonl"

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


def build_provenance(manifests: list[dict[str, Any]], statistics: dict[str, Any]) -> dict[str, Any]:
    return {
        "generated_from": "data/geography/datasets/",
        "datasets": [
            {
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
            for manifest in sorted(manifests, key=lambda item: item["id"])
        ],
        "inao_reconciliation": statistics,
        "semantic_distinctions": [
            "Wine-region labels are derived CARTA orientation points, not statutory polygons.",
            "INAO areas are cartographic representations of regulatory geographical areas, not parcel eligibility or actual vineyard land.",
            "Eligible communes, approved viticultural parcels, actual vineyard land, cadastral parcels, and lieux-dits remain distinct concepts.",
            "External sourced geography may be displayed without being promoted into governed CARTA identity."
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
    search_index = build_search_index(groups, region_labels)
    geometry_records = build_geometry_metadata(linkage["features_by_entity"])

    world_path = PUBLIC_DATA_DIR / "world-countries.geojson"
    aoc_path = PUBLIC_DATA_DIR / "france-appellations-aoc.geojson"
    igp_path = PUBLIC_DATA_DIR / "france-appellations-igp.geojson"
    region_path = PUBLIC_DATA_DIR / "france-wine-regions.geojson"
    search_path = PUBLIC_DATA_DIR / "search-index.json"

    write_json(world_path, world)
    write_json(aoc_path, {"type": "FeatureCollection", "features": groups["AOC"]})
    write_json(igp_path, {"type": "FeatureCollection", "features": groups["IGP"]})
    write_json(region_path, region_labels)
    write_json(search_path, search_index)
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
    updated_openfreemap = read_json(
        MANIFEST_DIR / "openfreemap-liberty-runtime.json"
    )
    write_json(
        PUBLIC_DATA_DIR / "provenance.json",
        build_provenance(
            [updated_inao, updated_natural, updated_openfreemap], inao_stats
        ),
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
                f"world_source={world_stats['source_features']}",
            ]
        )
    )


if __name__ == "__main__":
    main()
