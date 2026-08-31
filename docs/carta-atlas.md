# CARTA Atlas

CARTA Atlas is the geographic way into CARTA.

It should feel familiar before it feels novel: a person can begin with the world, orient to a country, understand ordinary geography, and then move through wine regions, subregions, appellations, places, vineyards, producers, grapes, and relationships at progressively finer scales.

The goal is not to make another decorative wine map. The goal is to make wine geography easier to understand while letting CARTA's deeper spatial, temporal, relational, legal, terroir, and ampelographic knowledge become visible when it is useful.

This document decides what Atlas *is*. The [Atlas editorial foundation](atlas-editorial-foundation.md) decides what Atlas *says*: its thesis, its voice, the registers a reader must be able to tell apart, and the rule that every regional world argues its own case rather than inheriting another world's copy. Learner-facing copy and every new regional world are governed there, and the checklist in its final section runs before a world ships.

The [Atlas terrain and environmental data contract](atlas-terrain-foundation.md) decides what Atlas is allowed to know about the ground: which elevation, relief and future environmental products may be registered, how each one keeps its provenance and its recipe, and the rule that terrain is context before it is interpretation. Physical relief never authorises a wine claim on its own.

## France-first v0.1

The working product slice follows this path:

**world → France → governed wine-region orientation → sourced appellation area → feature detail → Human Reference**

The initial world is an ordinary OpenFreeMap Liberty basemap with a small Natural Earth interaction layer. Entering France lazy-loads the default INAO AOC/AOP geography and five defensible governed region anchors derived from mapped child appellations. IGP remains a separate, off-by-default layer. Search covers every rendered INAO denomination and the governed region anchors.

The app distinguishes three things throughout:

- ordinary basemap context is presentation infrastructure, not wine authority;
- an INAO polygon is a cartographic representation of a regulatory geographical area, not commune membership, approved parcel eligibility, or actual vineyard land;
- a sourced feature can remain useful on the map without being promoted to a governed CARTA identity.

Region anchors are representative points and camera bounds derived from the union of mapped governed children. They are labels, not invented France-wide wine-region polygons. A region without enough mapped child geography is intentionally absent.

### Run locally

The committed app does not need Python or a network build step:

```bash
cd atlas-app
npm ci
npm run dev
```

`npm run build` produces a static-host-compatible `dist/` directory. OpenFreeMap is the only runtime map service; CARTA-owned thematic assets are committed under `atlas-app/public/data/` and require no API key.

To regenerate those assets from the checksummed upstream snapshots:

```bash
python -m pip install -r requirements-atlas.txt
python scripts/build_atlas.py
python scripts/build_terrain.py
python scripts/validate_atlas.py
```

`build_atlas.py` regenerates the wine geography and the learner projections. `build_terrain.py` regenerates the shaded relief and contours from the pinned elevation tiles in `.cache/atlas/terrain/`, under the [terrain and environmental data contract](atlas-terrain-foundation.md). Both write `provenance.json` from every registered manifest, so either can be run alone.

The generator downloads into an ignored local cache unless archives are supplied with `--source-archive DATASET_ID=/absolute/path.zip`. Raw source archives and raw elevation rasters are never committed. Dataset manifests, transformation parameters, checksums, licenses, derived-artifact metadata, and geographic meaning live in [`data/geography/datasets/`](../data/geography/datasets/); accepted external-ID reconciliation lives in [`data/geography/external-id-mappings/`](../data/geography/external-id-mappings/).

### Browser-delivery decision

Run 01 measured the generated assets after topology-preserving simplification and six-decimal coordinate rounding:

| Asset | Records | Bytes | Delivery |
|---|---:|---:|---|
| Natural Earth countries | 258 | 2,214,567 | initial interaction layer |
| INAO AOC/AOP | 1,320 | 7,853,848 | loaded on France entry |
| INAO IGP | 165 | 2,699,715 | loaded only when enabled |
| Governed region anchors | 5 | 4,281 | loaded on France entry |
| Search index | 1,483 | 957,518 | loaded on first useful search |
| Learner-guide projection | 27 entity routes | 158,276 | loaded on first place selection |

The split GeoJSON delivery is responsive in the tested desktop and phone flows and keeps IDs and feature-level click behavior simple. PMTiles would add complexity without solving an observed Run 01 problem, so it remains a measured future option rather than a default dependency. The manifests are the authoritative place for current sizes and checksums if later regeneration changes these values.

## Run 02 learner-guide and quantity contract

