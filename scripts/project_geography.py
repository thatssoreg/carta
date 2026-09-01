#!/usr/bin/env python3
"""Re-project CARTA Atlas geography from committed artifacts when the pinned
source archives cannot be re-acquired.

`scripts/build_atlas.py` remains the canonical entry point: it re-derives every
rendered feature from the pinned INAO and Natural Earth archives. This driver
exists for the narrower case in which those archives are unreachable — an
egress policy that does not allow the pinned hosts, or an offline run — while
governed authority has changed in ways that only touch the *mapping-derived*
half of the projection: which rendered features carry a CARTA identity, which
Human Reference page they resolve to, and everything downstream of that.

It follows the precedent set by `scripts/project_editorial.py`: recover the
geographic half from the committed artifact instead of re-downloading, then
reuse `build_atlas` so every build-time contract still applies. Where
`project_editorial.py` refuses as soon as the subject projection changes, this
driver accepts subject and geometry-metadata changes but refuses as soon as
anything that is *not* derived from the external-ID mapping table would change,
because that means the pinned source is genuinely in play and only
`scripts/build_atlas.py` can answer for it.

Nothing here invents geometry. Coordinates are carried through byte-identically
from the committed layers.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import build_atlas as builder

ROOT = Path(__file__).resolve().parents[1]
PUBLIC_DATA_DIR = ROOT / "atlas-app/public/data"

# The three feature properties that `build_inao_features` derives from the
# accepted external-ID mapping table and governed profile paths. Everything
# else on a rendered feature comes from the pinned source archive.
MAPPING_DERIVED_PROPERTIES = (
    "carta_entity_id",
    "human_reference_path",
    "governance_status",
)

LAYER_FILES = {
    "AOC": "france-appellations-aoc.geojson",
    "IGP": "france-appellations-igp.geojson",
}


def feature_sort_key(feature: dict[str, Any]) -> tuple[str, str, str]:
    properties = feature["properties"]
    return (
        properties["name"].casefold(),
        properties["source_denomination_id"],
        feature["id"],
    )


def recover_groups() -> dict[str, list[dict[str, Any]]]:
    """Read the committed rendered layers back as `build_inao_features` groups."""
    groups: dict[str, list[dict[str, Any]]] = {}
    for sign, filename in LAYER_FILES.items():
        collection = builder.read_json(PUBLIC_DATA_DIR / filename)
        features = collection["features"]
        if [feature_sort_key(feature) for feature in features] != sorted(
            feature_sort_key(feature) for feature in features
        ):
            raise SystemExit(
                f"{filename}: committed feature order is not the build order; "
                "rebuild with scripts/build_atlas.py"
            )
        for feature in features:
            if feature["properties"]["designation"] != sign:
                raise SystemExit(f"{filename}: unexpected designation in layer")
        groups[sign] = features
    return groups


def reapply_mapping(groups: dict[str, list[dict[str, Any]]]) -> dict[str, Any]:
    """Re-derive the mapping half of each feature exactly as the build does."""
    mappings = builder.load_mappings(builder.INAO_DATASET_ID)
    profile_paths = builder.entity_profile_paths()
    source_geometry_by_entity: dict[str, list[Any]] = {}
    source_feature_by_entity: dict[str, list[dict[str, Any]]] = {}
    changed = 0
    denomination_id_counts: dict[str, int] = {}
    for features in groups.values():
        for feature in features:
            denomination_id = feature["properties"]["source_denomination_id"]
            denomination_id_counts[denomination_id] = (
                denomination_id_counts.get(denomination_id, 0) + 1
            )

    for features in groups.values():
        for feature in features:
            properties = feature["properties"]
            mapping_record = mappings.get(properties["source_denomination_id"])
            if (
                mapping_record
                and denomination_id_counts[properties["source_denomination_id"]] > 1
                and builder.normalized_source_name(properties["name"])
                != builder.normalized_source_name(mapping_record["source_name"])
            ):
                # Match the canonical builder's handling of an INAO ID reused
                # by a base appellation and named geographical complements.
                mapping_record = None
            carta_entity_id = (
                mapping_record["carta_entity_id"] if mapping_record else None
            )
            projected = {
                "carta_entity_id": carta_entity_id,
                "human_reference_path": profile_paths.get(carta_entity_id),
                "governance_status": "governed" if carta_entity_id else "external_only",
            }
            for key, value in projected.items():
                if properties[key] != value:
                    changed += 1
                properties[key] = value
            if carta_entity_id:
                geometry = builder.polygonal_geometry(
                    builder.shape(feature["geometry"])
                )
                source_geometry_by_entity.setdefault(carta_entity_id, []).append(geometry)
                source_feature_by_entity.setdefault(carta_entity_id, []).append(feature)

    mapped_source_ids = {
        feature["properties"]["source_denomination_id"]
        for features in groups.values()
        for feature in features
        if feature["properties"]["carta_entity_id"]
    }
    missing_mappings = sorted(set(mappings) - mapped_source_ids)
    if missing_mappings:
        raise SystemExit(
            "accepted INAO mappings not present in the committed layers: "
            + ", ".join(missing_mappings)
        )
    return {
        "geometry_by_entity": source_geometry_by_entity,
        "features_by_entity": source_feature_by_entity,
        "changed_properties": changed,
    }


def recover_statistics(groups: dict[str, list[dict[str, Any]]], linkage: dict[str, Any]) -> dict[str, Any]:
    """Recompute the reconciliation counters the committed layers can answer for.

    Two counters describe the *pre-filter* source archive rather than the
    rendered layers, so they are carried forward from the committed provenance
    document instead of being invented here.
    """
    committed = builder.read_json(PUBLIC_DATA_DIR / "provenance.json")
    previous = committed["inao_reconciliation"]
    repaired = sum(
        1
        for features in groups.values()
        for feature in features
        if feature["properties"]["geometry_status"] == "repaired_and_simplified_for_web"
    )
    if repaired != previous["repaired_features"]:
        raise SystemExit(
            "committed layers disagree with recorded repair count; "
            "rebuild with scripts/build_atlas.py"
        )
    mapped_features = sum(
        len(features) for features in linkage["features_by_entity"].values()
    )
    wine_features = sum(len(features) for features in groups.values())
    return {
        "source_features": previous["source_features"],
        "wine_features": wine_features,
        "aoc_features": len(groups["AOC"]),
        "igp_features": len(groups["IGP"]),
        "mapped_features": mapped_features,
        "mapped_entities": len(linkage["features_by_entity"]),
        "unmapped_features": wine_features - mapped_features,
        "ambiguous_mappings": 0,
        "source_invalid_features": previous["source_invalid_features"],
        "repaired_features": repaired,
    }


def main() -> None:
    groups = recover_groups()
    linkage = reapply_mapping(groups)
    statistics = recover_statistics(groups, linkage)

    region_labels = builder.build_region_labels(linkage["geometry_by_entity"])
    geographic_search = builder.build_search_index(groups, region_labels)
    geometry_records = builder.build_geometry_metadata(linkage["features_by_entity"])
    atlas_guides = builder.build_atlas_guides(builder.entity_profile_paths())
    experience = builder.load_experience_config()
    producer_points = builder.build_producer_points(experience)
    atlas_subjects = builder.build_atlas_subjects(
        experience, geographic_search, producer_points
    )
    entry_points = builder.build_entry_points(experience, atlas_subjects["subjects"])
    editorial = builder.build_atlas_editorial(experience, atlas_subjects["subjects"])
    search_index = builder.extend_search_index(geographic_search, atlas_subjects["subjects"])

    world_path = PUBLIC_DATA_DIR / "world-countries.geojson"
    aoc_path = PUBLIC_DATA_DIR / LAYER_FILES["AOC"]
    igp_path = PUBLIC_DATA_DIR / LAYER_FILES["IGP"]
    region_path = PUBLIC_DATA_DIR / "france-wine-regions.geojson"
    search_path = PUBLIC_DATA_DIR / "search-index.json"
    guide_path = PUBLIC_DATA_DIR / "atlas-guides.json"
    subject_path = PUBLIC_DATA_DIR / "atlas-subjects.json"
    entry_path = PUBLIC_DATA_DIR / "atlas-entry-points.json"
    editorial_path = PUBLIC_DATA_DIR / "atlas-editorial.json"
    producer_path = PUBLIC_DATA_DIR / "atlas-producers.geojson"

    builder.write_json(aoc_path, {"type": "FeatureCollection", "features": groups["AOC"]})
    builder.write_json(igp_path, {"type": "FeatureCollection", "features": groups["IGP"]})
    builder.write_json(region_path, region_labels)
    builder.write_json(search_path, search_index)
    builder.write_json(guide_path, atlas_guides)
    builder.write_json(subject_path, atlas_subjects)
    builder.write_json(entry_path, entry_points)
    builder.write_json(editorial_path, editorial)
    builder.write_json(producer_path, producer_points)
    builder.write_jsonl(builder.GEOMETRY_METADATA_PATH, geometry_records)

    world = builder.read_json(world_path)
    natural_artifacts = [
        builder.artifact_metadata(
            world_path,
            "Generalized world country interaction layer",
            feature_count=len(world["features"]),
        )
    ]
    inao_artifacts = [
        builder.artifact_metadata(
            aoc_path,
            "Default AOC/AOP regulatory geographical-area layer",
            feature_count=len(groups["AOC"]),
        ),
        builder.artifact_metadata(
            igp_path,
            "Optional IGP regulatory geographical-area layer",
            feature_count=len(groups["IGP"]),
        ),
        builder.artifact_metadata(
            region_path,
            "Derived governed CARTA wine-region label anchors and camera bounds",
            feature_count=len(region_labels["features"]),
        ),
        builder.artifact_metadata(
            search_path,
            "Search records derived from rendered INAO features and governed region labels",
            record_count=len(search_index),
        ),
        builder.artifact_metadata(
            builder.GEOMETRY_METADATA_PATH,
            "CARTA geometry metadata for accepted INAO-to-CARTA mappings",
            record_count=len(geometry_records),
        ),
    ]

    updated_natural = builder.update_manifest(
        builder.MANIFEST_DIR / "natural-earth-admin-0-countries-5.1.1.json",
        natural_artifacts,
    )
    updated_inao = builder.update_manifest(
        builder.MANIFEST_DIR / "inao-aires-geographiques-siqo-2026-08-24.json",
        inao_artifacts,
    )
    all_manifests = [
        builder.read_json(path) for path in sorted(builder.MANIFEST_DIR.glob("*.json"))
    ]
    by_id = {manifest["id"]: manifest for manifest in all_manifests}
    by_id[updated_inao["id"]] = updated_inao
    by_id[updated_natural["id"]] = updated_natural
    builder.write_json(
        PUBLIC_DATA_DIR / "provenance.json",
        builder.build_provenance(list(by_id.values()), statistics),
    )

    print(
        "PASS "
        + ", ".join(
            [
                "source=committed-layers",
                f"aoc={len(groups['AOC'])}",
                f"igp={len(groups['IGP'])}",
                f"regions={len(region_labels['features'])}",
                f"mapped={statistics['mapped_features']}",
                f"unmapped={statistics['unmapped_features']}",
                f"mapping_properties_rewritten={linkage['changed_properties']}",
                f"search={len(search_index)}",
                f"guides={len(atlas_guides['guides'])}",
                f"subjects={len(atlas_subjects['subjects'])}",
                f"editorial_subjects={len(editorial['subjects'])}",
                f"producer_points={len(producer_points['features'])}",
            ]
        )
    )


if __name__ == "__main__":
    main()
