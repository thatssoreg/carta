# Run 06 — Parallel Research Reconciliation

## Scope

This run reconciles two external research handoffs against CARTA's live STRATA v0.2 contracts and fresh source checks:

- ChatGPT Web Run 06B: Domaine Labet / Vins Pepe Raventós / Soleras del Pacífico
- Claude Web Run 06A: Eruptio / Keller / Corison

The research handoffs are discovery material, not machine authority. This run accepts only bounded claims that survived source-level verification and preserves explicit rejections where the handoffs overreached.

Baseline: `3bfebcb23ac017767f7ba52f4fb7044c2a9d56ea`.

## Reconciliation posture

- STRATA v0.2 remains active.
- No STRATA v0.3 construct is introduced.
- Persistent wine identity remains the default; vintage-specific sourcing and cellar facts stay temporal.
- Consequential grape names use first-class name assertions rather than duplicate biological entities.
- Legal designation uses `CLASSIFIED_AS`; spatial containment remains distinct.
- Practices already have first-class representation, so flor, solera, ouillage and sous-voile do not require ontology expansion.
- The parallel research reports are not stored as canonical authority and are not copied wholesale into the repository.

## ChatGPT Run 06B corrections

### Domaine Labet

Accepted from stronger source checks:

- Domaine Labet is based in Rotalier in Sud-Revermont; the Jura interprofessional profile documents 13.5 hectares across 45 parcels.
- The estate explicitly distinguishes ouillé whites from wines aged sous voile.
- `Fleur de Savagnin` is an assembled wine from multiple Lias-marl parcels, not a single-parcel wine.
- `La Cuvée du Hasard` / Chardonnay du Hasard is documented as Chardonnay from vines older than 60 years, blended from multiple Lias-marl terroirs and aged sous voile in old 228 L pièces for 36–48 months.
- The 2022 `La Bardette` bottling is retained with vintage scope from specialist trade material rather than universalized across all La Bardette plantings.

Rejected or withheld:

- **Fortification of Chardonnay du Hasard before flor:** rejected. The official Jura profile documents sous-voile aging but no fortification. The research report appears to have transferred a technique from the Soleras del Pacífico seed into Labet.
- **Estate-wide avoidance of malolactic fermentation in whites:** rejected. Revue du Vin de France explicitly describes sulfur use after malolactic fermentation in its account of the estate.
- **Chardonnay du Hasard as a single `Le Clos` parcel:** not ingested. The official Jura source instead describes the cuvée as an assembly of different Lias-marl terroirs.
- Unverified Trousseau details and a separate `La Reine` authority surface are deferred rather than inferred from the handoff.

### Vins Pepe Raventós / Bastard Negre

Accepted:

- The 2022 Bastard Negre comes from Les Terrasses del Serral, a west-side parcel planted in 1974, and the first-party technical page documents the vintage's open-cask/qvevri fermentation.
- The report's `pre-phylloxera` characterization is rejected by implication: a parcel planted in 1974 cannot be described that way.
- Spain's official variety register recognizes `Morrastel` as a synonym of Graciano.

Cautious resolution:

- Raventós reports a 2012 DNA identification of its Bastard Negre as Morastell. CARTA therefore records `Bastard Negre` as a **provisional local name** on the Graciano identity, supported by the producer report plus the official Morrastel/Graciano synonym record.
- This does **not** assert that every historical or international use of `Bastard Negre` is automatically Graciano.

### Soleras del Pacífico / The Flor of Evangelho

Accepted:

- Jake Neustadt's project began from access to Evangelho Palomino in 2017 while he worked as a Bedrock viticulturist.
- The Flor of Evangelho is a single-vineyard Palomino Fino wine using native barrel fermentation, light spring fortification, flor aging and a four-level fractional solera.
- Bedrock's own vineyard directory identifies Bedrock Wine Co. as owner and farmer of Evangelho; Soleras del Pacífico documents the old Palomino vines within the site.

Guardrail:

- Flor, sous-voile and solera are represented as practices. No `equivalent-to` relationship is created between Jura and Andalusian/Californian terms. Analogy is not identity.

## Claude Run 06A corrections

### Eruptio / Arinto dos Açores

