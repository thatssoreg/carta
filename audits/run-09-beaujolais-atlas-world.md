# Run 09 — Beaujolais Atlas world

CARTA Atlas run 09. Global data-run number 16 for the narrowly required supporting claims and relationships. The release extends `data/atlas/run-08-beaujolais-canonical-ingestion.json` and consumes the authority merged by PR #39 rather than rebuilding it.

**Starting HEAD:** `384acc46b0fa2e492e8c2799d175b425a71ed180` — *Merge pull request #39 from thatssoreg/beaujolais-canonical-ingestion*.

**Branch:** `atlas-beaujolais-world`.

This run turns the governed Beaujolais subjects into CARTA's third mature regional-world proof, after Jura and Béarn / Jurançon. It also applies the terrain architecture established by PR #38 to one bounded Beaujolais extent. It creates neither a parallel truth store nor a second terrain pipeline.

## What the world argues

**Hero kicker:** *One grape · many places · a reputation still moving*

**Thesis:** Gamay accounts for 96% of the region's 2024 grape distribution. That apparent sameness is the reason to look harder: broad Beaujolais, a Villages mention and ten crus cross different hills and geological families, while Nouveau and several cellar paths keep changing what the same regional name can mean.

**Core learner question:** *How can one grape make the map more important, not less?*

The same grape is the thread through the world, not its universal explanation. The experience deliberately refuses the reductions “Beaujolais = granite,” “Beaujolais = Nouveau,” “Beaujolais = carbonic,” and “Beaujolais = the Gang of Four.”

## Five pillars

1. **Place** reads the long corridor between higher western country and the Saône plain, then interrupts it with Mont Brouilly, Py hill, Fleurie / Chiroubles, and the southern country around Charnay. Physical landforms, geological claims, and regulatory areas remain visibly different kinds of knowledge.
2. **Grapes & Wines** uses the dated 96% Gamay / 4% Chardonnay distribution to make dominance and minority structure legible. Gamay opens genetics, history, ten crus, Nouveau, and cellar choice; Chardonnay opens white-wine law and a meaningful southern route.
3. **People** gives five producers five different teaching jobs rather than presenting a ranking: transmission and succession; evidentiary discipline around influence; continuity outside the natural-wine frame; a producer-specific carbonic protocol; and southern Chardonnay plus operational transition.
4. **Culture** treats Nouveau and the Gang of Four as consequential but incomplete mechanisms. It does not tell a false decline-and-rescue story.
5. **Rules** teaches one broad AOC, the governed Villages mention, ten independent crus, current colour and grape permissions, and the bounded Nouveau mention. Legal names identify regulated origin and production, not vineyard parcels, quality rank, or a universal fermentation method.

## Questions Worth Following

Five entry questions provide movement with claim-backed payoffs:

- *How can one grape make the map more important, not less?* — Beaujolais → Gamay → regional and cru geography.
- *How did a wine released within weeks shape the whole region's recognition?* — Beaujolais → Nouveau → rules and chronology.
- *What does “carbonic” actually tell you about a Beaujolais?* — carbonic → semi-carbonic → whole cluster → producer examples.
- *What did the 1395 Gamay ordinance change—and what did it not?* — Gamay → historical event → explicit movement to Burgundy → context return.
- *Why does one hill carry two cru names?* — Mont Brouilly → Brouilly / Côte de Brouilly → Château Thivin.

## Spatial teaching moments

Four data-authored subject-linked camera moments use one reusable map-view contract:

- **Mont Brouilly** places the physical hill beside Brouilly and Côte de Brouilly without making the hill a vineyard or either cru a planted-area polygon.
- **Morgon / Py** keeps Morgon, Py hill, and Côte du Py distinct and opens Lapierre and Foillard as producer routes. No Côte du Py polygon was invented.
- **Fleurie / Chiroubles** compares neighboring hill positions without translating elevation into freshness or quality.
- **Charnay / southern Beaujolais** connects quieter relief, supported sedimentary context, Chardonnay, and Terres Dorées so that the world does not end at the northern crus.

