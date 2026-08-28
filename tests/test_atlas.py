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


if __name__ == "__main__":
    unittest.main()
