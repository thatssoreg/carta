# Run 08 — Atlas terrain foundation

CARTA Atlas run 08. Global data-run number 14 (`data/sources/run-14-atlas-terrain-foundation.jsonl`); the audit and the release identifier follow the Atlas run counter, as run 06 and run 07 did.

**Starting HEAD:** `0601b4868cedfd01483676fd9eb153c244e16df3` — *Merge CARTA Atlas editorial foundation*.

This run establishes the first governed terrain and environmental-data foundation for CARTA and proves it in one bounded geographic world: Béarn / Jurançon and the western Pyrenean foothills. It expands no editorial content, adds no wine knowledge, and touches no existing appellation geometry.

## The contract created

[`docs/atlas-terrain-foundation.md`](../docs/atlas-terrain-foundation.md) is the canonical environmental-data doctrine. It establishes four tiers and the boundary between them:

1. **Source observations** — measured datasets, acquired under an identified licence.
2. **Derived spatial products** — deterministic transformations that add no information (hillshade, contours, slope, aspect, reprojection).
3. **Modeled environmental products** — reserved, unused, and deliberately so: climate normals, interpolated surfaces, modeled exposure.
4. **Interpretive wine knowledge claims** — not expressible as spatial datasets at all. They stay in `data/claims/` under the evidence policy.

Canonical principle: **terrain is context before it is interpretation.** A hillshade may make a landform legible. It never authorises a statement about grape growing, ripening, drainage, exposure, climate or wine quality.

The fourth tier is enforced structurally rather than by convention: `product_class` in the spatial dataset schema has no value an interpretive claim could occupy, and no field that could carry one.

## Schema change

`schemas/spatial-dataset.schema.json` moves to **v0.2**. CARTA's existing spatial dataset model was extended rather than duplicated; there is still one manifest directory, one provenance document, one source register, one validator. Additions, all optional so the three existing manifests validate unchanged:

| Addition | Purpose |
|---|---|
| `product_class` | Which contract tier the dataset occupies. |
| `derived_from` (dataset level) | Dataset-to-dataset lineage; required for tiers 2 and 3. |
| `measurement` | `variable`, `unit`, `vertical_reference`, `native_resolution`, `uncertainty`, `scale_limitations`. |
| `geographic_extent` | The bounded extent acquired, and why it is bounded. |
| `source_files` | Per-file URL, byte count and SHA-256 for multi-file acquisitions. |
| `refresh_policy` | Whether the pinned snapshot is expected to move. |
| `retrieval_status: "derived_in_repository"` | Reserved for a future standalone modeled product. |
| `derived_artifacts[].product_class`, `.derived_from`, `.pixel_width`, `.pixel_height` | Per-asset tier, lineage and raster shape. |

The `acquired` integrity rule now accepts *either* a single archive checksum *or* per-file checksums, so a six-tile acquisition is pinned honestly instead of behind a synthetic digest.

## Terrain source: evaluated and selected

### Selected — Copernicus DEM GLO-30 Public

`spatial-dataset:copernicus-dem-glo30-2022-05-09`

- Digital **surface** model derived from TanDEM-X acquisitions 2011–2015.
- 1 arc-second grid: ≈30 m north–south, ≈23 m east–west at 43°N.
- EPSG:4326 (WGS84-G1150) horizontal; EGM2008 (EPSG:3855) vertical.
- Acquired from the AWS Open Data cloud-optimised mirror, which repackages `COP-DEM_GLO-30-DGED` by dropping the shared east/south edge row and column (3601→3600) and adding overviews. The mirror publishes no ESA release identifier, so the manifest pins the **2022-05-09 mirror snapshot** rather than asserting a release number CARTA cannot verify.
- Six 1°×1° tiles, **251,345,786 bytes** total. Every file is pinned by SHA-256 in `source_files`, and each downloaded byte stream was additionally checked against the object ETag the mirror publishes — all six matched, so the acquired bytes are provably the upstream bytes.
- Measured uncertainty is available per tile from the Copernicus accuracy masks: absolute vertical accuracy **LE90 1.741–1.971 m** (LE68 1.468–1.642 m) across the six tiles, against 278–3,985 ICESat control points each. Programme specification is LE90 < 4 m vertical, CE90 < 6 m horizontal.

