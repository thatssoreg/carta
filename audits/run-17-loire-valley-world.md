# Run 17 — Loire Valley canonical ingestion and Atlas world

## Execution frame

- Starting canonical `main`: `f2f78248cad5b881269b485a19d2fc6941a6c31a`
- Working branch: `atlas-loire-valley-world`
- Research inputs: completed Loire Run A (place/legal/terrain) and Run B (people/ecology/curriculum salience)
- Authority rule: the reports were research handoffs, never source records. Every promoted claim resolves to an existing governed source or a separately inspected primary, institutional, court-reporting, or fit-for-claim trade source.

## Regional argument

The finished world argues **river continuity, not sameness**. The Loire makes a long sequence navigable while physical ground, tributaries, grapes, wine forms, legal origins, institutions, and producer histories keep changing. Its human equivalent is overlapping family, work, advocacy, collaboration, ownership, and succession lineages—not one natural-wine school.

The core learner question is:

> How can one river connect Muscadet, Savennières, Vouvray, Chinon, and Sancerre without making them versions of the same place?

Seven supporting questions land on governed subjects: the tributary network, human transmission, Vin de France literacy, the Loir branch, competing meanings of Val de Loire, Chenin wine forms, and the legal meaning of `sur lie`.

## Canonical authority

Run 17 adds:

- 64 entities: six analytical component places, six river/tributary features, 15 appellation/classification-area identities, five grapes, nine producers, 19 people, and four institutions/ownership actors;
- 83 relationships across containment, watershed, traditional occurrence, producer location, work, collaboration, influence, family, ownership, acquisition, and succession;
- 36 supported claims and 15 source records;
- 25 spatial assertions: 15 official regulatory-area assertions and ten producer-base assertions;
- 25 geometry records after regeneration: 15 accepted INAO geometries and ten producer points;
- 21 profiles: four new published producer baselines and 17 governed stubs.

The existing Loire profile moves from baseline to deep. Clos du Tue-Boeuf moves from a navigation node to a published baseline. Existing Huet, Richard Leroy, and Tue-Boeuf authority gains map, regional, or work-line context without rewriting earlier supported claims.

Before/after validation counts:

| Authority surface | Before | After | Delta |
|---|---:|---:|---:|
| Entities | 552 | 616 | +64 |
| Relationships | 619 | 702 | +83 |
| Claims | 521 | 557 | +36 |
| Sources | 342 | 357 | +15 |
| Spatial assertions | 89 | 114 | +25 |
| Geometry records | 53 | 78 | +25 |
| Profiles | 202 | 223 | +21 |

## Place and legal geography

The analytical corridor resolves into Pays Nantais, Anjou, Saumur, Touraine, and Centre-Loire, with Vallée du Loir as a visible northern branch. The Loire, Sèvre Nantaise, Layon, Vienne, Cher, and Loir are separate river subjects. The Loir is explicitly not treated as a spelling variant of Loire.

Fifteen new INAO mappings raise governed INAO features from 40 to 55. The ingestion boundary now handles reused INAO denomination IDs generically: where an ID names a base appellation and several complements, the governed mapping name selects exactly one feature and siblings remain external context. This was exercised by Saumur rather than solved with a Loire-only exception.

Current AOP areas, Val de Loire IGP, InterLoire scope, BIVC scope, UNESCO's cultural landscape, and CARTA's analytical corridor stay separate. Broad Crémant de Loire and Val de Loire IGP geography remains below more specific areas in click priority. No Loire polygon was authored.

## Producer ecology and time

The five editorial doors are Domaines Landron, La Coulée de Serrant / Joly, Clos Rougeard / the Foucault world, Clos du Tue-Boeuf / Puzelat, and Domaine Alexandre Bain. They do five distinct teaching jobs and are presentation, not a producer canon. Domaine Huet sits immediately behind them.

The larger graph adds Domaine Mosse, Domaine du Collier, Domaine de Bellivière, Domaine Catherine et Pierre Breton, and Domaine Pierre-Olivier Bonhomme, while connecting existing Huet and Richard Leroy routes. High-confidence edges preserve the differences among work, partnership, inspiration, family, succession, and acquisition.

Time-aware material includes Landron's dated farming chronology, the Joly estate conversion and 2001 Renaissance des Appellations formation, the 2017 Clos Rougeard acquisition, the Mosse and Bellivière succession routes, the Breton family chronology, and Bain's bounded 2015–2017 control/court sequence. Vin de France stays a wine-, vintage-, event-, or decision-level classification question, not an estate or movement tag.

## Human Reference

Published manual baselines were added for Domaines Landron, La Coulée de Serrant, Clos Rougeard, and Domaine Alexandre Bain. Clos du Tue-Boeuf and the Loire regional guide were rewritten at their promoted maturities. Generated stubs make every new active place, producer, grape, and institution reachable. Navigation and provenance were regenerated from machine authority; the fixed Run 10 ratings cohort remains a regression test even as new profiles enter the live graph.

Natural Wine 2.5 affected salience—the five doors, work-line emphasis, legal-friction literacy, and which ecology nodes were prioritized. It supplied no factual authority, relationship, legal conclusion, or machine claim.

## Atlas and interaction

