import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXPERIENCE_LINEAGE = [
    "data/atlas/run-05-jura-final-cut.json",
    "data/atlas/run-06-bearn-jurancon-world.json",
    "data/atlas/run-07-editorial-foundation.json",
]


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

    def test_jura_and_bearn_rabbit_hole_is_projected_both_ways(self):
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
            "place:bearn",
            "appellation:bearn",
            "grape:gros-manseng",
            "grape:petit-courbu",
            "grape:courbu",
            "grape:raffiat-de-moncade",
            "producer:camin-larredya",
            "producer:domaine-cauhape",
            "producer:clos-uroulat",
            "producer:domaine-de-souch",
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
            petit_manseng_targets["grape:savagnin"]["predicate"],
            "GENETICALLY_CLOSE_TO",
        )
        self.assertEqual(
            subjects["appellation:jurancon"]["map_target"]["kind"], "bounds"
        )

    def test_run_06_editorial_pillars_signals_and_terms_are_governed(self):
        editorial = json.loads(
            (ROOT / "atlas-app/public/data/atlas-editorial.json").read_text()
        )
        self.assertEqual(
            editorial["generated_from"], EXPERIENCE_LINEAGE
        )
        self.assertEqual(editorial["release"], "atlas-run-07-editorial-foundation")
        self.assertEqual(
            {item["id"] for item in editorial["legend"]},
            {"iykyk", "same-energy"},
        )
        self.assertEqual(
            set(editorial["glossary"]),
            {
                "elevage", "flor", "foehn", "marl", "mistelle", "ouille",
                "passerillage", "sec", "sous-voile", "tries-successives",
                "vendanges-tardives", "voile",
            },
        )
        jura = editorial["subjects"]["place:jura"]
        self.assertNotIn("accent", jura)
        self.assertEqual(len(jura["hero_facts"]), 2)
        self.assertEqual(len(jura["people"]), 4)
        self.assertEqual(
            set(jura["pillar_map_reactions"]),
            {"place", "grapes", "people", "culture", "rules"},
        )
        subjects = json.loads(
                (ROOT / "atlas-app/public/data/atlas-subjects.json").read_text()
            )["subjects"]
        for person in jura["people"]:
            self.assertIn(person["target_id"], subjects)
            self.assertEqual(subjects[person["target_id"]]["kind"], "producer")
            self.assertTrue(subjects[person["target_id"]]["map_target"])
            for claim_id in person["claim_ids"]:
                self.assertIn(claim_id, editorial["claim_support"])

        bearn = editorial["subjects"]["place:bearn"]
        self.assertTrue(jura["regional_world"])
        self.assertTrue(bearn["regional_world"])
        self.assertEqual(len(bearn["hero_facts"]), 2)
        self.assertEqual(len(bearn["grape_cards"]), 5)
        self.assertEqual(len(bearn["style_comparison"]), 3)
        self.assertEqual(len(bearn["people"]), 4)
        self.assertEqual(
            set(bearn["pillar_map_reactions"]),
            {"place", "grapes", "people", "culture", "rules"},
        )
        self.assertNotIn(
            "tell",
            {route.get("signal") for route in bearn.get("featured_connections", [])},
        )
        metrics = {card["target_id"]: card["metric"] for card in bearn["grape_cards"]}
        self.assertEqual(metrics["grape:petit-manseng"], "Principal")
        self.assertEqual(metrics["grape:gros-manseng"], "Principal")
        self.assertEqual(metrics["grape:raffiat-de-moncade"], "Wider Béarn")

    def test_keep_wandering_routes_are_explained_and_live(self):
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
            self.assertNotIn("surprises", teaching)

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

    def test_regional_ui_contract_has_back_close_trail_and_active_map_reactions(self):
        html = (ROOT / "atlas-app/index.html").read_text()
        main = (ROOT / "atlas-app/src/main.js").read_text()
        self.assertIn("data-back-detail", html)
        self.assertIn("data-close-detail", html)
        self.assertIn("Your rabbit hole", html)
        self.assertIn("history.back()", main)
        self.assertIn("state.geographicSubjectId === subject.entity_id", main)
        self.assertIn("subject-areas-fill", main)
        self.assertIn("subject-producer-halos", main)
        self.assertIn("The Place", main)
        self.assertIn("The Grapes &amp; Wines", main)
        self.assertIn("The People", main)
        self.assertIn("The Culture", main)
        self.assertIn("The Rules", main)
        self.assertIn("activateRegionalPillar", main)
        self.assertIn("map_click_priority", main)
        self.assertNotIn("activeJuraPillar", main)
        self.assertNotIn("activateJuraPillar", main)
        self.assertNotIn("Surprise me", main)
        self.assertNotIn("data-surprise-subject", main)
        self.assertNotIn("A representative route selected by CARTA", main)
        self.assertNotIn("A useful way into the places, people, bottles", main)
        self.assertNotIn("Where next?", main)

    def test_producer_points_are_production_bases_with_honest_precision(self):
        points = json.loads(
            (ROOT / "atlas-app/public/data/atlas-producers.geojson").read_text()
        )["features"]
        self.assertEqual(len(points), 8)
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
        self.assertEqual(
            by_entity["producer:domaine-cauhape"]["properties"]["precision"],
            "approximate",
        )
        self.assertIn(
            "Approximate location",
            by_entity["producer:domaine-cauhape"]["properties"]["placement_note"],
        )
        for entity_id in (
            "producer:camin-larredya",
            "producer:domaine-cauhape",
            "producer:clos-uroulat",
            "producer:domaine-de-souch",
        ):
            self.assertIn(entity_id, by_entity)
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
        self.assertEqual(entries["generated_from"], EXPERIENCE_LINEAGE)
        self.assertEqual(entries["release"], "atlas-run-07-editorial-foundation")
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

    def test_no_world_inherits_another_worlds_voice(self):
        """Run 07: each regional world authors its own copy; the app holds none."""
        editorial = json.loads(
            (ROOT / "atlas-app/public/data/atlas-editorial.json").read_text()
        )
        worlds = {
            subject_id: configured
            for subject_id, configured in editorial["subjects"].items()
            if configured.get("regional_world")
        }
        self.assertEqual(set(worlds), {"place:jura", "place:bearn"})
        for subject_id, world in worlds.items():
            self.assertEqual(
                set(world["pillar_copy"]),
                {"place", "grapes", "people", "culture", "rules"},
                subject_id,
            )
            for pillar, copy in world["pillar_copy"].items():
                self.assertTrue(copy.get("intro"), f"{subject_id}:{pillar}")
                self.assertTrue(copy.get("lede"), f"{subject_id}:{pillar}")
            for key in ("kicker", "title", "text", "button"):
                self.assertTrue(world["place_story"].get(key), f"{subject_id}:{key}")
            self.assertTrue(world["rules"].get("intro"), subject_id)
            self.assertTrue(world["rules"].get("groups"), subject_id)

        # No world's copy may be duplicated as another world's default.
        def pillar_text(world):
            return {
                copy["lede"] for copy in world["pillar_copy"].values()
            } | {world["place_story"]["text"], world["rules"]["intro"]}

        jura_copy = pillar_text(worlds["place:jura"])
        bearn_copy = pillar_text(worlds["place:bearn"])
        self.assertFalse(jura_copy & bearn_copy)

        # The application ships no regional prose of its own.
        app = (ROOT / "atlas-app/src/main.js").read_text()
        for sentence in sorted(jura_copy | bearn_copy):
            self.assertNotIn(sentence, app)
        # The retired Jura defaults must never return as any world's fallback.
        for retired in (
            "Five principal grapes share a compact region",
            "Jura's cultural pull is easiest to understand",
            "Five grapes \u00b7 several cellar paths",
            "Jura's six AOPs do not form a simple ladder",
            "A narrow foothill vineyard, not one uniform site",
        ):
            self.assertNotIn(retired, app, retired)

    def test_learner_copy_stays_out_of_project_vocabulary(self):
        """Run 07: Atlas never explains its own architecture to a learner."""
        app = (ROOT / "atlas-app/src/main.js").read_text()
        shell = (ROOT / "atlas-app/index.html").read_text()
        forbidden = (
            "machine authority",
            "Human Reference",
            "STRATA",
            "profile maturity",
            "governance status",
            "projection contract",
            "roadmap",
            "A fuller story can grow later",
            "Why this is interesting",
            "Three considered next moves",
            "Good places to begin",
        )
        for phrase in forbidden:
            self.assertNotIn(phrase, app, phrase)
            self.assertNotIn(phrase, shell, phrase)

    def test_about_atlas_panel_carries_the_worldview(self):
        """Run 07: About Atlas is reachable from Sources, not the primary nav."""
        shell = (ROOT / "atlas-app/index.html").read_text()
        app = (ROOT / "atlas-app/src/main.js").read_text()
        self.assertIn("data-about-dialog", shell)
        self.assertIn("A geographic way into wine.", shell)
        self.assertIn("Cartography, Ampelography, Relationships, Time, Access.", shell)
        # Expanded exactly once, and never promoted into the header actions.
        self.assertEqual(shell.count("Cartography, Ampelography"), 1)
        header = shell.split('<section class="map-stage"')[0]
        self.assertNotIn("data-about", header)
        self.assertIn("data-open-about", app)

    def test_editorial_foundation_is_repository_doctrine(self):
        """Run 07: the foundation is committed and cross-linked, not a loose file."""
        foundation = ROOT / "docs/atlas-editorial-foundation.md"
        self.assertTrue(foundation.is_file())
        copy = foundation.read_text()
        self.assertIn("Questions Worth Following", copy)
        for companion in ("README.md", "docs/carta-atlas.md"):
            self.assertIn(
                "atlas-editorial-foundation.md",
                (ROOT / companion).read_text(),
                companion,
            )

    def test_terrain_is_registered_as_a_governed_source_observation(self):
        """Run 08: relief exists because a pinned, licensed dataset exists."""
        manifest = json.loads(
            (
                ROOT / "data/geography/datasets/copernicus-dem-glo30-2022-05-09.json"
            ).read_text()
        )
        self.assertEqual(manifest["product_class"], "source_observation")
        self.assertEqual(manifest["retrieval_status"], "acquired")
        self.assertEqual(len(manifest["source_files"]), 6)
        for entry in manifest["source_files"]:
            self.assertRegex(entry["sha256"], r"^[a-f0-9]{64}$")
            self.assertTrue(entry["resource_url"].startswith("https://"))
        self.assertIn("EGM2008", manifest["measurement"]["vertical_reference"])
        self.assertIn("LE90", manifest["measurement"]["uncertainty"])
        self.assertTrue(manifest["measurement"]["scale_limitations"])
        self.assertTrue(manifest["refresh_policy"])
        self.assertEqual(
            manifest["license"]["redistribution"], "permitted_with_attribution"
        )
        self.assertIn("Copernicus WorldDEM-30", manifest["license"]["attribution_text"])
        # The raw elevation model is pinned, never committed.
        tracked = subprocess.run(
            ["git", "ls-files"], cwd=ROOT, check=True, capture_output=True, text=True
        ).stdout.splitlines()
        self.assertFalse([path for path in tracked if path.endswith((".tif", ".tiff"))])

    def test_every_public_terrain_asset_traces_back_to_source_and_recipe(self):
        self.assertEqual(self.summary["terrain_artifacts"], 3)
        self.assertEqual(self.summary["terrain_source_files"], 6)
        self.assertGreater(self.summary["terrain_contours"], 0)
        descriptor = json.loads(
            (ROOT / "atlas-app/public/data/atlas-terrain.json").read_text()
        )
        manifest = json.loads(
            (
                ROOT / "data/geography/datasets/copernicus-dem-glo30-2022-05-09.json"
            ).read_text()
        )
        self.assertEqual(descriptor["recipe"], manifest["transformations"])
        operations = [step["operation"] for step in descriptor["recipe"]]
        self.assertEqual(operations[0], "verify_pinned_source_files")
        self.assertIn("hillshade_horn", operations)
        self.assertIn("contour_elevation_surface", operations)
        self.assertEqual(
            descriptor["attribution"], manifest["license"]["attribution_text"]
        )
        paths = {artifact["path"] for artifact in manifest["derived_artifacts"]}
        self.assertEqual(
            paths,
            {
                "atlas-app/public/data/atlas-terrain-hillshade.png",
                "atlas-app/public/data/atlas-terrain-contours.geojson",
                "atlas-app/public/data/atlas-terrain.json",
            },
        )

    def test_terrain_adds_no_machine_authority_and_no_wine_claim(self):
        """Run 08: a picture of the ground never becomes a CARTA identity or claim."""
        schema = json.loads((ROOT / "schemas/spatial-dataset.schema.json").read_text())
        # The contract's fourth tier is deliberately not expressible as a dataset.
        self.assertEqual(
            set(schema["properties"]["product_class"]["enum"]),
            {
                "source_observation",
                "derived_spatial_product",
                "modeled_environmental_product",
            },
        )
        contours = json.loads(
            (ROOT / "atlas-app/public/data/atlas-terrain-contours.geojson").read_text()
        )["features"]
        for feature in contours:
            properties = feature["properties"]
            self.assertNotIn("carta_entity_id", properties)
            self.assertNotIn("human_reference_path", properties)
            self.assertEqual(properties["feature_type"], "elevation_contour")
        search = json.loads(
            (ROOT / "atlas-app/public/data/search-index.json").read_text()
        )
        self.assertFalse([record for record in search if "terrain" in record["id"]])
        subjects = json.loads(
            (ROOT / "atlas-app/public/data/atlas-subjects.json").read_text()
        )["subjects"]
        self.assertFalse([key for key in subjects if "terrain" in key])
        # The elevation dataset is evidence for a picture, never for a wine fact.
        for directory in ("data/entities", "data/claims", "data/relationships",
                          "data/geography/assertions", "data/geography/geometry"):
            for path in sorted((ROOT / directory).glob("*.jsonl")):
                body = path.read_text()
                self.assertNotIn("copernicus", body.casefold(), path.name)
                self.assertNotIn("glo30", body.casefold(), path.name)

    def test_relief_stays_subordinate_to_wine_geography(self):
        main = (ROOT / "atlas-app/src/main.js").read_text()
        config = json.loads((ROOT / "atlas-app/src/atlas-config.json").read_text())
        zoom = config["semanticZoom"]
        # Relief is inserted beneath the wine layers, never above them.
        self.assertIn("terrainInsertionPoint", main)
        self.assertIn('"aoc-areas-fill", "subject-areas-fill", "wine-region-halos"', main)
        # Relief arrives at regional scale and leaves before it becomes texture.
        self.assertLess(zoom["terrainMin"], zoom["terrainFull"])
        self.assertLessEqual(zoom["terrainFull"], 8.0)
        self.assertLess(zoom["terrainFadeOut"], zoom["terrainMax"])
        self.assertLessEqual(zoom["terrainMax"], 12.0)
        # Contours are sparse first, detailed only when a reader is reading landform.
        self.assertGreater(zoom["contourIndexMin"], zoom["terrainMin"])
        self.assertGreater(zoom["contourIntermediateMin"], zoom["contourIndexMin"])
        descriptor = json.loads(
            (ROOT / "atlas-app/public/data/atlas-terrain.json").read_text()
        )
        self.assertEqual(descriptor["contours"]["interval_metres"], 100)
        self.assertEqual(descriptor["contours"]["index_interval_metres"], 500)
        # Terrain takes no part in selection, inspection or routing.
        for handler in ("handleMapClick", "inspectPoint"):
            self.assertIn(handler, main)
        self.assertNotIn('"terrain-hillshade", "producer', main)
        self.assertNotIn("data-go-to-terrain", main)

    def test_atlas_survives_without_terrain(self):
        """Run 08: relief is context, so losing it must not cost the wine map."""
        main = (ROOT / "atlas-app/src/main.js").read_text()
        self.assertIn("state.terrainUnavailable", main)
        self.assertIn("terrainCoversView", main)
        # The terrain descriptor is fetched outside the required experience payload.
        experience = main.split("async function loadExperience()")[1].split("\n}")[0]
        self.assertNotIn("config.data.terrain", experience)

    def test_relief_control_is_learner_facing(self):
        shell = (ROOT / "atlas-app/index.html").read_text()
        self.assertIn("data-layer-terrain", shell)
        self.assertIn("<strong>Relief</strong>", shell)
        for machine_word in ("hillshade", "DEM", "raster", "Copernicus", "EPSG"):
            self.assertNotIn(machine_word, shell, machine_word)

    def test_terrain_foundation_is_repository_doctrine(self):
        foundation = ROOT / "docs/atlas-terrain-foundation.md"
        self.assertTrue(foundation.is_file())
        copy = foundation.read_text()
        self.assertIn("Terrain is context before it is interpretation", copy)
        for tier in (
            "Source observations",
            "Derived spatial products",
            "Modeled environmental products",
            "Interpretive wine knowledge claims",
        ):
            self.assertIn(tier, copy)
        for companion in ("README.md", "docs/carta-atlas.md"):
            self.assertIn(
                "atlas-terrain-foundation.md",
                (ROOT / companion).read_text(),
                companion,
            )

    def test_run_08_terrain_audit_is_committed(self):
        audit = ROOT / "audits/run-08-atlas-terrain-foundation.md"
        self.assertTrue(audit.is_file())
        copy = audit.read_text()
        self.assertIn("Copernicus DEM GLO-30", copy)
        self.assertIn("What was deliberately left out", copy)

    def test_run_06_generalization_assessment_is_committed(self):
        assessment = ROOT / "audits/run-06-bearn-jurancon-generalization-assessment.md"
        self.assertTrue(assessment.is_file())
        copy = assessment.read_text()
        self.assertIn("What transferred cleanly?", copy)
        self.assertIn("No sensory Tell", copy)


if __name__ == "__main__":
    unittest.main()
