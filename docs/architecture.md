# CARTA Architecture v0.2

## Purpose

CARTA is a spatial-temporal wine knowledge and field-intelligence system. Its authority lives in inspectable, machine-readable records, while its Human Reference is designed as a deep reading experience for people.

Maps, graph views, timelines, reference profiles, search, and future AI interfaces are projections of the same governed authority rather than competing sources of truth.

## Architectural principles

1. **Identity is separate from assertion.** An entity can exist even when claims about it are disputed or incomplete.
2. **Relationships are typed.** Proximity, mentorship, synonymy, ownership, and genetic relatedness are never collapsed into a generic "related to" edge. Stylistic comparison remains in external analytical layers.
3. **Claims carry evidence.** Material assertions must point to sources and preserve disagreement.
4. **Source fitness is claim-specific.** Importer, distributor, retailer, producer, regulatory, scientific, and community sources can all be appropriate evidence when the source fits the claim.
5. **Time is first-class.** Relationships, names, ownership, appellation boundaries, permissions, classifications, locations, and availability may have validity intervals or observation dates.
6. **Space is first-class, but precision is not binary.** Actual geometry, reliable locality references, source-described areas, cultural/historical geographies, and analytical geographies can coexist without false precision.
7. **Reference and Frontier never silently merge.** Dated Frontier intelligence cannot become Reference truth without an explicit promotion decision. Personal Lens data lives outside CARTA core and may only consume stable CARTA IDs as an external/private overlay.
8. **The graph may expand without a seat count.** CARTA does not use curriculum-style quotas for grapes or producers.
9. **CARTA does not auto-expand Natural Wine 2.5.** Any downstream curriculum change remains a separate editorial action.
10. **Human readability is required.** A person browsing GitHub should be able to understand CARTA without reading JSONL.
11. **Human profiles are composite projections.** The ontology may separate person, producer, project, wine, place, and relationship records while one readable reference profile composes the records that belong together for a human reader.
12. **Discovery does not equal publication.** A valid graph node may remain unpublished as a standalone reference until it meets the Human Reference baseline.
13. **Projection disposition and navigation eligibility are explicit.** Every active producer, country, and grape has a governed Human Reference disposition, including deliberate machine-only deferral. Generated navigation links only to canonical profile paths; it keeps structural country membership distinct from reciprocal editorial anchors and applies deterministic source-kind semantics to graph-only two-hop discovery.

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
- dated Frontier claims on stable subjects.

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
- availability/access view.

### 4. AI / query layer

Future agents and search interfaces should query the same accepted machine authority and cite the same claims/sources. AI is an interface over CARTA, not a replacement authority.

## External/private Lens

Personal Lens data is deliberately outside CARTA core. Holdings, tasting notes, preferences, acquisition history, private watchlists, owner-specific hypotheses, and similar material should live in a separate private system if implemented. That system may reference stable CARTA IDs and consume CARTA projections, but it must not write personal data into CARTA authority or make private preference a condition of Reference truth.

## Core record types

- `entity` — a stable thing in the world or in a governed conceptual system.
- `relationship` — a typed edge between two entities.
- `claim` — an assertion about an entity, relationship, name, or spatial assertion, including disputed and provisional assertions.
- `source` — provenance supporting, contradicting, or contextualizing a claim.
- `name_assertion` — an evidence-bound name attached to an entity, including jurisdictional and historical naming.
- `geometry` — metadata pointing to actual mappable geometry.
- `spatial_assertion` — useful geographic knowledge that does not yet warrant fabricated geometry.
- `reference_profile` — governance metadata for a composite human-facing reference page, including component entities, maturity, publication state, path, anchors, and enrichment gaps.

## Derived lookup and display metadata

Claims, name assertions, and spatial assertions point forward to their subjects. Reverse lookup is derived from `claim.subject_ref`, `name_assertion.entity_id`, and `spatial_assertion.entity_id`; entity records do not carry an authored second copy. The legacy entity fields `claim_ids`, `name_assertion_ids`, and `spatial_refs` remain in the v0.2 schema only as deprecated compatibility fields.

