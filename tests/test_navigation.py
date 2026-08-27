#!/usr/bin/env python3
"""Focused regression coverage for Human Reference navigation semantics."""
from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from audit_navigation import analyze, evaluate_models, load_data, load_ratings  # noqa: E402
from validate_data import (  # noqa: E402
    TWO_HOP_POLICY_BY_SOURCE_KIND,
    load_and_validate_schema,
    navigation_adjacency,
    navigation_graph,
    resolve_navigation_candidate,
    two_hop_navigation_eligibility,
)


class NavigationPolicyTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.data, _ = load_and_validate_schema()
        cls.profiles = {profile["id"]: profile for profile in cls.data["profiles"]}
        cls.graph = navigation_graph(cls.data)
        cls.adjacency = navigation_adjacency(cls.data)
        cls.report = analyze(ROOT, load_data(ROOT))

    def decision(self, source_id: str, target_id: str) -> dict:
        return resolve_navigation_candidate(
            self.profiles[source_id],
            self.profiles[target_id],
            self.graph,
            self.adjacency,
        )

    def assert_decision(
        self,
        source_id: str,
        target_id: str,
        *,
        eligible: bool,
        route_kind: str,
        category: str | None = None,
        path_pattern: str | None = None,
    ) -> dict:
        decision = self.decision(source_id, target_id)
        explanation = json.dumps(decision, indent=2, sort_keys=True)
        self.assertEqual(decision["eligible"], eligible, explanation)
        self.assertEqual(decision["route_kind"], route_kind, explanation)
        self.assertEqual(decision["source_kind"], self.profiles[source_id]["profile_kind"])
        self.assertEqual(decision["target_kind"], self.profiles[target_id]["profile_kind"])
        if category is not None:
            self.assertEqual(decision.get("policy_category"), category, explanation)
        if path_pattern is not None:
            self.assertIn(
                path_pattern,
                [path["pattern"] for path in decision["paths"]],
                explanation,
            )
        return decision

    def test_every_profile_kind_has_an_explicit_two_hop_policy(self) -> None:
        schema = json.loads((ROOT / "schemas/reference-profile.schema.json").read_text())
        schema_kinds = set(schema["properties"]["profile_kind"]["enum"])
        self.assertEqual(schema_kinds, set(TWO_HOP_POLICY_BY_SOURCE_KIND))

    def test_structural_country_membership_is_directional_not_editorial(self) -> None:
        self.assert_decision(
            "profile:burgess-cellars",
            "profile:united-states",
            eligible=True,
            route_kind="structural_country_outbound",
        )
        self.assert_decision(
            "profile:united-states",
            "profile:burgess-cellars",
            eligible=False,
            route_kind="rejected_structural_country_reciprocal",
            category="structural_country_not_editorial",
        )
        self.assert_decision(
            "profile:united-states",
            "profile:ballard-canyon-ava",
            eligible=True,
            route_kind="structural_country_descendant",
        )

    def test_country_pages_keep_orientation_without_producer_flooding(self) -> None:
        profile_kinds = {
            profile_id: self.profiles[profile_id]["profile_kind"]
            for profile_id in self.profiles
        }
        united_states = self.report["profiles"]["profile:united-states"]
        displayed = united_states["model_displayed_ids"]["A_current"]
        self.assertTrue({"profile:california", "profile:napa-valley-ava"} <= set(displayed))
        self.assertFalse(
            any(profile_kinds[profile_id] == "producer" for profile_id in displayed),
            displayed,
        )
        self.assertNotIn(
            "profile:domaine-houillon",
            self.report["profiles"]["profile:france"]["model_displayed_ids"]["A_current"],
        )
        self.assertIn(
            "profile:richard-leroy",
            self.report["profiles"]["profile:france"]["model_displayed_ids"]["A_current"],
            "France explicitly anchors Richard Leroy; editorial selection must survive",
        )

    def test_up_then_down_sibling_geography_is_rejected(self) -> None:
        cases = [
            ("profile:loire-valley", "profile:jura", "WITHIN>/WITHIN<"),
            ("profile:jura", "profile:savoie", "WITHIN>/WITHIN<"),
            ("profile:savoie", "profile:loire-valley", "WITHIN>/WITHIN<"),
            (
                "profile:napa-valley-ava",
                "profile:santa-ynez-valley-ava",
                "WITHIN>/WITHIN<",
            ),
        ]
        for source_id, target_id, pattern in cases:
            with self.subTest(source=source_id, target=target_id):
                self.assert_decision(
                    source_id,
                    target_id,
                    eligible=False,
                    route_kind="rejected_two_hop",
                    category="shared_broad_geography",
                    path_pattern=pattern,
                )

    def test_downward_geographic_containment_survives(self) -> None:
        decision = self.assert_decision(
            "profile:california",
            "profile:ballard-canyon-ava",
            eligible=True,
            route_kind="two_hop_relationship",
            category="directional_geography_two_hop",
        )
        self.assertTrue(
            any(path["directions"] == ["reverse", "reverse"] for path in decision["paths"]),
            json.dumps(decision, indent=2, sort_keys=True),
        )

    def test_st_helena_is_linked_from_governed_containment(self) -> None:
        self.assert_decision(
            "profile:napa-valley-ava",
            "profile:st-helena-ava",
            eligible=True,
            route_kind="direct_relationship",
            path_pattern="WITHIN<",
        )

    def test_direct_professional_and_editorial_routes_survive(self) -> None:
        self.assert_decision(
            "profile:domaine-lampyres",
            "profile:matassa",
            eligible=True,
            route_kind="direct_relationship",
            path_pattern="WORKED_FOR>",
        )
        self.assert_decision(
            "profile:domaine-houillon",
            "profile:maison-pierre-overnoy",
            eligible=True,
            route_kind="editorial_anchor_outbound",
        )

    def test_broad_composite_producer_paths_are_rejected(self) -> None:
        for source_id, target_id in [
            ("profile:domaine-lampyres", "profile:bodegas-muga"),
            ("profile:domaine-labet", "profile:domaine-louis-michel-fils"),
            ("profile:clos-du-tue-boeuf", "profile:domaine-houillon"),
        ]:
            with self.subTest(source=source_id, target=target_id):
                self.assert_decision(
                    source_id,
                    target_id,
                    eligible=False,
                    route_kind="rejected_two_hop",
                    category="broad_composite_producer_two_hop",
                )

    def test_specific_two_hop_producer_context_survives(self) -> None:
        specific_practice_path = [
            {
                "distance": 2,
                "predicates": ["MADE_FROM", "USES_PRACTICE"],
                "directions": ["forward", "reverse"],
            }
        ]
        eligible, category, _ = two_hop_navigation_eligibility(
            "producer", "producer", specific_practice_path
        )
        self.assertTrue(eligible)
        self.assertEqual(category, "specific_producer_two_hop")

    def test_planting_alone_does_not_create_producer_adjacency(self) -> None:
        cases = [
            (
                "profile:weingut-gunther-steinmetz",
                "profile:hiyu-wine-farm",
                "MADE_FROM>/PLANTED_AT>",
            ),
            (
                "profile:weingut-keller",
                "profile:hofgut-falkenstein",
                "MADE_FROM>/PLANTED_AT>",
            ),
            (
                "profile:domaine-labet",
                "profile:hiyu-wine-farm",
                "MADE_FROM>/PLANTED_AT>",
            ),
        ]
        for source_id, target_id, pattern in cases:
            with self.subTest(source=source_id, target=target_id):
                self.assert_decision(
                    source_id,
                    target_id,
                    eligible=False,
                    route_kind="rejected_two_hop",
                    category="broad_composite_producer_two_hop",
                    path_pattern=pattern,
                )

    def test_disjoint_classification_history_does_not_create_lateral_adjacency(self) -> None:
        for source_id, target_id in [
            ("profile:cotes-du-rhone", "profile:vin-de-france"),
            ("profile:vin-de-france", "profile:cotes-du-rhone"),
        ]:
            with self.subTest(source=source_id, target=target_id):
                decision = self.assert_decision(
                    source_id,
                    target_id,
                    eligible=False,
                    route_kind="rejected_two_hop",
                    category="temporally_disjoint_classification_bridge",
                    path_pattern="CLASSIFIED_AS</CLASSIFIED_AS>",
                )
                self.assertTrue(
                    any(
                        path.get("validity_intervals")
                        == [
                            {"valid_from": "2021-01-01", "valid_to": "2021-12-31"},
                            {"valid_from": "2022-01-01", "valid_to": "2022-12-31"},
                        ]
                        or path.get("validity_intervals")
                        == [
                            {"valid_from": "2022-01-01", "valid_to": "2022-12-31"},
                            {"valid_from": "2021-01-01", "valid_to": "2021-12-31"},
                        ]
                        for path in decision["paths"]
                    ),
                    json.dumps(decision, indent=2, sort_keys=True),
                )

    def test_overlapping_or_unknown_classification_history_is_not_suppressed(self) -> None:
        overlapping = [
            {
                "distance": 2,
                "predicates": ["CLASSIFIED_AS", "CLASSIFIED_AS"],
                "directions": ["reverse", "forward"],
                "validity_intervals": [
                    {"valid_from": "2022-01-01", "valid_to": "2022-12-31"},
                    {"valid_from": "2022-06-01", "valid_to": "2023-05-31"},
                ],
            }
        ]
        eligible, category, _ = two_hop_navigation_eligibility(
            "appellation", "classification", overlapping
        )
        self.assertTrue(eligible)
        self.assertEqual(category, "directional_geography_two_hop")

        unknown = [
            {
                "distance": 2,
                "predicates": ["CLASSIFIED_AS", "CLASSIFIED_AS"],
                "directions": ["reverse", "forward"],
                "validity_intervals": [
                    {"valid_from": None, "valid_to": None},
                    {"valid_from": "2022-01-01", "valid_to": "2022-12-31"},
                ],
            }
        ]
        eligible, category, _ = two_hop_navigation_eligibility(
            "appellation", "classification", unknown
        )
        self.assertTrue(eligible)
        self.assertEqual(category, "directional_geography_two_hop")

    def test_grape_cooccurrence_does_not_create_general_adjacency(self) -> None:
        self.assert_decision(
            "profile:syrah",
            "profile:cabernet-sauvignon",
            eligible=False,
            route_kind="rejected_two_hop",
            category="grape_cooccurrence_two_hop",
            path_pattern="MADE_FROM</MADE_FROM>",
        )
        self.assert_decision(
            "profile:syrah",
            "profile:pax-wines",
            eligible=True,
            route_kind="editorial_anchor_reciprocal",
        )

    def test_full_run10_ratings_fixture_regression(self) -> None:
        ratings = load_ratings(
            ROOT / "audits/run-10-human-reference-navigation-ratings.json"
        )
        current = evaluate_models(self.report, ratings)["A_current"]
        self.assertEqual(current["ab_retained"], 109, current)
        self.assertEqual(current["retained_ratings"]["B"], 6, current)
        self.assertEqual(current["de_removed"], 72, current)
        self.assertNotIn("D", current["retained_ratings"], current)
        self.assertNotIn("E", current["retained_ratings"], current)
        self.assertNotIn("A", current["removed_links_by_rating"], current)


if __name__ == "__main__":
    unittest.main()