Chosen because it balances trustworthy provenance, an unambiguous free-and-open licence, single-vintage consistency across the whole proof area, sufficient resolution with headroom, a bounded and cheap acquisition, and — decisively — **global portability**. CARTA Atlas will not stay inside France, and a France-only elevation dependency would have to be replaced the first time a world sits in Spain, Portugal, Italy, Austria, Germany, Chile or the United States. Irouléguy already sits on the border this dataset crosses without a second acquisition path.

**Licensing implication.** The Copernicus WorldDEM-30 licence grants worldwide, royalty-free, unlimited-time rights to reproduce, distribute, communicate, adapt and combine, with no commercial restriction, on condition that the copyright notice and the liability disclaimer travel with the data. Because CARTA redistributes an *adapted* product, the required notice is the adaptation form:

> produced using Copernicus WorldDEM-30 © DLR e.V. 2010-2014 and © Airbus Defence and Space GmbH 2014-2018 provided under COPERNICUS by the European Union and ESA; all rights reserved. The organisations in charge of the Copernicus programme by law or by delegation do not incur any liability for any use of the Copernicus WorldDEM-30.

That exact string is the manifest's `license.attribution_text`, is repeated verbatim in the terrain descriptor, is attached to the map's attribution control, and appears in the Sources dialog through `provenance.json`. Validation fails if the manifest and the descriptor ever disagree.

### Rejected — IGN RGE ALTI

France's authoritative terrain model, 1 m and 5 m DTM, Licence Ouverte 2.0. Rejected on three counts:

- **Volume wildly beyond need.** Pyrénées-Atlantiques (D064) alone is **10,214,166,788 bytes** at 1 m, delivered as three split `.7z` archives; the 5 m product is still **422,799,101 bytes** for one department. The Béarn world's appellations also reach into D065, D032 and D040, so a real acquisition is several departments. The Atlas displays relief at roughly 110 m; acquiring a 1 m model to draw it is precisely the "enormous raster merely because it is available" this run was told to avoid.
- **France-only.** No portability beyond the first country.
- **Delivery format.** ASCII grids in `.7z` archives, in Lambert-93 / IGN69 — a second CRS and vertical datum to reconcile, in an archive format the repository already refuses to track.

Its genuine advantage is recorded honestly: RGE ALTI is a *terrain* model, so it does not carry canopy and buildings the way a surface model does. That advantage does not outweigh the three costs at the scale Atlas renders.

### Rejected — IGN BD ALTI v2 (25 m)

The practical IGN alternative, and much closer in size: the four relevant departments total **126,713,065 bytes** (D032 28,482,623 · D040 30,022,481 · D064 39,028,842 · D065 29,179,119). Rejected because it is departmental in more than file layout — those four archives carry **three different vintages** (D065 2020-02-11, D032 2021-02-11, D040 and D064 2021-04-19). A Béarn mosaic would silently blend three survey epochs across a region whose whole point is continuity of landform, and CARTA would have to describe that seam in every provenance statement. Copernicus gives one acquisition window for the entire proof area. Still France-only.

### Rejected — Copernicus DEM GLO-90

Same programme, same licence, same provenance quality, roughly one ninth the acquisition. Rejected because it offers no headroom: at 90 m it is already at the limit of the display grid this run produces, and any later move toward site-scale relief would require re-acquiring at 30 m anyway. The saving was not worth a permanently coarser foundation.

### Rejected — runtime terrain-tile services

Hosted terrain-RGB and shaded-relief services (commercial tile APIs, and the public AWS terrain tile set) were considered and rejected: they introduce a runtime dependency and, in the public case, a composite lineage stitched from several national elevation models. CARTA could not answer "which source version produced this pixel" for a composite tile, which is the question this contract exists to answer.

## The Béarn / Jurançon proof

