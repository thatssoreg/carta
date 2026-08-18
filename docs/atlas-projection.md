# CARTA Human-Readable Atlas Contract v0.1

CARTA's machine-readable records are the data authority. They are not the primary human reading experience.

The **CARTA Atlas** is a required Markdown projection of that authority so the repository remains useful to a person browsing GitHub, not only to code or an AI agent.

## Core rule

> A person should be able to click into CARTA and understand an entity without reading JSONL.

Atlas pages may synthesize and organize accepted records, but they may not silently invent facts that do not exist in the underlying claims, relationships, naming assertions, spatial records, or editorial synthesis.

## Repository shape

The intended projection is:

```text
atlas/
  ecosystems/
  countries/
  regions/
  appellations/
  grapes/
  producers/
  people/
  wines/
  institutions/
  practices/
  classifications/
  historical-events/
  indexes/
```

Not every entity type requires a page immediately. A page is generated or authored when the entity has enough accepted material to be useful to a human reader.

## Card families

### Grape cards

A grape card should prioritize:

1. **Why it matters**
2. **Identity and naming**
3. **Where it is grown / legally recognized**
4. **Genetics and biological relationships**
5. **Viticultural structure**
6. **Producer and wine connections**
7. **Structural/style range without deterministic tasting notes**
8. **Timeline where relevant**
9. **Open questions / contested claims**
10. **Sources and revision history**

A grape card should make jurisdictional names legible without flattening them into universal synonyms.

### Producer cards

A producer card should prioritize:

1. **Why this producer matters in CARTA**
2. **Person / estate / project identity**
3. **Place and farming footprint**
4. **Work, mentorship, collaboration, family, and succession network**
5. **Grapes**
6. **Farming and cellar practice**
7. **Key wines / projects**
8. **Appellation and classification relationships**
9. **Access / Frontier observations, clearly dated**
10. **Timeline**
11. **Open questions / disputed edges**
12. **Sources and revision history**

A producer page must not collapse a person, producer entity, collaborative project, or label when CARTA stores them separately.

### Person cards

A person card emphasizes career, roles, work history, mentorship, collaboration, family, cultural transmission, and the entities they founded, worked for, or participated in.

It should link clearly to producer and project cards rather than repeating those identities as if they were the same object.

### Region cards

A region card is generated from a `place` entity with an appropriate `place_kind` such as `wine_region`, `cultural_region`, `historical_territory`, or `administrative_region`.

It should prioritize:

1. **What this place means in CARTA**
2. **What kind of region it is**
3. **Geographic orientation**
4. **Overlapping and adjacent geographies**
5. **Appellations inside or overlapping it**
6. **Grapes and plant material**
7. **Producer networks**
8. **Climate, topography, hydrology, geology, and viticulture where evidenced**
9. **Historical changes**
10. **Current Frontier signals**
11. **Ecosystems that touch it**
12. **Open questions and sources**

A region card must not imply that an administrative, cultural, historical, legal, and analytical geography are the same because they share a label.

### Appellation cards

An appellation card is a legal/regulatory reference surface.

It should prioritize:

1. jurisdiction and legal identity;
2. current and historical boundaries;
3. creation and major revisions;
4. permitted / recommended / prohibited grapes;
5. production rules that matter to interpretation;
6. landscapes and places it overlaps;
7. producers and wines represented in CARTA;
8. unusual but compliant expressions;
9. declassification or boundary questions;
10. authoritative sources and version dates.

### Country cards

Country cards are **meta-navigation and synthesis surfaces**, not national wine encyclopedias.

A country page should answer:

- Which CARTA ecosystems touch this country?
- Which wine regions and appellations are currently represented?
- Which grape identities cross its borders under different names?
- Which producer networks move into or out of it?
- Which historical/legal turning points materially shape the represented wine world?
- Which Frontier signals are active?
- Where should a reader go next?

Country pages should be generated from `place` entities with `place_kind: country`.

### Ecosystem cards

An ecosystem card explains a relationship-generated field of inquiry.

It must state explicitly what kind of object it is and what it is **not**.

For example, the Pyrenean Atlantic ecosystem should say that it is not a single historical territory, appellation, or government region. Its usefulness comes from the braid of physical geography, legal geographies, grape-name systems, producer relationships, and professional networks.

An ecosystem page should prioritize:

1. **Why this ecosystem exists**
2. **Seed and discovered entities**
3. **Physical geography**
4. **Legal geography**
5. **Grape / naming / genetic network**
6. **Producer and cultural-transmission network**
7. **Timeline**
8. **Frontier / access layer**
9. **Contradictions and rejected edges**
10. **Why these things are connected**
11. **Where the explanatory boundary currently stops**
12. **Sources and revision history**

### Wine cards

Wine pages should be used when a wine or cuvée is itself a meaningful relationship node. They should distinguish persistent cuvée identity from vintage-specific claims and avoid turning one vintage's blend or cellar treatment into a timeless recipe.

## Page personality

Each page should have two layers of readability.

### Read-first layer

Near the top:

- Why I should care
- Where it fits
- What connects to it
- What makes it distinctive
- What CARTA is watching
- What remains unresolved

This is the primary human reading surface.

### Evidence layer

Further down:

- Typed relationships
- Naming assertions
- Spatial records
- Timeline
- Claims and confidence
- Sources
- Revision history

A reader should be able to stop after the first layer or inspect the machinery underneath.

## Generated versus editorial content

Where practical, factual tables should be generated from structured authority:

- names;
- typed relationships;
- dates;
- source lists;
- legal status;
- geography references;
- Frontier observations;
- open claims.

Human-readable synthesis may be editorially authored for sections such as:

- Why it matters
- Why these things are connected
- What makes this ecosystem useful
- Structural interpretation

Editorial synthesis must remain traceable to accepted claims and may not overwrite unresolved evidence.

## Navigation

Every card should link laterally, not only upward through a hierarchy.

A Petit Manseng page may link to:

- Jurançon;
- Bizkaiko Txakolina;
- the Pyrenean Atlantic ecosystem;
- Savagnin through genetics;
- Alfredo Egia / Rebel Rebel through use;
- Imanol Garay / Ixilune through use;
- Virginia through a clearly labeled Lens comparison.

This lateral navigation is a core CARTA behavior.

## Generation contract

The long-term goal is for Atlas pages to be generated or refreshed from accepted structured records so Markdown and machine authority cannot drift independently.

Until generation scripts exist:

- card prose may be authored manually;
- every factual section must be checked against accepted records;
- machine records remain authoritative if a discrepancy appears;
- any manually authored synthesis should be clearly distinguishable from raw claims.

The first ingestion should produce the initial proof set:

- Pyrenean Atlantic ecosystem page;
- Petit Manseng grape card;
- Petit Courbu grape card;
- Alfredo Egia producer/person surfaces;
- Imanol Garay producer/person surfaces;
- Jurançon appellation/region surfaces;
- at least one country meta card if the accepted data is sufficient.
