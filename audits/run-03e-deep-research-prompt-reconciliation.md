# Run 03E Deep Research Prompt Reconciliation Audit

## Outcome

Run 03E demonstrates that the revised Deep Research prompt was **materially better, but not yet self-policing enough to be trusted without CARTA's reconciliation layer**.

The research report is useful discovery input. It is not authority.

This audit records what improved, what still failed, what survived into CARTA, and what the next Deep Research prompt should tighten.

## What improved

Run 03E followed the four-seed structure and produced substantially better research scaffolding than Run 03D:

- four independent seed dossiers;
- a source ledger with many direct URLs;
- an identity-resolution register;
- a candidate-relationship register;
- a spatial/GIS register;
- a claim-risk register;
- an explicit cross-dossier contamination audit;
- an ingestion-frontier section;
- restrained treatment of existing CARTA clusters rather than recursively expanding Raj Parr, Savoie, Rioja, or Palette.

The report also surfaced several real identity questions that matter to CARTA, especially:

- persistent wine identity across vintages;
- wine versus vineyard identity at Le Haut-Lieu and Vigna La Casa;
- Vaudésir climat versus Chablis Grand Cru appellation;
- Sangiovese versus the local Montalcino name Brunello;
- grower-owned Clary Ranch versus Arnot-Roberts producer identity.

Those are exactly the kinds of problems the fridge-seed method should expose.

## What still failed

### 1. The contamination audit was not actually adversarial

The report concludes:

> “No contamination was found.”

But at least two direct cross-dossier failures survived into the final text:

- the Huet cellar section says Huet avoids new oak “per the Michel approach”;
- the Louis Michel historical section says “All Huet's bottles of Grand Cru have been made steel.”

The second sentence is especially diagnostic because Huet is not a Chablis Grand Cru producer. The audit existed as a section, but the model did not mechanically test its own output against it.

**Disposition:** reject both statements. No relationship or claim was ingested from them.

### 2. Source addressability improved but was incomplete

The prompt required actual URLs for material claims, yet the final candidate-relationship table left its “Direct source URL” cells blank.

The source ledger also contains:

- truncated URLs;
- placeholder ellipses inside URLs;
- entries described as “see find, no separate URL”;
- a malformed Vouvray URL;
- source references that do not provide an addressable claim-level locator.

The report therefore did not satisfy its own statement that every consequential claim was source-addressable.

**Disposition:** the ingestion pass recovered clean first-party, regulatory, institutional, and fit-for-purpose trade URLs independently and attached them to each admitted claim.

### 3. Numeric contradictions were not reconciled

Run 03E gives Vigna La Casa multiple incompatible elevations:

- approximately 220–250 m in the executive summary;
- approximately 500–550 m in the Caparzo dossier.

Caparzo's current first-party site gives **275 m**.

Run 03E also gives Vaudésir an unsupported 300–330 m elevation and gives Clary Ranch both an erroneous ~35°N placement and later unsupported approximate coordinates.

**Disposition:** ingest only source-addressable numbers. Store no invented coordinates.

### 4. Legal rules and producer practice still blurred

Run 03E claims:

- Chablis Grand Cru requires 12 months in oak;
- Brunello di Montalcino requires 36+ months in oak.

Both fail reconciliation.

Louis Michel's own Vaudésir page describes 18–20 months only in stainless steel, which alone should have triggered a contradiction check against the alleged Chablis oak requirement.

The current Brunello di Montalcino Consorzio rules state a minimum of two years in oak plus four months in bottle.

**Disposition:** legal claims use governing/institutional authority; producer-specific cellar practices remain separate claims.

### 5. Persistent identity was confused with non-vintage identity

The Huet dossier calls Le Haut-Lieu Sec “non-vintage.”

That is not what CARTA's architecture says. A named wine can be vintage-dated while retaining one durable entity across vintages.

**Disposition:** one persistent `wine:domaine-huet-le-haut-lieu-sec` identity; vintage-specific facts remain temporal claims.

### 6. GIS caution was stated but not consistently followed

The report correctly says authoritative vineyard boundaries were unavailable, then supplies approximate vineyard coordinates anyway and suggests deriving boundaries from satellite imagery.

That is false precision relative to CARTA's geography contract.

**Disposition:** source-described spatial assertions only. No inferred points or polygons.

### 7. Certification and farming language still overreached

The report sometimes treated HVE and organic certification as interchangeable, generalized estate farming practices to particular sites, or turned secondary descriptions into certification claims.

**Disposition:** only source-specific, scoped farming claims were admitted. No Louis Michel organic/HVE claim from Run 03E was ingested.

## High-value corrections made during reconciliation

### Domaine Huet

Accepted:

- 1928 founding by Victor and Gaston Huet;
- current 30-hectare Chenin context across Le Haut-Lieu, Le Mont and Clos du Bourg;
- Le Haut-Lieu as a 15-hectare brown-clay site;
- producer-described biodynamic chronology beginning in 1988;
- Vouvray/Chenin legal context;
- persistent Le Haut-Lieu Sec wine identity.