**Geographic extent proved:** `[-1.75, 42.70, 0.25, 43.80]` (EPSG:4326) — 2.00° × 1.10°.

It covers Jurançon, Béarn, Pacherenc du Vic-Bilh and Irouléguy with margin, the Gave de Pau and Gave d'Oloron corridors, the Landes plateau to the north-west, and enough of the Pyrenean front to the south that the foothills read as foothills rather than as bumps.

**Display grid:** 1,485 × 1,121 pixels in EPSG:3857 at 150 m per pixel, ≈109 m ground resolution at 43.25°N. Elevation across the derived grid runs from −60.1 m to 3,221.6 m.

The grid is Web Mercator, not plate carrée, so the rendered image's corner coordinates are its true corners and MapLibre places it without projective warping error. Slope is computed with a per-row `cos(latitude)` correction, because a Mercator cell is `1/cos(latitude)` too wide in ground terms and the same hill would otherwise look steeper further north.

### Processing recipe

Every parameter below is pinned in the manifest's `transformations` and republished verbatim as the descriptor's `recipe`; validation fails if the two drift apart.

1. `verify_pinned_source_files` — SHA-256 on all six tiles; refuse to derive anything on mismatch.
2. `mosaic_and_clip_source_observation` — clip to the proof extent with a 0.05° buffer, snapped to the source sample grid. Snapping matters: an unaligned clip put the mosaic on an offset grid and left a one-pixel seam at every tile join.
3. `reproject_to_display_grid` — EPSG:3857, 150 m, `average` resampling.
4. `hillshade_horn` — azimuth 315°, altitude 45°, z-factor 1.0, Mercator scale correction on.
5. `quantise_to_shadow_and_light_overlay` — response scale 0.32, shadow γ 0.62 to max α 0.38 in ink `rgb(58,51,44)`, light γ 1.30 to max α 0.07 in `rgb(255,253,248)`, 32 alpha steps per side, 5.5% cosine edge feather, written as an 8-bit paletted PNG with per-index alpha.
6. `contour_elevation_surface` — two passes of 3×3 binomial smoothing, 100 m interval, 500 m index interval, 140 m simplification tolerance, 2,500 m minimum length, 5-decimal coordinates.

The overlay only ever darkens or lightens; it paints no colour of its own across the map. The response scale and gamma were tuned on the Jurançon foothills specifically: with a linear response the vineyard slopes were invisible while the mountains saturated. The edge feather exists so the relief patch dissolves at the limits of CARTA's data instead of ending in a rectangle.

### Derived assets

| Asset | Format | Bytes | Shape |
|---|---|---:|---|
| `atlas-app/public/data/atlas-terrain-hillshade.png` | PNG-8 + alpha | 860,720 | 1,485 × 1,121 |
| `atlas-app/public/data/atlas-terrain-contours.geojson` | GeoJSON | 1,368,060 | 1,016 features, 44,131 vertices |
| `atlas-app/public/data/atlas-terrain.json` | JSON | 3,683 | extent, placement, intervals, attribution, recipe |

Contours split 187 index (500 m) and 829 intermediate (100 m). Both terrain assets are lazy-loaded, and only once the viewport actually intersects the proof extent at a zoom where relief is drawn, so a France overview pays nothing for them.

## Atlas behaviour added

**Relief is on by default inside its extent, with a learner-facing control to switch it off.** That decision follows the editorial foundation rather than convention: the Atlas's whole argument is that wine geography is a consequence of ground, and Béarn's argument is a foothill argument. An opt-in layer would mean most readers never meet the thing that explains where they are. The control exists because a reader comparing legal boundaries deserves a clean sheet of paper on request.

The control is labelled **Relief** — "Shaded slopes and contour lines, where the ground is mapped" — in the existing Layers panel, beside AOC areas, IGP areas, wine-region guides and producer bases. No machine vocabulary is exposed: the words *hillshade*, *DEM*, *raster*, *Copernicus* and *EPSG* appear nowhere in the shell.

Display thresholds (`atlas-config.json`):

