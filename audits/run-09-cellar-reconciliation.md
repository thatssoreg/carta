# Run 09 — Cellar Backlog Reconciliation and Activation

## Scope

Run 09 reconciles three parallel research handoffs against CARTA `main @ 27f3ab7f676279b454c8bface1bdd2aaeabb0a5a`, the Run 08 activation posture, STRATA v0.2, the evidence policy, and the Human Reference disposition contract.

Research inputs:

1. Run 09A: Domaine Houillon / Canne; Burgess Cellars / Promiscua; Natus Vini / Intus
2. Run 09B: Prieuré Saint-Jean de Bébian / Tartuguier; Domaine Carrel & Senger / Jongieux Blanc; Domaine Lampyres / Harvest Moon
3. Run 09C: Vindiou / Cœur Fidèle; Numa Cornut / Bourgogne Aligoté, plus targeted Run 08 closure

The external reports remain research handoffs, not machine authority. This pass re-checks their proposed identities and assertions against CARTA's actual schemas and existing records, narrows overreach, preserves contradictions, and adds only representation that the current evidence earns.

## Activation posture

Run 09 activates eight new cellar producer worlds and two load-bearing related Houillon producer stubs needed for honest surname disambiguation:

1. Domaine Houillon
2. Burgess Cellars
3. Natus Vini
4. Prieuré Saint-Jean de Bébian
5. Domaine Carrel & Senger
6. Domaine Lampyres
7. Vindiou
8. Numa Cornut
9. Maison Pierre Overnoy / Emmanuel Houillon
10. Renaud Bruyère & Adeline Houillon

Three new grape identities require explicit Human Reference dispositions: Trincadeira, Dureza and Aligoté.

Existing grape authority is reused wherever possible. In particular, French Grenache/Grenache Noir is governed as a name surface on existing `grape:garnacha-tinta`, and Portuguese Aragonez is governed on existing `grape:tempranillo`. No duplicate grape is created.

All new producer and grape Human Reference surfaces are honest `node/stub` profiles. No broad country, appellation or region fill is introduced.

## Reconciliation decisions

### Domaine Houillon / Canne

Accepted:

- Domaine Houillon is the southern Rhône producer world of Aurélien and Charlotte Houillon at Faucon.
- Canne is one durable wine identity rather than a vintage-specific entity.
- The 2021 release is time-scoped as 70% Grenache and 30% Syrah and Côtes-du-Rhône.
- Weaker 2022 evidence describing 100% Grenache and Vin de France is retained provisionally and time-scoped rather than promoted to a timeless identity fact.
- Aurélien Houillon's sibling relationships to Emmanuel and Adeline Houillon and his Pierre Overnoy mentorship are graph-worthy lineage facts.
- Maison Pierre Overnoy / Emmanuel Houillon and Renaud Bruyère & Adeline Houillon remain separate producer identities. Shared surname and family lineage do not collapse the three worlds.
- Ecocert organic certification is accepted from the specialist importer evidence reviewed; biodynamic language remains a practice description rather than a separate certification claim.

Withheld:

- No universal legal category, blend, maceration length or sulfur protocol is asserted for Canne across vintages.
- No geometry is invented for La Roche Coucourde or any reported parcel.

### Burgess Cellars / Promiscua

Accepted:

- Burgess Cellars remains one producer identity across the 2020 ownership transition.
- Tom Burgess's 1972 founding and Lawrence Wine Estates ownership from 2020 are time-scoped.
- Promiscua is one durable Burgess wine, first attested from the 2021 vintage, made from Cabernet Sauvignon.
- The 2021 production protocol and the 2022 Napa Valley designation remain vintage-scoped.
- Meghan Zobeck and Reid Griggs are represented with dated work relationships rather than contradictory timeless winemaker labels.
- Demeine Estates receives an observation-scoped distribution relationship.

Withheld:

- No organic or regenerative certification is asserted without certificate-level evidence.
- The disputed 2021 case count and exact Clos Abeille contribution are not promoted as settled machine facts.

### Natus Vini / Intus

Accepted:

- Natus Vini is the producer world associated with Hamilton Reis at Vidigueira, Alentejo.
- Intus is retained inside the Natus producer world rather than invented as a separate producer.
- Intus Tinto is one durable wine identity.
- The reviewed 2022 release is time-scoped to Trincadeira and Aragonez, with Aragonez governed on existing Tempranillo authority.
- Vinho Regional Alentejano is represented through an Alentejano protected-geography authority surface rather than being mislabeled as Vidigueira DOC.

Withheld:

- No timeless Intus blend is asserted.
- No named third-party grower entities are fabricated.
- Organic certification scope remains outside this activation where the handoff did not provide certificate-level authority adequate for a clean machine assertion.

### Prieuré Saint-Jean de Bébian / Tartuguier

Accepted:

- The seed spelling is corrected to `Tartuguier`; `Tartuguière` is retained as a rejected spelling assertion so the mistaken seed remains auditable.
- Tartuguier is one durable Bébian wine identity.
- Tartuguier is also the name of a Pézenas watercourse. CARTA therefore represents the hydronym as a `geographic_feature`, not as a vineyard.
- The 2022 composition remains contested because 70/30 Mourvèdre-Grenache and approximately 80/20 descriptions conflict.
- The reviewed 2021–2023 releases are classified as Vin de France.
- Ecocert organic engagement dated 2015-04-23 is retained from Agence Bio evidence.
- Williams Corner Wine receives an observation-scoped importer relationship.

Withheld:

- No cadastral vineyard, parcel boundary, ownership geometry or appellation containment is inferred from the Tartuguier name.
- No reason for the Vin de France choice is invented from an otherwise potentially admissible blend.

### Domaine Carrel & Senger / Jongieux Blanc

Accepted:

- Domaine Carrel & Senger is a continuous producer identity formerly named Domaine Eugène Carrel & Fils; the historical name is governed rather than represented as a second producer.
- Jongieux Blanc is one durable Jacquère wine under Vin de Savoie / Savoie, denomination géographique Jongieux, for the releases reviewed.
- The producer shop's Chardonnay tag is recorded as rejected source-data contamination rather than propagated.
- Williams Corner Wine receives an observation-scoped importer relationship.
- The shared string `Roussette` is recorded as a naming hazard: it must not merge Jacquère and Altesse.

Withheld:

- No automatic synonym edge is created between Jacquère and Altesse.
- No organic claim is created from absence/presence of unrelated environmental certification language.
- The exact nature of the 2022 ownership/partnership transaction is not over-specified.

### Domaine Lampyres / Harvest Moon

Accepted:

- `Domaine Lampyres` is the canonical producer identity, with `Domaine des Lampyres` and `Les Lampyres` retained as trade-name assertions.
- François-Xavier Dauré is the principal person.
- Espira-de-l'Agly is represented as the cellar location; the registered Rivesaltes office remains a sourced claim rather than a false cellar-geography edge.
- Harvest Moon is one durable wine despite material vintage changes.
- The 2023 wine is time-scoped as 50% Grenache / 50% Mourvèdre; the 2024 wine as 90% Grenache / 10% Mourvèdre.
- Both reviewed vintages are Vin de France.
- Ecocert organic engagement dated 2017-08-07 is accepted, while current conversion status is preserved as a dated qualification.
- Dauré's five-vintage work with Tom Lubbe / Domaine Matassa is retained as a source-supported professional-history claim.
- Terres Blanches receives an observation-scoped importer relationship for Harvest Moon.

Withheld:

- The unnamed neighboring fruit grower is not fabricated as an entity.
- Estate and non-estate fruit are not collapsed.
- No timeless blend, sulfur dose or élevage protocol is asserted.

### Vindiou / Cœur Fidèle

Additional reconciliation research resolves two handoff ambiguities:

- INSEE confirms the commune spelling `Plats`.
- Current company-register evidence shows Vindiou as an active wine-producing business managed by Thomas Junique and Cyprien De Lageneste whose activity includes both viticulture and purchasing grapes for vinification. CARTA therefore does not flatten the producer into either a pure estate or a pure négoce.

Accepted:

- Vindiou is the producer identity, founded in 2020 by Junique and De Lageneste.
- Cœur Fidèle is one durable Vin de France wine identity.
- The reviewed 2024 release is 100% Dureza.
- Dureza is introduced as a grape and linked genetically as a parent of existing Syrah on peer-reviewed authority.

Withheld:

- No vineyard ownership or grower identity is inferred for the Cœur Fidèle fruit beyond the source-specific statements.
- No broad producer-style similarity edges are introduced.

### Numa Cornut / Bourgogne Aligoté

Additional reconciliation research materially narrows the producer-type ambiguity in the handoff. Current importer material describes Numa Cornut as a Burgundy estate founded in 2020 with approximately 4.5 hectares of leased and owned vineyards. CARTA therefore represents Numa Cornut as a producer while preserving the mixed tenure model instead of choosing the handoff's all-owned or pure-négoce extremes.

Accepted:

- Numa Cornut is a Burgundy producer world separate from the Cornut family's Château Guiot world in the southern Rhône.
- The seed wine is represented conservatively as `Numa Cornut Bourgogne Aligoté`.
- The 2023 release is time-scoped as 100% Aligoté and Bourgogne Aligoté AOC.
- Aligoté is introduced as a governed grape identity.

Withheld:

- `Vieilles Vignes` remains a provisional name assertion because the distributor product authority reviewed omits it while retailers add it.
- No numerical old-vine age is inferred.
- Château Guiot is not activated as a second producer merely to express family context.

## Run 08 targeted closure

### Sandhi / Anika Grenache 2018

Run 08 correctly left the exact 2018 Grenache appellation unresolved. Run 09 finds merchant evidence explicitly listing Santa Barbara County, but no bottle image, TTB COLA or producer technical sheet adequate to close the legal claim.

Disposition: **REMAINS PROVISIONAL.**

CARTA adds the time-scoped provisional Santa Barbara County claim but does not create a legal-classification edge from it.

### François Blanchard / Le Grand Cléré Ecocert

Run 08 correctly withheld exact certification scope and dates pending certificate-level authority. Run 09 adds first-party evidence stating that the Grand-Cléré parcel is controlled by Ecocert, which materially strengthens the existence of Ecocert control.

