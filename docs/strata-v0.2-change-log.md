# STRATA v0.2 Change Log

**Basis:** Pyrenean Atlantic Deep Research Run 01 and owner review  
**Purpose:** Revise the architecture before candidate ingestion rather than forcing pilot evidence into v0.1.

## Adopted now

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

**Decision:** Keep actual geometry strict and add a parallel `spatial_assertion` record for reliable locality references, source-described areas, cultural areas, historical areas, analytical areas, and network anchors.

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

## Deferred until repeated evidence earns complexity

- explicit lease/rent/tenure predicates or objects;
- vintage-specific bottling entities;
- structured availability-observation entity/subtype;
- clone/accession entities;
- importer portfolio entities;
- climate/mesoclimate entities;
- sensory-structure ontology.

These remain visible design questions but are not added merely because the first pilot encountered one possible use.

## Explicitly not changed

- Actual geometry remains strict and sourceable.
- Relationship predicates remain typed.
- Reference / Frontier / Lens remain separate.
- Natural Wine 2.5 remains downstream and frozen unless separately revised.
- No Run 01 candidate is accepted merely by appearing in the research output.

## Next gate

After this revision is accepted:

1. normalize Run 01 candidates against STRATA v0.2;
2. evaluate claim-level source fitness without treating trade sources as automatically secondary;
3. convert jurisdictional names to name assertions;
4. convert useful non-geometric geography to spatial assertions;
5. ingest accepted machine records;
6. generate the first human-readable Atlas proof set;
7. audit machine records and Markdown cards for drift before scaling.