| Behaviour | Zoom |
|---|---|
| Relief begins to appear | 6.2 |
| Relief at full strength | 7.4 |
| Relief begins to fade | 10.6 |
| Relief gone | 11.8 |
| 500 m index contours appear | 8.2 |
| 100 m contours appear | 9.9 |
| Contours gone | 12.4 |

Relief therefore arrives as the map approaches the regional scale and is fully present when a reader enters Béarn, then withdraws before a ~109 m grid could pretend to be parcel-scale information.

Subordination is structural, not stylistic: terrain layers are inserted beneath `aoc-areas-fill`, so appellation fills, boundaries, region anchors, producer points and every label sit above the relief. Terrain layers appear in no hover, click, inspection, search, route, question or rabbit-hole query. Terrain is never a CARTA subject.

## Validation performed

- `python scripts/validate_data.py` — structured authority and Human Reference generation.
- `python -m unittest discover -s tests` — full suite, including nine new terrain regression tests.
- `python scripts/validate_atlas.py` — manifests, mappings, semantics, assets, and the new terrain contract.
- `npm ci && npm run build` in `atlas-app/` — production build.
- `python scripts/audit_navigation.py --ratings audits/run-10-human-reference-navigation-ratings.json` — navigation regression fixture.
- `python scripts/validate_data.py --write-human-reference && git diff --exit-code` — deterministic Human Reference regeneration.
- `python scripts/build_terrain.py` run twice with a clean `git diff` between runs — deterministic terrain regeneration.

What the terrain validation proves specifically:

- the elevation dataset is registered as a **source observation**, acquired, with vertical reference, published uncertainty, stated scale limitations, refresh policy and six per-file checksums;
- every public terrain asset declares its tier and a `derived_from` lineage, and every lineage reference resolves to a registered dataset or a sibling artifact;
- the PNG's real IHDR dimensions match the manifest, and the descriptor's placement corners match its stated image extent and cover the proof extent;
- the published recipe is byte-identical to the manifest transformations, and the descriptor's attribution is byte-identical to the licence's required notice;
- every contour sits on the declared interval, carries the correct index/intermediate class, and carries **no** `carta_entity_id` and **no** Human Reference path;
- no CARTA geometry record cites the elevation dataset as authority;
- no entity, claim, relationship, spatial-assertion or geometry record cites the elevation dataset or its source, and neither the search index nor the subject projection contains a terrain record;
- the zoom thresholds are ordered, and relief does not outlive its contours;
- no `.tif` or `.tiff` is tracked by Git — the raw rasters are added to the raw-GIS refusal set alongside `.zip`, `.7z`, `.shp`, `.dbf`, `.shx` and `.gpkg`.

## Performance observations

- New payload: **2,232,463 bytes (2.13 MiB)** across three assets, against 7.85 MB for the existing AOC layer. Text assets compress heavily in transit; the PNG is already compressed.
- Nothing is fetched until the viewport intersects the terrain extent at a relief zoom. Entering France, or any of the four other worlds, downloads none of it.
- The shaded relief is a single MapLibre `image` source: one HTTP request, one texture, no tiling infrastructure, and no third-party runtime dependency. A tiled or PMTiles delivery would add operational complexity to solve a problem this proof does not have.
- The contour source is a single GeoJSON with two filtered line layers; both are simple `line` layers with zoom-interpolated width and opacity.
- Full terrain rebuild from the pinned tiles: about seven seconds.

## Files added and changed

**Added**

- `docs/atlas-terrain-foundation.md`
- `scripts/build_terrain.py`
- `data/geography/datasets/copernicus-dem-glo30-2022-05-09.json`
- `data/sources/run-14-atlas-terrain-foundation.jsonl`
- `atlas-app/public/data/atlas-terrain-hillshade.png`
- `atlas-app/public/data/atlas-terrain-contours.geojson`
- `atlas-app/public/data/atlas-terrain.json`
- `audits/run-08-atlas-terrain-foundation.md`

**Changed**

