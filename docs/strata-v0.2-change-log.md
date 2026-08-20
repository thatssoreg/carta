# STRATA v0.2 Change Log

**Basis:** Pyrenean Atlantic Deep Research Run 01 and owner review  
**Purpose:** Revise the architecture before candidate ingestion rather than forcing pilot evidence into v0.1.

## Run 05 v0.2 maintenance

Run 05 retained the v0.2 schema boundary while removing duplicate or presentation-only authority:

- entity-side `claim_ids`, `name_assertion_ids`, and `spatial_refs` are deprecated authored reverse indexes; lookup is derived from forward records;
- `market_signal` is deprecated as an authored entity type, and Frontier is represented by dated claims on stable subjects;
- `network_anchor` is deprecated as spatial authority because map presentation is derived from the relationship graph;
- the four analytical comparison predicates and three `*_AT_TIME` predicates remain enum-compatible but are deprecated for authored core data;
- `WITHIN_APPELLATION` is physical containment, while a wine's legal designation uses `CLASSIFIED_AS`;
- entity summaries and tags are display/search metadata, not sourced authority.

No replacement predicates, observation entities, or STRATA v0.3 were introduced.

## Adopted in Run 01

### 1. Source fitness replaces source prestige

**Problem:** v0.1's wording risked treating importer/distributor material primarily as discovery evidence even though the wine trade often documents producer biography, work history, farming, cellar practice, fruit sourcing, and collaboration through those sources.

**Decision:** Source class remains descriptive. Fitness is evaluated at the claim-source pair as `excellent`, `good`, `limited`, or `lead_only`.

**Files:**

- `docs/evidence-policy.md`
- `schemas/claim.schema.json`

### 2. First-class jurisdictional name assertions

**Problem:** Petit Courbu / Hondarrabi Zuri Zerratia showed that a legal name can be valid in a jurisdiction without CARTA needing to create a second grape entity or claim universal synonymy.

**Decision:** Add `name_assertion` records carrying entity, name, kind, jurisdiction, time, status, and claim support.

**Files:**

- `schemas/name-assertion.schema.json`
- `schemas/entity.schema.json`
- `docs/ontology.md`

### 3. Place semantics

**Problem:** Basque Country and Béarn can refer to administrative, cultural, historical, wine, or analytical geographies.

**Decision:** Add optional `place_kind` values including country, administrative region, cultural region, historical territory, municipality, locality, wine region, and analytical region.

**Files:**

- `schemas/entity.schema.json`
- `docs/ontology.md`

### 4. Spatial assertions without fake geometry

**Problem:** v0.1 required actual geometry for every spatial record, causing the pilot to emit zero spatial records rather than invent town/vineyard coordinates or unofficial polygons.

**Decision:** Keep actual geometry strict and add a parallel `spatial_assertion` record for reliable locality references, source-described areas, cultural areas, historical areas, analytical areas, and network anchors. Run 05 later deprecated `network_anchor` as authored spatial authority while retaining the other assertion kinds.

**Files:**

- `schemas/spatial-assertion.schema.json`
- `docs/architecture.md`
- `docs/ontology.md`

### 5. First-class ecosystems

**Problem:** The Pyrenean Atlantic research object is not honestly a single place. It connects several physical/legal geographies plus non-spatial professional relationships.

**Decision:** Add `ecosystem` as an entity type.

**Files:**

- `schemas/entity.schema.json`
- `docs/architecture.md`
- `docs/ontology.md`

### 6. Human-readable Atlas is required

**Problem:** JSON/JSONL authority alone would make CARTA unpleasant and inefficient to use directly in GitHub.

**Decision:** Add an explicit human-readable Markdown projection contract for grape, producer, person, region, appellation, country, ecosystem, wine, and other pages.

**Files:**

- `docs/atlas-projection.md`
- `atlas/README.md`
- `docs/architecture.md`
- `README.md`

## Still deferred until concrete evidence earns complexity

- vintage-specific bottling entities;
- clone/accession entities;
- climate/mesoclimate entities;
- sensory-structure ontology.

Run 05 represented tenure, availability, and importer/distributor access without those proposed constructs, so they are no longer carried here as active architecture questions. The remaining questions are not additions-in-waiting; only a concrete representation failure can reopen them.

## Explicitly not changed

- Actual geometry remains strict and sourceable.
- Relationship predicates remain typed.
- Reference / Frontier / Lens remain separate.
- Natural Wine 2.5 remains an independent downstream editorial system rather than an automatic full-graph projection.

## Human Reference navigability closure

**Decision:** Close invisible-subject and stale-navigation failure modes in the Human Reference projection without changing STRATA core ontology.

- active producers, countries, and grapes require explicit profile dispositions;
- `machine_only` records deliberate no-page deferral at node maturity;
- honest stubs preserve visibility without lowering baseline quality;
- generated navigation resolves canonical profile targets and derives selective reciprocal discovery from existing typed relationships and editorial anchors;
- project and vineyard objects remain composite profile components because no core or projection information loss was demonstrated.

**Result:** STRATA remains v0.2. The repair changes projection governance, generation, and validation, not the entity or relationship vocabulary.
- No Run 01 candidate is accepted merely by appearing in the research output.

## Run 11 kind-aware Human Reference navigation

**Decision:** Keep the machine graph authoritative while giving its reader projection deterministic source-kind semantics.

- `country_entity_ids` remains structural geographic assignment: outbound to the containing country and downward from a country to its governed region/appellation surfaces, without automatic reciprocal producer recommendations;
- `representative_anchor_ids` remains explicit editorial projection authority with outbound and reciprocal discovery;
- shared components, direct governed relationships, structural routes, and explicit anchors survive without a two-hop gate;
- graph-only two-hop candidates are filtered by inspectable country, directional-geography, grape, and producer/person policies;
- composite producer profiles no longer turn a shared broad grape/classification component into producer adjacency unless another specific professional, site, farming, planting, practice, direct, or editorial route supports it;
- audit and test output expose source/target kinds, path predicates/directions, route class, and acceptance/rejection reason.

**Unchanged:** No STRATA v0.3, schema vocabulary, machine relationship, profile kind, cap, wine identity rule, or composite project/vineyard policy was introduced or removed.
