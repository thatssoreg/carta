# CARTA Human Reference Contract v0.2

CARTA's machine-readable graph is the authority. The **Human Reference** is the reading experience. Corrections land in machine records first and flow into the Human Reference through projection.

Those are deliberately not the same thing.

The graph may need separate records for a person, producer, project, wine, appellation, place, name assertion, and relationship. A human reader should not have to experience every machine object as a separate page merely because the ontology does.

## Core product rule

> A CARTA reference page should orient a curious wine person first and expose the machinery second.

The Human Reference is not a schema demonstration. It is a deep wine reference powered by a governed graph.

A reader encountering a grape, producer, region, appellation, landscape, wine, or ecosystem for the first time should be able to leave the page understanding what it is, what it is like, why it has mattered, who or what defines it, and where to go next.

Machine IDs, claim IDs, confidence tables, rejected edges, and revision history remain available, but they belong at the bottom of the page or inside a clearly subordinate evidence section.

## Human profiles are composite projections

Human profiles do **not** map one-to-one to entities.

Example:

A single **Alfredo Egia** producer profile may compose:

- `person:alfredo-egia`
- `producer:alfredo-egia-wine`
- `project:hegan-egin`
- `wine:rebel-rebel`
- related grapes, places, appellations, people, and claims

The machine graph keeps those identities separate. The human page composes them into one coherent reference experience.

Use `schemas/reference-profile.schema.json` and `data/reference-profiles/` to govern this projection layer.

## Reference maturity and promotion

Discovery does not equal publication.

CARTA uses three human-reference maturity levels:

### `node`

Enough evidence exists for the object to participate in the graph, but not enough for a useful standalone reference page.

A node may appear in links, network views, indexes, and relationship tables without receiving a full Human Reference profile.

### `baseline`

Enough evidence exists for a **generous, genuinely useful reference profile**. Baseline is not a thin card.

A baseline profile should answer the ordinary questions a serious wine reader would reasonably ask about that kind of object.

### `deep`

A mature dossier with unusually strong depth: historical development, multiple representative anchors, richer site or production detail, cultural context, current movement, meaningful contradictions, and a dense relationship network.

`publication_status` is separate from maturity. A profile may be queued, stubbed during migration, published, deliberately machine-only, or deprecated.

### Projection disposition invariant

Every active producer, country, and grape must occur in a governed `reference_profile` disposition. This is a projection-layer closure rule, not a claim that every entity deserves a page.

- `published` requires baseline or deep maturity and a canonical Atlas path.
- `stub` requires an honest node surface and a canonical Atlas path. It must identify itself as incomplete rather than imitating baseline depth.
- `queued` reserves a governed surface while enrichment or migration remains pending.
- `machine_only` is an explicit node-level deferral with no Atlas path.
- `deprecated` preserves historical profile governance without presenting a current surface.

The validator enforces this invariant for active producers, countries, and grapes. New ingestion therefore cannot create another invisible high-value producer or silently omit an entire country/grape population from projection governance.

## Promotion rule

When a graph node becomes important enough that CARTA expects a reader to click into it, the node should trigger a **baseline enrichment pass** before CARTA presents it as a finished reference profile.

A famous or consequential producer is not permitted to remain a one-edge "network node" simply because that was enough for the ecosystem research question that first discovered them.

Richard Leroy is the first explicit example of this rule.

## Editorial voice

### Do

Write like a serious, readable wine reference.

Lead with the object itself:

- who the producer is;
- what the grape is;
- what the region is like;
- what the appellation governs;
- what the wine is;
- what makes a landscape coherent.

Use concrete language about wine, farming, geography, history, culture, and style.

### Do not

Do not foreground project-aware headings such as:

- Why this producer matters in CARTA
- Why I should care
- What CARTA is watching
- Where it fits in CARTA

CARTA may appear where genuinely useful, but the reader should not feel as though every page is explaining the database to them.

Preferred headings include:

- Overview
- Background & trajectory
- Place & vineyards
- In the vineyard
- In the cellar
- Style
- History & significance
- Wines to know
- Producers to know
- Projects & collaborations
- Names & genetics
- Geography
- Appellation rules
- Current developments
- Open questions
- Explore next
- Sources

## Representative anchors

Reference pages should provide selective anchors rather than exhaustive catalogues.

Anchors can include:

- benchmark or historically important producers;
- widely known reference producers;
- contemporary interpreters;
- emerging producers when the Frontier evidence is strong;
- representative wines;
- important projects or collaborations.

"Known" does not mean "best." "Benchmark" does not mean "most expensive." Scarcity does not imply importance.

Where useful, label the role of an anchor explicitly: `historic`, `benchmark`, `contemporary`, `emerging`, `regional`, `stylistic`, or similar editorial language.