- `schemas/spatial-dataset.schema.json` — v0.2 environmental extension.
- `scripts/build_atlas.py` — provenance is projected from every registered manifest instead of a hardcoded three, so the two build scripts produce the same document.
- `scripts/validate_atlas.py` — artifact lineage resolution, terrain contract validation, raw-raster refusal.
- `tests/test_atlas.py` — nine terrain regression tests.
- `atlas-app/src/atlas-config.json`, `atlas-app/src/main.js`, `atlas-app/index.html` — relief layers, thresholds, control, lazy loading, graceful degradation.
- `atlas-app/public/data/provenance.json` — now carries the terrain dataset.
- `README.md`, `docs/carta-atlas.md` — cross-links and the terrain build step.
- `requirements-atlas.txt` — `rasterio`, `pillow`, `contourpy` pinned.
- `.github/workflows/validate.yml` — compile the new build script.

Nothing in `atlas/`, `data/entities/`, `data/claims/`, `data/relationships/`, `data/geography/geometry/`, `data/geography/assertions/` or `data/atlas/` changed. No appellation geometry moved.

## Known limitations

- **Copernicus DEM is a surface model.** It records canopy and buildings as if they were ground. In the wooded Béarn foothills, a few metres of apparent relief is trees. Acceptable for reading landform at this scale, and recorded in `measurement.scale_limitations` rather than hidden.
- **The display grid is ~109 m.** It cannot resolve a parcel, a terrace, a wall or a row orientation, which is why relief fades out by zoom 11.8.
- **The proof extent is a rectangle** and terrain exists nowhere else in the Atlas. The edge feather makes the limit read as a limit rather than as a coastline, but it is still a limit.
- **A local source artefact survives into the derived grid**: a small depression reaching −60 m near 1.00°W / 43.49°N in the Landes, about 14 pixels below −5 m. It is in the published Copernicus tiles, it is far from any vineyard, and it is left uncorrected rather than quietly patched — editing a source observation to look tidier is exactly what the contract forbids.
- **Determinism is verified against the pinned dependency set** (`requirements-atlas.txt`, Python 3.12). Outputs are quantised — 32 alpha steps, 5-decimal coordinates, 140 m simplification — so ordinary floating-point variation between library builds does not change the bytes, but the guarantee is stated against the pinned versions.
- **The acquisition is not automated.** `build_terrain.py` verifies the pinned tiles and refuses to run without them; it does not fetch them. The manifest carries each file's exact URL, byte count and checksum.

## What was deliberately left out

- No France-wide, or even department-wide, terrain ingestion. Six tiles, one world.
- No geology, no soils, no climate surfaces, no weather, no hydrology layer.
- No slope or aspect exposed as learner-facing products. Both are computed inside the hillshade derivation, which is all the architectural proof the contract needed; publishing a slope map would have invited exactly the causal reading the doctrine forbids.
- No solar-exposure or vineyard-parcel modelling.
- No modeled environmental products at all. Tier 3 is reserved and empty on purpose.
- No new editorial copy, no new regional worlds, no new producer or grape research.
- No change to the landing page, Questions Worth Following, About Atlas, machine authority, or existing legal geometry.
- No terrain-derived claim anywhere. The Béarn and Jurançon profiles say exactly what they said before this run.

## Recommended next run

**Hydrology, in the same extent, as the second environmental layer.**

The Béarn world is organised by its gaves — Jurançon sits between the Gave de Pau and the Gave d'Oloron, and the western Pyrenees page has been asking for watershed divides and drainage systems since Run 02. Hydrology is the layer that makes the relief already on the map *legible* rather than merely visible: a reader who can see valleys but cannot see which way the water runs is still reading a texture.

It is also the right second test of the contract, because it is a different acquisition shape. Elevation arrived as one global raster from one publisher; hydrology arrives as national vector networks with national identifiers, which is where `derived_from` lineage, per-file checksums and `authority_class` will be put under real pressure. And it stays firmly in tiers 1 and 2, so the reserved modeled tier stays empty until something genuinely modeled — climate normals being the obvious candidate after that — actually needs it.