The Jura, Burgundy, Loire Valley, Beaujolais, and Béarn/Jurançon worlds add a learner-facing projection at `atlas-app/public/data/atlas-guides.json`. Jura, Béarn/Jurançon, and Beaujolais are the three mature regional-world proofs. The build script generates the learner projection from claims, entities, profiles, and sources. It is not an authored content store.

Every projected sentence and measurement carries its originating `claim_id` and source IDs. Quantities live on the existing claim record in a small `quantity` object with a measure, numeric value, unit, explicit scope, observation date, and—where a percentage is used—its denominator. Grape shares also carry a governed grape entity reference. Optional `atlas_presentation` metadata selects and orders claims for a learner section; it does not restate the fact.

The validator rejects undated quantities, percentages outside zero to 100, percentages without denominators, missing grape dimensions, and duplicate supported measures with the same subject/date/scope/dimension key. Atlas validation then proves that every projected value, statement, subject, source, and URL still matches machine authority. The browser reads the numeric fields directly and never parses a number from prose.

Region profiles can provide a guide for mapped child appellations that do not yet merit their own Human Reference page. This is a presentation alias only: the selected map feature retains its own CARTA identity in the technical details, and a primary appellation profile always takes precedence.

## Human experience

A useful CARTA Atlas should let someone:

- start with recognizable world and country geography;
- learn wine geography in relation to cities, rivers, mountains, coasts, borders, and neighboring regions;
- zoom naturally from country to wine region to subregion to appellation and, where evidence supports it, vineyard or parcel scale;
- click a mapped feature and understand what it is without leaving the map;
- move from a mapped feature into the Human Reference for deeper reading;
- search for places, appellations, grapes, producers, and other CARTA subjects;
- see uncertainty and incomplete spatial knowledge honestly rather than through invented precision;
- eventually explore how geography, names, classifications, producers, plantings, and relationships change through time.

## Semantic zoom

The Atlas should reveal the right information at the right scale rather than display every label and boundary at once.

At broad scales, countries and major wine regions matter. At closer scales, subregions and appellations become useful. At local scales, communes, vineyards, parcels, producer locations, terrain, and other detailed features may appear when CARTA has defensible data for them.

This is a presentation rule, not a new authority layer. What appears at each zoom level is derived from governed CARTA records and sourced geographic data.

## STRATA as the layer system

STRATA gives the Atlas its deeper structure:

- **Space** — ordinary geography, wine regions, boundaries, containment, proximity, terrain, and mapped locations. Physical relief entered the Atlas in the Béarn / Jurançon terrain proof and now covers a second explicit Beaujolais proof through the same [terrain and environmental data contract](atlas-terrain-foundation.md).
- **Time** — historical boundaries, changing names and classifications, producer movement, plantings, and other dated geography.
- **Relationships** — selected graph relationships that become meaningful when viewed spatially.
- **Appellations** — legal wine geography and its nested or overlapping structures.
- **Terroir** — elevation, slope, aspect, geology, soils, hydrology, climate, and related evidence-backed layers.
- **Ampelography** — grape occurrence, legal authorization, naming, historical distribution, and relationships to places and producers.

The default map should remain understandable without turning every STRATA layer on. Depth should be available, not imposed.

## Authority and geometry

CARTA Atlas is a projection of CARTA, not a second source of truth.

Geographic truth can exist without digital geometry. CARTA may know that one appellation sits within another before it possesses either polygon. Likewise, a producer may be reliably associated with a municipality without CARTA knowing an exact vineyard point.

When geometry is used, it must retain provenance. Each adopted spatial dataset should have a documented source, license, geographic meaning, precision, and appropriate CARTA linkage.

Two rules apply:

> **No geometry without provenance. No geometry inference merely for visual completeness.**

> **Absence of geometry is not absence of spatial knowledge.**

## Technical direction

The first interactive Atlas implementation is expected to use MapLibre and open or appropriately licensed geographic data. GeoJSON is a practical early interchange and prototype format; source datasets may arrive as Shapefile, GeoPackage, GeoJSON, APIs, or other GIS formats.

The long-term delivery format may evolve as scale requires it. The durable requirement is that map features remain linked to stable CARTA entity IDs and that the visual layer can be regenerated from governed authority and documented spatial sources.

## Product-slice standard

A product slice should already be useful to a human being. It should not exist merely to demonstrate that a map can render.

The first useful Atlas should therefore provide recognizable geographic orientation, meaningful wine-region navigation, semantic zoom, clickable CARTA-linked features, and a clear path into Human Reference. Incomplete coverage is acceptable when it is stated honestly. Project-internal language, fake precision, and visually impressive but informationally empty interactions are not.