Entity `summary` and `tags` support display, navigation, and search. They are not factual authority. Ownership, certification, legal status, business structure, identity questions, and current practices belong in sourced claims when CARTA needs to assert them.

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

These machine distinctions do not force one-to-one Human Reference pages.

`market_signal` remains in the v0.2 schema only as a deprecated compatibility value. Frontier is a logical layer of dated claims attached to stable wine, producer, institution, relationship, or other appropriate subjects, not a parallel population of transient entities.

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

Spatial assertions can express reliable locality placement, source-described areas, cultural geographies, historical geographies, and analytical geographies without false precision.

`network_anchor` remains in the v0.2 schema only as a deprecated compatibility value. Where a graph relationship touches a map, the relationship remains graph truth; presentation placement is derived rather than authored as independent spatial authority.

## Appellation semantics

`WITHIN_APPELLATION` expresses supported physical containment of a spatial subject such as a vineyard or place within an appellation boundary. A wine's legal designation is not physical containment: use `CLASSIFIED_AS` with the appellation and preserve any vintage or validity scope. Parcel location, commune location, appellation boundary, and bottle designation remain separate truths.

## Temporal model

Use `valid_from`, `valid_to`, `observed_at`, and honest precision. Never manufacture exact dates. Frontier claims and market, availability, or price observations require `observed_at`; statements framed as current, recent, continuing, or otherwise perishable require a source-supported observation date and may also carry a validity interval.

A durable wine/cuvée identity persists across vintages. Vintage-specific facts are represented through dated claims, relationships, or temporal metadata on that persistent wine identity rather than by creating a separate wine entity for each year.

## Human Reference model

The Human Reference is required, but not every machine node earns a full page.

Profiles use three maturity levels:

- `node` — graph-useful, insufficient for a standalone reference;
- `baseline` — generous, publishable reference depth;
- `deep` — mature dossier depth.

A profile can separately be `queued`, `stub`, `published`, or `deprecated`.

`machine_only` is the explicit no-page disposition. It is valid only at `node` maturity and cannot claim an Atlas path. It prevents important graph populations from disappearing silently while preserving the rule that not every entity deserves a page.

The Human Reference contract defines profile-specific minimums, composite producer behavior, reader-facing geography, representative anchors, sensory/style writing, historical narrative, and the separation of ecosystem discovery from entity enrichment.

## Human geography

For people browsing the Atlas:

- country-specific regions and appellations are nested beneath their countries;
- genuine cross-border physical/cultural geographies live under `landscapes/`;
- relationship-generated analytical constructs live under `ecosystems/`.

This hierarchy does not replace typed `WITHIN`, `LOCATED_IN`, `OVERLAPS`, or other graph relationships.

## Cross-project operating contract

### CARTA Reference → Natural Wine 2.5

CARTA may provide deliberately selected, versioned reference facts. Curriculum inclusion, importance, sequencing, interpretation, and pedagogy remain Natural Wine 2.5 decisions; the curriculum is not a runtime consumer of the full CARTA graph.

### Natural Wine 2.5 → CARTA

Curriculum work may produce research questions, coverage signals, source leads, identity or relationship candidates, contradictions, and architectural stress cases. None becomes CARTA authority automatically.

### Shared boundaries

- Frontier is dated intelligence. Portfolio presence is not stock; stock is not continued availability; editorial attention is not durable importance; repeated observation is not automatic promotion to Reference.
- Human Reference consumes machine authority. Corrections land in machine records first and are then projected into reader-facing pages.
- Taste, holdings, substitutions, sensory analogies, watchlists, personal hypotheses, and normative judgments remain in external personal or analytical layers, even when they reference CARTA IDs.
- CARTA IDs and curriculum IDs identify different objects and may map many-to-many. CARTA does not maintain a centralized cross-project ID registry.

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
- deliberately selected, versioned Reference extracts for independent downstream use

External/private Lens systems may consume stable CARTA IDs and projections, but they are not CARTA core projections and must not write personal information into CARTA authority.

No projection is permitted to invent information missing from the underlying records.