Disposition: **PARTIALLY CLOSED.**

Ecocert control is supported. Certificate number, start date and exact historical scope remain unresolved. The existing Run 08 farming claim is not overwritten into false precision.

### Weingut Günther Steinmetz / `No AP`

Run 08 preserved `No AP` as source wording and refused to invent a German legal class. Run 09 adds German Wine Institute authority that Qualitätswein and Prädikatswein that pass the required test receive an Amtliche Prüfungsnummer.

Disposition: **CLOSED AT THE NEGATIVE IMPLICATION; LOWER TIER REMAINS OPEN.**

The 2018 `No AP` wording supports that the wine is not being presented as a tested Qualitätswein or Prädikatswein. It does **not** distinguish Landwein from Deutscher Wein. CARTA records that narrower legal meaning and leaves the exact lower tier unresolved.

Exact sulfur dose remains unresolved.

### Domaine de la Bergerie / Clos de la Bergerie

Run 09C briefly reopened the target against Nicolas Joly's separate wine of the same name because that research run could not read CARTA. Repository reconciliation resolves the identity cleanly: Run 08's subject is `producer:domaine-de-la-bergerie-anjou`, with Anne and Marie Guégniard, and its 2022 `Clos de la Bergerie` is the Coteaux du Layon wine already supported by first-party authority.

Disposition: **RUN 09C IDENTITY DETOUR REJECTED; RUN 08 IDENTITY RETAINED.**

No exact producer-authoritative 2022 ABV or residual sugar is added. Those chemistry questions remain unresolved.

## Naming and identity safeguards earned by Run 09

Run 09 adds or reinforces several high-value anti-collapse rules in the actual authority:

- `Houillon` is not a single producer identity.
- `Tartuguier` and the mistaken `Tartuguière` seed are not interchangeable; the latter also collides with an unrelated Bordeaux estate.
- `Roussette` cannot be used as a string-only bridge between Jacquère and Altesse.
- `Grenache` / `Grenache Noir` reuse Garnacha Tinta authority through governed naming rather than a duplicate grape.
- `Aragonez` reuses Tempranillo authority.
- `Domaine Lampyres`, `Domaine des Lampyres` and `Les Lampyres` are name surfaces on one producer.
- `Domaine Eugène Carrel & Fils` is the historical name of the continuous Carrel & Senger producer identity.
- `Vieilles Vignes` is not promoted into Numa Cornut's canonical wine name until label-level evidence earns it.

## Human Reference closure

Run 09 creates honest producer-world stubs for the eight new cellar worlds plus two related Houillon producer stubs needed for disambiguation.

It also creates grape stubs for Trincadeira, Dureza and Aligoté.

Existing country, producer, grape, region, appellation and classification surfaces will gain reciprocal generated navigation only where governed profiles and graph authority support it. New wines remain discoverable primarily through their composite producer profiles rather than receiving unnecessary parallel wine pages.

The generator remains authoritative for indexes, navigation and provenance. No second hand-maintained graph is introduced.

## Architecture result

Run 09 stress-tests:

- family-linked same-surname producer disambiguation;
- producer continuity across ownership and historical-name changes;
- a wine line nested inside a producer without inventing a project entity;
- persistent wines whose grapes, cellar protocol or legal category change by vintage;
- legal classification versus physical place;
- hydronym-derived cuvée naming without false vineyard identity;
- registered office versus cellar location;
- non-estate fruit without fabricated grower identity;
- multilingual grape-name governance;
- cross-variety synonym-string collisions;
- mixed owned/leased producer tenure;
- German approval-number semantics;
- certificate existence versus certificate date/scope;
- importer and distributor observations as dated access relationships.

All accepted facts remain representable with existing STRATA v0.2 entities, claims, relationships, name assertions, time, source fitness, and Human Reference dispositions.

**NO CONCRETE STRATA v0.2 REPRESENTATION FAILURE FOUND.**

No schema change or STRATA v0.3 gate is warranted.

## What this changes about the next run

The known cellar backlog represented by Runs 09A–09C is now structurally ready for activation. The next highest-value pressure test is no longer another ontology pass or a broad fill of France, Germany, Italy, Austria or other countries.

The graph is becoming dense enough that the next question is whether technically valid two-hop navigation is also editorially salient for a human reader.

After Run 09 activation, the preferred next run is therefore a **navigation-salience / density audit** before another fresh refrigerator tranche. That audit should test broad hubs such as countries, major grapes and large regions, identify technically valid but low-salience generated neighbors, and determine whether ranking, hub suppression, relationship weighting or editorial anchors can improve rabbit holes without creating a second graph.

Only after that audit should CARTA ingest another fresh cellar tranche.

## Final gate

Merge readiness requires:

1. all structured authority validates;
2. active producer/country/grape disposition invariants validate;
3. deterministic Human Reference generation is synchronized;
4. generated indexes and reciprocal navigation validate;
5. no temporary generation workflow remains on the branch;
6. the ordinary `Validate CARTA` GitHub Action passes on the final PR head.

Run 09 may merge only after all six conditions are true.