Click priority is data-authored: every cru outranks the Villages mention, which outranks broad Beaujolais. The broader regulatory context stays visible. All ten crus remain independent native subjects.

## Terrain extension

The existing `spatial-dataset:copernicus-dem-glo30-2022-05-09` source observation now records two explicit, discontinuous governed tile groups. The outer manifest envelope is not represented as coverage.

Two source tiles were added for Beaujolais:

| Tile | Bytes | SHA-256 |
|---|---:|---|
| `Copernicus_DSM_COG_10_N45_00_E004_00_DEM.tif` | 43,229,419 | `ccebea0a93d3ba6bfa3da64e1c309d7b80ba306ee8d1808ce9cbba7bd8b4c27f` |
| `Copernicus_DSM_COG_10_N46_00_E004_00_DEM.tif` | 43,469,680 | `d5efb23bfc44cba0d4b05b633786839b1614f0530491b96bba1868db2ea04f05` |

The bounded proof extent is `[4.05, 45.55, 4.98, 46.48]` in EPSG:4326. It covers southern Beaujolais through the ten-cru corridor, the higher western country, and Saône-facing low country; it is explicitly not a wine boundary.

The existing recipe produces a 691 × 994 Web Mercator relief image at 150 m per pixel and 213 sparse 100 m contours, with 500 m index contours. Elevation in the display grid runs from 149.0 m to 1,010.2 m. The Beaujolais products are:

| Asset | Bytes | Shape / count |
|---|---:|---|
| `atlas-terrain-beaujolais-hillshade.png` | 340,862 | 691 × 994 pixels |
| `atlas-terrain-beaujolais-contours.geojson` | 287,304 | 213 features |

The shared terrain descriptor now contains a `terrains` array. Each proof is lazy-loaded only when the viewport intersects that proof at a supported zoom. A France overview and the space between Béarn and Beaujolais therefore acquire no invented terrain surface. The same Relief control governs whichever bounded proof is loaded; all terrain remains below wine layers, unclickable, unsearchable, and absent from the subject graph.

Regeneration rewrote the inherited Béarn / Jurançon PNG's compressed bytes under the current image library, but a decoded RGBA comparison against starting commit `384acc4` is exact: 1,485 × 1,121 and no differing pixel. Its contour GeoJSON is byte-identical. This is a packaging rewrite, not a visual or evidentiary change.

The doctrinal boundary is unchanged: **terrain is context before it is interpretation**. No elevation or contour authorises a statement about flavour, freshness, quality, drainage, ripening, exposure, vineyard ownership, or planted extent.

## Nouveau, time, and cellar literacy

Nouveau receives a compact Then / Now lens whose two sides are explicitly not a continuous statistical series. The historical side records the specification's recalled mid-1980s peak near 500,000 hl and its statement that primeur never exceeded half of regional production. The current side records the bounded legal role for qualifying red and rosé Beaujolais, not white. The subject timeline carries early trade context, the 1951 turning point, the 1985 third-Thursday convention, and the current rule without calculating a synthetic decline percentage.

Carbonic maceration, semi-carbonic maceration, and whole-cluster fermentation have separate native subjects and first-use glossary definitions. A shared practice comparison states that whole cluster is handling, semi-carbonic is a related fermentation path, and deliberate external CO₂ is another process choice. Lapierre, Grand'Cour, and Terres Dorées provide bounded producer examples; no process is presented as appellation law or a universal Beaujolais recipe.

## People and culture

- **Domaine Marcel Lapierre** teaches direct Chauvet transmission, semi-carbonic detail, selective sulfur, and family succession in Morgon.
- **Jean Foillard** separates an individual producer from Gang shorthand and preserves “influence” rather than inventing mentorship or mutable acreage facts.
- **Château Thivin** is the human route through Mont Brouilly, Brouilly, Côte de Brouilly, and long family continuity outside the natural-wine frame.
- **Domaine de la Grand'Cour** makes an explicitly CO₂-saturated whole-bunch protocol producer-specific while distinguishing a domaine base, named-site relationships, and holdings.
- **Domaine des Terres Dorées** carries southern geography, Chardonnay, a different cellar history, and the documented 2024 operating transition while leaving conflicting total-acreage arithmetic unresolved.