## Producer profiles

A **baseline producer profile should be generous**. When knowable, it should include:

1. **Overview** — who they are, where they work, what they are known for, and the broad shape of their work.
2. **Background & trajectory** — origin story, prior work, training, mentorship, succession, or meaningful career path.
3. **Place & vineyards** — region, villages, sites, ownership/rental/purchased fruit distinctions where known, elevation/aspect/geology where meaningful.
4. **Farming** — organic/biodynamic/regenerative or other practice, certification where relevant, vineyard philosophy, notable material choices.
5. **Cellar approach** — fermentation, extraction, vessels, élevage, sulfur, filtration, and other recurring practices without turning one vintage into a timeless recipe.
6. **Grapes** — primary and secondary material, including meaningful local or unusual varieties.
7. **Wines to know** — several representative wines when the producer makes several; not necessarily exhaustive.
8. **Projects & collaborations** — side projects, shared labels, négociant work, incubators, family projects, or collaborative cuvées.
9. **People, lineage & influence** — documented work, mentorship, collaboration, succession, family, and cultural-transmission relationships. Stylistic resemblance alone is not lineage.
10. **Style & significance** — what the wines tend to explore, how the work relates to regional expectations, and why the producer matters in the wider wine world.
11. **Appellation / classification context** — relevant legal relationships, declassification, unusual compliant work, or tensions with local categories.
12. **Access** — importer/distributor relationships and dated Frontier availability when useful, clearly separated from permanent producer identity.
13. **Explore next** — a small editorial set of useful rabbit holes.
14. **Sources**.
15. **Record & provenance** — machine IDs, claims, confidence, unresolved edges, and revision history at the bottom.

A producer with only name + location + one relationship is a graph node, not a baseline producer reference.

### Person versus producer

Person and producer identities remain separate in the graph when warranted. The Human Reference usually presents a **composite producer profile named for the producer or principal maker** and pulls the relevant person record into it.

A separate person page is useful only when the person's career meaningfully exceeds one producer identity, for example a consultant, scientist, writer, importer, winemaker with multiple estates/projects, or major cultural transmitter.

## Grape profiles

A baseline grape profile should include:

1. **Overview** — what the grape is, where it is associated, and its broad significance.
2. **At a glance** — color, origin, ripening, acid behavior, vigor, berry/cluster structure, disease tendencies, and other durable viticultural traits where supported.
3. **In the vineyard** — practical growing behavior and site/climate interaction.
4. **In the glass** — useful structural and sensory range without deterministic tasting-note language.
5. **Styles** — common, historic, important, and emerging forms: dry, sweet, sparkling, oxidative, skin-contact, fortified, etc. only when supported.
6. **History & significance** — what role the grape has played, where it gained or lost importance, and why.
7. **Where it matters** — countries, regions, appellations, and important cross-border contexts.
8. **Producers to know** — selective historic, benchmark, contemporary, and emerging anchors.
9. **Wines to know** — representative bottles/cuvées when useful.
10. **Names & genetics** — prime name, synonyms, legal/local names, confusion risks, parentage, mutations, and genetic neighbors with uncertainty preserved.
11. **Current developments** — planting growth, revival, new regions/styles, climate relevance, or current attention when evidenced.
12. **Explore next**.
13. **Sources**.
14. **Record & provenance** at the bottom.

A grape page should never begin with its ontology problem. It should begin by telling the reader about the grape.

## Country profiles

Country pages are broad reference-navigation surfaces, not attempts to summarize an entire national wine culture in a few paragraphs.

They should orient the reader to:

- major wine geographies represented in CARTA;
- regional and appellation systems;
- important grape families and naming systems;
- notable producer traditions and networks;
- broad legal/classification structure;
- historical forces that materially shaped the current wine landscape;
- cross-border landscapes and ecosystems;
- current developments;
- representative rabbit holes.

The Human Reference physically nests country-specific regions and appellations beneath countries where appropriate.

## Region profiles

A region is a human geographic or wine-geographic reference object. It may be administrative, historical, cultural, or wine-geographic, but the page must say which.

A baseline region profile should cover:

- overview and geographic orientation;
- topography, climate, hydrology, geology/soils where meaningful;
- viticultural conditions;
- grapes;
- wine styles;
- important appellations or classifications;
- producers to know;
- cultural/historical significance;
- internal diversity;
- current developments;
- neighboring or overlapping geographies;
- Explore next.

## Appellation profiles

Appellations are legal/regulatory wine objects and are nested beneath their country in the Human Reference.

A baseline appellation profile should cover:

- overview and location;
- legal identity and jurisdiction;
- landscape and growing conditions;
- permitted/recommended/prohibited grapes where relevant;
- major production rules that materially shape the wines;
- normal and notable styles;
- history and significance of the appellation rather than only a chronology;
- producers and wines to know;
- unusual but compliant expressions;
- declassification or boundary tensions;
- current developments;
- Explore next;
- authoritative sources and legal version dates.

## Landscapes

`atlas/landscapes/` is for physical, climatic, geological, watershed, island, mountain, or cultural-landscape reference objects that may cross national borders.

Examples may include:

- Western Pyrenees
- Mosel river system
- Alpine arc
- Canary Islands volcanic systems

A landscape is not automatically an appellation, administrative region, or ecosystem.

## Ecosystems

Ecosystems are **relationship-generated analytical objects**, not a substitute for cross-border geography.

The Pyrenean Atlantic ecosystem is useful because it braids several geographies plus professional relationships that reach as far as Richard Leroy in the Loire. That is why it is not merely a region or landscape.

Ecosystem pages can remain more explicitly analytical than ordinary reference pages, but should still read as substantive wine essays rather than schema explanations.

## Wine profiles

A wine profile should explain:

- producer;
- place/site when known;
- grape composition or range across vintages;
- style and production approach;
- why the wine is representative, unusual, historically important, or otherwise useful;
- vintage variability where material;
- related wines/projects;
- access information if useful and dated.

Persistent cuvée identity must remain separate from vintage-specific claims.

## History

Timelines are supporting tools, not substitutes for history.

Human pages should explain **significance**:

- what changed;
- why it mattered;
- what it made possible or displaced;
- how it affected grapes, producers, law, land, culture, trade, or style.

Dates belong where they sharpen understanding.

## Sensory and style writing

Avoid both extremes:

- deterministic tasting-note stereotypes;
- sterile refusal to describe wine at all.

CARTA should describe **ranges, structures, recurring tendencies, and style families** with appropriate caveats.

A useful grape reference can say a variety often combines high acidity with significant sugar accumulation or tends toward particular structural possibilities without claiming every bottle tastes the same.

## Human geography and repository layout

The Human Reference uses a reader-facing hierarchy even though the graph remains relational and comparatively flat.

```text
atlas/
  countries/
    france/
      README.md
      regions/
      appellations/
    spain/
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
```

Rules:

- Country-specific appellations live beneath countries in the Human Reference.
- Country-specific regions normally live beneath countries.
- Cross-border physical/cultural geographies belong under `landscapes/` when they are genuinely geographic.
- Relationship-generated analytical constructs belong under `ecosystems/`.
- The machine graph does not need to mirror this directory hierarchy.

## Explore next

Every mature page should end its read-first layer with a small, editorially chosen set of lateral paths.

Do not dump every graph edge.

Choose the relationships most likely to deepen understanding.

### Governed navigation and reciprocal discovery

Machine graph connectivity and Human Reference navigation eligibility are different questions. The machine graph records supported or provisional typed authority. The projection resolver asks whether a shared component, direct edge, explicit anchor, structural country route, or two-hop path is appropriate for the reader job of the source profile kind. Rejecting a navigation candidate does not delete, weaken, or hide the underlying graph relationship from other machine and analytical surfaces.

The generator resolves every surfaced target through its canonical `reference_profile` path and writes a deterministic `Explore CARTA` block. It keeps the existing 16-link cap and uses only route tier, shortest distance, case-folded title, and profile ID for ordering. Alphabetical order is therefore only a stable tie-breaker inside an already eligible route tier; it is not a semantic score.

#### Structural countries versus editorial anchors

`country_entity_ids` records structural geographic assignment. It provides a strong outbound containing-country link from the subject page and a downward country-to-region/appellation orientation route. It does not make producers, grapes, classifications, or other subjects reciprocal country-page recommendations merely because they share the country assignment.

`representative_anchor_ids` records explicit editorial selection. It remains strong outbound projection authority and retains reciprocal discovery. An editorial anchor can select a component inside a composite profile without creating another relationship graph.

Machine-only dispositions are never rendered as fake links. When an outbound country or editorial anchor is deliberately machine-only, the generated block may identify it as deferred plain text. Broken or stale canonical paths remain ordinary validator failures.

#### Direct and two-hop routes

Shared components, direct governed relationships, structural country routes, and explicit editorial anchors do not need two-hop inference and therefore bypass the two-hop kind gate. This preserves professional history, mentorship/collaboration, sites and vineyards, production, grape composition, legal/appellation context, and other direct subject evidence. The resolver does not manufacture inverse machine authority when it traverses an eligible relationship in either direction for discovery.

Graph-only paths of exactly two relationships use these inspectable source-kind rules:

