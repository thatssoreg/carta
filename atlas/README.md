# CARTA Human Reference

The Human Reference is CARTA's reader-facing wine reference. It turns governed machine authority into readable profiles, connected paths, indexes, and provenance without becoming a second source of truth.

If you know wine but not CARTA, start by following a few different kinds of rabbit hole.

## A five-minute tour

- **[Pyrenean Atlantic](ecosystems/pyrenean-atlantic.md)**: a relationship-generated ecosystem where law, naming, geography, grapes, producer movement, and collaboration overlap across a national border.
- **[Hiyu Wine Farm](producers/hiyu-wine-farm.md)**: a producer world where sites, people, practice, and a multi-vintage wine test CARTA's persistent wine identity model.
- **[St. Helena AVA](countries/united-states/appellations/st-helena-ava.md)**: a compact example of evidence-backed appellation containment inside [Napa Valley AVA](countries/united-states/appellations/napa-valley-ava.md).
- **[Petit Manseng](grapes/petit-manseng.md)**: a grape-first route into ampelography, place, jurisdictional naming, and producers.
- **[Jurançon](countries/france/appellations/jurancon.md)**: an appellation-first route into legal geography, grapes, history, and surrounding place.
- **[Domaine Labet](producers/domaine-labet.md)**: an honest navigation stub that shows how CARTA keeps useful authority discoverable without pretending every subject has reached full dossier depth.

Then use the complete indexes below to move by grape, producer/person, wine, place, law, landscape, or ecosystem.

## How to read a profile

Human Reference pages usually combine three layers:

1. **Reader-facing orientation** explains why the subject matters and how its wine world fits together.
2. **Explore CARTA** is generated from governed profile dispositions, direct relationships, structural routes, editorial anchors, and eligible graph paths. It is not a hand-maintained recommendation list.
3. **Record & provenance** is generated from machine authority and exposes the profile identity, component records, material claims, sources, and open questions.

A producer page may compose a person, producer identity, project, vineyard, wine, place, and practice into one coherent dossier while those things remain distinct records in the machine layer. A grape page begins with biological identity and moves outward through names, places, producers, wines, and relationships. Country, region, appellation, landscape, and ecosystem pages answer different geographic or relational jobs rather than collapsing into one generic place type.

## What exists, and what does not

Human Reference maturity describes reading depth:

- **node**: useful in the graph, not yet a complete standalone reference
- **baseline**: generous, publishable orientation
- **deep**: mature dossier depth

Publication is a separate decision. An active subject may be published, represented by an honest stub, queued, or explicitly retained as `machine_only`. Machine-only authority can appear in generated indexes without a fake reader-facing page.

Projects and vineyards currently remain inside composite producer-world profiles unless a real representation failure proves that they need a separate projection kind.

## Authority and trust

The machine graph is the knowledge authority. If prose and structured authority disagree, [`data/`](../data/) wins until the conflict is resolved editorially.

Generated sections should never be edited as an independent truth layer. Change the governed records, then run:

```text
python scripts/validate_data.py --write-human-reference
```

CARTA validates profile governance, generated freshness, local Human Reference links, reachability from this page, and the evidence-backed structures that support navigation. Missing geography is not guessed and missing geometry is not fabricated.

For projection semantics and navigation rules, see the [Human Reference projection documentation](../docs/atlas-projection.md).

<!-- BEGIN GENERATED CARTA INDEX DIRECTORY -->
## Complete indexes

- [Grapes](indexes/grapes.md)
- [Producers and people](indexes/producers-and-people.md)
- [Wines](indexes/wines.md)
- [Places, law, landscapes, and ecosystems](indexes/places-and-law.md)
<!-- END GENERATED CARTA INDEX DIRECTORY -->