The Gang of Four is presented as Kermit Lynch's useful shorthand for Lapierre, Foillard, Guy Breton, and Jean-Paul Thévenet in a Chauvet-associated community of practice. It is not a formal organisation and does not prove equal bilateral collaboration among all four.

## Cross-region rabbit hole

Gamay opens the historically bounded 1395 ducal ordinance. `Explore` preserves the Beaujolais map; only the explicit Burgundy connection moves geography. When Burgundy is active the shared context-return contract offers **Back to Gamay in Beaujolais**. The route corrects a simplified banishment myth without translating medieval ducal territory into current Burgundy geometry. No false `RELATED_TO` or other Reference relationship was created merely to support the editorial route.

## Shared architecture changes

Beaujolais exposed small reusable gaps, addressed without a regional branch:

- editorial subjects may declare a generic `map_view` target, and all map movement paths consume the same subject-target helper;
- regional worlds may author subject-linked `map_moments`, pillar map reactions, and producer reactions in release data;
- Then / Now, timeline, comparison, and practice-example renderers consume generic editorial fields;
- the prior Jura area comparison moved out of application code into release data;
- terrain descriptors may contain multiple named extents, each with dynamic source/layer IDs and independent lazy-load/failure state;
- `geographic_extent.regions` records disconnected acquisitions without pretending their outer envelope is coverage.

No Beaujolais-specific frontend conditional, subject type, pillar, rendering system, or terrain pipeline was added. Jura and Béarn / Jurançon continue through the same contracts.

## Narrow authority additions

Implementation exposed three genuine omissions and two source-described spatial relationships. Run 16 adds claims for the physical corridor, a restrained north/south geological-family contrast, and the source-described Chardonnay area at Terres Dorées; it adds supported `OVERLAPS` relationships for Brouilly / Mont Brouilly and Morgon / Py hill. These relationships describe supported overlap, not vineyard parcel geometry. No rejected research claim entered the learner projection.

## Browser acceptance

The production build received a real browser pass at 1440 × 900 and 390 × 844. Both sizes loaded the live basemap, the generated learner data, and meaningful guide content without a Vite error overlay, page error, warning, or horizontal overflow.

Desktop acceptance covered:

- Beaujolais arrival, persistent map, five-pillar guide, source dialog, attribution, evidence disclosures, rabbit trail, and back behavior;
- viewport-scoped terrain loading: Beaujolais requested only its own hillshade, Béarn requested only its own hillshade in a fresh session, and a deliberately aborted Beaujolais relief request left the guide, wine map, and Relief control usable;
- Relief opt-out and restoration from the shared Layers control, with relief beneath strong wine-area fills;
- Mont Brouilly, Morgon / Py, Fleurie / Chiroubles, and Charnay / southern Beaujolais camera moments, including visible producer points and no invented site polygon;
- all ten cru controls, each resolving to its own native subject, plus the independent Villages mention and broad Beaujolais subject;
- Lapierre, Foillard, Thivin, Grand'Cour, and Terres Dorées `Explore` / explicit `Show on map` behavior, including the intended approximate or exact producer placement language;
- the carbonic glossary definition; separate carbonic, semi-carbonic, and whole-cluster subjects; and all three producer practice examples;
- Nouveau Then / Now and all five timeline labels, with the different-scope warning and no synthetic decline rate;
- the complete Beaujolais → Gamay → 1395 ordinance → explicit Burgundy move → **Back to Gamay in Beaujolais** route; and
- the source dialog's terrain dataset meaning and the full map attribution.

Mobile acceptance at 390 × 844 confirmed a 390 px document width, a readable bottom-sheet guide over a persistent map, one initially open regional pillar, 44 px map-moment controls, the complete Nouveau Then / Now and five-step timeline, and the cross-region context return. The return control measured 44 px high, was the topmost hit target at its centre, and restored both `Gamay noir à jus blanc` and the `Beaujolais` map breadcrumb. No browser warning or error was logged.

