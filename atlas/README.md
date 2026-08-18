# CARTA Human Reference

The Human Reference is the reader-facing projection of CARTA's machine authority.

It is designed as a deep wine reference, not as a display of database structure.

The machine graph can separate people, producers, projects, wines, places, appellations, claims, and relationships. Human profiles are allowed to compose those records into one coherent reading experience.

## Start here

- [Pyrenean Atlantic ecosystem](ecosystems/pyrenean-atlantic.md)
- [France](countries/france/README.md)
- [Spain](countries/spain/README.md)
- [Grapes](indexes/grapes.md)
- [Producers and people](indexes/producers-and-people.md)
- [Wines](indexes/wines.md)
- [Landscapes](landscapes/README.md)

## Human geography

Country-specific regions and appellations now live beneath their countries in the canonical Human Reference structure:

```text
countries/
  france/
    README.md
    regions/
    appellations/
  spain/
    README.md
    regions/
    appellations/
```

Cross-border physical and cultural geography belongs under `landscapes/`.

Relationship-generated analytical constructs remain under `ecosystems/`.

The older flat `regions/`, `appellations/`, and country Markdown paths remain temporarily as compatibility surfaces from the Run 01 proof set. New reference work should use the nested paths.

## Reference maturity

A valid graph node is not automatically a finished reference page.

CARTA distinguishes:

- **node** - enough to participate in the graph, not enough for a standalone reference;
- **baseline** - generous, publishable reference depth;
- **deep** - mature dossier depth.

Publication state is governed separately through `data/reference-profiles/`.

The Pyrenean Atlantic ecosystem is the first accepted baseline proof. Most Run 01 entity pages are now explicitly treated as stubs or enrichment targets under the Human Reference v0.2 standard.

## Composite profiles

Producer profiles should usually compose the relevant person, producer, project, wine, place, and relationship records rather than forcing a reader to navigate machine ontology one object at a time.

This is why the next enrichment pass will rewrite Alfredo Egia and Imanol Garay as composite producer references and build a real Richard Leroy producer dossier rather than leaving him as a one-edge person page.

## Editorial rule

Reference pages should lead with the subject itself:

- what it is;
- what it is like;
- where it comes from;
- how it developed;
- what styles or wines matter;
- who or what defines it;
- what is changing;
- where to explore next.

CARTA IDs, claims, confidence tables, rejected edges, and revision history belong in a subordinate provenance section near the bottom.

## Authority rule

The structured records under `data/` remain authoritative if a Human Reference page and the machine layer disagree.

See [`../docs/atlas-projection.md`](../docs/atlas-projection.md) for the full Human Reference v0.2 contract.
