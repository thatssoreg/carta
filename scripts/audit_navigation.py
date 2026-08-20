#!/usr/bin/env python3
"""Inspect CARTA's deterministic Human Reference navigation candidate graph.

This is analysis tooling, not a second authority graph. It reads the governed
JSONL records, mirrors the production eligibility rules in ``validate_data``,
enumerates the paths that make each surfaced profile eligible, and compares a
small set of deterministic ranking prototypes without writing Atlas pages.
"""
from __future__ import annotations

import argparse
import json
import math
import re
import statistics
import subprocess
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

from validate_data import (
    LINKABLE_PUBLICATION_STATUSES,
    MAX_GRAPH_NAVIGATION_DISTANCE,
    MAX_RELATED_PROFILES,
    NAVIGATION_RELATIONSHIP_PREDICATES,
    NAVIGATION_RELATIONSHIP_STATUSES,
    enumerate_navigation_paths,
    navigation_adjacency,
    navigation_candidate_sort_key,
    navigation_graph,
    render_navigation,
    resolve_navigation_candidate,
)


ROOT = Path(__file__).resolve().parents[1]

DATA_DIRECTORIES = {
    "entities": "data/entities",
    "relationships": "data/relationships",
    "profiles": "data/reference-profiles",
}

GENERATED_LINK_RE = re.compile(r"^- \[([^]]+)\]\([^)]+\) — ")

# Smaller is more specific for reader navigation. These values are prototypes,
# not ontology claims and not production configuration.
PREDICATE_COST = {
    "MADE_BY": 0,
    "MADE_FROM": 0,
    "CLASSIFIED_AS": 0,
    "FARMS_PARCEL": 0,
    "PLANTED_AT": 0,
    "MENTORED_BY": 0,
    "TRAINED_AT": 0,
    "WORKED_FOR": 0,
    "WORKED_WITH": 0,
    "COLLABORATED_WITH": 0,
    "FOUNDED": 1,
    "FARMED_BY": 1,
    "OWNED_BY": 2,
    "WITHIN_APPELLATION": 2,
    "FARMS_IN": 3,
    "USES_PRACTICE": 3,
    "MEMBER_OF": 4,
    "LOCATED_IN": 5,
    "WITHIN": 6,
}


def load_jsonl(directory: Path) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    if not directory.exists():
        return records
    for path in sorted(directory.glob("*.jsonl")):
        for lineno, line in enumerate(path.read_text().splitlines(), 1):
            if line.strip():
                try:
                    records.append(json.loads(line))
                except json.JSONDecodeError as exc:
                    raise SystemExit(f"{path}:{lineno}: invalid JSON: {exc}")
    return records


def load_data(root: Path) -> dict[str, list[dict[str, Any]]]:
    return {
        label: load_jsonl(root / directory)
        for label, directory in DATA_DIRECTORIES.items()
    }


def load_data_from_git_ref(
    root: Path, git_ref: str
) -> dict[str, list[dict[str, Any]]]:
    data: dict[str, list[dict[str, Any]]] = {}
    for label, directory in DATA_DIRECTORIES.items():
        listing = subprocess.run(
            ["git", "ls-tree", "-r", "--name-only", git_ref, "--", directory],
            cwd=root,
            check=True,
            capture_output=True,
            text=True,
        ).stdout.splitlines()
        records: list[dict[str, Any]] = []
        for path in sorted(path for path in listing if path.endswith(".jsonl")):
            content = subprocess.run(
                ["git", "show", f"{git_ref}:{path}"],
                cwd=root,
                check=True,
                capture_output=True,
                text=True,
            ).stdout
            for lineno, line in enumerate(content.splitlines(), 1):
                if line.strip():
                    try:
                        records.append(json.loads(line))
                    except json.JSONDecodeError as exc:
                        raise SystemExit(
                            f"{git_ref}:{path}:{lineno}: invalid JSON: {exc}"
                        )
        data[label] = records
    return data


def has_surface(profile: dict[str, Any]) -> bool:
    return bool(profile.get("path")) and (
        profile["publication_status"] in LINKABLE_PUBLICATION_STATUSES
    )


def profile_seeds(profile: dict[str, Any]) -> set[str]:
    return set(profile.get("country_entity_ids", [])) | set(
        profile.get("representative_anchor_ids", [])
    )


