# CARTA Architecture v0.2

## Purpose

CARTA is a spatial-temporal wine knowledge and field-intelligence system. Its authority lives in inspectable, machine-readable records, while its Human Reference is designed as a deep reading experience for people.

Maps, graph views, timelines, reference profiles, search, and future AI interfaces are projections of the same governed authority rather than competing sources of truth.

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
11. **Human profiles are composite projections.** The ontology may separate person, producer, project, wine, place, and relationship records while one readable reference profile composes the records that belong together for a human reader.
12. **Discovery does not equal publication.** A valid graph node may remain unpublished as a standalone reference until it meets the Human Reference baseline.

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

### 2. Human Reference / Atlas

Markdown under `atlas/` is the human-readable reference projection.

Human profiles can combine multiple machine entities. Their publication state and maturity are governed separately through `reference_profile` records.

See [`docs/atlas-projection.md`](atlas-projection.md) and [`schemas/reference-profile.schema.json`](../schemas/reference-profile.schema.json).

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
- `reference_profile` — governance metadata for a composite human-facing reference page, including component entities, maturity, publication state, path, anchors, and enrichment gaps.

## Entity families

Current machine-entity families are:

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

These machine distinctions do not force one-to-one Human Reference pages.

## Data layout

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
  reference-profiles/
  frontier/
  lens/

atlas/
  countries/
    <country>/
      README.md
      regions/
      appellations/
  landscapes/
  ecosystems/
  grapes/
  producers/
  wines/
  people/
  institutions/
  practices/
  classifications/
  historical-events/
  indexes/

research/
schemas/
docs/
pilots/
scripts/
```

The Human Reference hierarchy is a reading/navigation decision. The machine graph remains relational and does not need to mirror the directories.

## IDs

IDs are namespaced, stable, and not presentation labels.

Examples:

- `person:imanol-garay`
- `producer:alfredo-egia-wine`
- `ecosystem:pyrenean-atlantic`
- `grape:petit-courbu`
- `place:balmaseda`
- `appellation:bizkaiko-txakolina`
- `wine:rebel-rebel`
- `profile:alfredo-egia`
- `name:petit-courbu-hondarrabi-zuri-zerratia-bizkaiko`
- `spatial:imanol-garay-baigorry-source-described`

Names may change; IDs should not.

## Naming model

Names are not always identities.

An entity may have lightweight alternate names for display, but consequential legal, local, historical, contested, or time-bound names belong in first-class name assertion records.

## Spatial model

### Actual geometry

Use geometry records when actual point, line, or polygon geometry is available.

Geometry metadata can express source, precision, confidence, validity intervals, and observation dates.

### Spatial assertions without geometry

Useful wine geography often exists before CARTA acquires an official polygon or exact parcel coordinate.

Spatial assertions can express reliable locality placement, source-described areas, cultural geographies, historical geographies, analytical geographies, and network anchors without false precision.

## Temporal model

Use `valid_from`, `valid_to`, `observed_at`, and honest precision. Never manufacture exact dates.

## Human Reference model

The Human Reference is required, but not every machine node earns a full page.

Profiles use three maturity levels:

- `node` — graph-useful, insufficient for a standalone reference;
- `baseline` — generous, publishable reference depth;
- `deep` — mature dossier depth.

A profile can separately be `queued`, `stub`, `published`, or `deprecated`.

The Human Reference contract defines profile-specific minimums, composite producer behavior, reader-facing geography, representative anchors, sensory/style writing, historical narrative, and the separation of ecosystem discovery from entity enrichment.

## Human geography

For people browsing the Atlas:

- country-specific regions and appellations are nested beneath their countries;
- genuine cross-border physical/cultural geographies live under `landscapes/`;
- relationship-generated analytical constructs live under `ecosystems/`.

This hierarchy does not replace typed `WITHIN`, `LOCATED_IN`, `OVERLAPS`, or other graph relationships.

## Projections

Future projections may include:

- Human Reference / Atlas
- map view
- TRAMA network view
- timeline view
- grape genealogy/taxonomy view
- producer lineage view
- Frontier/discovery feed
- availability/access view
- personal Lens view
- Natural Wine 2.5 curriculum export

No projection is permitted to invent information missing from the underlying records.
