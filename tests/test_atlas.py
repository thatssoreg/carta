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


if __name__ == "__main__":
    unittest.main()