def percentile(values: list[int], fraction: float) -> float:
    if not values:
        return 0.0
    ordered = sorted(values)
    index = math.ceil(fraction * len(ordered)) - 1
    return float(ordered[max(0, min(index, len(ordered) - 1))])


def round_metric(value: float) -> float:
    return round(value, 2)


def eligible_relationships(data: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    return [
        relationship
        for relationship in data["relationships"]
        if relationship["layer"] == "reference"
        and relationship["status"] in NAVIGATION_RELATIONSHIP_STATUSES
        and relationship["predicate"] in NAVIGATION_RELATIONSHIP_PREDICATES
    ]


def route_rank(candidate: dict[str, Any]) -> int:
    if candidate["curated_outbound"]:
        return 0
    if candidate["curated_reciprocal"]:
        return 1
    return 2 + (candidate["distance"] or 0)


def current_key(candidate: dict[str, Any]) -> tuple[Any, ...]:
    return (
        route_rank(candidate),
        candidate["distance"] if candidate["distance"] is not None else 99,
        candidate["title"].casefold(),
        candidate["id"],
    )


def direct_first_key(candidate: dict[str, Any]) -> tuple[Any, ...]:
    distance = candidate["distance"]
    if distance in {0, 1}:
        tier = 0
    elif candidate["curated_outbound"]:
        tier = 1
    elif candidate["curated_reciprocal"]:
        tier = 2
    elif distance == 2:
        tier = 3
    else:
        tier = 4
    return (tier, distance if distance is not None else 99, candidate["title"].casefold(), candidate["id"])


def best_predicate_cost(candidate: dict[str, Any]) -> float:
    graph_paths = [path for path in candidate["paths"] if path["distance"] > 0]
    if not graph_paths:
        return 20.0
    return min(
        sum(PREDICATE_COST[predicate] for predicate in path["predicates"])
        + max(0, path["distance"] - 1) * 4
        for path in graph_paths
    )


def predicate_weighted_key(candidate: dict[str, Any]) -> tuple[Any, ...]:
    anchor_bonus = 2 if candidate["curated_outbound"] else 1 if candidate["curated_reciprocal"] else 0
    score = best_predicate_cost(candidate) - anchor_bonus
    return (
        score,
        candidate["distance"] if candidate["distance"] is not None else 99,
        candidate["title"].casefold(),
        candidate["id"],
    )


def best_hub_cost(candidate: dict[str, Any], degree: dict[str, int]) -> float:
    graph_paths = [path for path in candidate["paths"] if path["distance"] > 0]
    if not graph_paths:
        return 25.0
    costs = []
    for path in graph_paths:
        if path["distance"] == 1:
            costs.append(10.0)
        else:
            hub_degree = degree.get(path["intermediary"], 0)
            costs.append(20.0 + 4.0 * math.log2(hub_degree + 1))
    return min(costs)


def hub_penalized_key(candidate: dict[str, Any], degree: dict[str, int]) -> tuple[Any, ...]:
    anchor_bonus = 5 if candidate["curated_outbound"] else 3 if candidate["curated_reciprocal"] else 0
    score = best_hub_cost(candidate, degree) - anchor_bonus
    return (score, best_predicate_cost(candidate), candidate["title"].casefold(), candidate["id"])


def analyze(
    root: Path, data: dict[str, list[dict[str, Any]]] | None = None
) -> dict[str, Any]:
    data = data if data is not None else load_data(root)
    profiles = [profile for profile in data["profiles"] if has_surface(profile)]
    profiles.sort(key=lambda profile: profile["id"])
    entity_by_id = {entity["id"]: entity for entity in data["entities"]}
    relationships = eligible_relationships(data)
    adjacency = navigation_adjacency(data)
    graph = navigation_graph(data)
    degree = {entity_id: len(neighbors) for entity_id, neighbors in graph.items()}

    result_profiles: dict[str, dict[str, Any]] = {}
    intermediary_pairs: dict[str, set[tuple[str, str]]] = defaultdict(set)
    intermediary_path_counts: Counter[str] = Counter()

    for profile in profiles:
        starts = set(profile["component_entity_ids"])
        seeds = profile_seeds(profile)
        candidates: list[dict[str, Any]] = []
        for other in profiles:
            if other["id"] == profile["id"]:
                continue
            targets = set(other["component_entity_ids"])
            other_seeds = profile_seeds(other)
            curated_outbound_entities = sorted(seeds & targets)
            curated_reciprocal_entities = sorted(starts & other_seeds)
            decision = resolve_navigation_candidate(profile, other, graph, adjacency)
            distance = decision["distance"]
            if not curated_outbound_entities and not curated_reciprocal_entities and distance is None:
                continue
            paths = decision["paths"]
            candidate = decision | {
                "id": other["id"],
                "title": other["title"],
                "profile_kind": other["profile_kind"],
                "publication_status": other["publication_status"],
                "maturity": other["maturity"],
                # These legacy fields reconstruct Run 10, when structural countries
                # and editorial anchors were one reciprocal seed set.
                "curated_outbound": bool(curated_outbound_entities),
                "curated_outbound_entities": curated_outbound_entities,
                "curated_reciprocal": bool(curated_reciprocal_entities),
                "curated_reciprocal_entities": curated_reciprocal_entities,
                "path_count": len(paths),
                "direct_path_count": sum(path["distance"] == 1 for path in paths),
                "two_hop_path_count": sum(path["distance"] == 2 for path in paths),
            }
            candidates.append(candidate)

        current_candidates = [candidate for candidate in candidates if candidate["eligible"]]
        for candidate in current_candidates:
            for path in candidate["paths"]:
                intermediary = path["intermediary"]
                if intermediary:
                    intermediary_pairs[intermediary].add(
                        (profile["id"], candidate["id"])
                    )
                    intermediary_path_counts[intermediary] += 1

        model_lists = {
            "A_current": sorted(current_candidates, key=navigation_candidate_sort_key),
            "Run10_baseline": sorted(candidates, key=current_key),
            "B_direct_first": sorted(candidates, key=direct_first_key),
            "C_predicate_weighted": sorted(candidates, key=predicate_weighted_key),
            "D_hub_penalized": sorted(
                candidates, key=lambda candidate: hub_penalized_key(candidate, degree)
            ),
            "E_profile_kind_aware": sorted(
                current_candidates, key=navigation_candidate_sort_key
            ),
        }
        displayed_ids = {
            model: [candidate["id"] for candidate in ranked[:MAX_RELATED_PROFILES]]
            for model, ranked in model_lists.items()
        }
        production_titles = [
            match.group(1)
            for line in render_navigation(profile, data).splitlines()
            if (match := GENERATED_LINK_RE.match(line))
        ]
        computed_titles = [
            next(candidate["title"] for candidate in candidates if candidate["id"] == profile_id)
            for profile_id in displayed_ids["A_current"]
        ]
        if computed_titles != production_titles:
            raise SystemExit(
                f"{profile['id']}: audit Model A diverges from production navigation; "
                f"computed={computed_titles}, production={production_titles}"
            )
        current_ids = set(displayed_ids["A_current"])
        for candidate in candidates:
            candidate["displayed_current"] = candidate["id"] in current_ids
            candidate["run10_sort_key"] = list(current_key(candidate))
            if candidate["eligible"]:
                candidate["current_sort_key"] = list(
                    navigation_candidate_sort_key(candidate)
                )

        direct_candidates = sum(
            candidate["distance"] == 1 for candidate in current_candidates
        )
        two_hop_candidates = sum(
            candidate["distance"] == 2 for candidate in current_candidates
        )
        anchor_only = sum(
            candidate["distance"] is None
            and candidate["route_kind"]
            in {
                "editorial_anchor_outbound",
                "structural_country_outbound",
                "structural_country_descendant",
                "editorial_anchor_reciprocal",
            }
            for candidate in current_candidates
        )
        result_profiles[profile["id"]] = {
            "id": profile["id"],
            "title": profile["title"],
            "profile_kind": profile["profile_kind"],
            "path": profile["path"],
            "component_entity_ids": profile["component_entity_ids"],
            "structural_country_ids": sorted(profile.get("country_entity_ids", [])),
            "editorial_anchor_ids": sorted(
                profile.get("representative_anchor_ids", [])
            ),
            "direct_eligible_neighbors": direct_candidates,
            "two_hop_eligible_neighbors": two_hop_candidates,
            "two_hop_only_neighbors": two_hop_candidates,
            "anchor_only_neighbors": anchor_only,
            "raw_candidate_path_instances": sum(
                candidate["path_count"]
                + len(candidate["editorial_outbound_entities"])
                + len(candidate["structural_country_outbound_entities"])
                + len(candidate["editorial_reciprocal_entities"])
                for candidate in current_candidates
            ),
            "unique_candidate_profiles": len(current_candidates),
            "candidates_after_deduplication": len(current_candidates),
            "run10_baseline_candidate_profiles": len(candidates),
            "displayed": min(MAX_RELATED_PROFILES, len(current_candidates)),
            "displaced_by_cap": max(
                0, len(current_candidates) - MAX_RELATED_PROFILES
            ),
            "model_displayed_ids": displayed_ids,
            "candidates": sorted(
                current_candidates, key=navigation_candidate_sort_key
            ),
            "rejected_candidates": sorted(
                (candidate for candidate in candidates if not candidate["eligible"]),
                key=current_key,
            ),
        }

    recommended_frequency: Counter[str] = Counter()
    displayed_route_counts: Counter[str] = Counter()
    displayed_distance_counts: Counter[str] = Counter()
    all_current_links = 0
    for profile in result_profiles.values():
        by_id = {candidate["id"]: candidate for candidate in profile["candidates"]}
        for candidate_id in profile["model_displayed_ids"]["A_current"]:
            candidate = by_id[candidate_id]
            recommended_frequency[candidate_id] += 1
            all_current_links += 1
            displayed_route_counts[candidate["route_kind"]] += 1
            if candidate["distance"] is None:
                displayed_distance_counts["anchor_only"] += 1
            else:
                displayed_distance_counts[f"distance_{candidate['distance']}"] += 1

    run10_route_counts: Counter[str] = Counter()
    run10_distance_counts: Counter[str] = Counter()
    run10_displayed_links = 0
    for profile in result_profiles.values():
        all_candidates = profile["candidates"] + profile["rejected_candidates"]
        by_id = {candidate["id"]: candidate for candidate in all_candidates}
        for candidate_id in profile["model_displayed_ids"]["Run10_baseline"]:
            candidate = by_id[candidate_id]
            run10_displayed_links += 1
            if candidate["curated_outbound"]:
                run10_route_counts["outbound_anchor"] += 1
            elif candidate["curated_reciprocal"]:
                run10_route_counts["reciprocal_anchor"] += 1
            elif candidate["distance"] == 0:
                run10_route_counts["shared_component"] += 1
            elif candidate["distance"] == 1:
                run10_route_counts["direct_relationship"] += 1
            elif candidate["distance"] == 2:
                run10_route_counts["two_hop_relationship"] += 1

            if candidate["distance"] is None:
                run10_distance_counts["anchor_only"] += 1
            else:
                run10_distance_counts[f"distance_{candidate['distance']}"] += 1

    candidate_counts = [
        profile["unique_candidate_profiles"] for profile in result_profiles.values()
    ]
    saturated = sum(count >= MAX_RELATED_PROFILES for count in candidate_counts)
    displaced = sum(count > MAX_RELATED_PROFILES for count in candidate_counts)
    run10_candidate_counts = [
        profile["run10_baseline_candidate_profiles"]
        for profile in result_profiles.values()
    ]
    run10_saturated = sum(
        count >= MAX_RELATED_PROFILES for count in run10_candidate_counts
    )
    run10_displaced = sum(
        count > MAX_RELATED_PROFILES for count in run10_candidate_counts
    )

    kind_groups: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for profile in result_profiles.values():
        kind_groups[profile["profile_kind"]].append(profile)
    by_kind = {}
    for kind, group in sorted(kind_groups.items()):
        values = [profile["unique_candidate_profiles"] for profile in group]
        by_kind[kind] = {
            "profiles": len(group),
            "mean_candidates": round_metric(statistics.mean(values)),
            "median_candidates": round_metric(statistics.median(values)),
            "p95_candidates": percentile(values, 0.95),
            "max_candidates": max(values),
            "mean_direct": round_metric(
                statistics.mean(profile["direct_eligible_neighbors"] for profile in group)
            ),
            "mean_two_hop": round_metric(
                statistics.mean(profile["two_hop_eligible_neighbors"] for profile in group)
            ),
            "saturated_profiles": sum(
                profile["unique_candidate_profiles"] >= MAX_RELATED_PROFILES
                for profile in group
            ),
            "displaced_profiles": sum(
                profile["unique_candidate_profiles"] > MAX_RELATED_PROFILES
                for profile in group
            ),
        }

    def entity_summary(entity_id: str, value: int, key: str) -> dict[str, Any]:
        entity = entity_by_id.get(entity_id, {})
        return {
            "entity_id": entity_id,
            "name": entity.get("name", entity_id),
            "entity_type": entity.get("type", "unknown"),
            key: value,
        }

    highest_degree = [
        entity_summary(entity_id, value, "degree")
        for entity_id, value in sorted(
            degree.items(), key=lambda item: (-item[1], item[0])
        )[:25]
    ]
    intermediary_hubs = []
    for entity_id in sorted(
        intermediary_pairs,
        key=lambda candidate: (
            -len(intermediary_pairs[candidate]),
            -intermediary_path_counts[candidate],
            candidate,
        ),
    )[:25]:
        summary = entity_summary(
            entity_id, len(intermediary_pairs[entity_id]), "profile_pair_count"
        )
        summary["path_instance_count"] = intermediary_path_counts[entity_id]
        intermediary_hubs.append(summary)

    top_profiles_by_candidates = sorted(
        (
            {
                "profile_id": profile["id"],
                "title": profile["title"],
                "profile_kind": profile["profile_kind"],
                "candidate_profiles": profile["unique_candidate_profiles"],
                "displaced_by_cap": profile["displaced_by_cap"],
            }
            for profile in result_profiles.values()
        ),
        key=lambda item: (-item["candidate_profiles"], item["profile_id"]),
    )[:25]
    top_recommended = [
        {
            "profile_id": profile_id,
            "title": result_profiles[profile_id]["title"],
            "profile_kind": result_profiles[profile_id]["profile_kind"],
            "recommendation_count": count,
        }
        for profile_id, count in recommended_frequency.most_common(25)
    ]

    return {
        "root": str(root.resolve()),
        "algorithm": {
            "eligible_predicates": sorted(NAVIGATION_RELATIONSHIP_PREDICATES),
            "eligible_relationship_statuses": sorted(
                NAVIGATION_RELATIONSHIP_STATUSES
            ),
            "linkable_publication_statuses": sorted(
                LINKABLE_PUBLICATION_STATUSES
            ),
            "maximum_graph_distance": MAX_GRAPH_NAVIGATION_DISTANCE,
            "maximum_related_profiles": MAX_RELATED_PROFILES,
        },
        "overall": {
            "surfaced_profiles": len(result_profiles),
            "eligible_relationship_records": len(relationships),
            "candidate_profile_pairs_directed": sum(candidate_counts),
            "displayed_links": all_current_links,
            "mean_candidates": round_metric(statistics.mean(candidate_counts)),
            "median_candidates": round_metric(statistics.median(candidate_counts)),
            "p95_candidates": percentile(candidate_counts, 0.95),
            "max_candidates": max(candidate_counts),
            "saturated_profiles": saturated,
            "saturation_rate_percent": round_metric(100 * saturated / len(candidate_counts)),
            "displaced_profiles": displaced,
            "displacement_rate_percent": round_metric(100 * displaced / len(candidate_counts)),
            "displayed_route_counts": dict(sorted(displayed_route_counts.items())),
            "displayed_route_percent": {
                key: round_metric(100 * value / all_current_links)
                for key, value in sorted(displayed_route_counts.items())
            },
            "displayed_distance_counts": dict(
                sorted(displayed_distance_counts.items())
            ),
            "displayed_distance_percent": {
                key: round_metric(100 * value / all_current_links)
                for key, value in sorted(displayed_distance_counts.items())
            },
        },
        "run10_baseline": {
            "surfaced_profiles": len(result_profiles),
            "eligible_relationship_records": len(relationships),
            "candidate_profile_pairs_directed": sum(run10_candidate_counts),
            "displayed_links": run10_displayed_links,
            "mean_candidates": round_metric(
                statistics.mean(run10_candidate_counts)
            ),
            "median_candidates": round_metric(
                statistics.median(run10_candidate_counts)
            ),
            "p95_candidates": percentile(run10_candidate_counts, 0.95),
            "max_candidates": max(run10_candidate_counts),
            "saturated_profiles": run10_saturated,
            "saturation_rate_percent": round_metric(
                100 * run10_saturated / len(run10_candidate_counts)
            ),
            "displaced_profiles": run10_displaced,
            "displacement_rate_percent": round_metric(
                100 * run10_displaced / len(run10_candidate_counts)
            ),
            "displayed_route_counts": dict(sorted(run10_route_counts.items())),
            "displayed_route_percent": {
                key: round_metric(100 * value / run10_displayed_links)
                for key, value in sorted(run10_route_counts.items())
            },
            "displayed_distance_counts": dict(
                sorted(run10_distance_counts.items())
            ),
            "displayed_distance_percent": {
                key: round_metric(100 * value / run10_displayed_links)
                for key, value in sorted(run10_distance_counts.items())
            },
        },
        "by_profile_kind": by_kind,
        "highest_degree_entities": highest_degree,
        "highest_degree_surfaced_profiles": top_profiles_by_candidates,
        "most_frequent_intermediary_hubs": intermediary_hubs,
        "most_frequently_recommended_profiles": top_recommended,
        "profiles": result_profiles,
    }


def compare_reports(before: dict[str, Any], after: dict[str, Any]) -> dict[str, Any]:
    common = sorted(set(before["profiles"]) & set(after["profiles"]))
    if not common:
        return {"common_profiles": 0, "models": {}, "displacements": []}
    model_names = next(iter(after["profiles"].values()))["model_displayed_ids"].keys()
    model_results: dict[str, Any] = {}
    for model in model_names:
        changed_profiles = 0
        before_link_count = 0
        retained_link_count = 0
        removed_link_count = 0
        added_link_count = 0
        for profile_id in common:
            before_ids = set(
                before["profiles"][profile_id]["model_displayed_ids"][model]
            )
            after_ids = set(
                after["profiles"][profile_id]["model_displayed_ids"][model]
            )
            changed_profiles += before_ids != after_ids
            before_link_count += len(before_ids)
            retained_link_count += len(before_ids & after_ids)
            removed_link_count += len(before_ids - after_ids)
            added_link_count += len(after_ids - before_ids)
        model_results[model] = {
            "changed_profiles": changed_profiles,
            "changed_profile_rate_percent": round_metric(
                100 * changed_profiles / len(common)
            ),
            "before_displayed_links": before_link_count,
            "retained_displayed_links": retained_link_count,
            "retention_percent": round_metric(
                100 * retained_link_count / before_link_count
                if before_link_count
                else 0
            ),
            "removed_links": removed_link_count,
            "added_links": added_link_count,
        }

    displacements = []
    for profile_id in common:
        before_profile = before["profiles"][profile_id]
        after_profile = after["profiles"][profile_id]
        before_ids = before_profile["model_displayed_ids"]["A_current"]
        after_ids = after_profile["model_displayed_ids"]["A_current"]
        removed = [candidate for candidate in before_ids if candidate not in after_ids]
        added = [candidate for candidate in after_ids if candidate not in before_ids]
        after_candidate_ids = {
            candidate["id"] for candidate in after_profile["candidates"]
        }
        displaced = [candidate for candidate in removed if candidate in after_candidate_ids]
        if displaced:
            displacements.append(
                {
                    "profile_id": profile_id,
                    "title": after_profile["title"],
                    "before_displayed": before_ids,
                    "after_displayed": after_ids,
                    "newly_displayed": added,
                    "displaced_but_still_eligible": displaced,
                    "after_candidate_count": after_profile["unique_candidate_profiles"],
                }
            )
    return {
        "common_profiles": len(common),
        "before_surfaced_profiles": before["overall"]["surfaced_profiles"],
        "after_surfaced_profiles": after["overall"]["surfaced_profiles"],
        "models": model_results,
        "displacements": displacements,
    }


def load_ratings(path: Path | None) -> dict[str, dict[str, dict[str, str]]]:
    if path is None:
        return {}
    raw = json.loads(path.read_text())
    records = raw.get("ratings", raw)
    normalized: dict[str, dict[str, dict[str, str]]] = {}
    for profile_id, profile_ratings in records.items():
        # The durable fixture may use a compact, review-friendly shape that groups
        # candidates sharing a rating and explanation. Also accept the expanded
        # candidate-keyed shape for ad hoc callers.
        if set(profile_ratings).issubset({"A", "B", "C", "D", "E"}):
            expanded: dict[str, dict[str, str]] = {}
            for rating, groups in profile_ratings.items():
                for group in groups:
                    for candidate_id in group["candidates"]:
                        if candidate_id in expanded:
                            raise SystemExit(
                                f"{profile_id}: duplicate rating for {candidate_id}"
                            )
                        expanded[candidate_id] = {
                            "rating": rating,
                            "reason": group["reason"],
                        }
            normalized[profile_id] = expanded
        else:
            normalized[profile_id] = profile_ratings
    return normalized


def evaluate_models(
    report: dict[str, Any], ratings: dict[str, dict[str, dict[str, str]]]
) -> dict[str, Any]:
    if not ratings:
        return {}
    models = next(iter(report["profiles"].values()))["model_displayed_ids"].keys()
    output: dict[str, Any] = {}
    for model in models:
        ab_total = 0
        ab_retained = 0
        de_total = 0
        de_removed = 0
        rated_retained = Counter()
        links_changed = 0
        kind_totals: dict[str, Counter[str]] = defaultdict(Counter)
        kind_retained: dict[str, Counter[str]] = defaultdict(Counter)
        removed_by_rating: dict[str, list[str]] = defaultdict(list)
        for profile_id, candidate_ratings in ratings.items():
            profile = report["profiles"][profile_id]
            baseline = set(profile["model_displayed_ids"]["Run10_baseline"])
            rated = set(candidate_ratings)
            if rated != baseline:
                missing = sorted(baseline - rated)
                extra = sorted(rated - baseline)
                raise SystemExit(
                    f"{profile_id}: ratings must cover every Run 10 displayed link; "
                    f"missing={missing}, extra={extra}"
                )
            displayed = set(profile["model_displayed_ids"][model])
            links_changed += len(baseline - displayed)
            source_kind = profile["profile_kind"]
            for candidate_id, rating_record in candidate_ratings.items():
                rating = rating_record["rating"]
                kind_totals[source_kind][rating] += 1
                if rating in {"A", "B"}:
                    ab_total += 1
                    ab_retained += candidate_id in displayed
                if rating in {"D", "E"}:
                    de_total += 1
                    de_removed += candidate_id not in displayed
                if candidate_id in displayed:
                    rated_retained[rating] += 1
                    kind_retained[source_kind][rating] += 1
                else:
                    removed_by_rating[rating].append(
                        f"{profile_id} -> {candidate_id}"
                    )

        ratings_by_source_kind = {}
        for source_kind in sorted(kind_totals):
            totals = kind_totals[source_kind]
            retained = kind_retained[source_kind]
            baseline_total = sum(totals.values())
            retained_total = sum(retained.values())
            baseline_de = totals["D"] + totals["E"]
            retained_de = retained["D"] + retained["E"]
            ratings_by_source_kind[source_kind] = {
                "baseline_counts": dict(sorted(totals.items())),
                "retained_counts": dict(sorted(retained.items())),
                "baseline_de_rate_percent": round_metric(
                    100 * baseline_de / baseline_total if baseline_total else 0
                ),
                "retained_de_rate_percent": round_metric(
                    100 * retained_de / retained_total if retained_total else 0
                ),
            }
        output[model] = {
            "sample_profiles": len(ratings),
            "rated_links": sum(len(records) for records in ratings.values()),
            "ab_links": ab_total,
            "ab_retained": ab_retained,
            "ab_retained_percent": round_metric(
                100 * ab_retained / ab_total if ab_total else 0
            ),
            "de_links": de_total,
            "de_removed": de_removed,
            "de_removed_percent": round_metric(
                100 * de_removed / de_total if de_total else 0
            ),
            "current_links_removed_from_sample": links_changed,
            "run10_links_removed_from_sample": links_changed,
            "retained_ratings": dict(sorted(rated_retained.items())),
            "removed_links_by_rating": {
                rating: sorted(items)
                for rating, items in sorted(removed_by_rating.items())
            },
            "ratings_by_source_kind": ratings_by_source_kind,
        }
    return output


def compact_report(report: dict[str, Any], profile_ids: list[str]) -> dict[str, Any]:
    if not profile_ids:
        return report
    missing = [profile_id for profile_id in profile_ids if profile_id not in report["profiles"]]
    if missing:
        raise SystemExit("Unknown surfaced profile(s): " + ", ".join(missing))
    return {
        "root": report["root"],
        "algorithm": report["algorithm"],
        "profiles": {
            profile_id: report["profiles"][profile_id] for profile_id in profile_ids
        },
    }


def markdown_summary(report: dict[str, Any], model_evaluation: dict[str, Any]) -> str:
    overall = report["overall"]
    baseline = report["run10_baseline"]
    lines = [
        "# CARTA Human Reference navigation audit metrics",
        "",
        "| Metric | Run 10 baseline | Current production |",
        "|---|---:|---:|",
        f"| Surfaced profiles | {baseline['surfaced_profiles']} | {overall['surfaced_profiles']} |",
        f"| Directed candidate pairs | {baseline['candidate_profile_pairs_directed']} | {overall['candidate_profile_pairs_directed']} |",
        f"| Displayed links | {baseline['displayed_links']} | {overall['displayed_links']} |",
        f"| Mean candidates | {baseline['mean_candidates']} | {overall['mean_candidates']} |",
        f"| Median candidates | {baseline['median_candidates']} | {overall['median_candidates']} |",
        f"| p95 candidates | {baseline['p95_candidates']} | {overall['p95_candidates']} |",
        f"| Saturated profiles | {baseline['saturated_profiles']} | {overall['saturated_profiles']} |",
        f"| Displaced profiles | {baseline['displaced_profiles']} | {overall['displaced_profiles']} |",
        "",
        "## Displayed shortest-distance distribution",
        "",
        "| Distance | Run 10 | Current |",
        "|---|---:|---:|",
    ]
    for key in ("anchor_only", "distance_0", "distance_1", "distance_2"):
        label = key.replace("_", " ")
        lines.append(
            f"| {label} | {baseline['displayed_distance_counts'].get(key, 0)} "
            f"({baseline['displayed_distance_percent'].get(key, 0)}%) | "
            f"{overall['displayed_distance_counts'].get(key, 0)} "
            f"({overall['displayed_distance_percent'].get(key, 0)}%) |"
        )
    lines.extend(
        [
        "",
        "## Highest-degree entities",
        "",
        "| Entity | Type | Degree |",
        "|---|---:|---:|",
        ]
    )
    for item in report["highest_degree_entities"][:15]:
        lines.append(
            f"| `{item['entity_id']}` ({item['name']}) | {item['entity_type']} | {item['degree']} |"
        )
    lines.extend(
        [
            "",
            "## Most frequent two-hop intermediaries",
            "",
            "| Entity | Profile pairs | Path instances |",
            "|---|---:|---:|",
        ]
    )
    for item in report["most_frequent_intermediary_hubs"][:15]:
        lines.append(
            f"| `{item['entity_id']}` ({item['name']}) | {item['profile_pair_count']} | {item['path_instance_count']} |"
        )
    if model_evaluation:
        lines.extend(
            [
                "",
                "## Model evaluation against ratings",
                "",
                "| Model | A/B retained | D/E removed | Run 10 links removed |",
                "|---|---:|---:|---:|",
            ]
        )
        for model, item in model_evaluation.items():
            lines.append(
                f"| {model} | {item['ab_retained_percent']}% | {item['de_removed_percent']}% | {item['current_links_removed_from_sample']} |"
            )
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--root",
        type=Path,
        default=ROOT,
        help="Repository snapshot root (defaults to the current checkout).",
    )
    parser.add_argument(
        "--git-ref",
        help="Analyze governed JSONL records at this Git ref instead of the worktree.",
    )
    parser.add_argument(
        "--compare-ref",
        help="Compare this earlier Git ref with --git-ref (or the worktree).",
    )
    parser.add_argument(
        "--profile",
        action="append",
        default=[],
        help="Restrict JSON output to a surfaced profile ID; repeat as needed.",
    )
    parser.add_argument(
        "--ratings",
        type=Path,
        help="Optional JSON fixture with A-E ratings for current displayed links.",
    )
    parser.add_argument(
        "--format", choices={"json", "markdown"}, default="markdown"
    )
    args = parser.parse_args()

    data = (
        load_data_from_git_ref(args.root, args.git_ref)
        if args.git_ref
        else load_data(args.root)
    )
    report = analyze(args.root, data)
    if args.git_ref:
        report["git_ref"] = args.git_ref
    if args.compare_ref:
        before = analyze(
            args.root, load_data_from_git_ref(args.root, args.compare_ref)
        )
        report["history_comparison"] = compare_reports(before, report)
        report["history_comparison"]["before_ref"] = args.compare_ref
        report["history_comparison"]["after_ref"] = args.git_ref or "worktree"
    ratings = load_ratings(args.ratings)
    model_evaluation = evaluate_models(report, ratings)
    if model_evaluation:
        report["model_evaluation"] = model_evaluation

    if args.format == "json":
        print(json.dumps(compact_report(report, args.profile), indent=2, sort_keys=True))
    else:
        if args.profile:
            raise SystemExit("--profile is available only with --format json")
        print(markdown_summary(report, model_evaluation), end="")


if __name__ == "__main__":
    main()