Rejected or withheld:

- “non-vintage” characterization;
- simplified residual-sugar law;
- unsupported MLF/chaptalization/general cellar claims;
- the imported “Michel approach” language.

### Arnot-Roberts / Clary Ranch

Accepted:

- 2001 Arnot-Roberts founding by Duncan Arnot Meyers and Nathan Lee Roberts;
- Paul Clary's 2000 planting;
- current ownership/tending by Drew Beuchley;
- Petaluma Gap placement near Tomales Bay;
- 300-foot elevation, clone 470, Steinbeck-series sedimentary clay loam, organic farming and no-irrigation producer description;
- durable Clary Ranch Syrah identity;
- TTB Petaluma Gap legal context.

Rejected or withheld:

- ~35°N placement;
- approximate coordinates;
- inferred vineyard polygon;
- generalized exact stem/oak/elevage/filtration protocol for Clary Ranch.

### Louis Michel & Fils / Vaudésir

Accepted:

- Chablis producer identity and 1850 history;
- stainless-steel domaine practice;
- Vaudésir as one of seven named climats within Chablis Grand Cru;
- Louis Michel's specific north-facing Vaudésir parcel description;
- planting years 1950/1960/1970;
- current Vaudésir fermentation and 18–20 month stainless élevage.

Rejected or withheld:

- 12-month-oak legal requirement;
- 300–330 m elevation;
- Saint-Martin-sur-Choisille placement;
- “All Huet's bottles of Grand Cru...” contamination;
- unsupported certification and no-chaptalization claims.

### Caparzo / Vigna La Casa

Accepted:

- 1970 estate founding;
- 1977 separate Vigna La Casa vinification / first vintage;
- 1998 acquisition by Elisabetta Gnudi Angelini;
- La Casa at 5 hectares, 275 m, south-to-southeast exposure, galestro;
- current producer cellar protocol;
- current Brunello law;
- Sangiovese's local Montalcino name Brunello.

Rejected or narrowed:

- incompatible 220–250 m and 500–550 m elevations;
- 36-month oak legal requirement;
- “first single-vineyard Brunello in Italy” inflation;
- precise Montosoli slope geometry;
- unverified organic or filtration claims.

## Prompt lessons to carry forward

The next Deep Research prompt should keep almost all of Run 03E's structure, but replace self-certification with tests that are difficult for the model to wave through.

### A. Seed-name contamination scan

Before finalizing each dossier:

1. create an allowlist of names/entities belonging to that seed;
2. search the dossier for the producer names, people, sites, wines, and distinctive terms from every other seed;
3. list every foreign-seed hit;
4. either justify it as an evidenced cross-seed relationship or remove/correct it.

A generic “check for contamination” instruction was not enough.

### B. Claim-source completeness gate

Every candidate claim and candidate relationship should have a `source_id` that resolves to exactly one Source Ledger row with:

- a complete direct URL;
- source type;
- claim-specific fitness;
- temporal scope where relevant.

Blank URLs, `...`, “see find,” or homepage-only placeholders should fail the final quality gate.

### C. Numeric contradiction matrix

Before finalizing, mechanically compare every repeated:

- acreage;
- elevation;
- year/date;
- percentage;
- residual sugar;
- aging duration;
- distance;
- coordinates.

If two sections disagree, the report must resolve or mark the value contested before claiming the audit passed.

### D. Legal-source isolation

Any sentence using words such as:

- required;
- permitted;
- prohibited;
- minimum;
- maximum;
- AOC/AOP/DOCG/AVA rule;
- by law;

must cite a current governing or official institutional source.

Producer practice must never carry a legal rule.

### E. Persistent-identity language

The prompt should explicitly state:

> A persistent wine identity across vintages does not mean non-vintage. Do not use “non-vintage” unless the wine itself is actually sold without a vintage designation.

### F. Coordinate hard gate

No coordinate may appear unless the exact coordinate is provided by an identified source.

No satellite-estimated vineyard point or hand-digitized polygon belongs in a research deliverable intended for CARTA ingestion.

### G. Failed-audit rule

The final report may not say the contamination, source, or contradiction audit is “clean” while any flagged item remains unresolved in narrative text.

The audit should quote or identify the exact corrected passage.

## Assessment

**Run 03E was a better Deep Research prompt.**

It improved the research substrate enough that reconciliation could recover four useful cellar worlds without forcing the graph toward an existing canon. The source, identity, risk, and contamination structures were all worthwhile additions.

But the main remaining lesson is important: **asking the model to audit itself is not the same as making the audit operational.**

CARTA's next prompt should retain the richer research structure and add mechanical gates for foreign-seed names, missing source URLs, repeated numeric conflicts, legal-source provenance, and coordinates.

The reconciliation layer remains necessary, but it should increasingly be adjudicating genuine ambiguity rather than cleaning preventable research-output defects.
