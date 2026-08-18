# CARTA Atlas

This directory is the human-readable projection of CARTA's accepted machine authority.

> A person should be able to click into CARTA and understand an entity without reading JSONL.

The first proof set was generated from the accepted Pyrenean Atlantic Run 01 ingestion against STRATA v0.2.

## Start here

- [Pyrenean Atlantic ecosystem](ecosystems/pyrenean-atlantic.md)
- [Grapes](indexes/grapes.md)
- [Producers and people](indexes/producers-and-people.md)
- [Places and law](indexes/places-and-law.md)
- [Wines](indexes/wines.md)

## Card families now represented

- `ecosystems/`
- `countries/`
- `regions/`
- `appellations/`
- `grapes/`
- `producers/`
- `people/`
- `projects/`
- `wines/`
- `indexes/`

Future families remain available for institutions, practices, classifications, historical events, and other entity types when the accepted data becomes rich enough to justify a readable page.

## Authority rule

The structured records under `data/` are authoritative if an Atlas page and a machine record disagree.

Read-first prose is allowed to synthesize accepted evidence, but factual relationships, names, dates, geography, legal status, and source lists should remain traceable to the machine layer.

See [`../docs/atlas-projection.md`](../docs/atlas-projection.md).