| Source profile kind | Two-hop reader policy |
|---|---|
| `country` | Admit geographic, ecosystem, grape, and classification orientation targets; reject producer/person/wine adjacency unless a direct or editorial route independently supports it. |
| `region`, `appellation`, `landscape` | Reject peer geography when every path climbs a broad container and descends elsewhere; retain downward containment and other governed context. |
| `grape` | Reject general grape or classification adjacency established only by a two-hop wine/classification bridge; retain represented geography and producer/production context. |
| `producer`, `person` | For producer/person targets, require at least one path carrying professional, parcel/site, farming, planting, or explicit-practice semantics; reject paths supported only by broad grape, classification, or geography components. |
| `classification`, `ecosystem`, `wine`, `institution`, `practice`, `historical_event` | Retain governed two-hop context until surfaced fixtures demonstrate a narrower reader job. Direct and anchor behavior remains unchanged. |

Every schema profile kind must have an explicit entry in the production policy map. A new kind therefore cannot silently inherit accidental two-hop behavior.

Directional geography is evaluated from the authored relationship direction. Appellation → region → country and country → represented internal region/appellation are useful orientation. Jura → France → Loire Valley and Napa Valley → California → Santa Ynez Valley are up-then-down sibling traversal and are ineligible without another direct or editorial route. The projection never guesses missing containment to rescue a familiar geography.

Composite producer profiles still begin traversal from every governed component entity. Compression does not, however, promote producer → component wine → broad grape/classification → component wine → producer into a recommendation. A two-hop producer-world route survives only when an eligible specific path explains the connection; direct professional, site, production, and anchor routes continue to survive.

#### Auditing navigation quality

`scripts/audit_navigation.py` imports the production resolver, enumerates every relationship-record path with predicates and directions, reconstructs the Run 10 baseline, and evaluates the unchanged 28-page A–E ratings fixture. `tests/test_navigation.py` asserts focused route decisions and includes the full fixture regression. Re-run both with:

```text
python scripts/audit_navigation.py \
  --ratings audits/run-10-human-reference-navigation-ratings.json \
  --format json
python -m unittest discover -s tests -v
```

Run 11 changed projection eligibility and route explanation only. It did not change STRATA v0.2, the relationship vocabulary, machine authority, profile kinds, the 16-link cap, persistent wine identity, composite project/vineyard treatment, or the rule that generated Human Reference pages are projections rather than authority.

## Evidence and machine layer

Near the bottom of a mature reference page, use a subordinate section such as:

```markdown
## Sources
...

<details>
<summary>Record & provenance</summary>

Machine IDs, relationship tables, claim IDs, confidence, unresolved questions, revision history.

</details>
```

GitHub Markdown limitations may require a normal heading instead of `<details>` in some generated contexts. The principle is more important than the exact rendering.

For published profiles, this section should be a deterministic compact projection rather than a manually maintained second fact store. At minimum it should make discoverable:

- the profile's component CARTA entities;
- material claims used by the page;
- relevant sources;
- status or confidence where material;
- unresolved or contested questions where applicable.

Derive reverse lookup from canonical forward records: `claim.subject_ref`, `name_assertion.entity_id`, and `spatial_assertion.entity_id`. Do not restore entity-side reverse indexes merely to populate prose.

## Discovery versus enrichment workflow

CARTA now separates two research jobs.

### Ecosystem discovery

Purpose: discover what entities and relationships are needed to understand an ecosystem.

Output: graph nodes, claims, relationships, open questions, geography, candidate Frontier signals.

### Entity enrichment

Purpose: make promoted objects genuinely useful as human references.

Output: baseline/deep producer, grape, region, appellation, landscape, wine, and country dossiers with representative anchors and readable synthesis.

An ecosystem discovery run should not be expected to produce deep profiles for every adjacent entity it encounters.

## Projection maintenance

Each governed Human Reference profile has one canonical path. Alternate Markdown may serve navigation or historical context, but it must not claim parallel governed status. Profile indexes, provenance, and counts are derived or validated from machine authority so growth does not require hand-maintaining duplicate state.

`python scripts/validate_data.py --write-human-reference` creates honest node shells for new `stub` dispositions, refreshes generated navigation, provenance, and all indexes, and must be followed by a normal validation run. Generated files are committed with the governing records.

Projects and vineyards remain valid primary/component entities inside composite producer-world profiles. Current cases such as Tzum, Vins Pepe Raventós, Soleras del Pacífico, Moon Hill Farm, Evangelho Vineyard, Kronos Vineyard, Sunbasket Vineyard, Westhofener Kirchspiel, and Terrasses del Serral remain understandable without separate `project` or `vineyard` profile kinds. Add those kinds only if a future case cannot be represented honestly through the composite model.