The release overlay extends the existing Beaujolais world and uses the generic regional-world grammar. It ships:

- eight learner questions (one core and seven supporting);
- the five pillars: Place, Grapes & Wines, People, Culture, Rules;
- four map moments: Pays Nantais, Savennières/Layon, Vallée du Loir, and Centre-Loire;
- eight grape cards;
- five producer-door cards plus a larger mapped ecology;
- 11 governed French region/component anchors, 23 producer points, 173 native subjects, 54 editorial subjects, 65 guides, and 1,608 search records;
- reversible `Explore`, `Go there`, `Show on map`, browser-back, close, and regional-context returns.

The application contains no Loire entity conditional. The only generic UI change is collision-aware region labels using variable anchors, added after browser review exposed pressure from the richer component graph.

## Terrain

The existing Copernicus DEM GLO-30 pipeline was extended with two one-tile Loire proofs:

| Extent | Clip bbox (EPSG:4326) | Hillshade | Contours |
|---|---|---:|---:|
| Savennières / Layon | `[-0.85, 47.15, -0.35, 47.55]` | 372×439, 56,595 bytes | 11 features, 12,838 bytes |
| Sancerre / Pouilly-sur-Loire | `[2.55, 47.12, 2.99, 47.50]` | 327×416, 55,245 bytes | 39 features, 38,029 bytes |

The manifest now pins ten source tiles across four discontinuous groups and publishes nine derived artifacts. Terrain remains a digital surface-model picture below wine layers. It is not a vineyard boundary and makes no claim about drainage, exposure, ripening, quality, climate, or flavour. The intervening Loire corridor has no terrain carpet.

## Evidence decisions and deferrals

- The Bain record retains the mandatory-control cause and court remedy; the viral “tasted too natural” explanation was not promoted.
- Renaissance des Appellations is modeled as an advocacy/membership institution. Current producer membership edges were deferred pending a pinned current roster.
- No fair or event entity was added: the reports' cultural-infrastructure leads did not yet meet the source and identity bar for durable canonical ingestion.
- Domaine de l'Ecu, Pépière, Bretaudeau, Rémi Sédès, Mark Angeli, Thibaud Boudignon, Roches Neuves, Villemade, Chidaine, Taille aux Loups / Blot, Clos Roche Blanche, Noëlla Morantin, and additional Centre-Loire peers remain intentionally deferred. Adding names without independently reconciled entity, chronology, and relationship evidence would have enlarged the graph without improving it.
- Producer coordinates are published bases or municipality/locality orientations, never vineyards or complete holdings.
- Detailed legal permissions remain in current specifications; grape occurrence in the regional guide is never converted into universal authorization.
- Bottle and vintage classification histories, current estate roles, parcel holdings, cellar protocols, sulfur, filtration, and access remain explicitly unresolved where current direct evidence was not pinned.

## Architecture changes

Reused without a parallel Loire application: overlay inheritance and deep merge, canonical JSONL authority, profile projection, Atlas subjects and guide generation, generic regional pillars, active map reactions, producer-point projection, INAO mapping, search, provenance, lazy terrain loading, and context returns.

Generic changes only:

1. the current experience overlay and lineage advance to Run 17;
2. reused external IDs can be name-disambiguated at ingestion;
3. the terrain extent tuple grows from two to four proofs;
4. region labels use collision-aware variable anchors;
5. navigation ratings evaluation treats the reviewed fixture as the immutable Run 10 cohort while evaluating today's model.

No Loire-specific frontend branch, map component, terrain loader, search path, or authority type was introduced.

## Validation record

- `python3 scripts/validate_data.py --write-human-reference` — pass; generated pages and indexes current.
- `build_atlas.py` against the two pinned source archives — pass twice.
- `build_terrain.py --source-dir .cache/atlas/terrain` — pass twice.
- SHA-256 comparison of every public data artifact after consecutive full regenerations — identical.
- `python3 scripts/validate_atlas.py` — pass; 55 governed INAO features, 23 producer points, four terrain extents, nine terrain artifacts, eight questions.
- `python3 scripts/audit_navigation.py --format json` — pass; 200 surfaced profiles, 984 displayed links, 1.5% displacement rate.
- `python3 scripts/audit_navigation.py --ratings audits/run-10-human-reference-navigation-ratings.json --format json` — pass against the fixed 257-link Run 10 cohort.
- `python3 -m unittest discover -s tests` — 46 tests, all pass.
- `npm ci` — pass.
- `npm --prefix atlas-app run build` — pass; Vite reports only the existing >500 kB bundle advisory.
- Computer Use browser review — pass for landing, France questions, Loire entry, five-pillar interaction, producer map focus, context return, label collision, and bounded Savennières terrain loading/attribution.

## Maturity verdict

**Yes.** Loire Valley is now a mature CARTA Atlas regional-world proof. The verdict rests on a deep regional profile, an independently governed legal/physical map, a living producer graph behind the five presentation doors, time-aware claims, a full regional interaction grammar, bounded terrain, reachable Human Reference dispositions, deterministic generation, and green validation—not on raw entity count.

The principal known limitation is depth distribution: the regional synthesis and four doors are published baselines, while most second-line producers, grapes, and component places remain governed stubs. That is visible in the profile dispositions rather than hidden in prose.
