# CARTA Deep Research Run 01 — Pyrenean Atlantic

**Research date:** 2026-08-18  
**Status:** Research complete; candidate ingestion intentionally deferred pending STRATA v0.2  
**Research artifact SHA-256:** `8b0cc935d9901e001ba35b7d7668aa8770729c325c0b9dcfd15e5b3066d14fce`

## What the run produced

The Deep Research pilot returned a human-readable ecosystem report plus a schema-oriented candidate ingestion packet containing:

- 36 entity candidates;
- 29 relationship candidates;
- 25 claim candidates;
- 27 source records;
- 0 geometry records, because the v0.1 schema required actual geometry and the run correctly refused to fabricate it.

The full candidate packet is **not accepted CARTA authority yet**.

## Central finding

The research did not reveal a single legal or historical region called the Pyrenean Atlantic. It revealed a **braided ecosystem** in which several systems overlap:

1. Atlantic Basque wine-law geographies including Bizkaiko, Getariako, and Arabako Txakolina;
2. French Basque geography around Irouléguy;
3. the Béarn / Jurançon / Pacherenc wine world of the northern Pyrenean foothills;
4. a non-spatial professional network extending to Richard Leroy in the Loire.

This finding is why STRATA v0.2 adds `ecosystem` as a first-class analytical entity rather than forcing the pilot object into `place`.

## Important discoveries

The run also established several useful stress cases:

- Alfredo Egia, Imanol Garay, Gile Iturriondobeitia, and Hegan Egin require separate person / producer / project identities.
- The Egia → Garay → Leroy path contains different relationship types rather than one generic influence lineage.
- Petit Courbu / Hondarrabi Zuri Zerratia demonstrates jurisdiction-specific legal naming that should not require a duplicate biological entity.
- Cultural/historical Béarn and Béarn AOP cannot be modeled as the same type of place.
- Maslacq / Orthez locality evidence for Garay demonstrates that spatial assertions can be useful even before exact geometry is acquired.
- Raffiat de Moncade produced a productive ampelographic expansion through proposed Gouais blanc × Bouchalès parentage and Arriloba.
- U.S. retail observations demonstrated why Frontier access data must remain dated and separate from permanent Reference authority.

## Post-pilot decisions

STRATA v0.2 adopts the following before ingestion:

1. **Source fitness over source prestige.** Importer/distributor/trade material can be substantive evidence where the source fits the claim.
2. **Non-binary spatial provenance.** Actual geometry remains strict, while source-described, cultural, historical, analytical, and locality-scale spatial assertions gain their own representation.
3. **Required human-readable Atlas.** Accepted machine records must project into readable Markdown surfaces in GitHub.
4. **First-class name assertions.** Jurisdictional and historical names gain sourceable records.
5. **Place semantics.** `place_kind` distinguishes country, administrative region, cultural region, historical territory, municipality, locality, wine region, and analytical region.
6. **First-class ecosystems.** Relationship-generated analytical ecosystems are not forced into physical geography.

## What is deliberately not happening in this pass

- Candidate Run 01 records are not being copied into `data/` yet.
- No producer, grape, place, or relationship from the run is being canonized merely because Deep Research emitted it.
- No GIS geometry is being fabricated.
- No finished Atlas cards are being authored from prose before the revised records exist.

## Next step after STRATA v0.2 acceptance

Normalize the Run 01 packet against v0.2, resolve obvious identity/source-fit issues, ingest accepted records, and generate the first human-readable proof set including the Pyrenean Atlantic ecosystem, Petit Manseng, Petit Courbu, Alfredo Egia, Imanol Garay, and Jurançon surfaces.
