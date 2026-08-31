# CARTA Atlas terrain and environmental data

This document is the contract for physical-environment data in CARTA.

[CARTA Atlas](carta-atlas.md) decides what the Atlas *is*. The [Atlas editorial foundation](atlas-editorial-foundation.md) decides what it *says*. This document decides what the Atlas is allowed to **know about the ground** — where elevation, relief, slope, climate and their relatives come from, what they may and may not be used to assert, and how a rendered pixel stays traceable to a governed dataset.

It exists because environmental data is unusually good at smuggling in conclusions. A hillshade looks like an explanation. It is not one.

## The canonical principle

> **Terrain is context before it is interpretation.**

Atlas may reveal elevation, relief, slope, or orientation. It must not imply viticultural consequence unless CARTA separately possesses evidence for that consequence.

A slope drawn on a map is a statement about the shape of the ground and nothing else. It is not a statement about drainage, ripening, frost risk, exposure, sugar accumulation, harvest date, site quality, or why a wine tastes the way it does. Those are wine claims. They are governed by the [evidence policy](evidence-policy.md) and live in `data/claims/`, with sources, dates and scope, exactly as they did before CARTA owned a single elevation sample.

The two rules CARTA already applies to wine geography apply here without change:

> **No geometry without provenance. No geometry inference merely for visual completeness.**

> **Absence of geometry is not absence of spatial knowledge.**

## The four tiers

Environmental knowledge in CARTA occupies exactly four tiers. Confusing them is the failure mode this document exists to prevent.

### 1. Source observations

Measurements of the physical world, acquired from an identified publisher under an identified licence.

Examples: a digital elevation model; a measured environmental dataset such as a station temperature series or a gauged river record.

A source observation is registered as a spatial dataset manifest in [`data/geography/datasets/`](../data/geography/datasets/) with `product_class: "source_observation"`, and its evidentiary origin is a CARTA source record in `data/sources/`.

A source observation is what an instrument recorded. It is not automatically true of the ground today, and it is never true of a wine.

### 2. Derived spatial products

Deterministic transformations of a source observation that add no new information.

Examples: hillshade, contours, slope, aspect, reprojection, resampling, simplification.

A derived spatial product carries `product_class: "derived_spatial_product"` and a `derived_from` lineage naming the dataset — and, where the chain has more than one link, the sibling artifacts — it came from. Every parameter of the derivation is recorded in the manifest's `transformations`, so the artifact can be rebuilt byte for byte from the pinned source.

A derived product may be *prettier* than its source. It may never be *more certain* than its source.

### 3. Modeled environmental products

**Reserved.** Nothing in CARTA occupies this tier yet.

It is the home for products that add an assumption to the data: climate normals, interpolated surfaces, modeled exposure, modeled water balance, downscaled reanalysis. These are not observations, and they are not mere transformations — they carry a model whose assumptions can be wrong in ways the input data cannot reveal.

When the first one arrives it will be registered as its own dataset with `product_class: "modeled_environmental_product"`, `retrieval_status: "derived_in_repository"`, an explicit `derived_from` chain, and a `measurement.uncertainty` statement that describes model error and not just instrument error. The schema can already express this. CARTA has deliberately not used it, because a modeled surface presented beside measured relief invites a reader to trust both equally.

### 4. Interpretive wine knowledge claims

Statements about grapes, growing, people, law, style, or quality.

These are **not expressible as spatial datasets**, by design: `product_class` has no value for them, and the spatial dataset schema has no field that can carry one. They remain claims under the evidence policy, with sources, dates, scope and fitness — whether or not a map is showing terrain at the time.

This is the load-bearing boundary. A terrain layer can make a claim *legible*. It can never make one *true*.

### What the tiers forbid

- A hillshade does not authorise "these are south-facing slopes, which is why the wine ripens".
- A contour line does not authorise "the best sites are above 300 m".
- An elevation value at a producer's point does not authorise "this domaine farms at that altitude" — a producer base is an office or cellar, not a vineyard.
- A slope raster does not authorise a terroir explanation, however plausible.

If CARTA wants to say any of those things, it needs a claim with evidence. The terrain layer is not evidence for it. It is the picture the reader looks at while reading it.

## What a governed environmental dataset must record

Environmental data extends CARTA's existing [spatial dataset model](../schemas/spatial-dataset.schema.json) rather than standing beside it. There is one manifest directory, one provenance document, one source register and one validator. The v0.2 schema adds only what elevation and its successors genuinely need:

| Field | What it pins down |
|---|---|
| `source_id` | The CARTA source record carrying the dataset's evidentiary identity. |
| `dataset_url`, `resource_url`, `resource_id` | Publisher page and the exact acquisition path used. |
| `publisher` | Who produced the data, and under whose copyright. |
| `license` | Licence id and URL, the exact attribution text, commercial use, share-alike, redistribution status. |
| `source_release_date`, `retrieved_at` | Which snapshot, acquired when. |
| `source_files` | Every acquired file, with its own URL, byte count and SHA-256. |
| `checksum` | Single-archive integrity, where the acquisition is a single archive. |
| `source_crs` | Horizontal **and** vertical reference systems. |
| `source_format` | The delivered format, honestly named. |
| `measurement.variable`, `.unit` | What was measured, in what units. Never inferred from a filename. |
| `measurement.native_resolution` | The resolution the data actually has, not the resolution it is drawn at. |
| `measurement.uncertainty` | Published or measured error, where the publisher states one. |
| `measurement.scale_limitations` | What this data cannot resolve. Required, because the honest answer is always "less than a reader assumes". |
| `geographic_extent` | The bounded extent acquired, and why it is bounded that way. |
| `authority_class` | Whether the dataset is regulatory authority, institutional context, or presentation infrastructure. |
| `product_class` | Which tier above the dataset occupies. |
| `derived_from` | Dataset-level lineage for tiers 2 and 3. |
| `transformations` | Every processing step and every parameter, ordered, so the derivation is reproducible rather than described. |
| `derived_artifacts` | Each public asset, with its role, tier, `derived_from` lineage, byte count and SHA-256. |
| `refresh_policy` | Whether this snapshot is expected to move, and what would move it. |
| `retrieval_status` | `acquired`, `runtime_service`, or `derived_in_repository`. |

Two consequences follow from that table.

**Deterministic regeneration.** Because the recipe lives in the manifest and the inputs are checksummed, `scripts/build_terrain.py` run twice produces identical bytes, and `scripts/validate_atlas.py` proves every committed asset still matches the checksum the manifest claims. A derived asset whose bytes drift is a validation failure, not a cosmetic difference.

**Repository assets versus runtime services.** CARTA-owned derived assets are committed under `atlas-app/public/data/` and carry checksums. Runtime services — the basemap, and any future hosted terrain service — are registered as `retrieval_status: "runtime_service"` with no checksum, because CARTA does not control their bytes. Raw environmental source data is **never** committed: it lives in the ignored build cache, pinned by checksum, and the validator refuses to track raster or archive source formats.

**Attribution.** Where a licence requires a notice, the exact required string is the manifest's `license.attribution_text`, the terrain descriptor repeats it verbatim for the map credit, and validation fails if the two disagree. Attribution is a licence obligation, not a design choice.

## What Atlas may show, and how

Terrain in the Atlas is subordinate to wine geography. That is a design constraint with teeth:

- Relief renders **below every wine layer**, so appellation fills, boundaries, producer points and labels always sit on top of it.
- The shaded-relief overlay only darkens and lightens. It never paints a colour of its own across the map.
- Contours are sparse, thin, low-contrast, and appear at scales where a reader is actually reading landform.
- Terrain appears only where CARTA holds elevation data, and it dissolves at the edges of that extent rather than ending in a rectangle. Outside the extent there is no terrain, and the Atlas says so rather than inventing a smooth global surface.
- Terrain fades out at close zoom, where a ~100 m display grid would become texture pretending to be information.
- Terrain is not clickable, not searchable, and takes no part in hover, selection, routes, questions or rabbit holes. It never becomes a CARTA subject.

Relief is on by default inside its extent, with a learner-facing **Relief** control to turn it off. The Atlas's argument is that wine geography is the consequence of ground, so a reader entering a foothill region should meet the foothills without having to know that an option exists. The control is there because a reader comparing legal boundaries deserves a clean sheet of paper on request.

## What terrain is not allowed to change

A terrain run must leave the rest of CARTA exactly where it found it:

- machine authority in `data/` gains no new entities, relationships or claims from a picture of the ground;
- existing appellation and region geometry is untouched;
- Human Reference content is untouched;
- learner-facing copy elsewhere is untouched;
- and the application keeps working, with the wine map intact, when terrain is switched off or the terrain assets fail to load.

## Current state

The first governed environmental dataset is the Copernicus DEM GLO-30 tile set covering the western Pyrenees, proved in the Béarn / Jurançon world. Its manifest is [`data/geography/datasets/copernicus-dem-glo30-2022-05-09.json`](../data/geography/datasets/copernicus-dem-glo30-2022-05-09.json); the run that established it is recorded in [`audits/run-08-atlas-terrain-foundation.md`](../audits/run-08-atlas-terrain-foundation.md).

One honest caveat belongs in the reader's mind and in this document. Copernicus DEM is a digital **surface** model: it records the top of whatever stood on the ground when TanDEM-X flew, including forest canopy and buildings. In the wooded Béarn foothills a few metres of that height is trees, not slope. That is acceptable for reading landform at regional scale, and it is one of the reasons this contract requires `measurement.scale_limitations` on every environmental dataset.