The handoff treated producer attribution as genuinely contested. Fresh source checks materially changed that disposition.

Accepted:

- Abegoaria's own people page identifies Bernardo Cabral as Eruptio's winemaker and describes the Eruptio launch as a partnership with Abegoaria.
- Abegoaria's production-house page associates Eruptio with Adega do Pico and Cabral's technical responsibility for Azores wines.
- Contemporaneous Portuguese launch reporting independently names Bernardo Cabral + Abegoaria.
- Abegoaria's 2020 product page identifies Eruptio Arinto dos Açores as D.O. Pico and gives vintage-specific cellar details.

Rejected:

- A retailer page attributes Eruptio to António Maçanita. That statement is retained as contradicting evidence but is rejected for CARTA authority because it conflicts with the more specific first-party and contemporaneous launch record.

Ampelography:

- Portugal's official IVV list separately records `Arinto dos Açores` with synonym `Terrantez da Terceira` and mainland `Arinto` with synonym `Pedernã`. CARTA therefore creates a distinct Arinto dos Açores grape identity and does not merge it with mainland Arinto.

### Keller / Limestone + RR

The Claude handoff correctly recognized a false-merge risk but simplified the Limestone family incorrectly.

Accepted:

- `Keller Riesling limestone` and `Keller Riesling Kabinett limestone` are distinct durable wine identities.
- `Keller Riesling RR` remains one persistent identity even when sourcing changes by vintage.
- Vom Boden documents the normal RR basis as the red-soil pocket within Kirchspiel and reports additional Abtserde/Morstein casks in the 2022 RR.

Rejected:

- The base `Riesling limestone` is **not** automatically renamed or modeled as `Limestone trocken`. The verified portfolio separately lists `Riesling Trocken`, `Riesling limestone`, and `Riesling Kabinett limestone`.

This is an ingestion-discipline problem, not an ontology failure.

### Corison

Accepted from first-party/regulatory sources:

- Cathy Corison began her own Cabernet Sauvignon in 1987.
- The Napa Valley Cabernet Sauvignon is a continuing multi-vineyard identity sourced from three benchland vineyards and remains distinct from the Kronos and Sunbasket single-vineyard wines.
- Kronos was planted in 1971 on St. George rootstock and purchased by Corison/Martin in 1995.
- Sunbasket was purchased in 2015 after more than 25 years of fruit sourcing.
- TTB records the St. Helena AVA establishment date as 1995-09-11.

Withheld:

- The research handoff's 2009 fruit / 2014 label chronology for St. Helena is not ingested in this pass because the strongest source used for that specific chronology was trade reporting rather than Corison or the legal record. It remains a useful future verification target, not accepted authority here.

## Architecture result

The two handoffs produced several useful stress tests:

- one label family covering distinct wines (`Limestone` vs `Limestone Kabinett`);
- one persistent wine with vintage-variable source material (`RR`);
- a local grape name requiring cautious biological reconciliation (`Bastard Negre`);
- a homonymous grape-name trap (`Arinto dos Açores` vs mainland Arinto);
- process borrowing across wine cultures (flor / solera);
- parcel-vs-vineyard semantics in Labet and Raventós.

None requires STRATA v0.3. Existing wine identities, temporal claims, name assertions, practices, vineyards, classifications and typed relationships represent the verified facts without material distortion.

`NO CONCRETE STRATA v0.2 REPRESENTATION FAILURE FOUND.`

## Publication posture

This pass adds machine authority only. It intentionally does **not** publish new Human Reference profiles or Atlas pages while the parallel cellar-research queue is still running. Once the concurrent research waves settle, a later bounded publication pass can decide which of these worlds have enough reconciled authority for baseline Human Reference treatment.

## Deferred checks

- Domaine Labet `La Reine` and the supplied Trousseau bottle need the same source-addressable reconciliation before ingestion.
- Bastard Negre would benefit from a primary scientific genetic record directly tying the Raventós accession to Graciano.
- Eruptio vineyard sourcing beyond the project/wine identity remains unresolved.
- Keller exact first vintages for RR and the Limestone identities remain unasserted.
- Corison's St. Helena label chronology remains unasserted pending stronger direct evidence.
- No vineyard or appellation polygon is fabricated in this run.
