# CARTA

**Working expansion:** Cartography · Ampelography · Relationships · Time · Access

CARTA is a sibling knowledge project to Natural Wine 2.5. It is not an expansion of the curriculum canon.

Natural Wine 2.5 remains deliberately compressed for teaching. CARTA is allowed to expand: more grapes, producers, people, vineyards, places, appellations, wines, practices, institutions, historical events, market signals, and evidence-backed relationships can enter as the knowledge system warrants them.

> The reference system can become expansive while the curriculum remains edited.

## Three knowledge layers

1. **Reference** — governed identities, sourced claims, typed relationships, naming assertions, spatial records, and temporal records intended to remain useful beyond a single moment.
2. **Frontier** — dated, perishable signals about what is emerging, changing, becoming visible, scarce, newly available, or culturally important.
3. **Lens** — personal observations, taste preferences, hypotheses, watchlists, production questions, and other exploratory material. Lens records may guide research but do not become reference truth merely because they are interesting.

## Four product surfaces

CARTA's structured records are the machine authority, but they are only one surface of the system.

1. **Machine authority** — entities, relationships, claims, sources, names, and geography.
2. **Human Atlas** — readable Markdown pages for grapes, producers, people, regions, countries, appellations, ecosystems, wines, and other useful objects.
3. **Visual interfaces** — maps, TRAMA network views, timelines, genealogy, Frontier/access views, and future spatial tools.
4. **AI / query layer** — agents and search interfaces operating over the same governed authority.

## STRATA v0.2

The ontology and schema are called **STRATA**: Space · Time · Relationships · Appellations · Terroir · Ampelography.

v0.2 is the first post-pilot revision. It incorporates what the Pyrenean Atlantic research exposed:

- source fitness is assessed claim by claim rather than through a universal source hierarchy;
- importer and distributor evidence can substantively carry producer-world facts when fit to the claim;
- legal, local, and historical names can be represented without manufacturing duplicate entities;
- country, administrative, cultural, historical, wine, and analytical regions can remain distinct;
- useful spatial knowledge can exist without fabricated geometry;
- ecosystems can connect physical geographies and non-spatial networks;
- the GitHub repository must remain genuinely readable to humans through the CARTA Atlas.

Start here:

- [`docs/architecture.md`](docs/architecture.md)
- [`docs/ontology.md`](docs/ontology.md)
- [`docs/evidence-policy.md`](docs/evidence-policy.md)
- [`docs/atlas-projection.md`](docs/atlas-projection.md)
- [`schemas/entity.schema.json`](schemas/entity.schema.json)
- [`schemas/relationship.schema.json`](schemas/relationship.schema.json)
- [`schemas/claim.schema.json`](schemas/claim.schema.json)
- [`schemas/source.schema.json`](schemas/source.schema.json)
- [`schemas/name-assertion.schema.json`](schemas/name-assertion.schema.json)
- [`schemas/geometry.schema.json`](schemas/geometry.schema.json)
- [`schemas/spatial-assertion.schema.json`](schemas/spatial-assertion.schema.json)
- [`pilots/pyrenean-atlantic.md`](pilots/pyrenean-atlantic.md)
- [`atlas/README.md`](atlas/README.md)

## Current state

STRATA v0.2 is the post-pilot architecture pass. The Deep Research Run 01 candidate packet has **not** yet been ingested. That is intentional.

Next milestone after v0.2 acceptance:

1. normalize Run 01 candidates against the revised schemas;
2. ingest accepted Pyrenean Atlantic entities, relationships, claims, names, sources, and spatial assertions;
3. generate the first human-readable Atlas proof set;
4. audit the resulting graph and cards before expanding to another ecosystem.
