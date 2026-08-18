# Pyrenean Atlantic Vertical Slice — Pilot Specification v0.2

**Pilot research status:** Deep Research Run 01 completed on 2026-08-18. Candidate ingestion is intentionally deferred until STRATA v0.2 is accepted. See [`../research/run-01-pyrenean-atlantic/README.md`](../research/run-01-pyrenean-atlantic/README.md).

## Purpose

The first CARTA pilot tests the ontology against a real ecosystem before the graph scales. The goal is not to produce a complete regional encyclopedia. The goal is to discover whether STRATA can represent the relationships that make this ecosystem intelligible.

The research phase succeeded in stress-testing the schema and directly produced the post-pilot revisions in STRATA v0.2.

## Seed, not scope

The original entry points were:

- Alfredo Egia
- Imanol Garay
- Richard Leroy
- the western Pyrenees / Basque–Béarn–Jurançon corridor
- Petit Manseng
- Gros Manseng
- Petit Courbu / Hondarrabi Zuri Zerratia
- Courbu Blanc / Hondarrabi Zuri
- Raffiat de Moncade

These were seeds, not a closed list. The research run had explicit authority to add people, producers, grapes, wines, vineyards, places, appellations, institutions, practices, historical events, and geographic features when an evidence-backed relationship materially improved understanding of the ecosystem.

## Expansion rule

Add an entity when it is needed to explain one or more of:

- identity or naming;
- grape genetics or plant material;
- producer lineage, mentorship, work history, or collaboration;
- physical geography or spatial relationship;
- cultural transmission;
- appellation or regulatory structure;
- historical change;
- viticulture or site conditions;
- production practice;
- distribution, access, or market visibility;
- a meaningful contradiction, disputed relationship, or category boundary.

Do not add an entity merely because it is famous, nearby, fashionable, stylistically similar, sold by the same importer, or mentioned in the same discourse.

## Semantic saturation

Continue outward until newly discovered nodes are predominantly peripheral, duplicative, weakly evidenced, or fail to add a materially new relationship type or explanatory mechanism.

The pilot has no entity quota.

## Required proof surfaces

The accepted pilot should ultimately leave enough governed data to support at least four machine/visual projections plus a human-readable Atlas:

1. **Spatial view** — producer sites/cellars, relevant places, appellations, physical geography, and explicitly approximate/source-described spatial assertions where exact geometry is unavailable.
2. **TRAMA network view** — mentorship, work, collaboration, ownership, grape use, and other typed relationships.
3. **Ampelographic view** — synonyms, jurisdictional names, naming collisions, genetics, proposed genetics, traditional regions, and grape use.
4. **Temporal view** — historical/legal/ownership changes where evidence supports them.
5. **Human Atlas** — readable Markdown cards and ecosystem synthesis driven by the accepted records.

The ecosystem page must explain: **Why are all these things connected?**

## Questions the accepted pilot should be able to answer

- Trace Egia → Garay → Leroy and distinguish the evidence type for each edge.
- Show where Petit Courbu / Hondarrabi Zuri Zerratia is used and distinguish biological identity from jurisdictional naming and nearby/confused varieties.
- Show where Petit and Gros Manseng co-occur with Courbu-family material and distinguish documented genetics from geographic association.
- Identify producers on opposite sides of the western Pyrenees working the same grape under different names.
- Show which relevant geographic units overlap and which are merely adjacent: political border, appellation, watershed, mountain system, cultural region, and analytical ecosystem.
- Identify what is current Reference knowledge versus a Frontier signal about emerging attention or U.S. access.
- Surface unresolved or contradictory claims instead of smoothing them over.
- Remain readable in GitHub through grape, producer, region, appellation, country, and ecosystem Atlas pages.

## Additional Lens test

Use the pilot to test a personal/production-development question without promoting it to Reference truth:

> Which grape/site/production combinations in this ecosystem may help explain high-acid white wines that also retain textural mass, and what comparisons might be useful for Virginia and future Parallax Project exploration?

The pilot must separate cultivar physiology, site, climate, farming, harvest timing, and cellar choices when evidence permits, and must preserve uncertainty where causal attribution is not possible.

## Research-phase findings that changed STRATA

Deep Research Run 01 established that STRATA v0.1 needed:

- claim-specific source fitness rather than a universal source hierarchy;
- first-class jurisdictional name assertions;
- place semantics through `place_kind`;
- source-described spatial assertions that do not require fabricated geometry;
- first-class `ecosystem` identity for relationship-generated analytical objects;
- a required human-readable Atlas projection.

These are now STRATA v0.2 design requirements.

## Success criteria for ingestion

The pilot succeeds after ingestion if:

- no entity type feels obviously overloaded;
- relationship predicates remain meaningfully distinct;
- contradictory claims can coexist without corrupting identity;
- spatial and temporal records can change independently of narrative;
- source fitness can represent wine-trade knowledge without automatically penalizing importer/distributor evidence;
- the graph supports questions that a conventional country → region → appellation hierarchy cannot answer;
- the data can plausibly drive a map and network interface without restructuring the whole repository;
- the same accepted data can generate human-readable Atlas cards without factual drift.

STRATA is expected to keep changing after future pilots. That remains a feature, not a failure.
