# CARTA Architecture v0.1

## Purpose

CARTA is a spatial-temporal wine knowledge system. Its authority lives in inspectable, machine-readable records. Maps, graph views, timelines, essays, search, and future AI interfaces are projections of that authority, not substitutes for it.

## Architectural principles

1. **Identity is separate from assertion.** An entity can exist even when claims about it are disputed or incomplete.
2. **Relationships are typed.** Proximity, mentorship, synonymy, ownership, genetic relatedness, and stylistic comparison are never collapsed into a generic "related to" edge.
3. **Claims carry evidence.** Material assertions must point to sources and preserve disagreement.
4. **Time is first-class.** Relationships, names, ownership, appellation boundaries, permissions, and classifications may have validity intervals.
5. **Space is first-class.** Points, polygons, lines, and derived spatial intersections are stored independently of narrative.
6. **Reference, Frontier, and Lens never silently merge.** A current market signal or personal hypothesis cannot become reference truth without an explicit promotion decision.
7. **The graph may expand without a seat count.** CARTA does not use curriculum-style quotas for grapes or producers.
8. **CARTA does not auto-expand Natural Wine 2.5.** Any downstream curriculum change remains a separate editorial action.

## Core record types

- `entity` — a stable thing in the world or in a governed conceptual system.
- `relationship` — a typed edge between two entities.
- `claim` — an assertion about an entity or relationship, including disputed and provisional assertions.
- `source` — provenance supporting, contradicting, or contextualizing a claim.

## Entity families

Initial families are:

- `person`
- `producer`
- `project`
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

These are intentionally broader than a curriculum ontology. New entity families require an explicit schema revision, not an ad hoc `other` bucket.

## Data layout

Recommended repository layout after the pilot:

```text
data/
  entities/
  relationships/
  claims/
  sources/
  geography/
    points.geojson
    regions.geojson
  frontier/
  lens/
schemas/
docs/
pilots/
scripts/
```

Records should begin as JSON or YAML that validates against JSON Schema. GeoJSON should carry geometry, while entity IDs connect geometry to the semantic graph. A generated SQLite or DuckDB database may later provide fast local querying, but generated databases must never become the only authority.

## IDs

IDs are namespaced, stable, and not presentation labels.

Examples:

- `person:imanol-garay`
- `producer:alfredo-egia`
- `grape:petit-courbu`
- `place:balmaseda`
- `appellation:bizkaiko-txakolina`
- `wine:hegan-egin`

If two real entities collide on name, IDs receive a disambiguating suffix based on stable context. Names may change; IDs should not.

## Spatial model

Entity records may carry lightweight spatial references, but geometry itself should live in GeoJSON or another dedicated spatial file. A geometry record should be able to express:

- point, line, or polygon
- source
- precision
- confidence
- `valid_from`
- `valid_to`

This allows political borders, appellations, vineyard parcels, and other boundaries to change through time.

## Temporal model

Dates are intervals when the evidence only supports intervals. Never manufacture exact dates.

Use:

- `valid_from`
- `valid_to`
- `observed_at`
- `precision` such as `day`, `month`, `year`, `range`, `unknown`

A relationship such as ownership may therefore be true only during a stated interval.

## Projections

Future projections may include:

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
