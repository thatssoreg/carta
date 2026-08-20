# CARTA Run 09 follow-up: Lampyres → Matassa professional bridge

## Status

Targeted reconciliation patch after Run 09. Starting authority: `main @ f74088fb141fc0bfc205df411869ec0d9c2b6565`.

This patch does not perform a broad Matassa enrichment pass and does not change STRATA v0.2.

## Why this patch exists

Run 09 already carried `claim:daure-matassa-work-09` in the Domaine Lampyres provenance, supported by JancisRobinson.com, but Matassa and Tom Lubbe did not exist as graph endpoints. The work history therefore could not become a governed professional relationship or a real Human Reference navigation test.

The supplied follow-up research handoff revisited the evidence specifically to distinguish employment, collaboration, and mentorship and to check whether the commonly repeated biography was genuinely independent evidence.

## Evidence adjudication

The core relationship is supported.

- JancisRobinson.com describes François-Xavier Dauré as working for Tom Lubbe at Domaine Matassa while starting his own cellar, and reports five years of working with Lubbe.
- Terres Blanches states that Dauré joined Tom Lubbe at Matassa in 2015, worked in the vines and cellar for the next five vintages, and that 2019 was his last Matassa vintage.
- The sourced span therefore closes at five vintages, 2015 through 2019. CARTA uses that as a year-range representation, not as exact employment start and end dates.
- Lampyres' first vintage in 2016 overlaps this period, so the Matassa work is genuinely formative and concurrent rather than a later association.

The online evidence is not as independent as the number of retailer pages implies. Much of the repeated biography appears to descend from importer copy. This patch therefore keeps confidence at `medium` for the Dauré work-line claim despite the consistency of the reporting.

## Relationship semantics

### Asserted

`person:francois-xavier-daure WORKED_FOR producer:matassa`

This is the strongest existing STRATA predicate for the evidence. JancisRobinson.com explicitly frames Matassa as Dauré's day job / work for Lubbe, while Terres Blanches supplies the five-vintage vineyard-and-cellar scope.

`person:tom-lubbe FOUNDED producer:matassa`

Louis/Dressner is used only to stabilize the Matassa/Tom Lubbe identity and the 2003 founding needed for an honest Matassa stub.

### Deliberately not asserted

- `MENTORED_BY` between Dauré and Lubbe. The follow-up found apprenticeship/mentee language, but it is substantially trade/retailer supplied and not strong enough to collapse employment into mentorship.
- A separate `WORKED_WITH` edge to Tom Lubbe. The documented organizational relationship is already represented by `WORKED_FOR Matassa`; adding both would duplicate the same evidence without earning additional semantics.
- The repeated description of Dauré as Lubbe's "right hand" as machine fact. It is retained only as an attributed trade characterization in the research record, not CARTA authority.
- Any stylistic, philosophical, or sensory "Matassa influence" claim.
- Any Matassa wine, vineyard, grape, farming, cellar, appellation, or portfolio authority.

## Unresolved nuance

The JancisRobinson.com account adds that Dauré stepped in to help his father, who had been working for Matassa in the vineyards and cellar. This is a useful biographical nuance but is not reconciled into a father entity or additional work relationship here. A later Matassa/Lampyres enrichment can revisit it if primary evidence warrants expansion.

## Minimal Human Reference disposition

Matassa is activated as an honest `node/stub` producer profile with Tom Lubbe as a component entity and France as its only editorial orientation anchor.

Importantly, Domaine Lampyres is **not** added to Matassa's `representative_anchor_ids`, and Matassa is **not** added to Lampyres' anchors. If the work relationship produces useful reciprocal navigation, it must do so through governed graph authority and the existing generator. This preserves the relationship as a clean test case for Run 10's navigation salience/density audit.

## Architecture disposition

No STRATA v0.2 representation failure was found. The current `WORKED_FOR` and `FOUNDED` predicates are sufficient.

The patch is intentionally narrow: two entities, one source, two claims, two relationships, one Human Reference profile, and this audit addendum.

## Run 10 handoff

After deterministic Human Reference regeneration, inspect whether:

1. Lampyres surfaces Matassa through the supported Dauré work relationship;
2. Matassa surfaces Lampyres reciprocally;
3. the professional bridge ranks above or below broad geography/grape-derived candidates;
4. the relationship survives the existing 16-profile display cap without editorial anchors forcing the result.

Those observations belong to the navigation audit. They should not be solved by hand in this patch.
