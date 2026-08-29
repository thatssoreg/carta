import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class AtlasContractTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        result = subprocess.run(
            [sys.executable, "scripts/validate_atlas.py", "--json"],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
        cls.summary = json.loads(result.stdout)

    def test_governed_and_external_inao_features_coexist(self):
        self.assertGreater(self.summary["inao_mapped_features"], 0)
        self.assertGreater(self.summary["inao_unmapped_features"], 0)
        self.assertEqual(self.summary["inao_ambiguous_features"], 0)

    def test_every_accepted_inao_mapping_has_geometry_metadata(self):
        self.assertEqual(
            self.summary["inao_mapped_features"], self.summary["geometry_records"]
        )

    def test_wine_region_orientation_is_derived_and_governed(self):
        regions = json.loads(
            (ROOT / "atlas-app/public/data/france-wine-regions.geojson").read_text()
        )
        self.assertGreater(len(regions["features"]), 0)
        for feature in regions["features"]:
            properties = feature["properties"]
            self.assertEqual(feature["geometry"]["type"], "Point")
            self.assertEqual(
                properties["derivation"],
                "representative_point_of_union_of_mapped_child_inao_geometries",
            )
            self.assertTrue(properties["child_carta_entity_ids"])
            self.assertIn("not a statutory polygon", properties["representation_label"])

    def test_layer_defaults_prioritize_aoc_over_igp(self):
        config = json.loads((ROOT / "atlas-app/src/atlas-config.json").read_text())
        self.assertTrue(config["defaultLayers"]["aocAreas"])
        self.assertFalse(config["defaultLayers"]["igpAreas"])
        self.assertTrue(config["defaultLayers"]["wineRegions"])

    def test_five_france_worlds_have_derived_region_anchors(self):
        regions = json.loads(
            (ROOT / "atlas-app/public/data/france-wine-regions.geojson").read_text()
        )
        by_entity = {
            feature["properties"]["carta_entity_id"]: feature
            for feature in regions["features"]
        }
        self.assertEqual(
            set(by_entity),
            {
                "place:jura",
                "place:burgundy",
                "place:loire-valley",
                "place:beaujolais",
                "place:bearn",
            },
        )
        self.assertIn(
            "appellation:bourgogne-cote-d-or",
            by_entity["place:burgundy"]["properties"]["child_carta_entity_ids"],
        )

    def test_learner_guides_keep_claim_lineage_and_machine_quantities(self):
        guides = json.loads(
            (ROOT / "atlas-app/public/data/atlas-guides.json").read_text()
        )["guides"]
        claims = {}
        for path in sorted((ROOT / "data/claims").glob("*.jsonl")):
            for line in path.read_text().splitlines():
                if line.strip():
                    record = json.loads(line)
                    claims[record["id"]] = record
        for entity_id in (
            "place:jura",
            "place:burgundy",
            "place:loire-valley",
            "place:beaujolais",
            "place:bearn",
        ):
            guide = guides[entity_id]
            self.assertTrue(guide["sections"])
            self.assertTrue(guide["quantities"])
            for item in guide["sections"] + guide["quantities"]:
                claim = claims[item["claim_id"]]
                self.assertEqual(item["statement"], claim["statement"])
                self.assertEqual(item["source_ids"], [ref["source_id"] for ref in claim["source_refs"]])
                if "quantity" in item:
                    projected = dict(item["quantity"])
                    projected.pop("dimension_name", None)
                    self.assertEqual(projected, claim["quantity"])

    def test_jura_is_the_deepest_world_and_exposes_all_six_aops(self):
        guides = json.loads(
            (ROOT / "atlas-app/public/data/atlas-guides.json").read_text()
        )["guides"]
        jura = guides["place:jura"]
        self.assertEqual(jura["maturity"], "deep")
        expected = {
            "appellation:arbois",
            "appellation:cotes-du-jura",
            "appellation:chateau-chalon",
            "appellation:l-etoile",
            "appellation:cremant-du-jura",
            "appellation:macvin-du-jura",
        }
        self.assertTrue(expected.issubset(set(jura["component_entity_ids"])))
        self.assertGreaterEqual(len(jura["sources"]), 5)

    def test_run_04_native_jura_rabbit_hole_is_projected(self):
        subjects = json.loads(
            (ROOT / "atlas-app/public/data/atlas-subjects.json").read_text()
        )["subjects"]
        required = {
            "place:jura",
            "appellation:arbois",
            "appellation:cotes-du-jura",
            "appellation:chateau-chalon",
            "appellation:l-etoile",
            "appellation:cremant-du-jura",
            "appellation:macvin-du-jura",
            "producer:domaine-de-la-tournelle",
            "producer:domaine-labet",
            "producer:maison-pierre-overnoy",
            "producer:domaine-de-saint-pierre-jura",
            "grape:savagnin",
            "grape:petit-manseng",
            "appellation:jurancon",
        }
        self.assertTrue(required.issubset(subjects))

        savagnin_targets = {
            item["target_id"]: item
            for item in subjects["grape:savagnin"]["connections"]
        }
        self.assertIn("grape:petit-manseng", savagnin_targets)
        self.assertFalse(savagnin_targets["grape:petit-manseng"]["has_map_target"])
        self.assertEqual(
            savagnin_targets["grape:petit-manseng"]["predicate"],
            "GENETICALLY_CLOSE_TO",
        )

        petit_manseng_targets = {
            item["target_id"]: item
            for item in subjects["grape:petit-manseng"]["connections"]
        }
        self.assertTrue(petit_manseng_targets["appellation:jurancon"]["has_map_target"])
        self.assertEqual(
            subjects["appellation:jurancon"]["map_target"]["kind"], "bounds"
        )

    def test_run_04_editorial_signals_tells_and_terms_are_governed(self):
        editorial = json.loads(
            (ROOT / "atlas-app/public/data/atlas-editorial.json").read_text()
        )
        self.assertEqual(
            editorial["generated_from"], "data/atlas/run-04-experience.json"
        )
        self.assertEqual(
            {item["id"] for item in editorial["legend"]},
            {"rabbit-hole", "tell", "iykyk", "same-energy"},
        )
        self.assertEqual(
            set(editorial["glossary"]),
            {"elevage", "flor", "marl", "mistelle", "ouille", "sous-voile", "voile"},
        )
        jura = editorial["subjects"]["place:jura"]
        self.assertEqual(len(jura["accent"]["tells"]), 3)
        for tell in jura["accent"]["tells"]:
            self.assertTrue(tell["clue"])
            self.assertTrue(tell["why"])
            self.assertTrue(tell["correction"])
            self.assertIn(tell["target_id"], json.loads(
                (ROOT / "atlas-app/public/data/atlas-subjects.json").read_text()
            )["subjects"])
            for claim_id in tell["claim_ids"]:
                self.assertIn(claim_id, editorial["claim_support"])

    def test_run_04_keep_wandering_routes_are_explained_and_live(self):
        editorial = json.loads(
            (ROOT / "atlas-app/public/data/atlas-editorial.json").read_text()
        )
        subjects = json.loads(
            (ROOT / "atlas-app/public/data/atlas-subjects.json").read_text()
        )["subjects"]
        for subject_id, teaching in editorial["subjects"].items():
            direct = {item["target_id"] for item in subjects[subject_id]["connections"]}
            featured = teaching.get("featured_connections", [])
            self.assertLessEqual(len(featured), 3)
            for route in featured:
                self.assertIn(route["target_id"], subjects)
                self.assertTrue(route["reason"])
                self.assertTrue(route["claim_ids"])
                if route["target_id"] not in direct:
                    self.assertEqual(route["signal"], "same-energy")
            for surprise in teaching.get("surprises", []):
                self.assertIn(surprise["target_id"], subjects)

    def test_savagnin_and_chardonnay_have_distinct_teaching_grammars(self):
        editorial = json.loads(
            (ROOT / "atlas-app/public/data/atlas-editorial.json").read_text()
        )["subjects"]
        savagnin = editorial["grape:savagnin"]
        self.assertEqual(len(savagnin["style_paths"]), 3)
        self.assertEqual(
            {item["signal"] for item in savagnin["affinities"]},
            {"rabbit-hole", "same-energy"},
        )
        self.assertIn(
            "Same grape. Different cultural machine.",
            editorial["grape:chardonnay"]["thesis"],
        )

    def test_run_04_ui_contract_has_back_close_trail_and_active_map_reactions(self):
        html = (ROOT / "atlas-app/index.html").read_text()
        main = (ROOT / "atlas-app/src/main.js").read_text()
        self.assertIn("data-back-detail", html)
        self.assertIn("data-close-detail", html)
        self.assertIn("Your rabbit hole", html)
        self.assertIn("history.back()", main)
        self.assertIn("state.geographicSubjectId === subject.entity_id", main)
        self.assertIn("subject-areas-fill", main)
        self.assertIn("subject-producer-halos", main)
        self.assertNotIn("A useful way into the places, people, bottles", main)
        self.assertNotIn("Where next?", main)

    def test_producer_points_are_production_bases_with_honest_precision(self):
        points = json.loads(
            (ROOT / "atlas-app/public/data/jura-producers.geojson").read_text()
        )["features"]
        self.assertEqual(len(points), 4)
        by_entity = {
            feature["properties"]["carta_entity_id"]: feature
            for feature in points
        }
        self.assertEqual(
            by_entity["producer:domaine-de-saint-pierre-jura"]["properties"]["precision"],
            "municipality",
        )
        self.assertIn(
            "Approximate location",
            by_entity["producer:domaine-de-saint-pierre-jura"]["properties"]["placement_note"],
        )
        for feature in points:
            properties = feature["properties"]
            self.assertEqual(feature["geometry"]["type"], "Point")
            self.assertEqual(properties["feature_type"], "producer_base")
            self.assertIn("not vineyard", properties["representation_label"])
            self.assertTrue(properties["native_route"].startswith("#/producer/"))

    def test_entry_points_and_subject_claims_keep_authority_lineage(self):
        entries = json.loads(
            (ROOT / "atlas-app/public/data/atlas-entry-points.json").read_text()
        )
        self.assertEqual(len(entries["entry_points"]), 4)
        self.assertEqual(len(entries["featured_worlds"]), 5)
        claims = {}
        for path in sorted((ROOT / "data/claims").glob("*.jsonl")):
            for line in path.read_text().splitlines():
                if line.strip():
                    claim = json.loads(line)
                    claims[claim["id"]] = claim
        for entry in entries["entry_points"]:
            for projected in entry["supporting_claims"]:
                claim = claims[projected["claim_id"]]
                self.assertEqual(projected["statement"], claim["statement"])
                self.assertEqual(
                    projected["source_ids"],
                    [source["source_id"] for source in claim["source_refs"]],
                )


if __name__ == "__main__":
    unittest.main()
