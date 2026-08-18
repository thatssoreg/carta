# CARTA Architecture v0.2

## Purpose

CARTA is a spatial-temporal wine knowledge and field-intelligence system. Its authority lives in inspectable, machine-readable records, but its repository must also remain useful to a human reader.

Maps, graph views, timelines, Markdown cards, search, and future AI interfaces are projections of the same governed authority rather than competing sources of truth.

## Architectural principles

1. **Identity is separate from assertion.** An entity can exist even when claims about it are disputed or incomplete.
2. **Relationships are typed.** Proximity, mentorship, synonymy, ownership, genetic relatedness, and stylistic comparison are never collapsed into a generic "related to" edge.
3. **Claims carry evidence.** Material assertions must point to sources and preserve disagreement.
4. **Source fitness is claim-specific.** Importer, distributor, retailer, producer, regulatory, scientific, and community sources can all be appropriate evidence when the source fits the claim.
5. **Time is first-class.** Relationships, names, ownership, appellation boundaries, permissions, classifications, locations, and availability may have validity intervals or observation dates.
6. **Space is first-class, but precision is not binary.** Actual geometry, reliable locality references, source-described areas, cultural/historical geographies, and analytical geographies can coexist without false precision.
7. **Reference, Frontier, and Lens never silently merge.** A current market signal or personal hypothesis cannot become reference truth without an explicit promotion decision.
8. **The graph may expand without a seat count.** CARTA does not use curriculum-style quotas for grapes or producers.
9. **CARTA does not auto-expand Natural Wine 2.5.** Any downstream curriculum change remains a separate editorial action.
10. **Human readability is required.** A person browsing GitHub should be able to understand CARTA without reading JSONL.

## Four surfaces of the same system

### 1. Machine authority

Structured records are the canonical data layer:

- entities;
- relationships;
- claims;
- sources;
- name assertions;
- geometry metadata;
- source-described spatial assertions;
- Frontier and Lens records.

### 2. Human Atlas

Markdown pages under `atlas/` are the human-readable projection of the authority.

They include grape cards, producer cards, person cards, country pages, region pages, appellation pages, ecosystem pages, wine pages, indexes, and other useful reading surfaces.

See [`docs/atlas-projection.md`](atlas-projection.md).

### 3. Visual interfaces

Future interfaces may include:

- map;
- TRAMA relationship/network view;
- timeline;
- grape genealogy/taxonomy view;
- producer lineage view;
- Frontier/discovery feed;
- availability/access view;
- personal Lens view.

### 4. AI / query layer

Future agents and search interfaces should query the same accepted machine authority and cite the same claims/sources. AI is an interface over CARTA, not a replacement authority.

## Core record types

- `entity` — a stable thing in the world or in a governed conceptual system.
- `relationship` — a typed edge between two entities.
- `claim` — an assertion about an entity, relationship, name, or spatial assertion, including disputed and provisional assertions.
- `source` — provenance supporting, contradicting, or contextualizing a claim.
- `name_assertion` — an evidence-bound name attached to an entity, including jurisdictional and historical naming.
- `geometry` — metadata pointing to actual mappable geometry.
- `spatial_assertion` — useful geographic knowledge that does not yet warrant fabricated geometry.

## Entity families

Initial families after the first pilot are:

- `person`
- `producer`
- `project`
- `ecosystem`
- `grape`
- `wine`
- `vineyard`
- `place`
- `appellation`
- `geographic_feature`
- `geology`
- `practice`
- `institution`
- `classification`
- `historical_event`
- `market_signal`

New entity families require an explicit schema revision, not an ad hoc `other` bucket.

## Data layout

Recommended repository layout after the first ingestion:

```text
data/
  entities/
  relationships/
  claims/
  sources/
  names/
  geography/
    geometry/
    assertions/
  frontier/
  lens/

atlas/
  ecosystems/
  countries/
  regions/
  appellations/
  grapes/
  producers/
  people/
  wines/
  institutions/
  practices/
  classifications/
  historical-events/
  indexes/

research/
  run-01-pyrenean-atlantic/

schemas/
docs/
pilots/
scripts/
```

Records should begin as JSON or YAML that validates against JSON Schema. GeoJSON should carry actual geometry, while entity IDs connect geometry to the semantic graph. A generated SQLite or DuckDB database may later provide fast local querying, but generated databases must never become the only authority.

## IDs

IDs are namespaced, stable, and not presentation labels.

Examples:

- `person:imanol-garay`
- `producer:alfredo-egia`
- `ecosystem:pyrenean-atlantic`
- `grape:petit-courbu`
- `place:balmaseda`
- `appellation:bizkaiko-txakolina`
- `wine:hegan-egin`
- `name:petit-courbu-hondarrabi-zuri-zerratia-bizkaiko`
- `spatial:imanol-garay-baigorry-source-described`

If two real entities collide on name, IDs receive a disambiguating suffix based on stable context. Names may change; IDs should not.

## Naming model

Names are not always identities.

An entity may have lightweight alternate names for display, but consequential legal, local, historical, contested, or time-bound names belong in first-class name assertion records.

This allows CARTA to represent jurisdiction-specific naming without manufacturing duplicate grape identities.

## Spatial model

### Actual geometry

Use geometry records when actual point, line, or polygon geometry is available.

Geometry metadata can express:

- geometry reference;
- point, line, or polygon type;
- source;
- precision;
- confidence;
- `valid_from`;
- `valid_to`;
- `observed_at`.

This allows political borders, appellations, vineyard parcels, and other boundaries to change through time.

### Spatial assertions without geometry

Useful wine geography often exists before CARTA acquires an official polygon or exact parcel coordinate.

Spatial assertions can express:

- reliable locality placement;
- source-described areas;
- cultural geographies;
- historical geographies;
- analytical geographies;
- network anchors.

They must state precision and provenance and may later link to actual geometry.

A town coordinate must not masquerade as a vineyard coordinate. A source-described area must not masquerade as an official polygon.

## Temporal model

Dates are intervals when the evidence only supports intervals. Never manufacture exact dates.

Use:

- `valid_from`
- `valid_to`
- `observed_at`
- `precision` such as `day`, `month`, `year`, `range`, `unknown`

A relationship such as ownership may therefore be true only during a stated interval. A cellar location may change. A legal name can become valid or invalid. A retailer observation expires as evidence of current access.

## Human-readable projection contract

The Atlas is required, not optional.

Machine records remain authoritative, but CARTA should generate or maintain Markdown pages that make the system readable in GitHub.

The read-first layer should answer:

- Why should I care?
- Where does this fit?
- What connects to it?
- What makes it distinctive?
- What is CARTA watching?
- What remains unresolved?

The evidence layer should expose:

- typed relationships;
- name assertions;
- geography;
- timeline;
- claims and confidence;
- sources;
- revision history.

Where possible, factual tables should be generated from structured records so the Atlas cannot quietly drift away from the machine authority.

## Projections

Future projections may include:

- human Atlas
- map view
- TRAMA network view
- timeline view
- grape genealogy/taxonomy view
- producer lineage view
- frontier/discovery feed
- availability/access view
- personal Lens view
- Natural Wine 2.5 curriculum export

No projection is permitted to invent information missing from the underlying records.