The pass exposed and fixed two shared interaction defects: explicit `Go to current subject` movement now refreshes the place breadcrumb, and a context-return control can no longer be covered by the following hero's negative margin. Regression assertions cover both fixes.

## Validation

The release is gated by structured-data validation, Atlas validation, the full unit suite, navigation audit, deterministic Human Reference / Atlas / terrain regeneration, the production build, and the browser acceptance above.

- `python3 scripts/validate_data.py` — **PASS**: 552 entities, 619 relationships, 521 claims, 342 sources, 37 names, 53 geometry records, 89 spatial assertions, and 202 profiles.
- `.venv-atlas/bin/python scripts/build_atlas.py` — **PASS**: 258 countries, 1,320 AOC, 165 IGP, five regional labels, 40 mapped and 1,445 unmapped INAO features, 1,544 search records, 38 guides, 88 native subjects, 38 editorial subjects, and 13 producer points.
- `.venv-atlas/bin/python scripts/build_terrain.py` — **PASS**: Béarn / Jurançon 1,485 × 1,121 with 1,016 contours; Beaujolais 691 × 994 with 213 contours; all eight pinned inputs verified.
- `python3 scripts/validate_atlas.py` — **PASS**: four manifests, 1,485 relevant INAO features with zero ambiguous mappings, 41 mapping rows, 40 geometries, five terrain artifacts, 1,229 contours, two extents, eight source files, and 2,860,369 generated terrain bytes.
- `python3 -m unittest discover -s tests -p 'test_*.py'` — **PASS**: 45 tests.
- `python3 scripts/audit_navigation.py --ratings audits/run-10-human-reference-navigation-ratings.json` — **PASS**.
- deterministic regeneration — **PASS**: the complete working diff was byte-for-byte identical before and after Human Reference, Atlas, and terrain regeneration.
- `npm run build --prefix atlas-app` — **PASS**: production assets built successfully; Vite's advisory chunk-size warning is non-blocking.
- `git diff --check` — **PASS**.

Current measured Atlas totals after generation: 258 countries, 1,320 AOC features, 165 IGP features, 40 mapped and 1,445 intentionally unmapped INAO features, 1,544 search records, 38 guides, 88 native subjects, 38 editorial subjects, five entry points, 13 producer points, two terrain extents, eight pinned terrain files, and 1,229 contours. Structured authority currently validates at 552 entities, 619 relationships, 521 claims, 342 sources, 37 names, 53 geometry records, 89 spatial assertions, and 202 profiles.

## Known limitations and deliberate deferrals

- Py hill and Mont Brouilly have supported overlap relationships but no site or vineyard polygons; Côte du Py remains a named-site subject without fabricated geometry.
- There is no geology overlay. Geological distinctions remain claim-backed prose and map positioning; institutional graphics were not redistributed.
- Copernicus DEM is a surface model and cannot resolve parcels, terraces, walls, row orientation, or viticultural mechanism. It fades before parcel-scale reading.
- The two Beaujolais tiles carry programme-level uncertainty only; no unverified tile-mask precision is asserted.
- Métras, Foillard acreage/certification reconciliation, proposed Premier Cru status, vineyard holdings, climate trends, hydrology, and weather remain out of scope.
- Mutable producer facts retain dates and bounded language; Terres Dorées' unresolved total-acreage arithmetic is not silently reconciled.
- Terrain covers exactly two disconnected proofs. There is no France-wide surface.

## Files added and changed

The focused change adds the inherited run-09 Atlas release, three run-16 claims, two run-16 relationships, Beaujolais hillshade and contours, and this audit. It updates the shared Atlas generator, terrain generator, Atlas validator, spatial-dataset schema and manifest, application data/config/rendering/styles, generated Human Reference pages affected by the new authority, regression tests, and the durable Atlas / terrain documentation. Raw DEM files remain ignored build inputs and are not committed.

## Deferred follow-up

No deferred item blocks the bounded world. Future work may acquire properly licensed geology, hydrology, or modeled climate only through the environmental-data contract; reconcile mutable producer facts through new source review; or add site geometry when provenance exists. None should be inferred from this release's terrain or editorial routes.
