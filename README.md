# CARTA

**Cartography · Ampelography · Relationships · Time · Access**

CARTA is a spatial-temporal wine knowledge and field-intelligence system and a sibling project to Natural Wine 2.5.

Natural Wine 2.5 remains deliberately compressed for teaching. CARTA is allowed to expand: grapes, producers, people, vineyards, places, appellations, wines, practices, institutions, historical events, dated Frontier claims, and evidence-backed relationships can enter as the knowledge system warrants them.

> The reference system can become expansive while the curriculum remains edited.

## Core knowledge layers

1. **Reference** — governed identities, sourced claims, typed relationships, names, geography, and temporal knowledge.
2. **Frontier** — dated, perishable signals about what is emerging, changing, scarce, newly available, or culturally important.

**Personal Lens is external to CARTA core.** Private overlays may hold personal observations, taste preferences, holdings, hypotheses, watchlists, or production questions and may reference stable CARTA IDs, but that information is not stored in the shareable core repository and does not become Reference truth automatically.

## Four product surfaces

1. **Machine authority** — entities, relationships, claims, sources, names, and geography.
2. **Human Reference** — reader-first Markdown profiles that may compose several machine records into one coherent reference.
3. **Visual interfaces** — maps, TRAMA network views, timelines, genealogy, Frontier/access views, and spatial tools.
4. **AI / query layer** — agents and search interfaces over the same governed authority.

## STRATA v0.2

STRATA means **Space · Time · Relationships · Appellations · Terroir · Ampelography**.

The ontology distinguishes biological identity, legal naming, geography, professional relationships, production, classification, time, and evidence rather than flattening them into generic “connections.”

## Human Reference

The Human Reference is a deep wine reference, not a database demonstration.

Governed profile records determine publication status and canonical paths; the Atlas and its indexes are projections of those records and the underlying machine authority.

Start with [`atlas/README.md`](atlas/README.md).

## Machine authority

Counts are derived from canonical records rather than maintained in this README. Validation runs through `scripts/validate_data.py` and GitHub Actions.

## Repository hygiene

CARTA keeps durable product and reference infrastructure, not the conversational scaffolding used to create it.

Prompts, chat transcripts, scratch plans, and temporary queues stay outside the repository unless they become genuinely reusable operating artifacts. Durable audits may remain when they materially explain accepted editorial or evidence decisions.

## Architecture

- [`docs/architecture.md`](docs/architecture.md)
- [`docs/ontology.md`](docs/ontology.md)
- [`docs/evidence-policy.md`](docs/evidence-policy.md)
- [`docs/atlas-projection.md`](docs/atlas-projection.md)
- [`schemas/reference-profile.schema.json`](schemas/reference-profile.schema.json)
